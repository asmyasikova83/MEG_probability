#Ttest for sources
# Based on Script of Nikita Tyulenev: source_plot_get_full_stc.py
# Look Ttest_for_sources.ipynb for explanations

import os
import mne
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats import multitest as mul
from functions import signed_p_val


# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'
subjects = ['P304', 'P307', 'P312', 'P313', 'P314',
            'P316', 'P322',  'P323', 'P324', 'P325',
            'P326',  'P328','P329', 'P331',  'P334',
            'P336']
subjects.remove('P328')
vect_signed_p_val = np.vectorize(signed_p_val)

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['risk']
feedback = ['positive', 'negative']

#freq_range = 'beta_16_30'


inter = [-0.800, 2.400] # time interval


# download donor stc
#stc_test = mne.read_source_estimate('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/beta_16_30_stc_fsaverage_ave_into_subj/P001_risk_fb_cur_negative', 'fsaverage').crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
stc_test = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/P001_norisk_fb_cur_negative_sLoreta-lh.stc').crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
# make folder for output files
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/ttest_between_choice_type' , exist_ok = True)

#################### Ttest between feedback inside the condition ###############################

n =  stc_test.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn =  stc_test.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).

#omp1_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
#omp2_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))

fb = True

if fb:
    data_dir = '/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/beta_16_30_stc_fsaverage_ave_into_subj'
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/ttest_pos_vs_neg' , exist_ok = True)
    for t in trial_type:
        data_fb_0 = np.empty((0, sn, n))
        data_fb_1 = np.empty((0, sn, n))
        for ind, subj in enumerate(subjects):
            try:
                #print(ind + 1, subj)'
                print(os.path.join(data_dir, "{0}_{1}_fb_cur_{2}-lh.stc".format(subj, t, feedback[0])))
                stc = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}_fb_cur_{2}-lh.stc".format(subj, t, feedback[0]))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
                stc = stc.data.reshape(1, sn, n) # добавляем ось испытуемого (subj)

                data_fb_0 = np.vstack([data_fb_0, stc])  # собираем всех испытуемых в один массив 
                print(data_fb_0.shape)

            except(OSError):
                print('This file not exist')

            try:
                print(os.path.join(data_dir, "{0}_{1}_fb_cur_{2}-lh.stc".format(subj, t, feedback[1])))
                stc = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}_fb_cur_{2}-lh.stc".format(subj, t, feedback[1]))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
                stc = stc.data.reshape(1, sn, n) # добавляем ось испытуемого (subj)
                data_fb_1 = np.vstack([data_fb_1, stc])  # собираем всех испытуемых в один массив 
                print(data_fb_1.shape)
            except(OSError):
                print('This file not exist')

    #average over subjects
    print('feedback[0]', feedback[0])
    print('feedback[1]', feedback[1])
    print(data_fb_0.shape)
    print(data_fb_1.shape)

    data_fb_0 = np.mean(data_fb_0, axis = 0)
    print(data_fb_0.shape)
    data_fb_1 = np.mean(data_fb_1, axis = 0)
    print(data_fb_1.shape)
    mean_data = data_fb_1 - data_fb_0
    print(mean_data)
    stc_test.data = mean_data
    #stc_test.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/ttest_between_choice_type/norisk_vs_{0}_mean_beta'.format(t))
    stc_test.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/ttest_pos_vs_neg/{0}_fb_cur_pos_vs_neg_mean_beta'.format(t))


