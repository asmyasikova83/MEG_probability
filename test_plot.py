import mne, os
import numpy as np
from baseline_correction import retrieve_events_for_baseline
import pathlib

period_start = -2.20 # epoch start
period_end = 2.00 #epoch end
L_freq = 4
H_freq = 6
f_step = 1
freqs = np.arange(L_freq, H_freq+1, f_step)

data = []

fpath_raw = '/home/sasha/MEG/MIO_cleaning/{}_run{}_raw_tsss_mc.fif'
fpath_events = '/home/sasha/MEG/MIO_cleaning/{}_run{}_mio_corrected_positive.txt' 

# main loop
subjects = ['P005']
runs = ['2', '4']
for run in runs:
    for subject in subjects:
        rf = fpath_events.format(subject, run)
        file = pathlib.Path(rf)
        if file.exists():
            # raw_data
            print('\n\nThis file is being processed: ', rf)
            raw_file = fpath_raw.format(subject, run)
            raw_data = mne.io.Raw(raw_file, preload=True)
            picks = mne.pick_types(raw_data.info, meg = True)

            # events
            events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, rf, picks)

            # epochs
            epochs_of_interest = mne.Epochs(raw_data, events_of_interest, event_id = None, tmin = period_start,
                                            tmax = period_end, baseline = None, picks=picks, preload = True)
            epochs_of_interest = epochs_of_interest.resample(250, npad='auto')

            # multitape
            freq_show = mne.time_frequency.tfr_multitaper(epochs_of_interest, freqs = freqs, n_cycles =  freqs//2, use_fft = False, return_itc = False)

            # write
            temp = freq_show.data.sum(axis=1)
            freq_show.data = temp.reshape(temp.shape[0], 1, temp.shape[1])
            #print('\n\nfreq data shape', freq_show.data.shape)
            #print(freq_show)
            #print(freq_show.data)
            #print('\n\n')
            # [5]
            freq_show.freqs  = np.array([5])

            # read
            freq_show.save('test_plot-tfr.h5', overwrite=True)
            # [0]
            freq_show2 = mne.time_frequency.read_tfrs('test_plot-tfr.h5')[0]
            # freqs
            freq_show2.freqs  = freqs
            print('\n\nfreq data2 shape', freq_show2.data.shape)
            print(freq_show2)
            print(freq_show2.data)
            print('\n\n')

            # collect data
            data.append(freq_show2)

        else:
            print('\n\nThis file: ', rf, 'does not exit')
            continue

# plot average data
freq_data = mne.grand_average(data)
print('\n\nfreq data avrg shape', freq_data.data.shape)
print(freq_data)
print(freq_data.data)
print('\n\n')
freq_show3 = freq_data.apply_baseline(baseline=(-0.35,-0.05), mode="logratio")
freq_show3.plot_topo(title='Theta power in Positive Feedback Baseline')

