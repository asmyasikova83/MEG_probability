import mne
import os
import os.path as op
import numpy as np
#import pandas as pd
from config import *
from mne.io import read_raw_edf

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
freq_range = 'beta_16_30_trf_early_log'

#создаем папку, куда будут сохраняться полученные комбайны
#os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj'.format(freq_range), exist_ok = True)

prefix = ''

if Autists:
    line = 'autists'
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended/beta_16_30_trf_early_log_example_beta_normals/beta_16_30_trf_early_log_epo/'
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists'
    #subjects = ['P341']
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists_extended'
if Normals:
    line = 'normals'
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended/beta_16_30_trf_early_log_example_beta_normals/beta_16_30_trf_early_log_epo/'
    #subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended'


raw_fnames = os.listdir(path)

raw_fnames_negative = []
raw_fnames_positive = []
for f in raw_fnames:
    if f.split('_')[5] == 'negative':
        raw_fnames_negative.append(f)
    if f.split('_')[5] == 'positive':
        raw_fnames_positive.append(f)
os.chdir(path)

#subjects = ['P067']
#trial_type = ['norisk']

for s in subjects:
    for t in trial_type:
        epochs_neg  = list()
        epochs_pos  = list()
        for r in rounds:
            try:
                fname_neg = path + f'{s}_run{r}_{t}_fb_cur_negative_{freq_range}_epo.fif'
                epo_neg = mne.read_epochs(fname_neg)
                epochs_neg.append(epo_neg)
            except (OSError):
                print('This file not exist')
        if len(epochs_neg) != 0:
            concat_epochs_negative = mne.concatenate_epochs(epochs_neg, on_mismatch='ignore')
            concat_epochs_negative.save(f'{prefix_data}/{freq_range}_example_beta_{line}/{s}_{t}_negatives.fif', overwrite=True)
        for r in rounds:
            try:
                fname_pos = path + f'{s}_run{r}_{t}_fb_cur_positive_{freq_range}_epo.fif'
                epo_pos = mne.read_epochs(fname_pos)
                epochs_pos.append(epo_pos)
            except (OSError):
                print('This file not exist')
        if len(epochs_pos) != 0:
            concat_epochs_positive = mne.concatenate_epochs(epochs_pos, on_mismatch='ignore')
            concat_epochs_positive.save(f'{prefix_data}/{freq_range}_example_beta_{line}/{s}_{t}_positives.fif', overwrite=True)


