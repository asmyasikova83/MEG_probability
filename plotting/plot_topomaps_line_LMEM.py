import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

# загружаем комбайн планары, усредненные внутри каждого испытуемого
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
print(fr)
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################

if poster:
    N = 1
    t_start = 1.8
    t_end = 1.9
else:
    N = 17
    t_start = -0.8
    t_end =  2.4

# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов
########################### norisk vs risk ##############################
for p in planars:
    _, _, risk_mean, norisk_mean = ttest_pair(data_path, subjects, fr, parameter1 = f'{cond1}', parameter2 = f'{cond2}', parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
    if parameter3 == 'negative':
       title = (f'In {cond1} feedback negative vs positive, %s, noFDR'%p)
       #df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_factor_significance_MEG.csv')
       df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_Tukey_by_feedback_cur_MEG.csv')
    if parameter3 == None:
       print('parameter3 none', parameter3)
       title = (f'{cond1} vs {cond2}, %s, LMEM, noFDR'%p)
       #df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/p_val_low_{1}/p_vals_fb_cur_Tukey_by_trial_type_MEG.csv'.format(feedb, fr)) #TODO: fb_cur remove
       df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_fb_cur_Tukey_by_trial_type_MEG.csv')
    
    ########################### p value #############################
    # загружаем таблицу с pvalue, полученными с помощью LMEM в R

    pval_in_intevals = []
    # number of heads in line and the number of intervals into which we divided (see amount of tables with p_value in intervals)
    for i in range(102):
        
        pval_s = df[df['sensor'] == i]
        if parameter3 == 'negative':
            #TODO 
            pval_norisk_risk = pval_s[f'{cond1}-negative_positive'].tolist()
        if parameter3 == None:
            pval_norisk_risk = pval_s[f'norisk_{cond1}'].tolist()
        pval_in_intevals.append(pval_norisk_risk)
        
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)
    # считаем разницу бета и добавляем к шаблону (донору)
    temp.data = risk_mean - norisk_mean

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

    binary = p_val_binary(pval_in_intevals, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {parameter1} feedback negative vs positive, %s, LMEM, noFDR'%p)
    if parameter3 == None:
        title = (f'{cond2} vs {cond1}, %s, LMEM, noFDR'%p)
    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # space fdr
    binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {parameter1} feedback negative vs positive, %s, LMEM, space FDR'%p)
    if parameter3 == None:
        title = (f'{cond1} vs {cond2}, %s, LMEM, spaceFDR'%p)
    fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # full fdr
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {parameter1} feedback negative vs positive, %s, LMEM, fullFDR'%p)
    if parameter3 == None:
        title = (f'{cond2} vs {cond1}, %s, LMEM, fullFDR'%p)
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))


    #os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_risk/'.format(feedb, fr) , exist_ok = True)
    if parameter3 == 'negative':
        os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/{cond1}/', exist_ok = True)
        #fig3.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_risk/LMEM_norisk_vs_risk_stat_full_fdr_{2}_separ_fb.jpeg'.format(feedb, fr, p), dpi = 300)
        fig3.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/{cond1}/LMEM_{cond1}_vs_{parameter3}_vs_{parameter4}_stat_full_fdr_{fr}_separ_fb.jpeg', dpi = 900)
    if parameter3 == None:
        os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/{cond1}_vs_{cond2}/' , exist_ok = True)
        fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/{cond1}_vs_{cond2}/LMEM_{cond1}_vs_{cond2}_stat_no_fdr_{fr}_separ_fb.jpeg', dpi = 900)
        fig2.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/{cond1}_vs_{cond2}/LMEM_{cond1}_vs_{cond2}_stat_space_fdr_{fr}_separ_fb.jpeg', dpi = 900)
        #fig3.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_risk/LMEM_norisk_vs_risk_stat_full_fdr_{2}_separ_fb.jpeg'.format(feedb, fr, p), dpi = 300)
        fig3.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/{cond1}_vs_{cond2}/LMEM_{cond1}_vs_{cond2}_stat_full_fdr_{fr}_separ_fb.jpeg', dpi = 900)

'''

########################### cond1 ##############################

for p in planars:
   # _, _, prerisk_mean, norisk_mean = ttest_pair(data_path, subjects, fr, parameter1 = 'prerisk', parameter2 = 'norisk', parameter3 = 'negative', parameter4 = 'positive', planar = p, n = n)
    t_stat, pval, cond_mean = ttest_vs_zero(data_path, subjects, fr, cond1, parameter3, p, n)

       
    #pval_in_intevals = np.array(pval)
    pval_in_intevals = np.array(pval)
    pval_space_fdr = space_fdr(pval)
    pval_full_fdr =  full_fdr(pval)
    # считаем разницу бета и добавляем к шаблону (донору)
    temp.data = cond_mean

    # время в которое будет строиться топомапы
    if poster:
        times = np.array([1.8])
    else:
        times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])

    # интервалы усредения
    if poster:
        tmin = [1.7]
        tmax = [1.9]
    else:    
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

    binary = p_val_binary(pval_in_intevals, treshold = 0.05)
    title = (f'{cond1}, %s,  LMEM, noFDR'%p)
    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.1, vmax = 0.1, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # space fdr
    binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
    title = (f'{cond1}, %s, LMEM,  space FDR'%p)
    fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.1, vmax = 0.1, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # full fdr
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    if poster:
        title = (f'{cond1}, %s, full FDR'%p)
    else:
        #title = ('norisk vs prerisk, %s, LMEM, full FDR'%p)
        title = (f'{cond1}, %s, full FDR'%p)
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -7.2, vmax = 7.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))



    #os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_prerisk/'.format(feedb, fr) , exist_ok = True)
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/low_{fr}_CORR/topomaps_lines_LMEM_new_poster/{cond1}/' , exist_ok = True)
    #fig.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_prerisk/LMEM_norisk_vs_prerisk_stat_no_fdr_{2}_separ_fb.jpeg'.format(feedb, fr, p), dpi = 300)

    #fig2.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_prerisk/LMEM_norisk_vs_prerisk_stat_space_fdr_{2}_separ_fb.jpeg'.format(feedb, fr, p), dpi = 300)


    #fig3.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/topomaps_lines_LMEM_{1}_poster/norisk_vs_prerisk/LMEM_norisk_vs_prerisk_stat_full_fdr_{2}_separ_fb.jpeg'.format(feedb, fr, p), dpi = 300)
    fig3.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/low_{fr}_CORR/topomaps_lines_LMEM_new_poster/{cond1}/LMEM_full_fdr_{p}.jpeg', dpi = 300)
    fig2.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/low_{fr}_CORR/topomaps_lines_LMEM_new_poster/{cond1}/LMEM_space_fdr_{p}.jpeg', dpi = 300)
    fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/low_{fr}_CORR/topomaps_lines_LMEM_new_poster/{cond1}/LMEM_no_fdr_{p}.jpeg', dpi = 300)
'''