################## Ttest between the conditions ###############################    
if not fb:
    trial_type = ['prerisk', 'risk', 'postrisk']

    # change data dir
    data_dir = '/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/beta_16_30_fsaverage_ave_into_subj_united_fb'
    # make folder for output files
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/ttest_between_choice_type' , exist_ok = True)

    
    for t in trial_type:
        print(t)
        data_0 = np.empty((0, sn, n))
        data_1 = np.empty((0, sn, n))
        #comp1_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
        #comp2_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
        for ind, subj in enumerate(subjects):
            try:
                #print(ind + 1, subj)
                stc = mne.read_source_estimate(os.path.join(data_dir, "{0}_norisk-lh.stc".format(subj))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
                stc = stc.data.reshape(1, sn, n) # добавляем ось испытуемого (subj)
                data_0 = np.vstack([data_0, stc])  # собираем всех испытуемых в один массив 

            except(OSError):
                print('This file not exist')

            try:
                stc = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}-lh.stc".format(subj, t))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
                stc = stc.data.reshape(1, sn, n) # добавляем ось испытуемого (subj)

                data_1 = np.vstack([data_1, stc])  # собираем всех испытуемых в один массив 

            except(OSError):
                print('This file not exist')

        print(data_0.shape)
        print(data_1.shape)

        data_0 = np.mean(data_0, axis = 0)
        print(data_0.shape)
        print(t)
        data_1 = np.mean(data_1, axis = 0)
        print(data_1.shape)
        mean_data = data_1 - data_0
        print(mean_data)
        stc_test.data = mean_data
        print('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/ttest_between_choice_type/norisk_vs_{0}_mean_beta'.format(t))
        stc_test.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30_sLoreta/ttest_between_choice_type/norisk_vs_{0}_mean_beta'.format(t))
    '''
    t_stat, p_val = stats.ttest_rel(comp2_per_sub, comp1_per_sub, axis=0)
    
    print(p_val.min(), p_val.mean(), p_val.max())
    print(t_stat.min(), t_stat.mean(), t_stat.max())
    
    # full FDR
    
    width, height = p_val.shape
    p_val_resh = p_val.reshape(width * height)
    _, p_val = mul.fdrcorrection(p_val_resh)
    p_val = p_val.reshape((width, height))
    
    
    p_val = vect_signed_p_val(t_stat, p_val)
    
    # save the p value plotting on the brain (fsaverage)
    
    stc_test.data = p_val
    stc_test.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/ttest_pos_vs_neg/{0}_fb_cur_pos_vs_neg_pval_full_fdr'.format(t))
    
    # save the beta difference plotting on the brain (fsaverage)
    
    
    mean_data = (comp2_per_sub - comp1_per_sub).mean(axis=0) # усредняем между испытуемыми
    stc_test.data = mean_data
    stc_test.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/ttest_pos_vs_neg/{0}_fb_cur_pos_vs_neg_mean_beta'.format(t))
    

################## Ttest between the conditions ###############################    

trial_type = ['prerisk', 'risk', 'postrisk']

# change data dir
data_dir = '/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/beta_16_30_stc_fsaverage_ave_into_subj_united_fb'
# make folder for output files
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/ttest_between_choice_type' , exist_ok = True)

    
for t in trial_type:
    comp1_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
    comp2_per_sub = np.zeros(shape=(len(subjects), stc_test.data.shape[0], stc_test.data.shape[1]))
    for ind, subj in enumerate(subjects):
        #print(ind + 1, subj)
        temp1 = mne.read_source_estimate(os.path.join(data_dir, "{0}_norisk-lh.stc".format(subj))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
        #temp1.resample(40)
        comp1_per_sub[ind, :, :] = temp1.data
        temp2 = mne.read_source_estimate(os.path.join(data_dir, "{0}_{1}-lh.stc".format(subj, t))).crop(tmin=inter[0], tmax=inter[1], include_tmax=True)
        #temp2.resample(40)
        comp2_per_sub[ind, :, :] = temp2.data
        
    print(comp1_per_sub.shape)
    print(comp2_per_sub.shape)

    t_stat, p_val = stats.ttest_rel(comp2_per_sub, comp1_per_sub, axis=0)
    
    print(p_val.min(), p_val.mean(), p_val.max())
    print(t_stat.min(), t_stat.mean(), t_stat.max())
    
    # full FDR
    
    width, height = p_val.shape
    p_val_resh = p_val.reshape(width * height)
    _, p_val = mul.fdrcorrection(p_val_resh)
    p_val = p_val.reshape((width, height))
    
    
    p_val = vect_signed_p_val(t_stat, p_val)
    
    # save the p value plotting on the brain (fsaverage)
    
    stc_test.data = p_val
    stc_test.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/ttest_between_choice_type/norisk_vs_{0}_pval_full_fdr'.format(t))
    
    # save the beta difference plotting on the brain (fsaverage)
    '''
