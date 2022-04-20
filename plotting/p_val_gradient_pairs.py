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
# задаем время и донора in order to obtain beta power
#17 timeframes
N = 17
t_start = -0.8
t_end =  2.4

# время в которое будет строиться топомапы
times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
# интервалы усредения
tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")


fr = 'beta_16_30_trf_early_log'
planars = ['comb_planar']

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов
if response:
    if parameter3 == 'negative':
        data_path = f'{prefix}/beta_by_feedback/{fr}_ave_into_subj_comb_planar/'
    if parameter3 == None:
        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
else:
    freq_range = 'beta_16_30_trf_no_log_division_stim'
    if parameter3 == 'negative':
        data_path = '/{0}/stim_check/{1}_feedback/{1}_ave_comb_planar'.format(prefix, freq_range)
    if parameter3 == None:
        data_path = '/{0}/stim_check/{1}/{1}_ave_comb_planar'.format(prefix, freq_range)
# get beta power over conditions
for p in planars:
    print(p)
    print('data path', data_path)
    _, _, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1 = f'{cond1}', parameter2 = f'{cond2}', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
    #get p-values
    if parameter3 == 'negative':
        df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_feedback_cur_MEG_early_log.csv')
    if parameter3 == None:
        if response:
            df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_trial_type_MEG_early_log.csv')
        else:
            df = pd.read_csv(f'/{prefix}/stim_check/p_vals_fb_cur_Tukey_by_trial_type_MEG_stim.csv')

data_for_plotting = np.empty((102, 0))

temp.data = risk_mean - norisk_mean

#усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервало
# look at the power value to sort signed  p-vals
#17 for all data frames
for i in range(N):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])
print(data_for_plotting.shape)
###################### p value #############################
pval_in_intevals = []
for i in range(102):
    pval_s = df[df['sensor'] == i]
    if parameter3 == 'negative':
        pval_norisk_risk = pval_s[f'{cond1}-negative_positive'].tolist()
    if parameter3 == None:
        #pval_norisk_risk = pval_s[f'norisk_{cond1}'].tolist()
        pval_norisk_risk = pval_s[f'{cond2}_{cond1}'].tolist()
    pval_in_intevals.append(pval_norisk_risk)

pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)
# do the fdr correction of p-vals
save = False #get intersect of significant sensors
fullfdr = True #comppute signed p-vals
#intervals of interest
decision = False
anticip = True
fb = False
if fb:
    interval = [12, 13]
if decision:
    interval = [0, 1, 2]
if anticip:
    interval = 8
if save:
    sensors = []
    aver_interval = np.ones((102,1))
    for j in range(102):
        if decision:
            if pval_full_fdr[j, interval[0]] < 0.05 and pval_full_fdr[j, interval[1]] < 0.05 and pval_full_fdr[j, interval[2]] < 0.05:
                aver_interval[j] = (pval_full_fdr[j, interval[0]] + pval_full_fdr[j, interval[1]] + pval_full_fdr[j, interval[2]])/3
                sensors.append(j)
        if fb:
            if pval_full_fdr[j, interval[0]] < 0.05 and pval_full_fdr[j, interval[1]] < 0.05:
                aver_interval[j] = (pval_full_fdr[j, interval[0]] + pval_full_fdr[j, interval[1]])/2
                sensors.append(j)
        if anticip:
            if pval_in_intevals[j, interval] < 0.05:
                aver_interval[j] = pval_in_intevals[j, interval]
                sensors.append(j)
    aver_interval = np.array(aver_interval)
    sensors_to_save = np.array(sensors)
    sensors_to_save = sensors_to_save[np.newaxis]
    if parameter3 == None:
        #set param3,4 to None
        if fb:
            f_name = path + f'sensors_late_fb_1500_1900_{cond1}_vs_{cond2}.txt'
            f_name_aver = path + 'fb_aver.txt'
        if anticip:
            f_name = path + f'sensors_late_anticip_600_800_{cond1}_vs_{cond2}.txt'
            f_name_aver = path + 'anticip_aver.txt'
        if decision:
            f_name = path + f'sensors_decision_-900_-300_{cond1}_vs_{cond2}.txt'
            f_name_aver = path + 'decis_aver.txt'
    if parameter3 == 'negative':
        #set param3. 4 to mneg pos
        if fb:
            f_name = path + f'sensors_late_fb_1500_1900_{cond1}_{parameter3}_vs_{parameter4}.txt'
            f_name_aver = path + 'fb_fb_aver.txt'
    np.savetxt(f_name, sensors_to_save, fmt="%s")
    np.savetxt(f_name_aver, aver_interval, fmt="%d")
    exit()
