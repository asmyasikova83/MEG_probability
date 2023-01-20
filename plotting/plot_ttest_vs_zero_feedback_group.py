import mne
import os.path as op
import os
#from matplotlib import pyplot as plt
import numpy as np
#from scipy import stats
import copy
from scipy import stats
import statsmodels.stats.multitest as mul
from function import ttest_pair, ttest_vs_zero_feedback_test, ttest_vs_zero_test, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero
from config import *

choices = ['norisk', 'risk']
#choices = ['norisk']
feedback = ['positive', 'negative']
vmin = -4.5
vmax = 4.5

for choice in choices:
    for fb in feedback:
        if choice == 'norisk':
            print('IN NORISK')
            Autists = Autists_norisk
            Normals = Normals_norisk
        if choice == 'risk':
            if fb == 'positive':
                Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                            'P316',  'P320', 'P321',        'P323', 'P324',
                             'P325',         'P327',        'P329', 'P333',
                                   'P335', 'P338', 'P341', 'P342']
                Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                            'P034', 'P035', 'P039',         'P044', 'P047',
                             'P048',        'P055',         'P059', 'P060',
                                    'P063', 'P064', 'P065', 'P067']
            else:
                Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                            'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                             'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                                   'P335', 'P338', 'P341', 'P342']
                Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                            'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                             'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                                     'P063', 'P064', 'P065', 'P067']
        prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
        freq_range = 'beta_16_30_trf_early_log'

        data_path_Autists = '{0}/Autists_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)
        data_path_Normals = '{0}/Normals_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)

###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
        path = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_response_Normals_Autists_feedback_400ms_fin/'
        os.makedirs(path, exist_ok = True)
        # задаем время и донора

        prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
        fr = 'beta_16_30_trf_early_log'

        planars = 'comb_planar'

        # задаем время и донора
        time_to_plot = np.linspace(-0.7, 2.1, num = 8)

        #time_to_plot = np.linspace(-0.8, 2.4, num = 17)
        temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

        n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето
        ######### контраст prerisk wins vs 0, without correction #########################
        _, p_val_norisk, norisk_mean, norisk = ttest_vs_zero_feedback_test(data_path_Autists, Autists, parameter1 = choice, parameter3 = fb, freq_range = freq_range, planar = planars, n = n)
         
        #p_val_norisk_full_fdr= full_fdr(p_val_norisk)
        fig, temp = plot_topo_vs_zero(p_val_norisk, temp, norisk_mean, time_to_plot, vmin, vmax, title = f'Autists {choice} {fb} no FDR')

        fig.savefig(path + f'Autists_{choice}_{fb}_vs_0.jpeg', dpi = 900)
        _, p_val_norisk, norisk_mean, norisk = ttest_vs_zero_feedback_test(data_path_Normals, Normals, parameter1 = choice, parameter3 = fb, freq_range = freq_range, planar = planars, n = n)

        #p_val_norisk_full_fdr= full_fdr(p_val_norisk)
        fig, temp = plot_topo_vs_zero(p_val_norisk, temp, norisk_mean, time_to_plot, vmin, vmax, title = f'Normals {choice} {fb} no FDR')

        fig.savefig(path + f'Normals_{choice}_{fb}_vs_0.jpeg', dpi = 900)
