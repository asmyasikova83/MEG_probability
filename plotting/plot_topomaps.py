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

#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar'
data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
freq_range = 'beta_16_30'
planar = 'comb_planar'

subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
            'P021', 'P022', 'P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
            'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
            'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
'''
cond_list = ['_norisk_fb_cur_positive',
             '_prerisk_fb_cur_positive',
             '_risk_fb_cur_positive',
             '_postrisk_fb_cur_positive',
             '_norisk_fb_cur_negative',
             '_prerisk_fb_cur_negative',
             '_risk_fb_cur_negative',
             '_postrisk_fb_cur_negative'
             ]

#out_path='/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/' #path to epochs
out_path='/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim_second_bl_epo/'
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


subj_list = subjects.copy()
for i,subject in enumerate(subjects):
    subject_files = [file for file in f if subject in file] #make list with all subject files 
    for j in cond_list: #check if subject has all conditions
        if not any(j in s for s in subject_files):
            if subject in subj_list:
                subj_list.remove(subject)

subjects = subj_list
print(len(subjects))

'''
# задаем время и донора
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

'''
	##### 1. norisk - risk #####
######### 1.1 контраст norisk vs 0, without correction #########################
	
t_stat_norisk, p_val_norisk, norisk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'norisk', n = n)
title = 'norisk vs zero, no FDR'
fig, temp = plot_topo_vs_zero(p_val_norisk, temp, norisk_mean, time_to_plot, title)

fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_0_stat_no_fdr.jpeg', dpi = 300)

temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/norisk_vs_0.fif')  # save evoked data to disk
'''
######### 1.2 контраст risk vs 0, without correction #########################
	
t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'postrisk', freq_range = freq_range, planar = planar, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'postrisk vs zero, no FDR')

#fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/risk_vs_0_stat_no_fdr.jpeg', dpi = 300)
path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topolpmaps/postrisk_stim/'
os.makedirs(path, exist_ok = True)
fig.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topolpmaps/postrisk_stim/postrisk_vs_0.jpeg', dpi = 300)
#temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_lines_LMEM_new_poster/postrisk/postrisk_vs_0.fif')  # save evoked data to disk
'''
######### 1.3 контраст norisk vs risk, without correction #########################

t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, subjects, parameter1 = 'risk', parameter2 = 'norisk', n = n)

_, fig2, temp = plot_deff_topo(p_val, temp, norisk_mean, risk_mean, time_to_plot, title = 'norisk vs risk, no FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_risk_stat_no_fdr.jpeg', dpi = 300)

temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/norisk_vs_risk.fif')  # save evoked data to disk

######### 1.4 контраст norisk vs risk, with space fdr correction #########################

p_val_space_fdr = space_fdr(p_val)

_, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, risk_mean, time_to_plot, title = 'norisk vs risk, space FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_risk_stat_space_fdr.jpeg', dpi = 300)



######### 1.5 контраст norisk vs risk, with full fdr correction #########################

p_val_full_fdr = full_fdr(p_val)

_, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, risk_mean, time_to_plot, title = 'norisk vs risk, full FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_risk/norisk_vs_risk_stat_full_fdr.jpeg', dpi = 300)

'''
######### 1.5 контраст norisk vs postrisk, with full fdr correction #########################

t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, subjects, fr = freq_range, parameter1 = 'postrisk', parameter2 = 'norisk', parameter3 = None, parameter4 = None , planar = 'comb_planar',  n = n)

p_val_full_fdr = full_fdr(p_val)

_, fig2, temp = plot_deff_topo(p_val_full_fdr, temp, norisk_mean, risk_mean, time_to_plot, title = 'norisk vs postrisk, full FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topolpmaps/postrisk_stim//norisk_vs_postrisk_stat_full_fdr.jpeg', dpi = 300)
'''


	##### 2. norisk - prerisk #####

######### 2.1 контраст norisk vs 0, without correction #########################
	
t_stat_norisk, p_val_norisk, norisk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'norisk', n = n)

fig, temp = plot_topo_vs_zero(p_val_norisk, temp, norisk_mean, time_to_plot, title = 'norisk vs zero, no FDR')

fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_0_stat_no_fdr.jpeg', dpi = 300)

######### 2.2 контраст prerisk vs 0, without correction #########################
	
t_stat_prerisk, p_val_prerisk, prerisk_mean = ttest_vs_zero(data_path, subjects, parameter1 = 'prerisk', n = n)

fig, temp = plot_topo_vs_zero(p_val_prerisk, temp, prerisk_mean, time_to_plot, title = 'prerisk vs zero, no FDR')

fig.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/prerisk_vs_0_stat_no_fdr.jpeg', dpi = 300)

temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/prerisk_vs_0.fif')  # save evoked data to disk

######### 2.3 контраст norisk vs prerisk, without correction #########################
n
t_stat, p_val, prerisk_mean, norisk_mean = ttest_pair(data_path, subjects, parameter1 = 'prerisk', parameter2 = 'norisk', n = n)

_, fig2, temp = plot_deff_topo(p_val, temp, norisk_mean, prerisk_mean, time_to_plot, title = 'norisk vs prerisk, no FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_prerisk_stat_no_fdr.jpeg', dpi = 300)

temp.save('/home/vtretyakova/Рабочий стол/probability_learning/evoked_for_topo/norisk_vs_prerisk.fif')  # save evoked data to disk

######### 2.4 контраст norisk vs prerisk, with space fdr correction #########################

p_val_space_fdr = space_fdr(p_val)

_, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, prerisk_mean, time_to_plot, title = 'norisk vs prerisk, space FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_prerisk_stat_space_fdr.jpeg', dpi = 300)



######### 2.5 контраст norisk vs prerisk, with full fdr correction #########################

p_val_full_fdr = full_fdr(p_val)

_, fig2, temp = plot_deff_topo(p_val_space_fdr, temp, norisk_mean, prerisk_mean, time_to_plot, title = 'norisk vs prerisk, full FDR')

fig2.savefig('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/topomaps_lines/norisk_vs_prerisk/norisk_vs_prerisk_stat_full_fdr.jpeg', dpi = 300)
'''


