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

fpath_raw = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_events = '/home/asmyasnikova83/DATA/mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'
freq_path = data_path
data = []


for i in range(len(kind)):
    for run in runs:
        for subject in subjects:
            rf = fpath_events.format(kind[i],subject, run, stimulus, kind[i], train)
            file = pathlib.Path(rf)
            if file.exists() and os.stat(rf).st_size != 0:
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
                #raw_data.info['bads'] = ['MEG 2443']
                KIND = kind[i]
                events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, KIND, subject, run, picks)
                print('\n\nDone with the events!')
                BASELINE, b_line = compute_baseline_substraction_and_power(raw_data, events_with_cross, events_of_interest, picks)
                print('\n\nDone with the BASELINE I!')
                if BASELINE.all== 0:
                    print('Yes, BASELINE is dummy')
                    continue
                CORRECTED_DATA = correct_baseline_substraction(BASELINE, events_of_interest, raw_data, picks)
                print('\n\nDone with the CORRECTED!')
                plot_created_epochs_evoked = False
                epochs_of_interest, evoked = create_mne_epochs_evoked(KIND, subject, run, CORRECTED_DATA, events_of_interest, plot_created_epochs_evoked, raw_data, picks)
                # for time frequency analysis we need baseline II (power correction)
                freq_show = correct_baseline_power(epochs_of_interest, b_line, KIND, b_line_manually, subject, run, plot_spectrogram)
                print('\n\nDone with the BASELINE II!')
                #plot an example of topomap
                show_one = False
                if mode == 'server'and show_one:
                    topomap_one(freq_show)
                    freq_file = freq_fpath.format(prefix, kind[i], subject, run, spec, frequency, subject, KIND, train)
                    #read tfr data from (freq_file)[0]
                    freq_show = mne.time_frequency.read_tfrs(freq_file)[0]
                    #fix the hack array[5] for changed freq dim
                    freq_show.freqs  = freqs
                    data.append(freq_show)
            else:
                print('This file: ', rf, 'does not exit')
                continue

exit()
'''
print('\n\nGrand_average:')
freq_data = mne.grand_average(data)

print('\n\nPlot poto:')

if mode == 'server':
    #topomap for the general time inerval
    PM = freq_data.plot_topo(picks='meg', title='Theta average power in Negative Feedback')
    #topographic maps of time-frequency intervals of TFR data
    PM = freq_data.plot_topomap(tmin= 0.20, tmax=0.60, fmin=4, fmax=8, ch_type='grad')
    os.chdir('/home/asmyasnikova83/DATA')
    PM.savefig('output.png')
else:
    PM = freq_data.plot_topomap(tmin= 0.20, tmax=0.60, fmin=4, fmax=8, ch_type='grad')
    plt.show()
'''
