import mne, os, sys, numpy as np
from config import *
import pathlib

def container_process(conf):
    path_home = conf.path_home
    kind = conf.kind
    frequency = conf.frequency

    temp1 = mne.Evoked(f'{path_home}donor-ave.fif')
    fpath_events = conf.path_mio + '/mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'

    #get rid of runs, leave frequency data for pos and neg feedback for time course plotting 
    for i in range(len(kind)):
        data = []
        run_counter = 0
        for subject in subjects:
            for run in runs:
                if run == runs[-1]:
                    print('Dis is da last run!')
                    print('run', run)
                    rf = fpath_events.format(kind[i], subject, run, stimulus, kind[i], train)
                    file = pathlib.Path(rf)
                    if file.exists():
                        print('This file is being processed: ', rf)
                        freq_file = conf.path_tfr + data_path.format(subject, run, spec, frequency, stimulus, kind[i], train)
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
                        out_file = conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subject, spec, stimulus,  kind[i], frequency, train)
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
                    rf = fpath_events.format(kind[i], subject, run, stimulus, kind[i], train)
                    file = pathlib.Path(rf)
                    if file.exists():
                        print('This file is being processed: ', rf)
                        freq_file = conf.path_tfr + data_path.format(subject, run, spec, frequency, stimulus, kind[i], train)
                        freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                        data.append(freq_data.data)
                        run_counter = run_counter + 1