if fullfdr:
    #full fdr
    types = 'full'
    if parameter3 == None:
        if fb:
            f_name = path + f'sensors_late_fb_1500_1900_{cond1}_vs_{cond2}.txt'
            f_name_aver = path + 'fb_aver.txt'
        if anticip:
            f_name = path + f'sensors_late_anticip_600_800_{cond1}_vs_{cond2}.txt'
            f_name_aver = path + 'anticip_aver.txt'
        if decision:
            f_name = path + f'sensors_decision_-900_-300_{cond1}_vs_{cond2}.txt'
            f_name_aver = path + 'decis_aver.txt'
    if parameter3 == 'negative':
        if fb:
            #in config set param3, param4 to 'negative', 'positive'
            f_name = path + f'sensors_late_fb_1500_1900_{cond1}_{parameter3}_vs_{parameter4}.txt'
            f_name_aver = path + 'fb_fb_aver.txt'
    sensors = np.loadtxt(f_name, dtype = int)
    aver_interval = np.loadtxt(f_name_aver, dtype = int)
    ozeros = np.zeros((102,1))
    for i in range(102):
        for sen in sensors:
            if i == sen:
                if decision:
                    if (data_for_plotting[i, interval[0]] + data_for_plotting[i, interval[1]] + data_for_plotting[i, interval[2]])/3 > 0:
                        ozeros[i] = 1.0 -  10*aver_interval[i]
                    if (data_for_plotting[i, interval[0]] + data_for_plotting[i, interval[1]] + data_for_plotting[i, interval[2]])/3 < 0:
                        ozeros[i] = -1.0 +  10*aver_interval[i]
                if fb:
                    if (data_for_plotting[i, interval[0]] + data_for_plotting[i, interval[1]])/2 > 0:
                        ozeros[i] = 1.0 -  10*aver_interval[i]
                    if (data_for_plotting[i, interval[0]] + data_for_plotting[i, interval[1]])/2 < 0:
                        ozeros[i] = -1.0 +  10*aver_interval[i]
                if anticip:
                    if data_for_plotting[i, interval] > 0:
                        ozeros[i] = 1.0 -  10*pval_in_intevals[i, interval] #anticip, no fdr
                    if data_for_plotting[i, interval] < 0:
                        ozeros[i] = -1.0 +  10*pval_in_intevals[i, interval]
    binary_full = p_val_binary(aver_interval[:, np.newaxis], treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'{cond1}pos_neg, %s, LMEM, fullFDR'%p)
    else:
        title = (f'{cond1} vs {cond2}, %s, LMEM, fullFDR'%p)
#prepare the p-vals for plotting
temp.data = ozeros
plotting_LMEM = mne.EvokedArray(temp.data, info = temp.info)
plotting_LMEM.times = np.array([1.8])
#dummy
t_start = 1.8
t_end = 1.8
num = 1
time_to_plot = np.linspace(t_start, t_end, num)
print(time_to_plot.shape)
#TODO all figs
fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'p-val', show = False, vmin = -1.0, vmax = 1.0, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='black', markeredgecolor='yellow', linewidth=0, markersize=9, markeredgewidth=2))

if parameter3 == 'negative':
     os.makedirs(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign_pairs/{cond1}/', exist_ok = True)
     fig3.savefig(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign_pairs/{cond1}/LMEM_{cond1}_vs_{parameter3}_vs_{parameter4}_stat_{types}_fdr_{fr}.jpeg', dpi = 300)
if parameter3 == None:
    if response:
        os.makedirs(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign_pairs/{cond1}_vs_{cond2}/' , exist_ok = True)
        fig3.savefig(f'/{prefix}/topomaps/topomaps_rows_LMEM_response/p_val_sign_pairs/{cond1}_vs_{cond2}/LMEM_{cond1}_vs_{cond2}_decision.jpeg', dpi = 300)
        print('Saved!')
