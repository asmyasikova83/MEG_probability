import mne
import os
import os.path as op
import numpy as np
import pandas as pd


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
#rounds = [2]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk']
freq_range = '2_40_step_2_time_bandwidth_by_default_4_early_log'
# донор (donor creation see make_donor_for_tfr_plot.ipynb)
temp = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/donor_evoked.h5'.format(freq_range), condition=None)[0]

n = temp.data.shape[2] # количество временных точек (берем у донора, если донор из тех же данных).
fr = temp.data.shape[1]

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_ave_into_subj_fb_separ'.format(freq_range), exist_ok = True)
#os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/{0}/ave_into_subj_fb_negative'.format(freq_range), exist_ok = True)

for subj in subjects:
    for t in trial_type:
        ################################ Positive feedback ################################
        #set 1 for ch num if veog
        positive_fb = np.empty((0, 1, fr, n)) # эпохи х каналы х частоты (например: от 2 до 40 Гц, с шагом 2 Гц - 2, 4 ... 40, получается 20 частот) х временные точки
        for r in rounds:
            try:
                epochs_positive = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_epo/{1}_run{2}_{3}_fb_cur_positive_{0}-epo.h5'.format(freq_range, subj, r, t), condition=None)[0]  
                
                positive_fb = np.vstack([positive_fb, epochs_positive.data])
               
                
            except (OSError):
                
                print('This file not exist')

        ###### Шаг 1. Усреднили все положительные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if positive_fb.size != 0:
            positive_fb_mean = positive_fb.mean(axis = 0) # усредняем по оси количества эпох
            
            temp.data = positive_fb_mean
            temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_ave_into_subj_fb_separ/{1}_{2}_{0}_resp_fb_cur_positive.h5'.format(freq_range, subj, t), overwrite=True)

            
        else:
            print('Subject has no positive feedbacks on this condition')
            
            
            
        ########################## Negative feedback #############################
        negative_fb = np.empty((0, 1, fr, n))
        for r in rounds:
            try:
                
                epochs_negative = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_epo/{1}_run{2}_{3}_fb_cur_negative_{0}-epo.h5'.format(freq_range, subj, r, t), condition=None)[0]     
                           
                negative_fb = np.vstack([negative_fb, epochs_negative.data])
             
                
            except (OSError):
                print('This file not exist')

        ###### Шаг 1. Усреднили все отрицательные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if negative_fb.size != 0:
            negative_fb_mean = negative_fb.mean(axis = 0) # усредняем по оси количества эпох
            
            temp.data = negative_fb_mean
            temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_ave_into_subj_fb_separ/{1}_{2}_{0}_resp_fb_cur_negative.h5'.format(freq_range, subj, t), overwrite=True)
            

        else:
            print('Subject has no negative feedbacks on this condition')
        


