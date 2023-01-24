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
from function import ttest_pair, ttest_pair_independent, ttest_vs_zero_test, ttest_vs_zero_feedback_test, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
prefix = '_trained'
fr = 'beta_16_30_trf_early_log'
path_pic = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_test/{0}'.format(fr)
data_path_Autists = '{0}/Autists_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
data_path_Normals = '{0}/Normals_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
planars = 'comb_planar'

os.makedirs(path_pic, exist_ok = True)
# задаем время и донора
#time_to_plot = np.linspace(-0.8, 2.4, num = 17)
time_to_plot = np.linspace(-0.7, 2.1, num = 8)
vmin = -4.5
vmax = 4.5

conds = ['norisk', 'risk']
#conds = ['norisk']

parameter3  = 'positive'
fb = parameter3
#fb = 'positive'


print(prefix_data)
if parameter3 == None:
    df = pd.read_csv(f'/{prefix_data}/beta/p_vals_by_trial_type_MEG_group_400ms_fin.csv')
if parameter3 != None:
    df = pd.read_csv(f'/{prefix_data}/beta/p_vals_Tukey_by_feedback_MEG_group_400ms_fin_ed.csv')
print(df)
# интервалы усредения
#tmin = [-0.9, -0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3]
#tmax = [-0.7, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5]
tmin = [-0.9, -0.5, -0.1, 0.3,  0.7, 1.1, 1.5, 1.9]
tmax = [-0.5, -0.1, 0.3,  0.7, 1.1, 1.5, 1.9, 2.3]
# время в которое будет строиться топомапы
#times = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])
times = np.array([-0.7, -0.3, 0.1, 0.5, 0.9, 1.3, 1.7, 2.1])
#N = 17
N = 8
#t_start = -0.8
#t_end =  2.4
t_start = -0.8
t_end =  2.3
######### subjects for autists #########################
for cond in conds:
    print(cond)
    if cond == 'norisk':
        Normals_list = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
               'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
               'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
               'P061', 'P063', 'P064', 'P065', 'P067']
        Autists_list = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
               'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
               'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
               'P334', 'P335', 'P338', 'P341', 'P342']
    if cond == 'risk':
        if parameter3 == None:
            Normals_list = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                       'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                       'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                       'P063', 'P064', 'P065', 'P067']
            Autists_list = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                       'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
        if fb == 'positive':
            Autists_list = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                        'P316',  'P320', 'P321',        'P323', 'P324',
                        'P325',         'P327',        'P329', 'P333',
                        'P335', 'P338', 'P341', 'P342']
            Normals_list = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                        'P034', 'P035', 'P039',         'P044', 'P047',
                        'P048',        'P055',         'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']
        if fb == 'negative':
            Autists_list = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                       'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
            Normals_list = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                       'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                       'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                       'P063', 'P064', 'P065', 'P067']
    pval_in_intevals = []
    # number of heads in line and the number of intervals into which we divided (see amount of tables with p_value in intervals)
    for i in range(102):
        pval_s = df[df['sensor'] == i]
        if parameter3 != None:
            pval_norisk_risk = pval_s[f'{cond}-{fb}-normals_autists'].tolist()
        if parameter3 == None:
            pval_norisk_risk = pval_s[f'{cond}-normals_autists'].tolist()
        pval_in_intevals.append(pval_norisk_risk)
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)

    temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
    n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето
    if parameter3 == None:
        _, p_val, risk_mean_Autists, _ = ttest_vs_zero_test(data_path_Autists, Autists_list, parameter1 = cond, parameter3 =  None, freq_range = fr, planar = planars, n = n)
        _, p_val, risk_mean_Normals, _ = ttest_vs_zero_test(data_path_Normals, Normals_list, parameter1 = cond, parameter3 =  None, freq_range = fr, planar = planars, n = n)
    if parameter3 != None:
        _, p_val, risk_mean_Autists, _ = ttest_vs_zero_feedback_test(data_path_Autists, Autists_list, parameter1 = cond, parameter3 =  f'{fb}', freq_range = fr, planar = planars, n = n)
        _, p_val, risk_mean_Normals, _ = ttest_vs_zero_feedback_test(data_path_Normals, Normals_list, parameter1 = cond, parameter3 =  f'{fb}', freq_range = fr, planar = planars, n = n)
    # считаем разницу бета и добавляем к шаблону (донору)
    data_for_plotting = np.empty((102, 0))
    #усредняем сигнал в каждом из интервалов усреднения и собираем в единый np.array (102 x n) где 102 - количество комбайнд планаров, а n - количество интервалов усредения
    #we will plot the difference
    temp.data = risk_mean_Autists - risk_mean_Normals
    #temp1.data = risk_mean_Autists
    #temp2.data = risk_mean_Normals
    for i in range(N):
        data_in_interval = temp.copy()
        data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
        data_mean = data_in_interval.data.mean(axis = 1)
        data_mean = data_mean.reshape(102,1)
        data_for_plotting = np.hstack([data_for_plotting, data_mean])
    plotting_LMEM = mne.EvokedArray(data_for_plotting, info = temp.info)
    plotting_LMEM.times = times

    data_for_plotting = np.empty((102, 0))
    print('Drawing')
    if parameter3 == None:
        _, fig1, temp = plot_deff_topo(pval_in_intevals, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals noFDR')
        _, fig2, temp = plot_deff_topo(pval_space_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals spaceFDR')
        _, fig3, temp = plot_deff_topo(pval_full_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} Autists minus {cond} Normals fullFDR')
        fig1.savefig(path_pic + f'/{cond}_AT_minus_{cond}_NT_nofdr.jpeg', dpi = 500)
        fig2.savefig(path_pic + f'/{cond}_AT_minus_{cond}_NT_space_fdr.jpeg', dpi = 500)
        fig3.savefig(path_pic + f'/{cond}_AT_minus_{cond}_NT_full_fdr.jpeg', dpi = 500)
    if parameter3 != None:
        _, fig1, temp = plot_deff_topo(pval_in_intevals, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} {fb} Autists-Normals noFDR')
        _, fig2, temp = plot_deff_topo(pval_space_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} {fb} Autists-Normals spaceFDR')
        _, fig3, temp = plot_deff_topo(pval_full_fdr, Normals_Autists, plotting_LMEM, risk_mean_Autists, risk_mean_Normals, time_to_plot, -1.2, 1.2, title = f'{cond} {fb} Autists-Normals fullFDR')
        fig1.savefig(path_pic + f'/{cond}_{fb}_Autists-Normals_nofdr.jpeg', dpi = 500)
        fig2.savefig(path_pic + f'/{cond}_{fb}_Autists-Normals_space_fdr.jpeg', dpi = 500)
        fig3.savefig(path_pic + f'/{cond}_{fb}_Autists-Normals_full_fdr.jpeg', dpi = 500)
