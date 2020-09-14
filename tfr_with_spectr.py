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
            picks = mne.pick_types(raw_data.info, meg = 'grad')
            print('ch names', raw_data.info['ch_names'])
            #raw_data.info['bads'] = ['MEG 2443']
            events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, picks)
            print('\n\nDone with the events!')
            BASELINE, b_line = compute_baseline_substraction_and_power(raw_data, events_with_cross, picks)
            print('\n\nDone with the BASELINE I!')
            CORRECTED_DATA = correct_baseline_substraction(BASELINE, events_of_interest, raw_data, picks)
            print('\n\nDone with the CORRECTED!')
            plot_created_epochs_evoked = False
            epochs_of_interest, evoked = create_mne_epochs_evoked(kind, subject, run, CORRECTED_DATA, events_of_interest, plot_created_epochs_evoked, raw_data, picks)
            # for time frequency analysis we need baseline II (power correction)
            b_line_manually = True
            freq_show = correct_baseline_power(epochs_of_interest, b_line, kind, b_line_manually, subject, run)
            print('\n\nDone with the BASELINE II!')
            #plot an example of topomap
            show_one = False
            if mode == 'server'and show_one:
                topomap_one(freq_show)
            freq_file = freq_fpath.format(subject, run)
            #read tfr data from (freq_file)[0]
            freq_show = mne.time_frequency.read_tfrs(freq_file)[0]
            #print('freq_show', freq_show.data)
            #freq_show.data = 10*freq_show.data
            #print('freq_show mult', freq_show.data)
            #fix the hack array[5] for changed freq dim
            freq_show.freqs  = freqs
            data.append(freq_show)
        else:
            print('This file: ', rf, 'does not exit')
            continue


print('\n\nGrand_average:')
freq_data = mne.grand_average(data)

print('\n\nPlot poto:')


info = raw_data.info
info['sfreq'] = 250
freq_show.freqs = freqs
title = 'All channels ~4-48 Hz TFR '
#set fmin fmax in compliance with config!
PM = freq_show.plot(picks='meg', fmin=2, fmax=8, title=title)
if mode == 'server':
    os.chdir('/home/asmyasnikova83/DATA')
    PM.savefig('output.png')
else:
    plt.show()
    
