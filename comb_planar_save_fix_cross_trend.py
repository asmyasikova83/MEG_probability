import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from function import combine_planar_Epoches_TFR


# parametrs

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']
feedback = ['positive', 'negative']

tmin = -0.350

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_12_20_FIX_CROSS/beta_12_20_epo_comb_planar', exist_ok = True)
for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    epochs = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_12_20_FIX_CROSS/beta_12_20_epo_FIX_CROSS/{0}_run{1}_{2}_fb_cur_{3}_beta_12_20-epo.fif'.format(subj, r, t, fb), preload = True)
                    combined_planar = combine_planar_Epoches_TFR(epochs, tmin)
                    combined_planar.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_12_20_FIX_CROSS/beta_12_20_epo_comb_planar/{0}_run{1}_{2}_fb_cur_{3}_beta_12_20-epo_comb_planar.fif'.format(subj, r, t, fb), overwrite=True)
                    
                except (OSError, FileNotFoundError):
                    print('This file not exist')
                
                
                
