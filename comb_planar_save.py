import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from function import combine_planar_Epoches_TFR
from config import *

# parametrs

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

tmin = -1.750

freq_range = 'beta_16_30_trf_early_log'

prefix = '_ignore_train'

if Autists:
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists_extended'
if Normals:
    subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended'
os.makedirs('/{0}/{1}{2}_classical_bline/{1}_epo_comb_planar'.format(prefix_data, freq_range, prefix), exist_ok = True)
########################## файл, со входными параметрами ############################################
print(subjects)
lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin)]


with open("/{0}/{1}{2}_classical_bline/{1}_epo_comb_planar/config.txt".format(prefix_data, freq_range, prefix), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################



for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    epochs = mne.read_epochs('/{0}/{1}{2}_classical_bline/{1}_epo/{3}_run{4}_{5}_fb_cur_{6}_{1}_epo.fif'.format(prefix_data, freq_range, prefix, subj, r, t, fb), preload = True)
                    combined_planar = combine_planar_Epoches_TFR(epochs, tmin)
                    combined_planar.save('{0}/{1}{2}_classical_bline/{1}_epo_comb_planar/{3}_run{4}_{5}_fb_cur_{6}_{1}-epo_comb_planar.fif'.format(prefix_data, freq_range, prefix, subj, r, t, fb), overwrite=True)
                except (OSError, FileNotFoundError):
                    print('This file not exist')

