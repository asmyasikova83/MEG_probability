import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.stats.multitest as mul
from function import ttest_pair, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *


cond1 = 'risk'
cond2 = 'norisk'

parameter3 = None
parameter4 = None
#parameter3 = 'negative'
#parameter4 = 'positive'
# задаем время и донора
#N = 17
#t_start = -0.8
#t_end =  2.4
N = 8
t_start = -0.7
t_end =  2.1

#N = 5
#t_start = -0.6
#t_end =  1.8
# время в которое будет строиться топомапы
#times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
# интервалы усредения
#tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
#tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
times = np.array([-0.7, -0.3, 0.1, 0.5, 0.9, 1.3, 1.7, 2.1])
tmin = [-0.9, -0.5, -0.1, 0.3,  0.7, 1.1, 1.5, 1.9]
tmax = [-0.5, -0.1, 0.3,  0.7, 1.1, 1.5, 1.9, 2.3]
#tmin = [-0.9, -0.3, 0.3, 0.9, 1.5]
#tmax = [-0.3, 0.3, 0.9,  1.5, 2.1]
#times = np.array([-0.6, 0.0, 0.6, 1.2, 1.8])

temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
prefix = '_trained'
fr = 'beta_16_30_trf_early_log'

path_pic = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_400ms_pval_grad/{0}'.format(fr)
if parameter3 == None:
    if Normals:
        subjects = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']
    if Autists:
         subjects = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                         'P335', 'P338', 'P341', 'P342']
if parameter4 == 'positive':
    if Autists:
        subjects = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321',    'P323', 'P324',
                       'P325',          'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
    if Normals:
        subjects = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055',         'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']
if Normals:        
    data_path = '{0}/Normals_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
    group = 'normals'
if Autists:
    data_path = '{0}/Autists_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
    group = 'autists'
print(data_path)

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов
#if response:
#    if parameter3 == 'negative':
#        #data_path = f'/{prefix}/beta/beta_16_30_fb_ave_comb_planar/'
#    if parameter3 == None:
#        fr = 'beta_16_30_trf_early_log'
#        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
#else:
#    freq_range = 'beta_16_30_trf_no_log_division_stim'
#    if parameter3 == 'negative':
#        data_path = '/{0}/stim_check/{1}_feedback/{1}_ave_comb_planar'.format(prefix, freq_range)
#    if parameter3 == None:
#        data_path = '/{0}/stim_check/{1}/{1}_ave_comb_planar'.format(prefix, freq_range)
########################### norisk vs risk ##############################
#for p in planars:
#    print('data path', data_path)
#    _, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1 = f'{cond1}', parameter2 = f'{cond2}', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
#    if parameter3 == 'negative':
#        df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_feedback_cur_MEG_early_log.csv')
#    if parameter3 == None:
#        if response:
#            df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_trial_type_MEG_early_log.csv')
#        else:
#            df = pd.read_csv(f'/{prefix}/stim_check/p_vals_fb_cur_Tukey_by_trial_type_MEG_stim.csv')

for p in planars:
    _, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1 = f'{cond1}', parameter2 = f'{cond2}', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
    if parameter3 == 'negative':
        #df = pd.read_csv(f'/{prefix_data}/beta/p_vals_by_feedback_MEG_group_600ms_fin.csv')
        df = pd.read_csv(f'/{prefix_data}/beta/p_vals_by_feedback_MEG_group_400ms_fin.csv')
    if parameter3 == None:
        #df = pd.read_csv(f'/{prefix_data}/beta/p_vals_by_trial_type_group_MEG_600ms_fin.csv')
        df = pd.read_csv(f'/{prefix_data}/beta/p_vals_by_trial_type_group_MEG_400ms_fin.csv')
data_for_plotting = np.empty((102, 0))

print('Normals', Normals)
print('Autists', Autists)
print(df)

temp.data = risk_mean - norisk_mean
#усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервало
# look at the power value to sort signed  p-vals
for i in range(N):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])
###################### p value #############################
pval_in_intevals = []
for i in range(102):
    pval_s = df[df['sensor'] == i]
    if parameter3 == 'negative':
        pval_norisk_risk = pval_s[f'{group}_{cond1}-negative_positive'].tolist()
    if parameter3 == None:
        pval_norisk_risk = pval_s[f'{group}-norisk_{cond1}'].tolist()
    pval_in_intevals.append(pval_norisk_risk)

