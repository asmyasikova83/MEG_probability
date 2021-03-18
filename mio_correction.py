import mne, os
import numpy as np
from config import conf
import pathlib

def clean_events(epochs_ar, thres):
    '''
    conditions for clean
    '''
    #N_events, N_chans, N_times
    epochs_ar = epochs_ar.swapaxes(0, 1).swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    
    EV_DATA = np.abs(epochs_ar)
    
    CHAN_MAX = np.max(EV_DATA, axis=1)
    RESH_DATA = EV_DATA.reshape(N_chans,  N_events* N_times) 
    
    CHAN_MEAN = np.mean(RESH_DATA, axis=1)
    CHAN_STD = np.std(RESH_DATA, axis=1)
    
    good_events = []
    for i in range(N_events):
        select = np.where(CHAN_MAX[:, i] > CHAN_MEAN + thres*CHAN_STD)
        if select[0].shape[0] <= N_chans//4:
            good_events.append(i)

    return np.array(good_events)

def call_clean_events(conf, subj, run, kind_idx, fpath_events, fpath_mio_out):
    '''
    extract cleaned events (txt) and save raw events by extracted index
    '''
    verbose = conf.verbose
    stimulus = conf.stimulus
    train = conf.train
    kind = conf.kind

    raw_data = mne.io.Raw(conf.fpath_raw.format(subj, run, subj), preload=True, verbose='ERROR').filter(l_freq=70, h_freq=None)

    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset',
        consecutive='increasing', min_duration=0, shortest_event=1, mask=None,
        uint_cast=False, mask_type='and', initial_event=False, verbose='ERROR')

    events = np.loadtxt(fpath_events.format(subj, run, stimulus, kind[kind_idx], train), dtype=int)
    # (3,) -> (3,1)
    if events.shape == (3,):
        events = events[np.newaxis, :]
    if verbose:
        print(events.shape)

    epochs = mne.Epochs(raw_data, events, event_id=None, tmin=conf.period_start, tmax=conf.period_end,
        picks=mne.pick_types(raw_data.info, meg=True), preload=True, verbose='ERROR').pick(picks="grad")

    thres = 7 #procedure to remove epochs-outliers based on thres*STD difference
    clean = clean_events(epochs.get_data(), thres)
    if clean.any():
        if verbose:
            print(subj, thres, str(events.shape[0]) + " ~~~~ " + str(events[clean].shape[0]) )
        cleaned = events[clean]
        if verbose:
            print(cleaned)

        full_ev = []
        for i in range(cleaned.shape[0]):
            event_ind = events_raw.tolist().index(cleaned[i].tolist())
            full_ev.append(events_raw[event_ind].tolist())
            event_ind += 1

        mio_corrected_events_file = open(fpath_mio_out.format(kind[kind_idx], subj, run, stimulus, kind[kind_idx], train), "w")
        np.savetxt(mio_corrected_events_file, full_ev, fmt="%d")
        mio_corrected_events_file.close()
    else:
        if verbose:
            print('Events cleaned are empty!')

def mio_correction(conf):
    '''
    extract cleaned events
    '''
    print('\trun mio_extraction...')
    kind = conf.kind
    stimulus = conf.stimulus
    train = conf.train
    verbose = conf.verbose
    for i in range(len(kind)):
        fpath_events = conf.path_events + '{0}_run{1}_events_{2}{3}{4}.txt'
        fpath_mio_out = conf.path_mio + 'mio_out_{0}/{1}_run{2}_mio_corrected_{3}{4}{5}.txt'
        fpath_mio_dir = conf.path_mio + 'mio_out_{}/'
        os.makedirs(fpath_mio_dir.format(kind[i]), exist_ok = True)

        for run in conf.runs:
            for subject in conf.subjects:
                print('\t\t', kind[i], run, subject)
                rf = fpath_events.format(subject, run, stimulus, kind[i], train)
                if verbose:
                    print(rf)
                file = pathlib.Path(rf)
                if file.exists() and os.stat(rf).st_size != 0:
                    if verbose:
                        print('This file is being processed: ', rf)
                    call_clean_events(conf, subject, run, i, fpath_events, fpath_mio_out)
                else:
                    if verbose:
                        print('This file: ', rf, 'does not exit')
                    continue

    print('\tmio_extraction completed')
