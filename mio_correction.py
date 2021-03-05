import mne, os
import numpy as np
from config import *
import pathlib

def no_mio_events(epochs_ar, thres):
    #N_events, N_chans, N_times
    epochs_ar = epochs_ar.swapaxes(0, 1)
    epochs_ar = epochs_ar.swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    
    EV_DATA = np.abs(epochs_ar)
    
    CHAN_MAX = np.max(EV_DATA, axis=1)
    RESH_DATA = EV_DATA.reshape(N_chans,  N_events* N_times) 
    
    CHAN_MEAN = np.mean(RESH_DATA, axis=1)
    CHAN_STD = np.std(RESH_DATA, axis=1)
    
    good_chan = []
    for i in range(N_events):
        select = np.where(CHAN_MAX[:, i] > CHAN_MEAN + thres*CHAN_STD)
        if select[0].shape[0] <= N_chans//4:
            good_chan.append(i)
    return np.array(good_chan) 

fpath_raw = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'

def calculate_beta(conf, subj, run, stimulus, kind, train, fpath_raw, fpath_events, fpath_mio_out):
    period_start = conf.period_start
    period_end = conf.period_end

    raw_data = mne.io.Raw(fpath_raw.format(subj, run, subj), preload=True)
    raw_data = raw_data.filter(l_freq=70, h_freq=None)
    picks = mne.pick_types(raw_data.info, meg = True)
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    events = np.loadtxt(fpath_events.format(subj, run, stimulus, kind, train), dtype=int)
    if events.shape == (3,):
        events = events[np.newaxis, :]
    print(events.shape)
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start, tmax = period_end, picks=picks, preload = True)
    epochs = epochs.pick(picks="grad")

    thres = 7 #procedure to remove epochs-outliers based on thres*STD difference
    clean = no_mio_events(epochs.get_data(), thres)
    if clean.any():
        print(subj, thres, str(events.shape[0]) + " ~~~~ " + str(events[clean].shape[0]) )
        cleaned = events[clean]
        print(cleaned)
        del epochs, events, clean, picks, raw_data

        full_ev = []
        for i in range(cleaned.shape[0]):
            event_ind = events_raw.tolist().index(cleaned[i].tolist())
            full_ev.append(events_raw[event_ind].tolist())
            event_ind += 1

        mio_corrected_events_file = open(fpath_mio_out.format(kind, subj, run, stimulus, kind, train), "w")
        np.savetxt(mio_corrected_events_file, full_ev, fmt="%d")
        mio_corrected_events_file.close()
    else:
        print('Events cleaned are empty!')

    del events_raw

def mio_correction(conf):
    kind = conf.kind
    for i in range(len(kind)):
        fpath_events = conf.path_events + '{0}_run{1}_events_{2}{3}{4}.txt'
        fpath_mio_out = conf.path_mio + 'mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'
        fpath_mio_dir = conf.path_mio + 'mio_out_{}/'
        os.makedirs(fpath_mio_dir.format(kind[i]), exist_ok = True)

        for run in runs:
            for subject in subjects:

                rf = fpath_events.format(subject, run, stimulus, kind[i], train)
                print(rf)
                file = pathlib.Path(rf)
                print('file', file)
                if file.exists() and os.stat(rf).st_size != 0:
                    print('This file is being processed: ', rf)
                    calculate_beta(conf, subject, run, stimulus, kind[i], train, fpath_raw, fpath_events, fpath_mio_out)
                else:
                    print('This file: ', rf, 'does not exit')
                    continue

