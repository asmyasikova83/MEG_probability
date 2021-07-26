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

#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['norisk', 'risk']

file_dir = ['theta_4_8_epo_FIX_CROSS',
            'theta_4_8_epo_RESPONSE',
            'theta_4_8_epo_FIX_CROSS_BASELINE',
            'theta_4_8_epo_RESPONSE_BASELINE']

for  fi in  file_dir:
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/{fi}/ave/', exist_ok = True)
# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")
#temp.tmax = -50
#n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.

# time points for fix cross
n = 91

for f in file_dir:
    for subj in subjects:
        for t in trial_type:
            ################################ DATA ################################
            data_container = np.empty((0, 306, n))
            for r in rounds:
                try:
                               
                    epochs = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/{0}/{1}_run{2}_{3}_fb_cur_{4}-epo.fif'.format(f, subj, r, t, fr), preload = True)
                    data_in_rounds = np.vstack([data_container, epochs.get_data()])
               
                
                except (OSError):
                
                    print('This file not exist')

            ###### Шаг 1. Усреднили внутри испытуемого (между блоками 1 -6) #################
            if data_in_rounds.size != 0:
                data_in_rounds_mean = data_in_rounds.mean(axis = 0) 
                print('data_in_rounds.size', data_in_rounds.size)
            else:
                data_in_rounds_mean = np.empty((0, 306, n))
        
            if data_in_rounds_mean.size != 0:
                print('data_in_rounds_mean.size', data_in_rounds_mean.size)
                fix_cross_evoked = mne.Evoked(data_in_rounds_mean, info = temp.info, tmin = -0.350)
                # сохраняем данные, усредненные внутри испытуемого. Шаг усредения 3, это усреднение между испытуемыми делается при рисовании топомапов
                fix_cross_evoked.save('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/{0}/ave/{1}_{2}_evoked_{3}_resp.fif'.format(f, subj, t, fr))
            else:
                print('Data for averaginh not found')
                pass


