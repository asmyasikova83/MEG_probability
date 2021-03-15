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
from config import *
import pathlib

if mode == 'server':
    fpath_raw = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
    fpath_ev = '/net/server/data/Archive/prob_learn/experiment/'
    fpath_fr= '/net/server/data/Archive/prob_learn/experiment/TFR/'
    out_path = '/net/server/data/Archive/prob_learn/experiment/TFR/'
else:
    fpath_raw = '/home/sasha/MEG/MIO_cleaning/run{}_{}_raw_ica.fif'
    fpath_ev =  '/home/sasha/MEG/MIO_cleaning/'
    fpath_fr = '/home/sasha/MEG/Time_frequency_analysis/'
    out_path = '/home/sasha/MEG/Time_frequency_analysis/'
data = []

kind = 'positive'
type_spec = 'to_10_Hz'

if kind == 'negative':
    #explore negative feedback
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_negative/{}_run{}_mio_corrected_negative.txt'
        if type_spec == 'to_10_Hz':
            freq_fpath = fpath_fr + 'negative/{0}_run{1}_spec_negative_2_10_int_50ms-tfr.h5'
        if type_spec == 'to_100_Hz':
            freq_fpath = fpath_fr + 'negative/{0}_run{1}_spec_negative_int_50ms-tfr.h5'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_negative.txt'
        freq_fpath = fpath_fr +  '{0}_run{1}_spec_negative_int_50ms-tfr.h5'
        #freq_fpath = '/home/sasha/MEG/Time_frequency_analysis/{0}_run{1}_alpha_negative_int_50ms-tfr.h5'
        #freq_fpath = '/home/sasha/MEG/Time_frequency_analysis/{0}_run{1}_beta_negative_int_50ms-tfr.h5'
if kind == 'positive':
    if mode == 'server':
        fpath_events = fpath_ev + 'mio_out_positive/{}_run{}_mio_corrected_positive.txt'
        if type_spec == 'to_10_Hz':
            freq_fpath = fpath_fr + 'positive/{0}_run{1}_spec_positive_2_10_int_50ms-tfr.h5'
        if type_spec == 'to_100_Hz':
            freq_fpath = fpath_fr + 'positive/{0}_run{1}_spec_positive_int_50ms-tfr.h5'
    if mode != 'server':
        fpath_events = fpath_ev + '{}_run{}_mio_corrected_positive.txt'
        freq_fpath = fpath_fr +  '{0}_run{1}_spec_positive_int_50ms-tfr.h5'
        #freq_fpath = '/home/sasha/MEG/Time_frequency_analysis/{0}_run{1}_alpha_positive_int_50ms-tfr.h5'
        #freq_fpath = '/home/sasha/MEG/Time_frequency_analysis/{0}_run{1}_beta_positive_int_50ms-tfr.h5'
data = []
run_counter = 0

for subject in subjects:
    for run in runs:
        if run == '6':
            print('Dis is da last run!')
            print('run', run)
            rf = fpath_events.format(subject, run)
            file = pathlib.Path(rf)
            if file.exists():
                print('This file is being processed: ', rf)
                if mode == 'server':
                    raw_file = fpath_raw.format(subject, run, subject)
                    print('raw file', raw_file)
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
                freq_file = freq_fpath.format(subject, run)
                #read tfr data from (freq_file)[0]
                freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                #fix the hack array[5] for changed freq dim
                data.append(freq_data.data)
                run_counter = run_counter + 1
            if run_counter > 0:
                fq_data = np.asarray(data)
                print('fq_data shape', fq_data.shape)
                #mean across runs
                fq_data = fq_data.mean(axis=0)
                print('shape', fq_data.shape)
                freq_data.data = fq_data
                if type_spec == 'to_10_Hz':
                    out_file = out_path + "{0}_feedback_{1}_spec_2_10_int_50ms-tfr.h5".format(subject, kind)
                if type_spec == 'to_100_Hz':
                    out_file = out_path + "{0}_feedback_{1}_spec_int_50ms-tfr.h5".format(subject, kind)
                print(out_file)
                freq_data.save(out_file, overwrite=True)
                run_counter = 0
                data = []
            else:
                print('For this subj all runs are empty')
                run_counter = 0
                data = []
                continue            
        else:
           print('run', run)
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
                freq_file = freq_fpath.format(subject, run)
                #read tfr data from (freq_file)[0]
                freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                #fix the hack array[5] for changed freq dim
                data.append(freq_data.data)
                run_counter = run_counter + 1

sdata = []       
for subject in subjects:
    if type_spec == 'to_10_Hz':
        out_file = out_path + "{0}_feedback_{1}_spec_2_10_int_50ms-tfr.h5".format(subject, kind)
    if type_spec == 'to_100_Hz':
        out_file = out_path + "{0}_feedback_{1}_spec_int_50ms-tfr.h5".format(subject, kind)
    file = pathlib.Path(out_file)
    if file.exists():
        print('This file is being processed: ', out_file)
        freq_subject_data = mne.time_frequency.read_tfrs(out_file)[0]
        sdata.append(freq_subject_data)
 

print('\n\nGrand_average:')
freq_spec_data = mne.grand_average(sdata)
if type_spec == 'to_10_Hz' and kind == 'positive':
    title = 'All channels ~2-10 Hz TFR in Positive FB'
if type_spec == 'to_10_Hz' and kind == 'negative':
    title = 'All channels ~2-10 Hz TFR in Negative FB'
if type_spec == 'to_100_Hz' and kind == 'positive':
    title = 'All channels ~2-100 Hz TFR in Positive FB'
if type_spec == 'to_100_Hz' and kind == 'negative':
    title = 'All channels ~2-100 Hz TFR in Negative FB'

#p_mul = 0.5
#set fmin fmax in compliance with config!
PM = freq_spec_data.plot(picks='meg', vmin=-0.1, vmax=0.1, title=title)



print('\n\nPlot poto:')

if mode == 'server':
    #topomap for the general time inerval
    #PM = freq_data.plot_topo(picks='meg', title='Theta average power in Negative Feedback')
    #topographic maps of time-frequency intervals of TFR data
    #PM = freq_data.plot_topomap(tmin= 0.20, tmax=0.60, fmin=4, fmax=8, ch_type='grad')
    os.chdir('/net/server/data/Archive/prob_learn/experiment/TFR/')
    PM.savefig('output.png')
else:
    #PM = freq_data.plot_topomap(tmin= 0.20, tmax=0.60, fmin=4, fmax=8, ch_type='grad')
    plt.show()
