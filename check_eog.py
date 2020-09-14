import mne, os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from baseline_correction import retrieve_events_for_baseline
from baseline_correction import reshape_epochs
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline_substraction_and_power
from baseline_correction import correct_baseline_substraction
from baseline_correction import correct_baseline_power
from baseline_correction import topomap_one
from config import *
import pathlib

if mode == 'server':
    fpath_raw = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
    fpath_ev = '/home/asmyasnikova83/DATA/'
    fpath_fr= '/home/asmyasnikova83/DATA/TFR/'
else:
    fpath_raw = '/home/sasha/MEG/MIO_cleaning/run{}_{}_raw_ica.fif'
    fpath_ev =  '/home/sasha/MEG/MIO_cleaning/'
    fpath_fr = '/home/sasha/MEG/Time_frequency_analysis/'
data = []

kind = 'negative'

if kind == 'negative':
    #explore negative feedback
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_negative/{}_run{}_mio_corrected_negative.txt'
        freq_fpath = fpath_fr + 'negative/{0}_run{1}_theta_negative_int_50ms-tfr.h5'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_negative.txt'
        freq_fpath = fpath_fr +  '{0}_run{1}_theta_negative_int_50ms-tfr.h5'
if kind == 'positive':
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_positive/{}_run{}_mio_corrected_positive.txt'
        freq_fpath = fpath_fr + 'positive/{0}_run{1}_theta_positive_int_50ms-tfr.h5'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_positive.txt'
        freq_fpath = fpath_fr +  '{0}_run{1}_theta_positive_int_50ms-tfr.h5'


for run in runs:
    for subject in subjects:
        rf = fpath_events.format(subject, run)
        file = pathlib.Path(rf)
        if file.exists():
            print('This file is being processed: ', rf)
            if mode == 'server':
                raw_file = fpath_raw.format(subject, run, subject)
            else:
                raw_file = fpath_raw.format(run, subject)
            raw_data = mne.io.Raw(raw_file, preload=True)
            #filter 1-50 Hz
            raw_data = raw_data.filter(None, 50, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
            raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts          
            picks = mne.pick_types(raw_data.info, meg = True, misc = True)
            events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, picks)
            epochs_of_interest = mne.Epochs(raw_data, events_of_interest, event_id = None, tmin = period_start,
            tmax = period_end, baseline = None, preload = True)
            freq_show = mne.time_frequency.tfr_multitaper(epochs_of_interest, freqs = freqs,  n_cycles =  freqs//2, use_fft = False, return_itc = False, picks= ['MISC301', 'MISC302'])
            freq_show = freq_show.crop(tmin=period_start+0.350, tmax=period_end-0.350, include_tmax=True)
            freq_show.apply_baseline(baseline=(-0.5,-0.1), mode="logratio")
       
            if kind == 'positive':
                if mode == 'server':
                    tfr_path = '/home/asmyasnikova83/DATA/TFR/positive/{0}_run{1}_theta_positive_int_50ms-tfr.h5'
                else:
                    tfr_path = '/home/sasha/MEG/Time_frequency_analysis/{0}_run{1}_theta_positive_int_50ms-tfr.h5'
            if kind == 'negative':
                if mode == 'server':
                    tfr_path = '/home/asmyasnikova83/DATA/TFR/negative/{0}_run{1}_theta_negative_int_50ms-tfr.h5'
                else:
                    tfr_path = '/home/sasha/MEG/Time_frequency_analysis/{0}_run{1}_theta_negative_int_50ms-tfr.h5'
            freq_show.save(tfr_path.format(subject, run), overwrite=True)
            print(tfr_path.format(subject, run))


for run in runs:
    for subject in subjects:
        rf = fpath_events.format(subject, run)
        file = pathlib.Path(rf)
        if file.exists():
            print('This file is being processed: ', rf)
            freq_file = freq_fpath.format(subject, run)
            freq_show = mne.time_frequency.read_tfrs(freq_file)[0]
            freq_show.freqs  = freqs
            data.append(freq_show)
        else:
            print('This file: ', rf, 'does not exit')
            continue


info = raw_data.info
info['sfreq'] = 250
freq_show.freqs = freqs
title = 'VEOG Theta TFR '

#topographic maps of time-frequency intervals of TFR data of VEOG channel
PM = freq_show.plot(picks=['MISC301'], fmin=4, fmax=8, title=title)
if mode == 'server':
    os.chdir('/home/asmyasnikova83/DATA')
    PM.savefig('output.png')
else:
    plt.show
