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
if Autists:
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists_extended'
if Normals:
    subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended'
os.makedirs('/{0}/{1}_classical_bline/{1}_epo_comb_planar'.format(prefix_data, freq_range), exist_ok = True)
########################## файл, со входными параметрами ############################################
print(subjects)
lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin)]


with open("/{0}/{0}_epo_classical_bline_comb_planar/config.txt".format(prefix_data, freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################



for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    epochs = mne.read_epochs('/{0}/{1}_classical_bline/{1}_epo/{2}_run{3}_{4}_fb_cur_{5}_{1}_epo.fif'.format(prefix_data, freq_range, subj, r, t, fb), preload = True)
                    combined_planar = combine_planar_Epoches_TFR(epochs, tmin)
                    combined_planar.save('{0}/{1}_classical_bline/{1}_epo_comb_planar/{2}_run{3}_{4}_fb_cur_{5}_{1}-epo_comb_planar.fif'.format(prefix_data, freq_range, subj, r, t, fb), overwrite=True)
                except (OSError, FileNotFoundError):
                    print('This file not exist')

