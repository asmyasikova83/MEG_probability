import mne
import os.path as op
import os
import numpy as np
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

fr = 'beta_16_30_trf_early_log'
# загружаем комбайн планары, усредненные внутри каждого испытуемого
if parameter3 == 'negative':
    data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(fr)
if parameter3 == None:
    data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
poster = True
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################

decision = False
fb = True

if poster:
    N = 1
    if decision:
        # decision  making efects, dummy
        t_start = -0.3 
        t_end = -0.3
    if fb:
        t_start = 1.7
        t_end = 1.7
else:
    N = 17
    t_start = -0.8
    t_end =  2.4

# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

p = 'comb_planar'

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов
t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1 = f'{cond1}', parameter2 = f'{cond2}', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
########################### p value #############################
# загружаем таблицу с pvalue, полученными с помощью ttest 
pval_in_intevals = p_val
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)
# считаем разницу бета и добавляем к шаблону (донору)
temp.data = risk_mean - norisk_mean


# время в которое будет строиться топомапы
if poster:
    # decision-making
    if decision:
        times = np.array([-0.3])
        # интервалы усредения
        tmin = [-0.9, -0.7, -0.5]
        tmax = [-0.7, -0.5, -0.3]
        interval = 'decision'
    if fb:
        # fb related effects
        times = np.array([1.7])
        tmin = [1.5, 1.7]
        tmax = [1.7, 1.9]
        interval = 'fb'
else:
    times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
    tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
    tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]

data_for_plotting = np.empty((102, 0))

#усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения
if decision:
        r = 2
else:
        r = 1

for i in range(N+r):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])

#average beta power across predefined time intervals. for decision we have 3 intervals
if decision:
    data_to_sum = (data_for_plotting[:,0] + data_for_plotting[:,1] +  data_for_plotting[:,2])/3
else:
    data_to_sum = (data_for_plotting[:,0] + data_for_plotting[:,1])/2
    
plotting_LMEM = mne.EvokedArray(data_to_sum[:, np.newaxis], info = temp.info)
plotting_LMEM.times = times

#plotting with nostat and stat
stat = False

if not stat:
    if parameter3 == 'negative':
        title = (f'In {parameter1} fb negpos, nostat')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2} nofdr, nostat')
    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.5, vmax = 0.5, time_unit='ms', title = title, colorbar = True, extrapolate = "local")
    print('Pic ready')

if stat:
    #no fdr
    binary = p_val_binary(pval_in_intevals, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {parameter1} fb negpos, ttest,noFDR')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, ttest,noFDR')
    fig1 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # space fdr
    binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {parameter1} fb negpos, ttest, space FDR')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, %s, ttest, spaceFDR')
    fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # full fdr
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {parameter1} feedback negpos, ttest, fullFDR')
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, ttest, fullFDR')
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.7, vmax = 0.7, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))


if parameter3 == 'negative':
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_ttest_sum/{cond1}/', exist_ok = True)
    if not stat:
        fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_ttest_sum/{cond1}/LMEM_{cond1}_vs_{parameter3}_vs_{parameter4}_{interval}_nostat_{fr}_separ_fb.jpeg', dpi = 900)
if parameter3 == None:
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_ttest_sum/{cond1}_vs_{cond2}/' , exist_ok = True)
    if not stat:
        fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_ttest_sum/{cond1}_vs_{cond2}/LMEM_{cond1}_vs_{cond2}_{interval}_nostat_{fr}.jpeg', dpi = 900)
