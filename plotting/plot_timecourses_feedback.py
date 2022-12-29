import mne
import os.path as op
import os
from scipy import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import scipy
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import resample_before_stat, space_fdr, full_fdr, p_val_binary, compute_p_val, plot_stat_comparison, to_str_ar, clear_html, add_str_html,  add_pic_time_course_html
from config import *

options = {
    'page-size':'A2',
    'orientation':'Portrait',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}
prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
freq_range = 'beta_16_30_trf_early_log'
parameter3 = 'negative'
parameter4 = 'positive'

#parameter3 = None
#parameter4 = None

# загружаем комбайн планары, усредненные внутри каждого испытуемого
if parameter3  == None:
    if response:
        data_path = '{0}/Autists_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)
        #data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
        # if pretrial
        #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_comb_planar/'
    else:
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
if parameter3  == 'negative' or parameter3  == 'positive':
    if response:
        data_path = '{0}/Normals_extended/{1}_trained_classical_bline/{1}_ave_into_subjects_comb_planar/'.format(prefix, freq_range)
        #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/beta_16_30_fb_ave_comb_planar/'
    else:
        #stim-locked
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim_feedback/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
#out_path = f'/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_epo/'#TODO
#out_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_second_bl_epo/'.format(freq_range)
#out_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended/{0}_trained_classical_bline/beta_16_30_trf_early_log_epo/'.format(freq_range)
#f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


# задаем время и донора
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
donor = False
if donor:
    #assign the time of donor
    time = temp.times
    t = len(time)
else:
    #assign a shorter time interval to remove artifacts from the edges
    t = 1051
    time, idx_array_extended = resample_before_stat(t_min, t_max)
#print(time)
print(idx_array_extended.shape)
#print(idx_array_extended)
#print(len(idx_array_extended))
########################### norisk vs risk ##############################


#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/net/server/data/Archive/prob_learn/asmyasnikova83/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'/net/server/data/Archive/prob_learn/asmyasnikova83/channel_labels.mat')['chanlabels'])
os.makedirs(path + 'output/', exist_ok=True)


cond1 = 'risk'
cond2= 'risk'

cond1_name = cond1
cond2_name = cond2
if cond1 == 'norisk':
    #subjects = Autists
    subjects = Normals
if cond1 == 'risk':
    subjects = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
               'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
               'P048', 'P053', 'P055',         'P059', 'P060',
               'P063', 'P064', 'P065', 'P067']
    #subjects = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
    #           'P316',  'P320', 'P321',         'P323', 'P324',
    #           'P325',          'P327', 'P328', 'P329', 'P333',
    #                    'P335', 'P338', 'P341', 'P342']
#if cond1 == 'prerisk':
#    Autists = Autists_norisk
#    Normals = Normals_norisk
#if cond1 == 'postrisk':
#    Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
#               'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
#               'P048', 'P053', 'P055',         'P059', 'P060',
#               'P061', 'P063', 'P064', 'P065'        ]
#    subjects = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
#               'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
#               'P325',  'P326', 'P327',        'P329', 'P333',
#               'P334',  'P335', 'P338', 'P341'       ]
fr = 'beta_16_30_trf_early_log'
path = '{0}/Normals_extended/'.format(prefix, freq_range)

for p in planars:
    #extract data and ttest
    print(data_path)
    comp1_mean, comp2_mean, comp3_mean, comp1, comp2, p_val = compute_p_val(response, data_path, subjects, cond1, cond2, parameter3, parameter4, fr, time, t, idx_array_extended)
    #scaling
    if comp1_mean.max()>comp2_mean.max():
        p_mul_max=comp1_mean.max()+ abs(comp1_mean.max()/10)
    else:
        p_mul_max=comp2_mean.max()+ abs(comp2_mean.max()/10)

    if comp1_mean.min()<comp2_mean.min():
        p_mul_min=comp1_mean.min() - abs(comp1_mean.min()/10)
    else:
        p_mul_min=comp2_mean.min() - abs(comp2_mean.min()/10)
    print('comp1_label', comp1_label)
    print('comp2_label', comp2_label)
    print('cond1_name', cond1_name)
    print('cond2_name', cond2_name)
    aver = False
    print('comp1.shape', comp1.shape)
    print('comp1.shape', comp1.shape)
    comp1_stderr = np.zeros((comp1.shape[1], comp1.shape[2]))
    comp2_stderr = np.zeros((comp1.shape[1], comp2.shape[2]))
    print('comp1_stderr.shape', comp1_stderr.shape)
    for idx in range(102):
        comp1_stderr[idx,:] = scipy.stats.sem(comp1[:, idx, :], axis=0)
        comp2_stderr[idx,:] = scipy.stats.sem(comp2[:, idx, :], axis=0)
        rej,p_fdr = mne.stats.fdr_correction(p_val[idx,:], alpha=0.05, method='indep')

        plot_stat_comparison(response, aver, path, comp1_mean[idx], comp2_mean[idx],comp1_stderr[idx], comp2_stderr[idx], comp3_mean[idx], p_mul_min, p_mul_max, p_val[idx], p_fdr, parameter3, cond1_name, time, title = chan_labels[idx+204],
                            folder = "%s_vs_%s" % (cond1_name, cond2_name), comp1_label = cond1_name, comp2_label = cond2_name, comp3_label = 'difference')

    for ind, planar in enumerate(planars):
        #place the channel time courses in html file
        html_name = path + 'output/' + 'pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{cond1_name}', f'{cond2_name}', 'all')
        clear_html(html_name)
        add_str_html(html_name, '<!DOCTYPE html>')
        add_str_html(html_name, '<html>')
        add_str_html(html_name, '<body>')
        if response:
            add_str_html(html_name, '<p style="font-size:32px;"><b>NORMALS  %s AVERAGED AT RESPONSE %s, averaged %s, %d subjects, <span style="color:green;"> p_val < 0.05 </span> <span style="color:Magenta;">p_fdr < 0.05 </span> </b></p>' % (cond1, planar, fr, len(subjects)))
        else:
            add_str_html(html_name, '<p style="font-size:32px;"><b>AVERAGED AT STIMULUS %s, averaged %s, %d subjects <span style="color:green;"> p_val < 0.05 </span> <span style="color:Magenta;">p_fdr < 0.05 </span> </b></p>' % (planar, fr, len(subjects)))

        if parameter3 == None:
            add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: red;"> %s </span> vs <span style="color: blue;"> %s </span> </b></p>' % (cond1_name, cond2_name))
        if parameter3 == 'negative':
            add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: red;"> %s </span> vs <span style="color: blue;"> %s </span> </b></p>' % (parameter3, parameter4))
        #placing the channel time courses and save the html
        ind = 2
        if ind == 2:
            for ch_num in range(204, len(chan_labels)):
                pic = chan_labels[ch_num] + '.png'
                add_pic_time_course_html(html_name, pic, f'{cond1_name}_vs_{cond2_name}', pos[ch_num], [200,150])
        else:
            for ch_num in range(ind, 204, 2):
                pic = chan_labels[ch_num] + '.png'
                add_pic_time_course_html(html_name, pic, f'{cond1_name}_vs_{cond2_name}', pos[ch_num], [200,150])

        add_str_html(html_name, '</body>')
        add_str_html(html_name, '</html>')
        pdf_file = html_name.split("/")[1].split('.')[0]
        print(html_name)
        pdf_path = path + 'output/' + f'all_pdf/'
        os.makedirs(pdf_path, exist_ok = True)
    print('\tAll printed')
