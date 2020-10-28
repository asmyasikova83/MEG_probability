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

#data_path = '/home/asmyasnikova83/DATA/links/'
#out_path = f'theta_reinforced_{L_freq}_{H_freq}/'
#os.makedirs(os.path.join(os.getcwd(), "Sensor", "TFR", out_path), exist_ok = True)

fpath_raw = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'

def calculate_beta(subj, run, fpath_raw, fpath_events, fpath_mio_out):
   # freqs = np.arange(L_freq, H_freq, f_step)
        
    raw_data = mne.io.Raw(fpath_raw.format(subj, run, subj), preload=True)
    raw_data = raw_data.filter(l_freq=70, h_freq=None)
    picks = mne.pick_types(raw_data.info, meg = True)
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    events = np.loadtxt(fpath_events.format(subj, run), dtype=int)
    print(events)
    if events.shape == (3,):
        events = events[np.newaxis, :]
    print(events.shape)
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start, tmax = period_end, picks=picks, preload = True)
    epochs = epochs.pick(picks="grad")

    thres = 7 #procedure to remove epochs-outliers based on thres*STD difference
    clean = no_mio_events(epochs.get_data(), thres)
   
    print(subj, thres, str(events.shape[0]) + " ~~~~ " + str(events[clean].shape[0]) )
    cleaned = events[clean]
    print(cleaned)
    del epochs, events, clean, picks, raw_data

    full_ev = []
    for i in range(cleaned.shape[0]):
        event_ind = events_raw.tolist().index(cleaned[i].tolist())
        full_ev.append(events_raw[event_ind].tolist())
        event_ind += 1

    del events_raw

    mio_corrected_events_file = open(fpath_mio_out.format(subj, run), "w")
    np.savetxt(mio_corrected_events_file, full_ev, fmt="%d")
    mio_corrected_events_file.close()

for i in range(len(kind)):
    if kind[i] == 'positive':
        fpath_events = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_positive_no_train.txt'
        fpath_mio_out = '/home/asmyasnikova83/DATA/mio_out_positive/{}_run{}_mio_corrected_positive_no_train.txt'
        fpath_mio_dir = '/home/asmyasnikova83/DATA/mio_out_positive/'
    if kind[i] == 'negative':
        fpath_events = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_negative_no_train.txt'
        fpath_mio_out = '/home/asmyasnikova83/DATA/mio_out_negative/{}_run{}_mio_corrected_negative_no_train.txt'
        fpath_mio_dir = '/home/asmyasnikova83/DATA/mio_out_negative/'
    if kind[i] == 'prerisk':
        fpath_events = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_prerisk.txt'
        fpath_mio_out = '/home/asmyasnikova83/DATA/mio_out_prerisk/{}_run{}_mio_corrected_prerisk.txt'
        fpath_mio_dir = '/home/asmyasnikova83/DATA/mio_out_prerisk/'
    if kind[i] == 'risk':
        fpath_events = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_risk.txt'
        fpath_mio_out = '/home/asmyasnikova83/DATA/mio_out_risk/{}_run{}_mio_corrected_risk.txt'
        fpath_mio_dir = '/home/asmyasnikova83/DATA/mio_out_risk/'
    if kind[i] == 'postrisk':
        fpath_events = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_postrisk.txt'
        fpath_mio_out = '/home/asmyasnikova83/DATA/mio_out_postrisk/{}_run{}_mio_corrected_postrisk.txt'
        fpath_mio_dir = '/home/asmyasnikova83/DATA/mio_out_postrisk/'

    os.makedirs(fpath_mio_dir, exist_ok = True)

    for run in runs:
        for subject in subjects:

            rf = fpath_events.format(subject, run)
            print(rf)
            file = pathlib.Path(rf)
            print('file', file)
            if file.exists() and os.stat(rf).st_size != 0:
                print('This file is being processed: ', rf)
                calculate_beta(subject, run, fpath_raw, fpath_events, fpath_mio_out)
            else:
                print('This file: ', rf, 'does not exit')
                continue

