import mne, os
import os.path as op
import numpy as np
import pathlib
from os.path import exists
from find_fix_cross import read_events
from config import *

def clean_events(epochs_ar, thres):
    '''
    conditions for clean
    '''
    #N_events, N_chans, N_times
    epochs_ar = epochs_ar.swapaxes(0, 1).swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    
    EV_DATA = np.abs(epochs_ar)
    
    CHAN_MAX = np.max(EV_DATA, axis=1)
    RESH_DATA = EV_DATA.reshape(N_chans,  N_events* N_times) 
    
    CHAN_MEAN = np.mean(RESH_DATA, axis=1)
    CHAN_STD = np.std(RESH_DATA, axis=1)
    
    good_events = []
    for i in range(N_events):
        select = np.where(CHAN_MAX[:, i] > CHAN_MEAN + thres*CHAN_STD)
        if select[0].shape[0] <= N_chans//4:
            good_events.append(i)

    return np.array(good_events)

def call_clean_events(data_path, data_path_raw, raw_name, subj, r, cond, fb):
    '''
    extract cleaned events (txt) and save raw events by extracted index
    '''
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True).filter(l_freq=70, h_freq=None)
    #raw_data = mne.io.Raw(conf.fpath_raw.format(subj, run, subj), preload=True, verbose='ERROR').filter(l_freq=70, h_freq=None)
    #for po63-p067 and autists 
    events_raw = np.loadtxt(op.join(data_path_raw, raw_name.format(subj, r)), dtype = 'int')
    #For p00-p062
    #events_raw = read_events(op.join(data_path_raw, raw_name.format(subj, r)))
    if Autists:
        if exists('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_autists{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb)):
            events = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_autists{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb), dtype='int')
        else:
            pass
    if Normals:
        if exists('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_normals{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb)):
            events = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_normals{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb), dtype='int')
    # (3,) -> (1,3)
    if events.shape == (3,):
        events = events[np.newaxis, :]
    print('events before',events)
    print(events.shape)
    # список индексов трайлов
    cleaned = []
    for i in range(len(events_raw)):
        for j in range(len(events)):
            if np.all((events_raw[i] - events[j] == 0)):
                cleaned.append(events[j])  
    cleaned = np.array(cleaned)

    if cleaned.any():
        print('events after', cleaned)
        if Autists:
            mio_corrected_events_file = open('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb), "w")
        if Normals:
            mio_corrected_events_file = open('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_mio_list_compare{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb), "w")
        np.savetxt(mio_corrected_events_file, cleaned, fmt="%d")
        mio_corrected_events_file.close()

prefix = '_not_trained'

rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
##trial_type = ['norisk']

feedback = ['positive', 'negative']
period_start = -1.750
period_end = 2.750
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
assert(not Normals_Autists)
if Autists:
    data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/'
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare{0}/'.format(prefix), exist_ok = True)
if Normals:
    subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/mio_free_events/'
    #data_path_raw = '/net/server/data/home/inside/Events_probability/Events_clean'
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_mio_list_compare{0}/'.format(prefix), exist_ok = True)

#for po063-p0567 and autists
raw_name = '{0}/{0}_run{1}_mio_free.txt'
#raw_name = '{0}_run{1}_events_clean.txt'

'''
extract cleaned events
'''
print('\trun mio_extraction...')

print(subjects)

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                if Autists:
                    rf = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_autists{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb)
                if Normals:
                    rf = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_normals{0}/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix, subj, r, cond, fb)
                if pathlib.Path(rf).exists() and os.stat(rf).st_size != 0:
                    call_clean_events(data_path, data_path_raw, raw_name, subj, r, cond, fb)
                else:
                    print('This file: ', rf, 'does not exit')

print('\tmio_extraction completed')
