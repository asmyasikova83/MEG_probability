import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
# задаем время и донора
if poster:
    N = 1
    t_start = 1.8
    t_end = 1.9
else:
    N = 17
    t_start = -0.8
    t_end =  2.4

time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

if response:
    if parameter3 == 'negative':
        data_path = f'/{prefix}/beta/beta_16_30_fb_ave_comb_planar/'
    if parameter3 == None:
        fr = 'beta_16_30_trf_early_log'
        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
else:
    freq_range = 'beta_16_30_trf_no_log_division_stim'
    if parameter3 == 'negative':
        data_path = '/{0}/stim_check/{1}_feedback/{1}_ave_comb_planar'.format(prefix, freq_range)
    if parameter3 == None:
        data_path = '/{0}/stim_check/{1}/{1}_ave_comb_planar'.format(prefix, freq_range)
########################### norisk vs risk ##############################
for p in planars:
    _, _, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1 = f'{cond1}', parameter2 = f'{cond2}', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
    if parameter3 == 'negative':
        df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_feedback_cur_MEG_early_log.csv')
        sign_df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_feedback_MEG_t_ratio_test.csv')
    if parameter3 == None:
        if response:
            sign_df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_condition_contrast_MEG_t_ratio_test.csv')
            #sign_df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_condition_contrast_MEG.csv')
            #df = pd.read_csv(f'/{prefix}/beta/p_vals_fb_cur_Tukey_by_trial_type_MEG.csv')
            df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_trial_type_MEG_early_log.csv')
        else:
            df = pd.read_csv(f'/{prefix}/stim_check/p_vals_fb_cur_Tukey_by_trial_type_MEG_stim.csv')

########################## p value #############################
#read signed p-vals

sign_pval_in_intevals = []
for i in range(102):
    sign_pval_s = sign_df[sign_df['sensor'] == i]
    if parameter3 == 'negative':
        sign_pval_norisk_risk = sign_pval_s[f'{cond1}-negative_positive'].tolist()
    if parameter3 == None:
        sign_pval_norisk_risk = sign_pval_s[f'norisk_{cond1}'].tolist()
    sign_pval_in_intevals.append(sign_pval_norisk_risk)

pval_in_intevals = []
for i in range(102):
    pval_s = df[df['sensor'] == i]
    if parameter3 == 'negative':
        pval_norisk_risk = pval_s[f'{cond1}-negative_positive'].tolist()
    if parameter3 == None:
        pval_norisk_risk = pval_s[f'norisk_{cond1}'].tolist()
    pval_in_intevals.append(pval_norisk_risk)

#print('pval_in_intevals', pval_in_intevals)
pval_in_intevals = np.array(pval_in_intevals)
sign_pval_in_intevals = np.array(sign_pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)
#print('pval_full_fdr', pval_full_fdr)
# prepare p-vals for plotting
ozeros = np.zeros((102,17))
nofdr = True
spacefdr = False
fullfdr = False

#print(sign_pval_in_intevals)
#print(pval_in_intevals)

if nofdr:
    types = 'no'
    for i in range(102):
        for j in range(17):
            if sign_pval_in_intevals[i, j] > 0 and sign_pval_in_intevals[i, j] < 0.05:
                if pval_in_intevals[i, j] < 0.05:
                    ozeros[i, j] = 1.0 -  10*pval_in_intevals[i, j]
            if sign_pval_in_intevals[i, j] < 0 and sign_pval_in_intevals[i, j] > -0.05:
                if pval_in_intevals[i, j] < 0.05:
                    ozeros[i, j] = -1.0 +  10*pval_in_intevals[i, j]
    binary_full = p_val_binary(pval_in_intevals, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1} pos_neg, %s, LMEM, noFDR'%p)
    else:
        title = (f'{cond1} vs {cond2}, %s, LMEM, noFDR'%p)
if spacefdr:
    types = 'space'
    for i in range(102):
        for j in range((17)):
            if sign_pval_in_intevals[i, j] > 0 and sign_pval_in_intevals[i, j] < 0.05:
                if pval_space_fdr[i, j] < 0.05:
                    ozeros[i, j] = 1.0 -  10*pval_space_fdr[i, j]
            if sign_pval_in_intevals[i, j] < 0 and sign_pval_in_intevals[i, j] > -0.05:
                if pval_space_fdr[i, j] < 0.05:
                    ozeros[i, j] = -1.0 +  10*pval_space_fdr[i, j]
    binary_full = p_val_binary(pval_space_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1} pos_neg, %s, LMEM, spaceFDR'%p)
    else:
        title = (f'{cond1} vs {cond2}, %s, LMEM, spaceFDR'%p)
if fullfdr:
    types = 'full'
    for i in range(102):
        for j in range((17)):
            if sign_pval_in_intevals[i, j] > 0 and sign_pval_in_intevals[i, j] < 0.05:
                if pval_full_fdr[i, j] < 0.05:
                    ozeros[i, j] = 1.0 -  10*pval_full_fdr[i, j]
            if sign_pval_in_intevals[i, j] < 0 and sign_pval_in_intevals[i, j] > -0.05:
                if pval_full_fdr[i, j] < 0.05:
                    ozeros[i, j] = -1.0 +  10*pval_full_fdr[i, j]
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1} pos_neg, %s, LMEM, fullFDR'%p)
    else:
        title = (f'{cond1} vs {cond2}, %s, LMEM, fullFDR'%p)
temp.data = ozeros
print(temp.data)
# время в которое будет строиться топомапы
if poster:
    times = np.array([1.8])
else:
    times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
if poster:
    tmin = [1.7]
    tmax = [1.9]
else:
    # интервалы усредения
    tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
    tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

plotting_LMEM = mne.EvokedArray(temp.data, info = temp.info)
plotting_LMEM.times = times
'''
if parameter3 == 'negative':
    title = (f'In {parameter1} feedback negative vs positive, %s, LMEM, fullFDR'%p)
if parameter3 == None:
    title = (f'{cond2} vs {cond1}, %s, LMEM, fullFDR'%p)
'''
fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'p-val', show = False, vmin = -1.0, vmax = 1.0, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='black', markeredgecolor='yellow', linewidth=0, markersize=9, markeredgewidth=2))

if parameter3 == 'negative':
     os.makedirs(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign/{cond1}/', exist_ok = True)
     fig3.savefig(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign/{cond1}/LMEM_{cond1}_vs_{parameter3}_vs_{parameter4}_stat_{types}_fdr_{fr}.jpeg', dpi = 300)
if parameter3 == None:
    if response:
        os.makedirs(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign/{cond1}_vs_{cond2}/' , exist_ok = True)
        fig3.savefig(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign/{cond1}_vs_{cond2}/LMEM_{cond1}_vs_{cond2}_stat_{types}_fdr_{fr}.jpeg', dpi = 300)
        print()
        print('Saved!')