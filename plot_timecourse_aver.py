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
from function import space_fdr, full_fdr, p_val_binary, compute_p_val, plot_stat_comparison, to_str_ar, clear_html, add_str_html,  add_pic_time_course_html
from config import *

options = {
    'page-size':'A2',
    'orientation':'Portrait',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}

freq_range = 'beta_16_30_trf_no_log_division'
#freq_range = = 'beta_16_30_trf_early_log'

print('cond1', cond1)
print('cond2', cond2)
# загружаем комбайн планары, усредненные внутри каждого испытуемого
#data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/{1}_ave_comb_planar'.format(feedb, fr)
if parameter3  == None:
    #TODO
    if response:
        #response-locked data
        print('Response is true')
        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
        # if pretrial
        #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_comb_planar/'
        #TODO FOR stim and resp
    else:
        print('Response is false')
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/stim/{0}/{0}_ave_comb_planar/'.format(freq_range)
if parameter3  == 'negative':
    data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta/beta_16_30_fb_ave_comb_planar'
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
#out_path='/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/{1}_epo/'.format(feedb, fr) #path to epochs
#out_path = f'/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_epo/'#TODO
out_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/stim/{0}/{0}_second_bl_epo'.format(freq_range)
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


# задаем время и донора
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

time = temp.times# количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

########################### norisk vs risk ##############################


#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/net/server/data/Archive/prob_learn/asmyasnikova83/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'/net/server/data/Archive/prob_learn/asmyasnikova83/channel_labels.mat')['chanlabels'])
os.makedirs(path + 'output/', exist_ok=True)

for p in planars:
    #extract data and ttest
    print(data_path)
    comp1_mean, comp2_mean, p_val = compute_p_val(response, data_path, subjects, cond1, cond2, parameter3, parameter4, fr, time)
    #scaling
    if comp1_mean.max()>comp2_mean.max():
        p_mul_max=comp1_mean.max()+ abs(comp1_mean.max()/10)
    else:
        p_mul_max=comp2_mean.max()+ abs(comp2_mean.max()/10)

    if comp1_mean.min()<comp2_mean.min():
        p_mul_min=comp1_mean.min() - abs(comp1_mean.min()/10)
    else:
        p_mul_min=comp2_mean.min() - abs(comp2_mean.min()/10)

    if parameter3 == 'negative':
        name = cond1
        cond1 = name + '_negative'
        cond2 = name + '_positive'
    if cond1 == 'prerisk':
        cond1_name = 'pre-LP'
    if cond1 == 'risk':
        cond1_name = 'LP'
    if cond1 == 'postrisk':
        cond1_name = 'post-LP'
    cond2_name = 'HP'
    #comp2_label = cond2
    #cond1_name = cond1
    #cond2_name = cond2
    #print('comp1_label', comp1_label)
    #print('comp2_label', comp2_label)
    print('cond1_name', cond1_name)
    print('cond2_name', cond2_name)
    #for indx in range(102):
    #average time course for   3 channels decision making , ch1 = 15, ch2 = 68, ch3 = 69
    #posterror ch1 = 8, ch2 = 16, ch3 = 19
    #feedback 26 60 69
    #set your channels
    ch1 = 26
    ch2 = 60
    ch3 = 69
    p_val_aver = (p_val[ch1,:] + p_val[ch2,:] + p_val[ch3,:])/3
    print(p_val_aver.shape)
    print(p_val_aver)
    comp1_mean_aver = (comp1_mean[ch1,:] + comp1_mean[ch2,:] + comp1_mean[ch3,:])/3
    comp2_mean_aver = (comp2_mean[ch1,:] + comp2_mean[ch2,:] + comp2_mean[ch3,:])/3
    rej,p_fdr = mne.stats.fdr_correction(p_val_aver, alpha=0.05, method='indep')
    if response:
        title = f'{cond1_name} vs {cond2_name}RES'
    else:
        title = f'{cond1_name} vs {cond2_name}STI'
    plot_stat_comparison(path, feedb, fr, comp1_mean_aver, comp2_mean_aver, -7.5, 5.0, p_val_aver, p_fdr, parameter3, time, title = title,
                             folder = "%s_vs_%s" % (cond1_name, cond2_name), comp1_label = cond1_name, comp2_label = cond2_name)
    print('\tAll printed')
