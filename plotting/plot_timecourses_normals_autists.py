import mne
import os.path as op
import os
from scipy import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import ttest_pair_independent, resample_before_stat, space_fdr, full_fdr, p_val_binary, compute_p_val, plot_stat_comparison, to_str_ar, clear_html, add_str_html,  add_pic_time_course_html
from config import *

options = {
    'page-size':'A2',
    'orientation':'Portrait',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}

freq_range = 'beta_16_30_trf_early_log'
# загружаем комбайн планары, усредненные внутри каждого испытуемого
if parameter3  == None:
    if response:
        if Normals:
            #data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_ave_into_subj_comb_planar/'.format(freq_range)
        if Autists:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/'.format(freq_range)
        # if pretrial
        #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_comb_planar/'
    else:
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
if parameter3  == 'negative':
    if response:
        if Normals:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/beta_16_30_fb_ave_comb_planar/'
        if Autists:
            data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range)
    else:
        #stim-locked
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim_feedback/beta_16_30_trf_no_log_division_stim_ave_comb_planar/'
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
'''
if Normals:
    #out_path = f'/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_epo/'#TODO
    #out_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/beta_16_30_trf_no_log_division_stim/beta_16_30_trf_no_log_division_stim_second_bl_epo/'.format(freq_range)
if Autists:
    out_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_16_30_trf_early_log/beta_16_30_trf_early_log_epo/'.format(freq_range)
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке
'''

# задаем время и донора
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

if donor:
    #assign the time of donor
    time = temp.times
    t = len(time)
else:
    #assign a shorter time interval to remove artifacts from the edges
    #t = 1051
    time, idx_array_extended = resample_before_stat(t_min, t_max)
########################### norisk vs risk ##############################


#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/net/server/data/Archive/prob_learn/asmyasnikova83/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'/net/server/data/Archive/prob_learn/asmyasnikova83/channel_labels.mat')['chanlabels'])
os.makedirs(path + 'output/', exist_ok=True)

planars = ['comb_planar']
if Normals_Autists:
    fr1 =  'beta_16_30_trf_early_log'
    fr2 =  'beta_16_30_trf_early_log'
    data_path1 = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/'.format(freq_range)
    data_path2 = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/beta_16_30_ave_into_subjects_comb_planar/'

choice_type = ['norisk', 'risk', 'prerisk', 'postrisk']
for choice in choice_type:
    for p in planars:
        #extract data and ttest
        print(planars)
        print(data_path)
        #comp1_mean, comp2_mean, comp3_mean, p_val = compute_p_val(response, data_path, subjects, cond1, cond2, parameter3, parameter4, fr, time, t, idx_array_extended)
        t_stat, p_val, comp1_mean, comp2_mean = ttest_pair_independent(data_path1, data_path2, response, Autists, Normals, fr1, fr2, choice, parameter3, p, t)
        #scaling
        if comp1_mean.max()>comp2_mean.max():
            p_mul_max=comp1_mean.max()+ abs(comp1_mean.max()/10)
        else:
            p_mul_max=comp2_mean.max()+ abs(comp2_mean.max()/10)

        if comp1_mean.min()<comp2_mean.min():
            p_mul_min=comp1_mean.min() - abs(comp1_mean.min()/10)
        else:
            p_mul_min=comp2_mean.min() - abs(comp2_mean.min()/10)
        if choice == 'prerisk':
            cond1_name = 'pre-LP'
        if choice == 'risk':
            cond1_name = 'LP'
        if choice == 'postrisk':
            cond1_name = 'post-LP'
        if choice == 'norisk':
            cond1_name = 'HP'
        cond2_name = 'HP'
        comp3_mean = np.zeros(len(time))
        contrast = False
        for indx in range(102):
            rej,p_fdr = mne.stats.fdr_correction(p_val[indx,:], alpha=0.05, method='indep')
            plot_stat_comparison(response, contrast, path, comp1_mean[indx], comp2_mean[indx],  comp3_mean[indx], -5.0, 5.0, p_val[indx], p_fdr, parameter3, time, title = chan_labels[indx+204],
                             folder = "%s_vs_%s" % (cond1_name, cond2_name), comp1_label = cond1_name, comp2_label = cond2_name, comp3_label = 'difference')

        for ind, planar in enumerate(planars):
            #place the channel time courses in html file
            html_name = path + 'output/' + 'pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{cond1_name}', f'{cond2_name}', 'all')
            clear_html(html_name)
            add_str_html(html_name, '<!DOCTYPE html>')
            add_str_html(html_name, '<html>')
            add_str_html(html_name, '<body>')
            if response:
                add_str_html(html_name, '<p style="font-size:32px;"><b>AUTISTS vs NORMALS, AVERAGED AT RESPONSE %s, averaged %s, %d subjects, <span style="color:green;"> p_val < 0.05 </span> <span style="color:Magenta;">p_fdr < 0.05 </span> </b></p>' % (planar, fr, len(subjects)))
            else:
                add_str_html(html_name, '<p style="font-size:32px;"><b>AUTISTS AVERAGED AT STIMULUS %s, averaged %s, %d subjects <span style="color:green;"> p_val < 0.05 </span> <span style="color:Magenta;">p_fdr < 0.05 </span> </b></p>' % (planar, fr, len(subjects)))

            if parameter3 == None:
                add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: red;"> %s </span> vs <span style="color: blue;"> %s </span> </b></p>' % (cond1_name, cond2_name))
            if parameter3 == 'negative':
                add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: red;"> %s </span> vs <span style="color: blue;"> %s </span> </b></p>' % (cond1_name, cond2_name))
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