############################################The spherical morphing of the surfaces accomplished by FreeSurfer can be employed to bring data from different subjects into a common anatomical frame################
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

subjects = ['P301', 'P304', 'P307', 'P309',  'P312', 'P313', 'P314',
            'P316', 'P322',  'P323', 'P324', 'P325',
            'P326',  'P328','P329', 'P331',  'P333', 'P334',
            'P336', 'P340']
subjects.remove('P328')

#subjects = ['P301', 'P304']

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

rounds = [1, 2, 3, 4, 5, 6]

freq_range = 'beta_16_30'

#создаем папку, куда будут сохраняться полученные файлы
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_fsaverage_epo_var2'.format(freq_range), exist_ok = True)

# for stc epochs

for subj in subjects:
    print(subj)
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_num = os.listdir('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}'.format(freq_range, subj, r, cond, fb))
                    print('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}'.format(freq_range, subj, r, cond, fb))
                    print(epochs_num)
                    print (int(len(epochs_num)/2))
                    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_fsaverage_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}_fsaverage'.format(freq_range, subj, r, cond, fb))
                
                    for ep in range(int(len(epochs_num)/2)):
                    
                        stc= mne.read_source_estimate("/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}/{5}".format(freq_range, subj, r, cond, fb, ep))                     
                        print(stc)
                        morph = mne.compute_source_morph(stc, subject_from=subj, subject_to='fsaverage')
                        stc_fsaverage = morph.apply(stc)
                        stc_fsaverage.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/{0}_sLoreta/{0}_stc_fsaverage_epo_var2/{1}_run{2}_{3}_fb_cur_{4}_{0}_fsaverage/{5}'.format(freq_range, subj, r, cond, fb, ep))
                except (OSError):
                    print('This file not exist')



                    


