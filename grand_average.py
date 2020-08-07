import mne, os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from baseline_correction import retrieve_events_for_baseline
from baseline_correction import reshape_epochs
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline
from baseline_correction import correct_baseline
from config import *
import pathlib

fpath_raw = '/home/asmyasnikova83/DATA/links/{}/{}_run{}_raw_tsss_mc.fif'
fpath_events = '/home/asmyasnikova83/DATA/mio_out/{}_run{}_mio_corrected.txt'
fpath_out = '/home/asmyasnikova83/DATA/evoked_ave/{}_run{}_evoked_ave.fif'

evoked_ave = []

for run in runs:
    for subject in subjects:
        rf = fpath_events.format(subject, run)
        file = pathlib.Path(rf)
        if file.exists():
            print('This file is being processed: ', rf)
            raw_file = fpath_raw.format(subject, subject, run)
            raw_data = mne.io.Raw(raw_file, preload=True)
            #filter 1-50 Hz
            raw_data = raw_data.filter(None, 50, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
            raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts           
            picks = mne.pick_types(raw_data.info, meg = True)
            events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, picks)
            print('Done with the events!')
            BASELINE = compute_baseline(raw_data, events_with_cross, picks)
            print('Done with the BASELINE!')
            CORRECTED_DATA = correct_baseline(BASELINE, events_of_interest, raw_data, picks)
            print('Done with the CORRECTED!')
            plot = False
            evoked = create_mne_epochs_evoked(CORRECTED_DATA, events_of_interest, plot, raw_data, picks)
            evoked_ave.append(evoked)
        else:
            print('This file: ', rf, 'does not exit')
            continue

grand_averages = mne.grand_average(evoked_ave)
print(grand_averages)
GA = grand_averages.plot(spatial_colors=True, gfp=True, picks=picks, show=False)
os.chdir('/home/asmyasnikova83/DATA/evoked_ave')
GA.savefig('output.png')

