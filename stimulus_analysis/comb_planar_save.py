import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from make_freq_stim import combine_planar_Epoches_TFR


# parametrs

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

tmin = -1.750

#freq_range = 'alpha_8_12_trf_early_log'
freq_range = 'beta_16_30_trf_no_log_division_stim'

prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83'

os.makedirs('/{0}/stim_check/{1}_feedback/{1}_epo_comb_planar'.format(prefix, freq_range), exist_ok = True)
########################## файл, со входными параметрами ############################################

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin)]


with open("/{0}/stim_check/{1}_feedback/{1}_epo_comb_planar/config.txt".format(prefix, freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################



for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    print('/{0}/stim_check/{1}_feedback/{1}_epo/{2}_run{3}_{4}_fb_cur_{5}_{1}_epo.fif'.format(prefix, freq_range, subj, r, t, fb))
                    epochs = mne.read_epochs('/{0}/stim_check/{1}_feedback/{1}_epo/{2}_run{3}_{4}_fb_cur_{5}_{1}_epo.fif'.format(prefix, freq_range, subj, r, t, fb), preload = True)
                    combined_planar = combine_planar_Epoches_TFR(epochs, tmin)
                    combined_planar.save('/{0}/stim_check/{1}_feedback/{1}_epo_comb_planar/{2}_run{3}_{4}_fb_cur_{5}_{1}-epo_comb_planar.fif'.format(prefix, freq_range, subj, r, t, fb), overwrite=True)
                    
                    
                except (OSError, FileNotFoundError):
                    print('This file not exist')

