import mne
import os.path as op
import os
#from matplotlib import pyplot as plt
import numpy as np
#from scipy import stats
import copy
import pandas as pd
from scipy import stats
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_pair_independent, ttest_vs_zero_test, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
fr = 'beta_16_30_trf_early_log'
path_pic = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Autists/{0}'.format(fr)
data_path_Normals = '{0}/Normals_extended/{1}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, fr)
data_path_Autists = '{0}/Autists_extended/{1}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, fr)

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
planars = 'comb_planar'
line = 'Normals_Autists'

os.makedirs(path, exist_ok = True)
# задаем время и донора
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
#vmin = -4.5
#vmax = 4.5

conds = ['prerisk',  'risk', 'postrisk']
#conds = ['risk', 'postrisk']

Normals_Autists = True

if parameter3 == 'negative':
    df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_feedback_MEG_early_log_group.csv')
if parameter3 == None:
    df = pd.read_csv(f'/{prefix}/beta/p_vals_Tukey_by_trial_type_MEG_early_log_group.csv')
# интервалы усредения
tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
# время в которое будет строиться топомапы
times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
N = 17
t_start = -0.8
t_end =  2.4
######### контраст prerisk wins vs 0, without correction #########################
for cond in conds:
    if cond == 'norisk':
        #normals len 24
        if Normals_Autists:
            Normals = Normals_norisk
            Autists = Autists_norisk
        else:
            subjects = subjects_norisk
    if cond == 'prerisk':
        #normals len 18
        if Normals_Autists:
            Normals = Normals_prerisk
            Autists = Autists_prerisk
        else:
            subjects = subjects_prerisk
    if cond == 'risk':
        #normals len 21
        if Normals_Autists:
            Normals = Normals_risk
            Autists = Autists_risk
        else:
            subjects = subjects_risk
    if cond == 'postrisk':
        #normals len 23
        if Normals_Autists:
            Normals = Normals_postrisk
            Autists = Autists_postrisk
        else:
            subjects = subjects_postrisk
    pval_in_intevals = []
    # number of heads in line and the number of intervals into which we divided (see amount of tables with p_value in intervals)
    for i in range(102):
        pval_s = df[df['sensor'] == i]
        if parameter3 == 'negative':
            pval_norisk_risk = pval_s[f'{cond}-negative_positive'].tolist()
        if parameter3 == None:
            pval_norisk_risk = pval_s[f'norisk_{cond}'].tolist()
        pval_in_intevals.append(pval_norisk_risk)
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)

    #inside samples
    paired = False
    #between samples
    independent = True

    temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
    n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето
    if independent:
        _, p_val, risk_mean_Autists, _ = ttest_vs_zero_test(data_path_Autists, Autists, parameter1 = cond, parameter3 =  parameter3, freq_range = fr, planar = planars, n = n)
        _, p_val, risk_mean_Normals, _ = ttest_vs_zero_test(data_path_Normals, Normals, parameter1 = cond, parameter3 =  parameter3, freq_range = fr, planar = planars, n = n)
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
    #fr = 'beta_16_30'
    if paired:
        #TODO using LMM
        title = cond + line + 'noFDR'
        _, p_val, data_mean,  data = ttest_vs_zero_test(data_path, subjects, parameter1 = cond, parameter3 =  parameter3, freq_range = fr, planar = planars, n = n)

        fig, temp = plot_topo_vs_zero(p_val, temp, data_mean, time_to_plot,  vmin, vmax,  title = title)

        fig.savefig(path + title, dpi = 500)
        t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr, parameter1 = cond , parameter2 = 'norisk', parameter3 = parameter3, parameter4 = parameter4, planar = 'comb_planar', n = n)
        p_val_full_fdr = full_fdr(p_val)
        _, fig, temp = plot_deff_topo(p_val_full_fdr, Normals_Autists, temp, risk_mean, norisk_mean, time_to_plot, -1.2, 1.2, title = f'{cond} minus norisk {line}fullFDR')
        fig.savefig(data_pic + f'/{cond}_minus_norisk_{line}.jpeg', dpi = 500)
    if independent:
        if parameter3 == None:
            _, fig1, temp = plot_deff_topo(pval_in_intevals, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals noFDR')
            _, fig2, temp = plot_deff_topo(pval_space_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals spaceFDR')
            _, fig3, temp = plot_deff_topo(pval_full_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals fullFDR')
            fig1.savefig(path_pic + f'/{cond}_minus_{cond}_both_nofdr.jpeg', dpi = 500)
            fig2.savefig(path_pic + f'/{cond}_minus_{cond}_both_space_fdr.jpeg', dpi = 500)
            fig3.savefig(path_pic + f'/{cond}_minus_{cond}_both_full_fdr.jpeg', dpi = 500)
        if parameter3 == 'negative':
            _, fig1, temp = plot_deff_topo(pval_in_intevals, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals noFDR')
            _, fig2, temp = plot_deff_topo(pval_space_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals spaceFDR')
            _, fig3, temp = plot_deff_topo(pval_full_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals fullFDR')
            fig1.savefig(path_pic + f'/{cond}_minus_{cond}_both_nofdr.jpeg', dpi = 500)
            fig2.savefig(path_pic + f'/{cond}_minus_{cond}_both_space_fdr.jpeg', dpi = 500)
            fig3.savefig(path_pic + f'/{cond}_minus_{cond}_both_full_fdr.jpeg', dpi = 500)
