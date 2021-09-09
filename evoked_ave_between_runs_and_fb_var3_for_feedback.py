import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from config import *


print(fr)
print(feedb)

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
        
# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
subjects.remove('P000')
subjects.remove('P020')
subjects.remove('P036')
subjects.remove('P049')
subjects.remove('P056')

rounds = [1, 2, 3, 4, 5, 6]
#rounds = [3]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk']

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{1}_fb_ave_separ'.format(fr, fr), exist_ok = True)
# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.


for subj in subjects:
    for t in trial_type:
        ################################ Positive feedback ################################
        #positive_fb = np.empty((0, 306, n))
        positive_fb = np.empty((0,306, n))
        for r in rounds:
            try:
                               
                #epochs_positive = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/low_{0}_CORR/{1}_epo/{2}_run{3}_{4}_fb_cur_positive_{5}-epo.fif'.format(fr, fr, subj, r, t, fr), preload = True)             #print(epochs)  
                epochs_positive = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_epo/{0}_run{1}_{2}_fb_cur_positive_{3}_trf_no_log_division_epo.fif'.format(subj, r, t, fr), preload = True)
                positive_fb = np.vstack([positive_fb, epochs_positive.get_data()])
               
                
            except (OSError):
                
                print('This file not exist')

        ###### Шаг 1. Усреднили все положительные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if positive_fb.size != 0:
            positive_fb_mean = positive_fb.mean(axis = 0) 
            #positive_fb_mean = positive_fb_mean.reshape(1, 306, 1350) # добавляем ось для фидбека
        else:
            #positive_fb_mean = np.empty((0, 306, n))
            positive_fb_mean = np.empty((306, n))
            
            
        ########################## Negative feedback #############################
        #negative_fb = np.empty((0, 306, n))
        negative_fb = np.empty((0,306, n))
        for r in rounds:
            try:
                               
                #epochs_negative = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/low_{0}_CORR/{1}_epo/{2}_run{3}_{4}_fb_cur_negative_{5}-epo.fif'.format(fr, fr, subj, r, t, fr), preload = True)
                epochs_negative = mne.read_epochs('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_epo/{0}_run{1}_{2}_fb_cur_negative_{3}_trf_no_log_division_epo.fif'.format(subj, r, t, fr), preload = True)
                negative_fb = np.vstack([negative_fb, epochs_negative.get_data()])
             
                
            except (OSError):
                print('This file not exist')

        ###### Шаг 1. Усреднили все отрицательные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if negative_fb.size != 0:
            negative_fb_mean = negative_fb.mean(axis = 0) 
            #egative_fb_mean = negative_fb_mean.reshape(1, 306, 1350) # добавляем ось для фидбека
        else:
            #negative_fb_mean = np.empty((0, 306, n))
            negative_fb_mean = np.empty((306, n))
        ####################### Шаг 2 усреднения. Усредняем данные внутри испытуемого #####################################
        #data_into_subj = np.vstack([negative_fb_mean, positive_fb_mean])
        
        #if data_into_subj.size != 0:
            #temp.data = data_into_subj.mean(axis = 0) 
            # сохраняем данные, усредненные внутри испытуемого. Шаг усредения 3, это усреднение между испытуемыми делается при рисовании топомапов
            #temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/low_{0}_CORR/{1}_ave_into_subjects_fb_ave_separ/{2}_{3}_evoked_{4}_resp.fif'.format(fr, fr, subj, t, fr))
            
        if  negative_fb_mean.size != 0:
            temp.data  = negative_fb_mean
            # сохраняем данные, усредненные внутри испытуемого. Шаг усредения 3, это усреднение между испытуемыми делается при рисовании топомапов
            temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{1}_fb_ave_separ/{2}_{3}_evoked_{4}_negative_resp.fif'.format(fr, fr, subj, t, fr))
        else:
            print('Subject has no negative feedbacks in this condition')
            pass
        if  positive_fb_mean.size != 0:
            temp.data  = positive_fb_mean
            # сохраняем данные, усредненные внутри испытуемого. Шаг усредения 3, это усреднение между испытуемыми делается при рисовании топомапов
            temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{1}_fb_ave_separ/{2}_{3}_evoked_{4}_positive_resp.fif'.format(fr, fr, subj, t, fr))
        else:
            print('Subject has no positive feedbacks in this condition')
            pass


