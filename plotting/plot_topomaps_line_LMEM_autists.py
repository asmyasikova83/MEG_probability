import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

N = 17
t_start = -0.8
t_end =  2.4

# интервалы усредения
tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
# задаем время и донора
time_to_plot = np.linspace(t_start, t_end, num = N)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
p = 'comb_planar'
n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов
# время в которое будет строиться топомапы
times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'

if parameter3 == 'negative':
#TODO
    df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_feedback_MEG_early_log_group.csv')
if parameter3 == None:
    df = pd.read_csv(f'/{prefix}/beta/p_vals_group_by_trial_type_MEG_beta.csv')

fr = 'beta_16_30_trf_early_log'
conditions = ['norisk', 'prerisk', 'risk', 'postrisk']

#if response:
for cond in conditions:
    if cond == 'norisk':
        subjects_Normals = Normals_norisk
        subjects_Autists = Autists_norisk
    if cond == 'risk':
        subjects_Normals = Normals_risk
        subjects_Autists = Autists_risk
    if cond == 'prerisk':
        subjects_Normals = Normals_prerisk
        subjects_Autists = Autists_prerisk
    if cond == 'postrisk':
        subjects_Normals = Normals_postrisk
        subjects_Autists = Autists_postrisk
    path_pic_Autists = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Autists/{0}/'.format(fr)
    path_pic_Normals = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Normals/{0}/'.format(fr)
    data_path_Normals = '{0}/Normals_extended/{1}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, fr)
    data_path_Autists = '{0}/Autists_extended/{1}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, fr)
#else:
#    #TODO for stim
#    freq_range = 'beta_16_30_trf_no_log_division_stim'
#    if parameter3 == 'negative':
#        data_path = '/{0}/stim_check/{1}_feedback/{1}_ave_comb_planar'.format(prefix, freq_range)
#    if parameter3 == None:
#        data_path = '/{0}/stim_check/{1}/{1}_ave_comb_planar'.format(prefix, freq_range)

    # загружаем комбайн планары, усредненные внутри каждого испытуемогo
    _, _, risk_mean_Autists, norisk_mean_Autists = ttest_pair(data_path_Autists, response, subjects_Autists, fr, parameter1 = f'{cond}', parameter2 = 'norisk', 
                                                              parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
    _, _, risk_mean_Normals, norisk_mean_Normals = ttest_pair(data_path_Normals, response, subjects_Normals, fr, parameter1 = f'{cond}', parameter2 = 'norisk', 
                                                              parameter3 = parameter3, parameter4 = parameter4, planar = p,  n = n)
    ########################### p value #############################

    pval_in_intevals = []
    # number of heads in line and the number of intervals into which we divided (see amount of tables with p_value in intervals)
    for i in range(102):
        pval_s = df[df['sensor'] == i]
        if parameter3 == 'negative':
            #TODO for autists
            pval_norisk_risk = pval_s[f'{cond}-negative_positive'].tolist()
        if parameter3 == None:
            pval_norisk_risk = pval_s[f'{cond}-normals_autists'].tolist()
        pval_in_intevals.append(pval_norisk_risk)
        
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)
    # считаем разницу бета и добавляем к шаблону (донору)
    temp.data = risk_mean_Autists - risk_mean_Normals
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

    #no fdr
    binary = p_val_binary(pval_in_intevals, treshold = 0.05)
    if parameter3 == 'negative':
        # TODO between samples
        title = (f'In {cond} feedback negative vs positive, %s, LMEM, noFDR'%p)
    if parameter3 == None:
        title = (f'{cond} Autists minus {cond} Normals, %s, LMEM, noFDR'%p)
    fig = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2,                                                                                                         time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), 
                                      mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # space fdr
    binary_space = p_val_binary(pval_space_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {cond} feedback negative vs positive, %s, LMEM, space FDR'%p)
    if parameter3 == None:
        title = (f'{cond} Autists minus {cond} Normals, %s, LMEM, spaceFDR'%p)
    fig2 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, 
                                      time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_space),
                                      mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))

    # full fdr
    binary_full = p_val_binary(pval_full_fdr, treshold = 0.05)
    if parameter3 == 'negative':
        title = (f'In {cond} feedback negative vs positive, %s, LMEM, fullFDR'%p)
    if parameter3 == None:
        title = (f'{cond} Autists minus {cond} Normals, %s, LMEM, fullFDR'%p)
    fig3 = plotting_LMEM.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, 
                                      time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary_full), 
                                      mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=9, markeredgewidth=4))

    print('FIGS ready, saving...')

    if parameter3 == 'negative':
        os.makedirs(f'/{path_pic_Autists}/{cond}_across_samples/', exist_ok = True)
        fig.savefig(f'/{path_pic_Autists}/{cond}_across_samples/LMEM_{cond}_{parameter3}_vs_{parameter4}_stat_no_fdr_{fr}_separ_fb.jpeg', dpi = 900)
        fig3.savefig(f'/{path_pic_Autists}/{cond}_across_samples/LMEM_{cond}_{parameter3}_vs_{parameter4}_stat_space_fdr_{fr}_separ_fb.jpeg', dpi = 900)
        fig3.savefig(f'/{path_pic_Autists}/{cond}_across_samples/LMEM_{cond}_{parameter3}_vs_{parameter4}_stat_full_fdr_{fr}_separ_fb.jpeg', dpi = 900)
    if parameter3 == None:
        os.makedirs(f'/{path_pic_Autists}/{cond}_minus_{cond}_both/' , exist_ok = True)
        fig.savefig(f'/{path_pic_Autists}/{cond}_minus_{cond}_both/LMEM_{cond}_minus_{cond}_both_stat_no_fdr_{fr}.jpeg', dpi = 900)
        fig2.savefig(f'/{path_pic_Autists}/{cond}_minus_{cond}_both/LMEM_{cond}_minus_{cond}_stat_space_fdr_{fr}.jpeg', dpi = 900)
        fig3.savefig(f'/{path_pic_Autists}/{cond}_minus_{cond}_both/LMEM_{cond}_minus_{cond}_stat_full_fdr_{fr}.jpeg', dpi = 900)

