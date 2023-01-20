import mne
import os.path as op
import os
from scipy import stats
import numpy as np
import copy
import statsmodels.stats.multitest as mul
from function import p_val_binary, ttest_pair, extract_and_av_cond_data
from config import *

# загружаем комбайн планары, усредненные внутри каждого испытуемого
prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
freq_range = 'beta_16_30_trf_early_log'
Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
               'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
               'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                        'P335', 'P338', 'P341', 'P342']
data_path_Autists = '{0}/Autists_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)
Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                    'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                    'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                            'P063', 'P064', 'P065', 'P067']
data_path_Normals = '{0}/Normals_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################

N = 8
#t_start = -0.8
#t_end =  2.4
# время в которое будет строиться топомапы
t_start = -0.7
t_end =  2.1
#_start = t
#_end =  t

# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

summarized = True
norisk = False
risk = False
prerisk = False
postrisk = False

########################### norisk vs risk ##############################
for p in planars:
    #Autists

    comp1_risk_A,  comp1_norisk_A, risk_mean_A, norisk_mean_A, p1_val, p2_val  = extract_and_av_cond_data(data_path_Autists, Autists, fr,  n)
    #risk_mean_A, norisk_mean_A, prerisk_mean_A, postrisk_mean_A, p1_val, p2_val, p3_val, p4_val  = extract_and_av_cond_data(data_path_Autists, Autists, fr,  n)
    #Normals
    comp1_risk_N,  comp1_norisk_N, risk_mean_N, norisk_mean_N, p1_val, p2_val  = extract_and_av_cond_data(data_path_Normals, Normals, fr,  n)
    #risk_mean_N, norisk_mean_N, prerisk_mean_N, postrisk_mean_N, p1_val, p2_val, p3_val, p4_val  = extract_and_av_cond_data(data_path_Normals, Normals, fr,  n)
    # считаем бета и добавляем к шаблону (донору)
    if summarized:
        #temp.data = ((comp1_risk_A + comp1_norisk_A)/2 + (comp1_risk_N + comp1_norisk_N)/2)/2
        temp.data = (comp1_norisk_N + comp1_norisk_A)/2
        #temp.data = (risk_mean_A +  norisk_mean_A + prerisk_mean_A + postrisk_mean_A)/4
        #risk_mean = (risk_mean_A + risk_mean_N)/2
        #norisk_mean = (norisk_mean_A + norisk_mean_N)/2
        #prerisk_mean = (prerisk_mean_A + prerisk_mean_N)/2
        #postrisk_mean = (postrisk_mean_A + postrisk_mean_N)/2
        #temp.data = (risk_mean +  norisk_mean + prerisk_mean + postrisk_mean)/4
        print('temp.data.shape', temp.data.shape)
        t_stat, p_val = stats.ttest_1samp(temp.data, 0, axis=0)
        temp.data = temp.data.mean(axis = 0) 
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

    #усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения

    title = 'norisk NT + AT against baseline'
    binary = p_val_binary(p_val, treshold = 0.05)

    fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.4, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',                     markerfacecolor='white', markeredgecolor='yellow', linewidth=0, markersize=7, markeredgewidth=2))
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_autists/' , exist_ok = True)
    fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_autists/{title}_baseline.jpeg', dpi = 900)
