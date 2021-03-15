import mne, os
import numpy as np
import numpy.matlib
from baseline_correction import retrieve_events_for_baseline
from baseline_correction import reshape_epochs
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline_substraction_and_power
from baseline_correction import correct_baseline_substraction
from config import *
import pathlib

def baseline_GA(subject, subjects1, KIND):
    #set baseline == 'fixation_cross_norisks' and GA_correction = True to build a well-behaved baseline for additional substraction in GA (remove trend this way) 
    run_counter = 0
    fpath_events = '/home/asmyasnikova83/DATA/mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'
    fpath_raw = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'

    for run in runs:
        rf = fpath_events.format(KIND,subject, run, stimulus, KIND, train)
        file = pathlib.Path(rf)
        if file.exists() and os.stat(rf).st_size != 0:
            run_counter = run_counter + 1
            print('run_counter', run_counter)

    SUBJ_BASE = np.zeros(204)
    BASE =  np.zeros((run_counter, 204))
    ind = 0
    for run in runs:
        rf = fpath_events.format(KIND,subject, run, stimulus, KIND, train)
        file = pathlib.Path(rf)
        if file.exists() and os.stat(rf).st_size != 0:
            raw_file = fpath_raw.format(subject, run, subject)
            raw_data = mne.io.Raw(raw_file, preload=True)
            #filter 1-50 Hz
            raw_data = raw_data.filter(None, 50, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
            raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts
            picks = mne.pick_types(raw_data.info, meg = 'grad')
            events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, KIND, subject, run, picks)
            print('\n\nEvents with cross extracted!')
            BASELINE, b_line = compute_baseline_substraction_and_power(raw_data, events_with_cross, events_of_interest, picks)
            print('\n\nDone with the BASELINE I!')
            if BASELINE.all== 0:
                print('Yes, BASELINE is dummy')
                continue
            ind = ind + 1
            print('Baseline shape', BASELINE.shape)
            #average over epochs
            BASELINE = np.mean(BASELINE, axis = 1)
            print('Baseline new shape', BASELINE.shape)
            print('ind', ind)
            #put here baseline for each run
            BASE[ind - 1, 0:204] = BASELINE
    print('BASE', BASE)
    #average baseline over runs/blocks
    SUBJ_BASE = np.mean(BASE, axis = 0)
    print('SUBJ BASE', SUBJ_BASE)
    #prepare for further baseline correction
    SUBJ_BASE = np.matlib.repmat(SUBJ_BASE, int(time.shape[0]), 1)
    SUBJ_BASE = np.transpose(SUBJ_BASE)
    print('SUBJ BASE shape', SUBJ_BASE.shape)
            
    return SUBJ_BASE   
            
            
