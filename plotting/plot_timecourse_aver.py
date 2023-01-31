import mne
import os.path as op
import os
import scipy
from scipy import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import space_fdr, full_fdr, p_val_binary, compute_p_val, compute_p_val_group, plot_stat_comparison, to_str_ar, clear_html, add_str_html,  add_pic_time_course_html,resample_before_stat
from config import *

options = {
    'page-size':'A2',
    'orientation':'Portrait',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}


prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
prefix = '_trained'
fr = 'beta_16_30_trf_early_log'
path_pic = '/net/server/data/Archive/prob_learn/asmyasnikova83/timecourses_LMEM_test/{0}'.format(fr)


cond1 = 'norisk'
cond2 = 'norisk'
#parameter3 = 'negative'
#parameter4 = 'negative'

parameter3 = None
parameter4 = None

if Autists:
    data_path = '{0}/Autists_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
    if parameter3 == None:
        subjects = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                       'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
    if parameter3 == 'negative':
        subjects = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321',    'P323', 'P324',
                       'P325',          'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
if Normals:
    data_path = '{0}/Normals_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
    if parameter3 == None:
        subjects = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']
    if parameter3 == 'negative':
        subjects = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055',         'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']
if Normals_Autists:
    data_path_AT = '{0}/Autists_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
    data_path_NT = '{0}/Normals_extended/{1}{2}_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix_data, fr, prefix)
    if parameter3 == None:
        Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                       'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
        Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']
    if parameter3 == 'negative' or parameter3 == 'positive':
        Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
                       'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
                       'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
                       'P335', 'P338', 'P341', 'P342']
        Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
                        'P063', 'P064', 'P065', 'P067']

temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
#array for fewer time points for t stat
time, idx_array_extended = resample_before_stat(t_min, t_max)

# задаем время и донора

#time = temp.times# количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

########################### norisk vs risk ##############################


#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/net/server/data/Archive/prob_learn/asmyasnikova83/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'/net/server/data/Archive/prob_learn/asmyasnikova83/channel_labels.mat')['chanlabels'])
os.makedirs(path + 'output/', exist_ok=True)

group = True

for p in planars:
    #extract data and ttest
    if group:
        print(data_path_AT)
        print(data_path_NT)
        print(cond1)
        print(cond2)
        print(parameter3)
        print(parameter4)
        comp1_mean, comp2_mean, comp3_mean, _, _, p_val = compute_p_val_group(response, data_path_AT, data_path_NT, Autists, Normals, cond1, cond2, parameter3, parameter4, fr, time, t, idx_array_extended)
    else:
        assert(group == False)
        comp1_mean, comp2_mean, comp3_mean, _, _, p_val = compute_p_val(response, data_path, subjects, cond1, cond2, parameter3, parameter4, fr, time, t, idx_array_extended)
    #scaling
    if comp1_mean.max()>comp2_mean.max():
        p_mul_max=comp1_mean.max()+ abs(comp1_mean.max()/10)
    else:
        p_mul_max=comp2_mean.max()+ abs(comp2_mean.max()/10)

    if comp1_mean.min()<comp2_mean.min():
        p_mul_min=comp1_mean.min() - abs(comp1_mean.min()/10)
    else:
        p_mul_min=comp2_mean.min() - abs(comp2_mean.min()/10)

    if group != True:
        if parameter3 == 'negative' or parameter3 == 'positive':
            if cond1 == 'risk':
                name = 'LP'
            if cond1 == 'norisk':
                name = 'HP'
            cond1_name = name + '_' + parameter3
            cond2_name = name + '_' + parameter4
        if parameter3 == None:
            if cond1 == 'risk':
               cond1_name = 'LP'
               cond2_name = 'HP'
    if group == True:
        if parameter3 == 'negative' or parameter3 == 'positive':
            if cond1 == 'risk':
                name = 'LP'
            if cond1 == 'norisk':
                name = 'HP'
            cond1_name = name + '_' + parameter3
            cond2_name = name + '_' + parameter3
        if parameter3 == None:
            if cond1 == 'risk':
                cond1_name = 'LP'
                cond2_name = 'LP'
            if cond1 == 'norisk':
                cond1_name = 'HP'
                cond2_name = 'HP'

    print('cond1_name', cond1_name)
    print('cond2_name', cond2_name)
    #for indx in range(102):
    #average time course for   3 channels decision making , ch1 = 15, ch2 = 68, ch3 = 69
    #posterror ch1 = 8, ch2 = 16, ch3 = 19
    #feedback 26 60 69
    #set your channels
    #decision
    chs = [76, 77, 88, 78, 71]
    #late fb Anterior
    #chs = [5, 9, 10, 19, 20]
    print('p val shape', p_val.shape)
    p_val_aver = np.mean(p_val[chs, :], axis = 0)
    comp1_mean_aver = np.mean(comp1_mean[chs, :], axis = 0)
    comp2_mean_aver = np.mean(comp2_mean[chs, :], axis = 0)
    comp3_mean_aver = np.mean(comp3_mean[chs, :], axis = 0)
    rej,p_fdr = mne.stats.fdr_correction(p_val_aver, alpha=0.05, method='indep')
    comp1_stderr = scipy.stats.sem(comp1_mean_aver, axis=0)
    comp2_stderr = scipy.stats.sem(comp2_mean_aver, axis=0)
    #rint(comp1_stderr)

    contrast = True
    if response:
        if group:
            if Normals_Autists:
                title = f'Betw-group{cond1_name}ATvs{cond2_name}NT'
        if group == False:
            if Normals:
                title = f'{cond1_name}vs{cond2_name}NT'
            if Autists:
                title = f'{cond1_name}vs{cond2_name}AT'
    else:
        title = f'{cond1_name} vs {cond2_name}STI'
    print(title)
    print('cond2_name', cond2_name)
    plot_stat_comparison(response, contrast, path_pic, comp1_mean_aver, comp2_mean_aver, comp1_stderr, comp2_stderr, comp3_mean_aver, -6.0, 6.0,    p_val_aver, p_fdr, parameter3, cond1_name, time, title = title, folder = "%s_vs_%s" % (cond1_name, cond2_name), comp1_label = cond1_name, comp2_label = cond2_name, comp3_label = 'difference')
    print('\tAll printed')
