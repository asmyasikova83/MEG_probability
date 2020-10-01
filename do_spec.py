import mne, os, sys, numpy as np
from config import *
import pathlib


fpath_ev = '/net/server/data/Archive/prob_learn/experiment/'
fpath_fr= '/net/server/data/Archive/prob_learn/experiment/TFR/'
out_path = '/net/server/data/Archive/prob_learn/experiment/TFR/'
freq_file = '/net/server/data/Archive/prob_learn/experiment/TFR/positive/P004_run5_spec_32_48_gamma_positive_int_50ms-tfr.h5'
temp1 = mne.time_frequency.read_tfrs(freq_file)[0]
kind = 'positive'


if kind == 'negative':
    #explore negative feedback
    fpath_events = fpath_ev + 'mio_out_negative/{}_run{}_mio_corrected_negative.txt'
    data_path = fpath_fr + 'negative/{0}_run{1}_spec_32_48_gamma_negative_int_50ms-tfr.h5'
if kind == 'positive':
    fpath_events = fpath_ev + 'mio_out_positive/{}_run{}_mio_corrected_positive.txt'
    data_path = fpath_fr + 'positive/{0}_run{1}_spec_32_48_gamma_positive_int_50ms-tfr.h5'

#get rid of runs, prepare frequency data for pos and neg feedback for spectrogramm 
data = []
run_counter = 0
for subj in subjects:
    for run in runs:
        if run == '6':
            print('Dis is da last run!')
            print('run', run)
            rf = fpath_events.format(subj, run)
            file = pathlib.Path(rf)
            if file.exists():
                print('This file is being processed: ', rf)
                freq_file = data_path.format(subj, run)
                freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                print('freq data init shape', freq_data.data.shape)
                data.append(freq_data.data)
                run_counter = run_counter + 1
            if run_counter > 0:
                new_freq = temp1.copy()
                fq_data = np.asarray(data)
                print('fq_data shape', fq_data.shape)
                #mean across runs and remove abundant axis
                fq_data = fq_data.mean(axis=0)
                print('shape', fq_data.shape)
                new_freq.data = fq_data
                out_file = out_path + "{0}_feedback_{1}_spec_gamma_int_50ms-tfr.h5".format(subj, kind)
                print(out_file)
                new_freq.save(out_file, overwrite=True)
                run_counter = 0
                data = []
            else:
                print('For this subj all runs are empty')
                run_counter = 0
                data = []
                continue
        else:
           print('run', run)
           rf = fpath_events.format(subj, run)
           file = pathlib.Path(rf)
           if file.exists():
                print('This file is being processed: ', rf)
                freq_file = data_path.format(subj, run)
                freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                data.append(freq_data.data)
                run_counter = run_counter + 1



sdata = []       
for subject in subjects:
    out_file = out_path + "{0}_feedback_{1}_spec_gamma_int_50ms-tfr.h5".format(subject, kind)
    file = pathlib.Path(out_file)
    if file.exists():
        print('This file is being processed: ', out_file)
        freq_subject_data = mne.time_frequency.read_tfrs(out_file)[0]
        sdata.append(freq_subject_data)

print('\n\nGrand_average:')
freq_data = mne.grand_average(sdata)

print('\n\nPlot poto:')

if mode == 'server':
    #topomap for the general time inerval
    PM = freq_data.plot_topo(picks='meg', title='Gamma average power in Negative Feedback')
    #topographic maps of time-frequency intervals of TFR data
    #PM = freq_data.plot_topomap(ch_type='grad')
    os.chdir('/home/asmyasnikova83/DATA')
    PM.savefig('output.png')
else:
    PM = freq_data.plot_topomap(ch_type='grad')
    plt.show()
