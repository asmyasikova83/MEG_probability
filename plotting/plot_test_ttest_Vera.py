import mne
import os.path as op
import os
#from matplotlib import pyplot as plt
import numpy as np
#from scipy import stats
import copy
from scipy import stats
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero_test, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero



subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                        'P021', 'P022', 'P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                                        'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                                                        'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'

freq_range = 'beta_16_30_trf_early_log'

planars = 'comb_planar'

path = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_article/'
os.makedirs(path, exist_ok = True)
# задаем время и донора
time_to_plot = np.linspace(-0.8, 2.4, num = 17)
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето
######### контраст prerisk wins vs 0, without correction #########################
_, p_val_prerisk, prerisk_mean,  prerisk = ttest_vs_zero_test(data_path, subjects, parameter1 = 'prerisk', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_prerisk, temp, prerisk_mean, time_to_plot, title = 'prerisk no FDR')

fig.savefig(path + 'prerisk_vs_0.jpeg', dpi = 900)
_, p_val_risk, risk_mean, risk = ttest_vs_zero_test(data_path, subjects, parameter1 = 'risk', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_risk, temp, risk_mean, time_to_plot, title = 'risk no FDR')

fig.savefig(path + 'risk_vs_0.jpeg', dpi = 900)
_, p_val_norisk, norisk_mean, norisk = ttest_vs_zero_test(data_path, subjects, parameter1 = 'norisk', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_norisk, temp, risk_mean, time_to_plot, title = 'norisk no FDR')

fig.savefig(path + 'norisk_vs_0.jpeg', dpi = 900)
t_stat_risk, p_val_postrisk, postrisk_mean, postrisk = ttest_vs_zero_test(data_path, subjects, parameter1 = 'postrisk', freq_range = freq_range, planar = planars, n = n)

fig, temp = plot_topo_vs_zero(p_val_postrisk, temp, postrisk_mean, time_to_plot, title = 'postrisk no FDR')

fig.savefig(path + 'postrisk_vs_0.jpeg', dpi = 900)

summarized = True
decision = False
early_fb = False
late_fb = False
default = False

if decision:
    time_to_plot = np.linspace(-0.7, 2.5, num = 6)
if early_fb or late_fb:
    time_to_plot = np.linspace(-0.7, 2.5, num = 9)
if default: 
    time_to_plot = np.linspace(-0.8, 2.4, num = 17)
os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_article/' , exist_ok = True)
if summarized:
    temp.data = (prerisk + risk + norisk + postrisk)/4
    t_stat, p_val = stats.ttest_1samp(temp.data, 0, axis=0)
    binary = p_val_binary(p_val.mean(axis = 0), treshold = 0.05)
    temp.data = temp.data.mean(axis = 0).mean(axis = 0)
    fig_sum_test  = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.6, units = 'dB', show = False, vmin = -1.8, vmax = 1.8, time_unit='s', title = 'pooled choice types', colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',      markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))
    fig_sum_test.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_article/sum_600_ms_avr.jpeg', dpi = 900)
if early_fb:
    cond1 = 'risk'
    cond2 = 'norisk'
    temp.data = risk_mean - norisk_mean
    fig  = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.1, units = 'dB', show = False, vmin = -0.6, vmax = 0.6, time_unit='s', title = f'{cond1} minus {cond2}', colorbar = True, extrapolate = "local")
    fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_article/{cond1}_minus_{cond2}.jpeg', dpi = 900)
