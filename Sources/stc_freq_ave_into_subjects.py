import mne
import os
import os.path as op
import numpy as np
import pandas as pd

subjects = ['P301', 'P304', 'P307',  'P309',  'P312', 'P313', 'P314',
            'P316', 'P322',  'P323', 'P324', 'P325',
            'P326',  'P328','P329', 'P331',  'P333', 'P334',
            'P336', 'P340']
subjects.remove('P328')

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']

feedback = ['positive', 'negative']

freq_range = 'beta_16_30'

#создаем папку, куда будут сохраняться полученные файлы
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_fsaverage_ave_into_subj'.format(freq_range), exist_ok = True)


# донор
#temp = mne.read_source_estimate('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/beta_16_30/beta_16_30_stc_fsaverage_epo_var2/P336_run5_norisk_fb_cur_positive_beta_16_30_fsaverage')
temp = mne.read_source_estimate('/net/server/data/Archive/prob_learn/vtretyakova/P001_norisk_fb_cur_negative_sLoreta-lh.stc')
n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
sn = temp.data.shape[0] # sources number - количество источников (берем у донора, если донор из тех же данных).

for subj in subjects:
    for t in trial_type:
        for fb in feedback:
            data_fb = np.empty((0, sn, n))
            for r in rounds:
                
                
                try:
                    stc = mne.read_source_estimate('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_average_epo/{1}_run{2}_{3}_fb_cur_{4}'.format(freq_range, subj, r, t, fb), 'fsaverage').data
                    print(stc)
                    print(stc.data.shape)
                    stc = stc.reshape(1, sn, n) # добавляем ось блока (run)
                    
                except (OSError):
                    stc = np.empty((0, sn, n))
                    print('This file not exist')
                    
                data_fb = np.vstack([data_fb, stc])  # собираем все блоки в один массив 
                
            if data_fb.size != 0:
                temp.data = data_fb.mean(axis = 0)    # усредняем между блоками (run)
                temp.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_fsaverage_ave_into_subj/{1}_{2}_fb_cur_{3}'.format(freq_range, subj, t, fb))
            else:
                print('Subject has no feedbacks in this condition')
                pass
                    
