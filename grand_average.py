import mne, os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from baseline_correction import retrieve_events_for_baseline
from baseline_correction import reshape_epochs
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline_substraction_and_power
from baseline_correction import correct_baseline_substraction
from config import *
import pathlib

if mode == 'server':
    fpath_raw = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
    fpath_ev = '/home/asmyasnikova83/DATA/'
else:
    fpath_raw = '/home/sasha/MEG/MIO_cleaning/{}_run{}_raw_tsss_mc.fif'
    fpath_ev =  '/home/sasha/MEG/MIO_cleaning/'
data = []


kind = 'positive'

if kind == 'negative':
    #explore negative feedback
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_negative/{}_run{}_mio_corrected_negative.txt'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_negative.txt'
if kind == 'positive':
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_positive/{}_run{}_mio_corrected_positive.txt'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_positive.txt'

evoked_ave = []

for run in runs:
    for subject in subjects:
        rf = fpath_events.format(subject, run)
        file = pathlib.Path(rf)
        if file.exists():
            print('This file is being processed: ', rf)
            if mode == 'server':
                raw_file = fpath_raw.format(subject, run, subject)
            else:
                raw_file = fpath_raw.format(subject, run)
            raw_data = mne.io.Raw(raw_file, preload=True)
            raw_data = raw_data.filter(None, 50, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
            raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts           
            picks = mne.pick_types(raw_data.info, meg = True)
            events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, picks)
            print('Done with the events!')
            BASELINE, b_line = compute_baseline_substraction_and_power(raw_data, events_with_cross, picks)
            print('\n\nDone with the BASELINE I!')
            CORRECTED_DATA = correct_baseline_substraction(BASELINE, events_of_interest, raw_data, picks)
            print('\n\nDone with the CORRECTED!')
            plot_created_epochs_evoked = False
            epochs_of_interest, evoked = create_mne_epochs_evoked(kind, subject, run, CORRECTED_DATA, events_of_interest, plot_created_epochs_evoked, raw_data, picks)
            evoked_ave.append(evoked)
        else:
            print('This file: ', rf, 'does not exit')
            continue

grand_averages = mne.grand_average(evoked_ave)
if batterfly:
    GA = grand_averages.plot(spatial_colors=True, gfp=True, picks=picks, show=False)
if topomap:
    GA = grand_averages.pick_types(meg='grad').plot_topo(color='r', legend=False)
print(grand_averages)
if mode == 'server':
    os.chdir('/home/asmyasnikova83/DATA/evoked_ave')
    GA.savefig('output.png')
else:
    plt.show()

