#https://mne.tools/dev/auto_examples/stats/plot_fdr_stats_evoked.html#sphx-glr-auto-examples-stats-plot-fdr-stats-evoked-py

import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_pair_independent, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий  see config ###################


freq_range =  'beta_16_30_trf_early_log'
fr1 =  'beta_16_30_trf_early_log'
fr2 =  'beta_16_30_trf_early_log'

#data path
if not response:
    #stimulus data
    data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/topomaps_stim/ttests/'
else:
    if parameter3 == 'negative':
        if Normals:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subjects_comb_planar/'.format(freq_range)
        if Autists:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
        if Normals_Autists:
            #contrast between N and A
            data_path1 = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
            data_path2 = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subjects_comb_planar/'.format(freq_range)
    if  parameter3 == None:
        if Normals:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/beta_16_30_ave_into_subjects_comb_planar/'
        if Autists:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
        if Normals_Autists:
            #contrast between N and A
            data_path1 = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/'.format(freq_range)
            #data_path2 = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar'
            data_path2 = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/beta_16_30_ave_into_subjects_comb_planar/'

#path for plots
if Normals:
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/supplementary/Normals/ttests_fin_ch_bline_full_fdr/'
if Autists:
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/supplementary/Autists/ttests_fin_ch_bline_full_fdr/'
if Normals_Autists:
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/supplementary/Normals_Autists/ttests_fin_ch_bline_full_fdr/'
print(path)
os.makedirs(path, exist_ok = True)
# задаем время и донора
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето
#resolution of plots, settings for plotting
resolution = 300
vmin = -4.5
vmax = 4.5
vmin_contrast = -1.2
vmax_contrast = 1.2
choice_type_vs_zero = True
main_contrast = False
main_contrast_across_samples = False
#check the sample of participants and data path
print(data_path)
#print(subjects)

#choice_type = ['norisk', 'risk', 'prerisk', 'postrisk']
choice_type = ['norisk']
#for risk fb neg, risk fb pos 21 autists (minus 322, 326, 327)
#for prerisk fb neg, risk fb pos 20 autists (minus 313, 318, 333, 312, 316, 322, 326,  P329) - 13 subj
######### контраст choice_type vs 0, without correction #########################
for choice in choice_type:
    if choice_type_vs_zero:
        assert(not Normals_Autists)

        if parameter3 == None:
            t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = choice, parameter3 = parameter3, freq_range = freq_range, planar = planars, n = n)
            fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, vmin, vmax, title = f'{choice} {sample} no fdr')

            fig.savefig(path + f'{choice}_vs_0_{sample}_test.jpeg', dpi = resolution)

        if parameter3 == 'negative':
            t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = choice, parameter3 = parameter3, freq_range = freq_range, planar = planars, n = n)

            fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, vmin, vmax, title = f'{choice} {parameter3} {sample}')

            fig.savefig(path + f'{choice}_{parameter3}_vs_0_{sample}.jpeg', dpi = resolution)

            t_stat_risk, p_val_risk, risk_mean = ttest_vs_zero(data_path, subjects, parameter1 = choice, parameter3 = parameter4, freq_range = freq_range, planar = planars, n = n)

            fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, vmin, vmax, title = f'{choice} {parameter4} {sample}')

            fig.savefig(path + f'{choice}_{parameter4}_vs_0_{sample}.jpeg', dpi = resolution)

######### контраст norisk vs choice type in a sample separately, no full fdr correction #########################

    if main_contrast:
        assert(not Normals_Autists)
        t_stat, p_val, risk_mean, norisk_mean = ttest_pair(data_path, response, subjects, fr = freq_range, parameter1 = choice, parameter2 = 'norisk', parameter3 = parameter3, parameter4 = parameter4 , planar = planars,  n = n)
        p_val_no_fdr = p_val

        p_val_full_fdr = full_fdr(p_val)

        if parameter3 == None:

            _, fig1, temp = plot_deff_topo(p_val_full_fdr, Normals_Autists, temp, risk_mean, norisk_mean, time_to_plot, vmin_contrast, vmax_contrast, title = f'{choice} minus norisk {sample}, full FDR')

            fig1.savefig(path + f'{choice}_minus_norisk_stat_full_fdr.jpeg', dpi = resolution)

        if parameter3 == 'negative':

            _, fig1, temp = plot_deff_topo(p_val_full_fdr, Normals_Autists, temp, risk_mean, norisk_mean, time_to_plot, vmin_contrast, vmax_contrast, title = f'{choice} {parameter3}-{parameter4}')

            fig1.savefig(path + f'{choice}_{parameter3}_minus_{parameter4}_stat_full_fdr.jpeg', dpi = resolution)

######### контраст norisk vs choice type across Normals and Autists, no full fdr correction #########################
    if main_contrast_across_samples:
        assert(Normals_Autists)

        if parameter3 == None:
            t_stat, p_val, risk_mean, norisk_mean = ttest_pair_independent(data_path1, data_path2, response, Autists, Normals, fr1, fr2, parameter1 = choice, 
                                                                       parameter3 = parameter3, planar = planars,  n = n)

            p_val_no_fdr = p_val

            p_val_full_fdr = full_fdr(p_val)

            _, fig1, temp = plot_deff_topo(p_val_full_fdr,  Normals_Autists, temp, risk_mean, norisk_mean, time_to_plot, vmin_contrast, vmax_contrast, title = f'{choice} Autists minus {choice} Norm,full FDR')

            fig1.savefig(path + f'{choice}_minus_{choice}_{sample}_stat_full_fdr.jpeg', dpi = resolution)

        if parameter3 == 'negative':

            t_stat, p_val, risk_mean, norisk_mean = ttest_pair_independent(data_path1, data_path2, response, Autists, Normals, fr1, fr2, parameter1 = choice, 
                                                                       parameter3 = parameter3, planar = planars,  n = n)

            p_val_no_fdr = p_val

            p_val_full_fdr = full_fdr(p_val)

            _, fig1, temp = plot_deff_topo(p_val_full_fdr,  Normals_Autists, temp, risk_mean, norisk_mean, time_to_plot, vmin_contrast, vmax_contrast, title = f'{choice} Autists {parameter3}- Norm {parameter3},full FDR')

            fig1.savefig(path + f'{choice}_{parameter3}-{parameter3}_{sample}_stat_full_fdr.jpeg', dpi = resolution)

            t_stat, p_val, risk_mean, norisk_mean = ttest_pair_independent(data_path1, data_path2, response, Autists, Normals, fr1, fr2, parameter1 = choice, 
                                                                       parameter3 = parameter4, planar = planars,  n = n)

            p_val_no_fdr = p_val

            p_val_full_fdr = full_fdr(p_val)

            _, fig1, temp = plot_deff_topo(p_val_full_fdr,  Normals_Autists, temp, risk_mean, norisk_mean, time_to_plot, vmin_contrast, vmax_contrast, title = f'{choice} Autists {parameter4}-Norm {parameter4}, full FDR')

            fig1.savefig(path + f'{choice}_{parameter4}-{parameter4}_{sample}_stat_full_fdr.jpeg', dpi = resolution)
