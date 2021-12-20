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
#ubjects.remove('P000')
#ubjects.remove('P020')
#ubjects.remove('P036')
#ubjects.remove('P049')
#ubjects.remove('P056')

rounds = [1, 2, 3, 4, 5, 6]
#rounds = [2]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk','risk']

freq_range = 'beta_16_30_trf_early_log'

#создаем папку, куда будут сохраняться полученные комбайны
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_ave_into_subj'.format(freq_range), exist_ok = True)

timing  = 3001
for subj in subjects:
    for t in trial_type:
        ################################ Positive feedback ################################
        positive_fb = np.empty((0, 1, timing))
        for r in rounds:
            try:
                               
                epochs_positive = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_positive_{0}_epo.fif'.format(freq_range, subj, r, t), preload = True)             
                print(epochs_positive)
                positive_fb = np.vstack([positive_fb, epochs_positive.get_data()])
               
                
            except (OSError):
                
                print('This file not exist')

        ###### Шаг 1. Усреднили все положительные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if positive_fb.size != 0:
            positive_fb_mean = positive_fb.mean(axis = 0) 
            positive_fb_mean = positive_fb_mean.reshape(1, 1,timing) # добавляем ось для фидбека
            
        else:
            positive_fb_mean = np.empty((0, 1, timing))
            
            
        ########################## Negative feedback #############################
        negative_fb = np.empty((0, 1, timing))
        for r in rounds:
            try:
                               
                epochs_negative = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_negative_{0}_epo.fif'.format(freq_range, subj, r, t), preload = True)
                negative_fb = np.vstack([negative_fb, epochs_negative.get_data()])
             
                
            except (OSError):
                print('This file not exist')

        ###### Шаг 1. Усреднили все отрицательные фидбеки внутри испытуемого (между блоками 1 -6) #################
        if negative_fb.size != 0:
            negative_fb_mean = negative_fb.mean(axis = 0) 
            negative_fb_mean = negative_fb_mean.reshape(1, 1, timing) # добавляем ось для фидбека
        else:
            negative_fb_mean = np.empty((0, 1, timing))
        ####################### Шаг 2 усреднения. Усредняем данные внутри испытуемого #####################################
        if negative_fb_mean.size == 0 and positive_fb_mean.size != 0:
            data_into_subj = positive_fb_mean
                
        elif negative_fb_mean.size != 0 and positive_fb_mean.size == 0:
                
            data_into_subj = negative_fb_mean
                
        elif negative_fb_mean.size != 0 and positive_fb_mean.size != 0:
                                        
            data_into_subj = np.vstack([negative_fb_mean, positive_fb_mean])
            
        else:
            data_into_subj = np.empty((0, 1, timing))

        if data_into_subj.size != 0:
            data_mean = data_into_subj.mean(axis = 0)
            info = mne.create_info(ch_names=['EMG064'], sfreq=1000, ch_types='emg', verbose=None)
            evoked  = mne.EvokedArray(data_mean, info, tmin=-1.000, kind='average', baseline=None, verbose=None)
            print(evoked)        
            # сохраняем данные, усредненные внутри испытуемого. Шаг усредения 3, это усреднение между испытуемыми делается при рисовании топомапов
            evoked.save('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
            
        else:
            print('Subject has no feedbacks in this condition')
            pass


