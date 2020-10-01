import mne, os
from baseline_correction import retrieve_events_for_baseline
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline_substraction_and_power
from baseline_correction import correct_baseline_substraction
from baseline_correction import correct_baseline_power
from config import *
import pathlib

fpath_raw = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_ev = '/home/asmyasnikova83/DATA/'

data = []

kind = 'positive'

if kind == 'negative':
    #explore negative feedback
    fpath_events = fpath_ev + 'mio_out_negative/{}_run{}_mio_corrected_negative.txt'
if kind == 'positive':
    fpath_events = fpath_ev + 'mio_out_positive/{}_run{}_mio_corrected_positive.txt'

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
            raw_data = raw_data.filter(None, 100, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
            raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts          
            picks = mne.pick_types(raw_data.info, meg = 'grad')
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
            plot_spectrogram = True
            freq_show = correct_baseline_power(epochs_of_interest, b_line, kind, b_line_manually, subject, run, plot_spectrogram)
            print('\n\nDone with the BASELINE II!')
        else:
            print('This file: ', rf, 'does not exit')
            continue

