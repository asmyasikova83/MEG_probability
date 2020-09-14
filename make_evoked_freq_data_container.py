import mne, os, sys, numpy as np
from config import *
import pathlib


if mode == 'server':
    fpath_ev = '/home/asmyasnikova83/DATA/'
    fpath_fr= '/home/asmyasnikova83/DATA/TFR/'
    temp1 = mne.Evoked('/home/asmyasnikova83/DATA/P006_run6_evoked-ave.fif')
    out_path = '/home/asmyasnikova83/DATA/evoked_ave/'
else:
    fpath_ev =  '/home/sasha/MEG/MIO_cleaning/'
    fpath_fr = '/home/sasha/MEG/Time_frequency_analysis/'
    temp1 = mne.Evoked('/home/sasha/MEG/MIO_cleaning/P006_run6_evoked-ave.fif')
    out_path = '/home/sasha/MEG/Evoked/'

kind = 'negative'
#kind = 'negative'



if kind == 'negative':
    #explore negative feedback
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_negative/{}_run{}_mio_corrected_negative.txt'
        data_path = fpath_fr + 'negative/{0}_run{1}_theta_negative_int_50ms-tfr.h5'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_negative.txt'
        data_path = fpath_fr +  '{0}_run{1}_theta_negative_int_50ms-tfr.h5'
if kind == 'positive':
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_positive/{}_run{}_mio_corrected_positive.txt'
        data_path = fpath_fr + 'positive/{0}_run{1}_theta_positive_int_50ms-tfr.h5'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_positive.txt'
        data_path = fpath_fr +  '{0}_run{1}_theta_positive_int_50ms-tfr.h5'
#get rid of runs, leave frequency data for pos and neg feedback for time course plotting 
data = []
run_counter = 0
for subj in subjects:
    for run in runs:
        if run == '6':
            print('Dis is da last run!')
            print('run', run)
            rf = fpath_events.format(subj, run)
            file = pathlib.Path(rf)
            if file.exists():
                print('This file is being processed: ', rf)
                freq_file = data_path.format(subj, run)
                freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                data.append(freq_data.data)
                run_counter = run_counter + 1
            if run_counter > 0:
                new_evoked = temp1.copy()
                new_evoked.info = freq_data.info
                new_evoked.nave = 98  #all
                new_evoked.kind = "average"
                new_evoked.times = freq_data.times
                new_evoked.first = 0
                new_evoked.last = new_evoked.times.shape[0] - 1
                new_evoked.comment = freq_data.comment
                fq_data = np.asarray(data)
                print('fq_data shape', fq_data.shape)
                #mean across runs
                fq_data = fq_data.mean(axis=0).mean(axis=1)
                print('shape', fq_data.shape)
                new_evoked.data = fq_data
                out_file = out_path + "{0}_feedback_{1}_theta-ave.fif".format(subj, kind)
                print(out_file)
                new_evoked.save(out_file)
                run_counter = 0
                data = []
            else:
                print('For this subj all runs are empty')
                run_counter = 0
                data = []
                continue
        else:
           print('run', run)
           rf = fpath_events.format(subj, run)
           file = pathlib.Path(rf)
           if file.exists():
                print('This file is being processed: ', rf)
                freq_file = data_path.format(subj, run)
                freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                data.append(freq_data.data)
                run_counter = run_counter + 1