LMEM = True
ttest = False

if LMEM:
    stat = 'LMEM'
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)
    # num of timeframes
    t = 8
    #t = 5
    time_to_plot = np.linspace(t_start, t_end, num = N)
    line = 'LMM'
if ttest:
    stat = 'ttest'
    pval_in_intevals = np.array(p_val)
    pval_space_fdr = space_fdr(p_val)
    pval_full_fdr =  full_fdr(p_val)
    #num of timepoints
    t = 1350
    time_to_plot = np.arange(t_start, t_end, 0.4)
    line = 'ttest'

# do the fdr correction of p-vals
ozeros = np.zeros((102,1350))
nofdr = True
spacefdr = False
fullfdr = False

if nofdr:
    types = 'no'
    for i in range(102):
        for j in range((t)):
            if pval_in_intevals[i, j] < 0.05:
                if temp.data[i, j] > 0:
                #if data_for_plotting[i, j] > 0:
                    ozeros[i, j] = 1.0 -  10*pval_in_intevals[i, j]
                #if data_for_plotting[i, j] < 0:
                if temp.data[i, j] < 0:
                    ozeros[i, j] = -1.0 +  10*pval_in_intevals[i, j]
    binary_full = p_val_binary(pval_in_intevals, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1} pos_neg {group}, %s, {line}, noFDR'%p)
    else:
        title = (f'{cond1} vs {cond2} {group}, %s, {line}, noFDR'%p)
if spacefdr:
    types = 'space'
    for i in range(102):
        for j in range((t)):
            if pval_space_fdr[i, j] < 0.05:
                #if data_for_plotting[i, j] > 0:
                if temp.data[i, j] > 0:
                    ozeros[i, j] = 1.0 -  10*pval_space_fdr[i, j]
                #if data_for_plotting[i, j] < 0:
                if temp.data[i, j] < 0:
                    ozeros[i, j] = -1.0 +  10*pval_space_fdr[i, j]
    binary_full = p_val_binary(pval_space_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1} pos_neg {group}, %s, {line}, spaceFDR'%p)
    else:
        title = (f'{cond1} vs {cond2} {group}, %s, {line}, spaceFDR'%p)
if fullfdr:
    types = 'full'
    for i in range(102):
        for j in range((t)):
            if pval_full_fdr[i, j] < 0.05:
                #if data_for_plotting[i, j] > 0:
                if temp.data[i, j] > 0:
                    ozeros[i, j] = 1.0 -  10*pval_full_fdr[i, j]
                #if data_for_plotting[i, j] < 0:
                if temp.data[i, j] < 0:
                    ozeros[i, j] = -1.0 +  10*pval_full_fdr[i, j]
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1} pos_neg {group}, %s, {line}, fullFDR'%p)
    else:
        title = (f'{cond1} vs {cond2} {group}, %s, {line}, fullFDR'%p)

#prepare the p-vals for plotting
temp.data = ozeros
plotting_LMEM = mne.EvokedArray(temp.data, info = temp.info)
#TODO all figs

if LMEM:
    plotting_LMEM.times = times
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'p-val', show = False, vmin = -1.0, vmax = 1.0, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='black', markeredgecolor='yellow', linewidth=0, markersize=9, markeredgewidth=2))
if ttest:
    plotting_LMEM.times = np.arange(-0.820, 2.420, 0.0024)
    print(plotting_LMEM.times.shape)
    #exit()
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, average = 0.4, scalings = 1, ch_type='planar1', units = 'p-val', show = False, vmin = -1.0, vmax = 1.0, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='black', markeredgecolor='yellow', linewidth=0, markersize=9, markeredgewidth=2))
print(fig3)
if parameter3 == 'negative':
     os.makedirs(f'/{path_pic}/{group}/{cond1}/', exist_ok = True)
     fig3.savefig(f'/{path_pic}/{group}/{cond1}/{stat}_{cond1}_vs_{parameter3}_vs_{parameter4}_stat_{types}_fdr_{fr}.jpeg', dpi = 300)
if parameter3 == None:
    if response:
        os.makedirs(f'/{path_pic}/{group}/{cond1}_vs_{cond2}/' , exist_ok = True)
        fig3.savefig(f'/{path_pic}/{group}/{cond1}_vs_{cond2}/{stat}_{cond1}_vs_{cond2}_stat_{types}_fdr_{fr}.jpeg', dpi = 300)
        print('Saved!')
