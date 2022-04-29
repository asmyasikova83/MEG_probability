#https://mne.tools/dev/auto_examples/stats/plot_fdr_stats_evoked.html#sphx-glr-auto-examples-stats-plot-fdr-stats-evoked-py

import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий  see config ###################
#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar'
if not response:
    data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_stim/ttests/'
else:
    if parameter3 == 'negative':
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
    if  parameter3 == None:
        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar'

path = '/net/server/data/Archive/prob_learn/asmyasnikova83/supplementary/ttests/'
freq_range = 'beta_16_30_trf_early_log'
os.makedirs(path, exist_ok = True)
# задаем время и донора
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето
resolution = 300
planars = 'comb_planar'
######### контраст norisk losses vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'norisk', parameter3 = 'negative', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'norisk losses no FDR')

fig.savefig(path + 'norisk_losses_vs_0.jpeg', dpi = resolution)
    ######### контраст norisk wins vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'norisk', parameter3 = 'positive', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'norisk wins no FDR')

fig.savefig(path + 'norisk_wins_vs_0.jpeg', dpi = resolution)
######### контраст prerisk losses vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'prerisk', parameter3 = 'negative', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'prerisk losses no FDR')

fig.savefig(path + 'prerisk_losses_vs_0.jpeg', dpi = resolution)
######### контраст prerisk wins vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'prerisk', parameter3 = 'positive', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'prerisk wins no FDR')

fig.savefig(path + 'prerisk_wins_vs_0.jpeg', dpi = resolution)
######### контраст risk losses vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'risk', parameter3 = 'negative', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'risk losses no FDR')

fig.savefig(path + 'risk_losses_vs_0.jpeg', dpi = resolution)
######### контраст risk wins vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'risk', parameter3 = 'positive', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'risk wins no FDR')

fig.savefig(path + 'risk_wins_vs_0.jpeg', dpi = resolution)
######### контраст postrisk losses vs 0, without correction #########################
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'postrisk', parameter3 = 'negative', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'postrisk losses no FDR')

fig.savefig(path + 'postrisk_losses_vs_0.jpeg', dpi = resolution)
######### контраст postrisk wins vs 0, without correction #########################
	
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'postrisk', parameter3 = 'positive', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'postrisk wins no FDR')

fig.savefig(path + 'postrisk_wins_vs_0.jpeg', dpi = resolution)
'''
######### контраст norisk vs postrisk, with full fdr correction #########################

t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr = freq_range, parameter1 = 'postrisk', parameter2 = 'norisk', parameter3 = None, parameter4 = None , planar = 'comb_planar',  n = n)

p_val_full_fdr = full_fdr(p_val)

_, fig1, temp = plot_deff_topo(p_val_full_fdr, temp, norisk_mean, risk_mean, time_to_plot, title = 'norisk vs postrisk, full FDR')

fig1.savefig(path + 'norisk_vs_postrisk_stat_full_fdr.jpeg', dpi = 900)

'''
