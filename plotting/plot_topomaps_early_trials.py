import mne
import os
import numpy as np
import copy
from function import ttest_pair_early_trials,ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

# загружаем комбайн планары, усредненные внутри каждого испытуемого
data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
#data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/hp_early_trials/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_into_subj_comb_planar/'
#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
fr = 'beta_16_30_trf_early_log'
#poster = True
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
N = 17
t_start = -0.8
t_end =  2.4

#subjects = []
#for i in range(0,63):
#    if i < 10:
#        subjects += ['P00' + str(i)]
#    else:
#        subjects += ['P0' + str(i)]
# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

p = 'comb_planar'
n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

combined_cond = False
contrast_cond = False
#look at the conditions separately
separate_cond_separ = True

if combined_cond:
     _, _, prerisk_neg, prerisk_pos = ttest_pair_early_trials(data_path, response, subjects, fr, parameter1 = 'prerisk', parameter2 = 'norisk', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
     _, _, norisk_neg, norisk_pos= ttest_pair_early_trials(data_path, response, subjects, fr, parameter1 = 'norisk', parameter2 = 'norisk', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
     _, _, postrisk_neg, postrisk_pos= ttest_pair_early_trials(data_path, response, subjects, fr, parameter1 = 'postrisk', parameter2 = 'norisk', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
if contrast_cond:
     _, p_val, risk_mean, norisk_mean = ttest_pair_early_trials(data_path, response, subjects, fr, parameter1 = cond1, parameter2 = cond2, parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
if separate_cond_separ:
     _, p_val, risk_mean, norisk_mean = ttest_pair_early_trials(data_path, response, subjects, fr, parameter1 = cond1, parameter2 = cond2, parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)

# считаем разницу бета и добавляем к шаблону (донору)

#temp.data = risk_mean - norisk_mean
if combined_cond:
    temp.data = (prerisk_neg + norisk_neg + postrisk_neg)/3 - (prerisk_pos + norisk_pos + postrisk_pos)/3
    title = f'In favourable outcomes_losses_minus_wins'
if contrast_cond:
    print(cond1)
    temp.data = risk_mean - norisk_mean
    title = f'{cond1}_losses_minus_wins'
if separate_cond_separ:
    #temp.data = risk_mean
    #title = f'{cond1}_losses'
    temp.data = norisk_mean
    title = f'{cond1}_wins'

# время в которое будет строиться топомапы
times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

data_for_plotting = np.empty((102, 0))

#усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения

for i in range(N):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])

plotting_LMEM = mne.EvokedArray(data_for_plotting, info = temp.info)
plotting_LMEM.times = times
print(plotting_LMEM)
#plotting with nostat and stat
stat = True

if not stat:
    if parameter3 == 'negative':
        #title = (f'In favourable choices, nostat')
        print('todo')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2} nofdr, nostat')
    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -4.5, vmax = 4.5, time_unit='ms', title = title, colorbar = True, extrapolate = "local")
    print('Pic ready')

if stat:
    title = title + '_fullfdr'
    #no fdr
    ########################## p value #############################
    # загружаем таблицу с pvalue, полученными с помощью ttest 
    pval_in_intevals = p_val
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)
    
    binary = p_val_binary(pval_in_intevals, treshold = 0.05)
    if parameter3 == 'negative':
        #title = (f'In {parameter1} fb negpos, ttest,noFDR')
        print('todo')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, ttest,noFDR')
    fig1 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -4.5, vmax = 4.5, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # space fdr
    binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        #title = (f'In {parameter1} fb negpos, ttest, space FDR')
        print('todo')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, %s, ttest, spaceFDR')
    fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -4.5, vmax = 4.5, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # full fdr
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    print(binary_full)
    if parameter3 == 'negative':
        #title = (f'In {parameter1} feedback negpos, ttest, fullFDR')
        print('todo')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, ttest, fullFDR')
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

if parameter3 == 'negative':
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps/supplementary_cond/', exist_ok = True)
    fig1.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps/supplementary_cond/{title}_separ_fb.jpeg', dpi = 300)
if parameter3 == None:
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps/early_trials/' , exist_ok = True)
    fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps/early_trials/{cond1}_10_trials.jpeg', dpi = 900)
