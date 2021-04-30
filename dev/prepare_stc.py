import mne, os
import numpy as np
from config import conf
import pathlib
from surfer import Brain

os.environ["SUBJECTS_DIR"] = "/net/server/data/Archive/prob_learn/freesurfer/"

def stc_process(conf):
    print('\trun source...')
    kind = conf.kind
    train = conf.train
    verbose = conf.verbose
    fpath_raw = conf.fpath_raw
    fpath_events = f'{conf.path_mio}/' + 'mio_out_{}/{}_run{}_mio_corrected_{}{}.txt'
    conductivity = (0.3,)  # for single layer
    subjects_dir = '/net/server/data/Archive/prob_learn/experiment/P011/170214/ORIGINAL_TSSS/'
    path_forward = '/home/asmyasnikova83/DEV/source/MEG_probability/links/'
    path_cov = '/home/asmyasnikova83/DEV/source/MEG_probability/links/'
    snr = 1
    lambda2 = 1 / snr ** 2
    method = 'MNE'
    data = []
    stc_list = []


    for i in range(len(kind)):
        for run in conf.runs:
            for subject in conf.subjects:
                print('\t\t', kind[i], run, subject)
                path_events = fpath_events.format(kind[i],subject, run, kind[i], train)
                if conf.baseline == 'fixation_cross_norisks':
                    path_events_with_cross = f'{conf.path_mio}/mio_out_norisk/{subject}_run{run}_mio_corrected_norisk.txt'
                else:
                    path_events_with_cross = path_events
                if pathlib.Path(path_events).exists() and os.stat(path_events).st_size != 0 and \
                    pathlib.Path(path_events_with_cross).exists() and os.stat(path_events_with_cross).st_size != 0:
                    if verbose:
                        print('This file is being processed: ', path_events)
