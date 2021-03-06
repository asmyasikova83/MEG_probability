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
from mne import read_evokeds

evoked_ave = []

fpath_raw = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_events = '/home/asmyasnikova83/DATA/mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'
temp1 = mne.Evoked(f'{prefix}donor-ave.fif')
folder = 'GA'
run_counter = 0


for i in range(len(kind)):
    for subject in subjects:
        for run in runs:
            if run == '6':
                print('Dis is da last run!')
                rf = fpath_events.format(kind[i], subject, run, stimulus, kind[i], train)
                print('rf', rf)
                file = pathlib.Path(rf)
                if file.exists():
                    if mode  == 'server':
                        raw_file = fpath_raw.format(subject, run, subject)
                    else:
                        raw_file = fpath_raw.format(subject, run)
                    raw_data = mne.io.Raw(raw_file, preload=True)
                    raw_data = raw_data.filter(None, 50, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
                    raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts
                    picks = mne.pick_types(raw_data.info, meg = 'grad')
                    KIND = kind[i]
                    events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, KIND, subject, run, picks)
                    print('Done with the events!')
                    BASELINE, b_line = compute_baseline_substraction_and_power(raw_data, events_with_cross, events_of_interest, picks)
                    if BASELINE.all== 0:
                        print('Yes, BASELINE is dummy')
                        continue
                    print('\n\nDone with the BASELINE I!')
                    CORRECTED_DATA = correct_baseline_substraction(BASELINE, events_of_interest, raw_data, picks)
                    print('\n\nDone with the CORRECTED!')
                    plot_created_epochs_evoked = False
                    epochs_of_interest, evoked = create_mne_epochs_evoked(KIND, subject, run, CORRECTED_DATA, events_of_interest, plot_created_epochs_evoked, raw_data, picks)
                    evoked_ave.append(evoked.data)
                    run_counter = run_counter + 1
                if run_counter > 0:
                    new_evoked = temp1.copy()
                    new_evoked.info = evoked.info
                    new_evoked.nave = 98  #all
                    new_evoked.kind = "average"
                    new_evoked.times = evoked.times
                    new_evoked.first = 0
                    new_evoked.last = evoked.times.shape[0] - 1
                    ev_data = np.asarray(evoked_ave)
                    ev_data = ev_data[:, np.newaxis]
                    print('ev_data shape', ev_data.shape)
                    #mean across runs
                    ev_data = ev_data.mean(axis=0).mean(axis=0)
                    #v_data = ev_data.mean(axis = 0)
                    print('shape', ev_data.shape)
                    new_evoked.data = ev_data
                    out_file = out_path + folder + "/{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subject, spec, stimulus,  kind[i], frequency, train)
                    mne.write_evokeds(out_file, new_evoked)
                    run_counter = 0
                    evoked_ave = []
                else:
                    print('For this subj all runs are empty')
                    run_counter = 0
                    evoked_ave = []
                    continue
            else:
                print('run', run)
                rf = fpath_events.format(kind[i], subject, run, stimulus, kind[i], train)
                file = pathlib.Path(rf)
                if file.exists():
                    print('This file is being processed: ', rf)
                    if mode  == 'server':
                        raw_file = fpath_raw.format(subject, run, subject)
                    else:
                        raw_file = fpath_raw.format(subject, run)
                    raw_data = mne.io.Raw(raw_file, preload=True)
                    raw_data = raw_data.filter(None, 50, fir_design='firwin') # for low frequencies, below the peaks of power-line noise low pass filter the data
                    raw_data = raw_data.filter(1., None, fir_design='firwin') #remove slow drifts
                    picks = mne.pick_types(raw_data.info, meg = 'grad')
                    KIND = kind[i]
                    events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, KIND, subject, run, picks)
                    print('Done with the events!')
                    BASELINE, b_line = compute_baseline_substraction_and_power(raw_data, events_with_cross, events_of_interest, picks)
                    if BASELINE.all== 0:
                        print('Yes, BASELINE is dummy')
                        continue
                    print('\n\nDone with the BASELINE I!')
                    CORRECTED_DATA = correct_baseline_substraction(BASELINE, events_of_interest, raw_data, picks)
                    print('\n\nDone with the CORRECTED!')
                    plot_created_epochs_evoked = False
                    epochs_of_interest, evoked = create_mne_epochs_evoked(KIND, subject, run, CORRECTED_DATA, events_of_interest, plot_created_epochs_evoked, raw_data, picks)
                    evoked_ave.append(evoked.data)
                    run_counter = run_counter + 1


for subject in subjects:
    sdata = []
    #change kind[0] to kind[1] to get another output.png
    out_file = out_path + folder + "/{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subject, spec, stimulus, kind[0], frequency, train)
    print(out_file)
    file = pathlib.Path(out_file)
    if file.exists():
        print('This file is being processed: ', out_file)
        evoked = mne.Evoked(out_file)
        print(type(evoked))
        print(evoked)
        sdata.append(evoked)

print('\n\nGrand_average:')
grand_averages = mne.grand_average(sdata)
if butterfly:
    GA = grand_averages.plot(spatial_colors=True, gfp=True, picks=picks, show=False)
if topomap:
    GA = grand_averages.pick_types(meg='grad').plot_topo(color='r', legend=False)
    print('Pic done')
print(grand_averages)
if mode == 'server':
    os.chdir('/home/asmyasnikova83/DATA/evoked_ave')
    GA.savefig('output.png')
else:
    plt.show()

