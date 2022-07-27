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
from function import resample_before_stat, space_fdr, full_fdr, p_val_binary, compute_p_val, plot_stat_comparison, to_str_ar, clear_html, add_str_html,  add_pic_time_course_html
from config import *

options = {
    'page-size':'A2',
    'orientation':'Portrait',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}

if response:
    freq_range = 'beta_16_30_trf_early_log'
else:
    freq_range = 'beta_16_30_trf_no_log_division_stim'
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
        data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/'
        # if pretrial
        #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_comb_planar/'
        #TODO FOR stim and resp
    else:
        #stimulus-locked data
        print('Response is false')
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/stim_check/{0}/{0}_ave_comb_planar/'.format(freq_range)
if parameter3  == 'negative':
    if response:
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/beta_16_30_trf_early_log_ave_into_subjects_comb_planar/'
    else:
        print('Response is false')
        data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/stim_check/{0}_feedback/{0}_ave_comb_planar/'.format(freq_range)
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
#out_path='/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/{1}_epo/'.format(feedb, fr) #path to epochs
#out_path = f'/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_epo/'#TODO
#out_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/{0}/{0}_second_bl_epo'.format(freq_range)
#f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


# задаем время и донора
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

time = temp.times# количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

#n, comp2_mean, comp3_mean, p_val = compute_p_val(response, data_path, subjects, cond1, cond2, parameter3, parameter4, fr, time, t, idx_array_extended)########################## norisk vs risk ##############################


#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/net/server/data/Archive/prob_learn/asmyasnikova83/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'/net/server/data/Archive/prob_learn/asmyasnikova83/channel_labels.mat')['chanlabels'])
os.makedirs(path + 'output/', exist_ok=True)


#set time boundaries and step if there is no dono
#resample
print(donor)
if donor:
    time = temp.times
    t = len(time)
    t_min = time[0]
    t_max = time[-1]
    #Fit to donor
    time, idx_array_extended = resample_before_stat(t_min, t_max)
else:
    time, idx_array_extended = resample_before_stat(t_min, t_max)
for p in planars:
    #extract data and ttest
    print(data_path)
    comp1_mean, comp2_mean, comp3_mean, p_val = compute_p_val(response, data_path, subjects, cond1, cond2, parameter3, parameter4, freq_range, time, t, idx_array_extended)
    #scaling
    if comp1_mean.max()>comp2_mean.max():
        p_mul_max=comp1_mean.max()+ abs(comp1_mean.max()/10)
    else:
        p_mul_max=comp2_mean.max()+ abs(comp2_mean.max()/10)

    if comp1_mean.min()<comp2_mean.min():
        p_mul_min=comp1_mean.min() - abs(comp1_mean.min()/10)
    else:
        p_mul_min=comp2_mean.min() - abs(comp2_mean.min()/10)
    print('cond1_name', cond1_name)
    print('cond2_name', cond2_name)
    #average time course for   3 channels decision making , ch1 = 15, ch2 = 68, ch3 = 69
    #posterror ch1 = 8, ch2 = 16, ch3 = 19
    #feedback 26 60 69
    #set your times
    le = len(idx_array_extended)
    p_val_aver = np.zeros(le)
    comp1_mean_aver = np.zeros(le)
    comp2_mean_aver = np.zeros(le)
    comp3_mean_aver = np.zeros(le)
    counter = 0
    #significant channels in the intersect of decision and fb whole
    #cluster = [5, 6, 9, 10, 12, 13, 15, 22, 26, 37, 59, 60, 64, 66, 69, 70, 71, 74, 75, 76, 77, 78, 84, 86]
    #significant sensors in anticipation of feedback
    #cluster = [8, 9, 11, 16, 17, 18, 19]
    #3 most significant in anticipation
    #cluster = [8, 16, 19]
    #plot_timecourse_aver_all_ch.py5 best sensors in the intersect of decision and fb whole
    #cluster = [15, 66, 75, 76]
    #pos-response (100-500 ms) cluster
    #cluster = [70, 71, 73, 74, 75, 77, 86, 89]
    #for contrasts w tukey
    #Decision [68, 75, 76]
    #orisk prerisk
    #nticipation of feedback [8, 16, 19]
    #in risk neg pos tukey
    #cluster = [59, 66, 69]
    # best anterior TODO REMOVE 5 DONE
    cluster = [10, 12, 20]
    #3 best poster
    #cluster = [60, 69, 76]
    #3 best early feedback
    #cluster = [76, 77, 70]
    #average p_vals and timecourses over all 102 channels 
    for i in range(0, len(cluster)):
        j = cluster[i]
        p_val_aver = p_val_aver + p_val[j,:]
        comp1_mean_aver = comp1_mean_aver + comp1_mean[j,:]
        comp2_mean_aver = comp2_mean_aver + comp2_mean[j,:]
        comp3_mean_aver = comp3_mean_aver + comp3_mean[j,:]
        counter = counter + 1
    p_val_aver_fin = p_val_aver/counter
    comp1_mean_aver_fin = comp1_mean_aver/counter
    comp2_mean_aver_fin = comp2_mean_aver/counter
    comp3_mean_aver_fin = comp3_mean_aver/counter
    rej,p_fdr = mne.stats.fdr_correction(p_val_aver_fin, alpha=0.05, method='indep')
    if response:
        title = f'{cond1_name} vs {cond2_name}RELfb'
    else:
        title = f'{cond1_name} vs {cond2_name}STLfb'
    print('title', title)
    p_mul_min = -5.5
    p_mul_max = 5.5
    #to plot difference
    aver = True
    plot_stat_comparison(response, aver, path, comp1_mean_aver_fin, comp2_mean_aver_fin,  comp3_mean_aver_fin, p_mul_min, p_mul_max, p_val_aver_fin, p_fdr, parameter3, time, title = title,
                                                 folder = "%s_vs_%s" % (cond1_name, cond2_name), comp1_label = cond1_name, comp2_label = cond2_name, comp3_label = 'difference')
    print('\tAll printed')
