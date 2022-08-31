import mne
import os.path as op
import os
import numpy as np
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, extract_and_av_cond_data
from config import *

# загружаем комбайн планары, усредненные внутри каждого испытуемого
#TODO correct paths
assert(Normals)
if parameter3 == 'negative':
    freq_range = 'beta_16_30_trf_early_log'
    if Normals:
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subjects_comb_planar/'.format(freq_range)
    if Autists:
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
if parameter3 == None:
    if Normals:
        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
    if Autists:
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_into_subj_comb_planar/'

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################

decision = True
early_fb = False
late_fb = False

#1 picture
N = 1
if decision:
    t = -0.5
if early_fb:
    t = 1.3
if late_fb:
    t = 1.7
#for one pic in a row t_start, t_end and times will be dummy
t_start = t
t_end =  t

# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

summarized = False
if not summarized:
    norisk = True
    risk = False
    prerisk = False
    postrisk = False

########################### norisk vs risk ##############################
for p in planars:
    if parameter3 == 'negative':
        #TODO check the function
        if Normals:
            _, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, freq_range, parameter1 = cond1, parameter2 = cond2, parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
        if Autists:
            t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1, parameter2, parameter3, parameter4, planar, n)
        #fb negative
        #temp.data = risk_mean
        #fb positive
        temp.data = norisk_mean
    if parameter3 == None:
        risk_mean, norisk_mean, prerisk_mean, postrisk_mean, p1_val, p2_val, p3_val, p4_val  = extract_and_av_cond_data(data_path, subjects, fr,  n)
        # считаем бета и добавляем к шаблону (донору)
        if summarized:
            temp.data = (risk_mean +  norisk_mean + prerisk_mean + postrisk_mean)/4
            cond = 'summarized'
        if norisk:
            temp.data = norisk_mean
            cond = 'norisk'
        if risk:
            temp.data = risk_mean
            cond = 'risk'
        if prerisk:
            temp.data = prerisk_mean
            cond = 'prerisk'
        if postrisk:
            temp.data = postrisk_mean
            cond = 'postrisk'
    # время в которое будет строиться топомапы
    times = np.array([t])
    # интервалы усредения
    if decision:
        tmin = [-0.9, -0.7, -0.5]
        tmax = [-0.7, -0.5, -0.3]
        #num of intervals to average over
        R = 3
    if early_fb:
        tmin = [1.1, 1.3]
        tmax = [1.3, 1.5]
        R = 2
    if late_fb:
        tmin = [1.5, 1.7]
        tmax = [1.7, 1.9]
        R = 2
    data_for_plotting = np.empty((102, 0))

    #усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения
    
    for i in range(R):
        data_in_interval = temp.copy()
        data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
        data_mean = data_in_interval.data.mean(axis = 1)
        data_mean = data_mean.reshape(102,1)
        data_for_plotting = np.hstack([data_for_plotting, data_mean])
    #summarize 2 timeframes and  obtain a head
    
    data_to_sum = data_for_plotting.mean(axis = 1)
    plotting_LMEM = mne.EvokedArray(data_to_sum[:, np.newaxis], info = temp.info)
    plotting_LMEM.times = times

    stat_sensors=[]
    if decision:
        print(f'{cond}')
        title = f'decision_{cond}'
        f_name = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/signif_sensors/sensors_decision_pre_resp_900_200.txt'
        stat_sensors = np.loadtxt(f_name, dtype = int)
    if early_fb:
        title = f'early_fb_{cond}'
    if late_fb:
        if parameter3 == None:
            title = f'late_fb_{cond1}'
        if parameter3 == 'negative':
            #title = cond1 + 'late_fb_losses'
            title = cond1 + 'late_fb_wins'
        f_name = '/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/threshold/Anterior.txt'
        anterior_sensors = np.loadtxt(f_name, dtype = int)
        f_name = '/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/threshold/Posterior.txt'
        posterior_sensors = np.loadtxt(f_name, dtype = int)
        stat_sensors = np.hstack((anterior_sensors, posterior_sensors))
    cluster = np.zeros((102, 1))

    plot_significant_channels = False
    if plot_significant_channels:
        for s in stat_sensors:
            cluster[s] = 1
    else:
        cluster = np.zeros((102, 1))

    if summarized:
        vmin =  -1.8
        vmax = 1.8
    else:
        vmin =  -4.9
        vmax = 4.9

    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = vmin, vmax = vmax, time_unit='ms', title = title, colorbar = True, extrapolate = "local",  mask = np.bool_(cluster), mask_params = dict(marker='o',            markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps/' , exist_ok = True)
    if Normals:
        fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps/Normals_{title}.jpeg', dpi = 900)
    if Autists:
        fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps/Autists_sum_{title}.jpeg', dpi = 900)
