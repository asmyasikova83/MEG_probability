# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
#from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero, nocolor_topomaps_line
from function import space_fdr, full_fdr, p_val_binary, nocolor_topomaps_line
from config import *

# загружаем таблицу с pvalue, полученными с помощью LMEM в R

if Normals:
    freq_range = 'beta_16_30'
    group = 'normals'
    path_pic = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Normals/{0}/'.format(freq_range)
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Normals/{0}/'.format(freq_range), exist_ok = True)
    #df = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/dataframe_for_LMEM_{0}/p_values_LMEM/p_vals_factor_significance_MEG.csv'.format(freq_range))
    df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_factor_significance_MEG.csv')
if Autists:
    freq_range = 'beta_16_30_trf_early_log'
    group = 'autists'
    path_pic = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Autists/{0}/'.format(freq_range)
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Autists/{0}/'.format(freq_range), exist_ok = True)
    #df = pd.read_csv('/home/vtretyakova/Рабочий стол/probability_learning/dataframe_for_LMEM_{0}/p_values_LMEM/p_vals_factor_significance_MEG.csv'.format(freq_range))
    df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_factor_significance_MEG_group.csv')

# задаем время для построения топомапов (используется в функции MNE plot_topomap)
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = 17 # количество говов в ряду

# задаем временные точнки, в которых будем строить головы, затем мы присвоим их для донора (template)
times_array = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])


##############  empty topomaps line (without color) ##################

temp = nocolor_topomaps_line(n, temp, times_array, temp)

############### 1. feedback_cur #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    pval_s = df[df['sensor'] == i]
    pval_feedback_cur = pval_s['feedback_cur'].tolist()
    pval_in_intevals.append(pval_feedback_cur)

pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'feedback_cur, LMEM %s Hz, noFDR'%freq_range
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, 
        units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', 
        title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), 
        mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', 
            linewidth=0, markersize=10, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'feedback_cur, LMEM %s Hz,  space FDR'%freq_range
fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'feedback_cur, LMEM %s Hz, full FDR'%freq_range
fig3 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

fig3.savefig(f'{path_pic}/LMEM_feedback_cur_stat_{freq_range}_full_fdr.jpeg', dpi = 900)

############### 2. trial_type #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_trial_type = pval_s['trial_type'].tolist()
    pval_in_intevals.append(pval_trial_type)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'trial_type, LMEM %s Hz, noFDR'%freq_range
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, 
        units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s',
        title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), 
        mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k',
            linewidth=0, markersize=10, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'trial_type, LMEM %s Hz,  space FDR'%freq_range
fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1,
        units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s',
        title = title, colorbar = True, extrapolate = "local", mask =
        np.bool_(binary_space), mask_params = dict(marker='o',
            markerfacecolor='green', markeredgecolor='k', linewidth=0,
            markersize=10, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'trial_type, LMEM %s Hz, full FDR'%freq_range
fig3 = temp.plot_topomap(times = time_to_plot,
        ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin =
        -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True,
        extrapolate = "local", mask = np.bool_(binary_full), mask_params =
        dict(marker='o', markerfacecolor='green', markeredgecolor='k',
            linewidth=0, markersize=10, markeredgewidth=2))


fig3.savefig(f'{path_pic}/LMEM_trial_type_stat_{freq_range}_full_fdr.jpeg', dpi = 900)


############### 3. trial_type:feedback_cur #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_trial_type_feedback_cur = pval_s['trial_type:feedback_cur'].tolist()
    pval_in_intevals.append(pval_trial_type_feedback_cur)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

binary = p_val_binary(pval_in_intevals, treshold = 0.05)
title = 'trial_type:feedback_cur, LMEM %s Hz, noFDR'%freq_range
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, 
        units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', 
        title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), 
        mask_params = dict(marker='o', markerfacecolor='green', 
        markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

# space fdr
binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
title = 'trial_type:feedback_cur, LMEM %s Hz, space FDR'%freq_range
fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, 
        units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', 
        title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space), 
        mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', 
        linewidth=0, markersize=10, markeredgewidth=2))

# full fdr
binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
title = 'trial_type:feedback_cur, LMEM %s Hz, full FDR'%freq_range
fig3 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))

fig3.savefig(f'{path_pic}/LMEM_trial_type_feedback_cur_stat_{freq_range}_full_fdr.jpeg', dpi = 900)
