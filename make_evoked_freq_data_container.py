import mne, os, sys, numpy as np
from config import conf
import pathlib

def container_results(freq_data, data, donor, out_file, verbose):
    new_evoked = donor.copy()
    new_evoked.info = freq_data.info
    new_evoked.nave = 98  #all
    new_evoked.kind = "average"
    new_evoked.times = freq_data.times
    new_evoked.first = 0
    new_evoked.last = new_evoked.times.shape[0] - 1
    new_evoked.comment = freq_data.comment
    fq_data = np.asarray(data)
    if verbose:
        print('fq_data shape', fq_data.shape)
    #mean across runs
    fq_data = fq_data.mean(axis=0).mean(axis=1)
    if verbose:
        print('shape', fq_data.shape)
    new_evoked.data = fq_data
    if verbose:
        print(out_file)
    new_evoked.save(out_file)

def container_process(conf):
    print('\trun tfr container...')
    path_home = conf.path_home
    kind = conf.kind
    stimulus = conf.stimulus
    train = conf.train
    frequency = conf.frequency
    spec = conf.spec
    data_path = conf.data_path
    verbose = conf.verbose

    donor = mne.Evoked(f'{path_home}donor-ave.fif', verbose = 'ERROR')
    fpath_events = conf.path_mio + '/mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'

    #get rid of runs, leave frequency data for pos and neg feedback for time course plotting 
    for i in range(len(kind)):
        for subject in conf.subjects:
            data = []
            processing_done = False
            out_file = conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subject, spec, stimulus, kind[i], frequency, train)
            for run in conf.runs:
                print('\t\t', kind[i], run, subject)
                file_exists = False
                path_events = fpath_events.format(kind[i], subject, run, stimulus, kind[i], train)
                if pathlib.Path(path_events).exists():
                    if verbose:
                        print('This file is being processed: ', path_events)
                    file_exists = True

                    freq_file = conf.path_tfr + data_path.format(subject, run, spec, frequency, stimulus, kind[i], train)
                    old_level = mne.set_log_level(verbose='ERROR', return_old_level=True)
                    freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                    mne.set_log_level(verbose=old_level)
                    data.append(freq_data.data)

                if run == conf.runs[-1]:
                    if file_exists:
                        processing_done = True
                    if processing_done:
                        container_results(freq_data, data, donor, out_file, verbose)
                    else:
                        if verbose:
                            print('For this subj all runs are empty')
                else:
                    if file_exists:
                        processing_done = True

    print('\ttfr container completed')

