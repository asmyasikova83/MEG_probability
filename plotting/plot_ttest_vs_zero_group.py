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

prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
freq_range = 'beta_16_30_trf_early_log'

data_path_Autists = '{0}/Autists_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)
data_path_Normals = '{0}/Normals_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)

path = '/net/server/data/Archive/prob_learn/asmyasnikova83/topomaps_LMEM_600ms/'
os.makedirs(path, exist_ok = True)
choices = [ 'norisk', 'risk']
#feedback = ['positive', 'negative']
vmin = -4.5
vmax = 4.5

fr = 'beta_16_30_trf_early_log'

planars = 'comb_planar'
# задаем время и донора
#time_to_plot = np.linspace(-0.7, 2.1, num = 8)

#time_to_plot = np.linspace(-0.8, 2.4, num = 17)
time_to_plot = np.linspace(-0.6, 1.8, num = 5)

temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

n = temp.data.shape[1] # количество временных отчетов для combined planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчето

for choice in choices:
    assert(Normals_Autists)
    if choice == 'norisk':
        Autists = Autists
        Normals = Normals
    if choice == 'risk':
        Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                    'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                    'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                            'P063', 'P064', 'P065', 'P067']
        Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                   'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                    'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                            'P335', 'P338', 'P341', 'P342']

    _, p_val_risk, risk_mean, risk = ttest_vs_zero_test(data_path_Autists, Autists, parameter1 = choice, parameter3 = None, freq_range = freq_range, planar = planars, n = n)
    #p_val_risk_full_fdr= full_fdr(p_val_risk)
    p_val_risk_full_fdr= p_val_risk

    fig, temp = plot_topo_vs_zero(p_val_risk_full_fdr, temp, risk_mean,  time_to_plot,  vmin, vmax, title = f'{choice} Autists no FDR')
    fig.savefig(path + f'{choice}_Autists_vs_0.jpeg', dpi = 500)

    _, p_val_risk, risk_mean, risk = ttest_vs_zero_test(data_path_Normals, Normals, parameter1 = choice, parameter3 = None, freq_range = freq_range, planar = planars, n = n)
    #p_val_risk_full_fdr= full_fdr(p_val_risk)
    p_val_risk_full_fdr= p_val_risk

    fig, temp = plot_topo_vs_zero(p_val_risk_full_fdr, temp, risk_mean, time_to_plot,  vmin, vmax, title = f'{choice} Normals no FDR')
    fig.savefig(path + f'{choice}_Normals_vs_0.jpeg', dpi = 500)

