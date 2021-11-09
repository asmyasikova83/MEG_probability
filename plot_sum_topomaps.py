import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero, extract_and_av_cond_data
from config import *

# загружаем комбайн планары, усредненные внутри каждого испытуемого
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
print(fr)
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################

N = 1
#for one pic in a row t_start, t_end and times will be dummy
#t_start = 0.7
#t_end =  0.7
t_start = -0.3
t_end = -0.3

# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов
########################### norisk vs risk ##############################
for p in planars:
    risk_mean, norisk_mean, prerisk_mean, postrisk_mean, p1_val, p2_val, p3_val, p4_val  = extract_and_av_cond_data(data_path, subjects, fr,  n)
       #df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/p_val_low_{1}/p_vals_fb_cur_Tukey_by_trial_type_MEG.csv'.format(feedb, fr)) #TODO: fb_cur remove
    
    ########################### p value #############################
    # загружаем таблицу с pvalue, полученными с помощью LMEM в R

    # number of heads in line and the number of intervals into which we divided (see amount of tables with p_value in intervals)
    # считаем разницу бета и добавляем к шаблону (донору)
    #temp.data = risk_mean +  norisk_mean + prerisk_mean + postrisk_mean
    temp.data = norisk_mean
    #tmin = [-0.5, -0.3]
    #tmax = [-0.3, -0.1]
    # время в которое будет строиться топомапы
    #times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
    times = np.array([-0.3])
        # интервалы усредения
    #tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
    #tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
    tmin = [-0.5, -0.3]
    tmax = [-0.3, -0.1]
    #tmin = [1.5, 1.7]
    #tmax = [1.7, 1.9]

    data_for_plotting = np.empty((102, 0))

    #усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения
    
    for i in range(N+1):
        data_in_interval = temp.copy()
        data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
        data_mean = data_in_interval.data.mean(axis = 1)
        data_mean = data_mean.reshape(102,1)
        data_for_plotting = np.hstack([data_for_plotting, data_mean])
    #summarize 2 timeframes and obtain a head     
    data_to_sum = (data_for_plotting[:,0] + data_for_plotting[:,1])/2
    plotting_LMEM = mne.EvokedArray(data_to_sum[:, np.newaxis], info = temp.info)
    plotting_LMEM.times = times
    #title = ('sum cond decision')
    title = ('norisk')
    pval_full_fdr =  full_fdr(p2_val)
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.8, vmax = 1.8, time_unit='ms', title = title, colorbar = True, extrapolate = "local", mask_params = dict(marker='o',            markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    #fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -6.0, vmax = 6.0, time_unit='s', title = title, colorbar = True, extrapolate = "local")

    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps/' , exist_ok = True)
    fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps/decision_norisk.jpeg', dpi = 900)
