import mne, os
import os.path as op
import numpy as np
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

def call_clean_events(data_path, data_path_raw, raw_name, subj, r, cond, fb):
    '''
    extract cleaned events (txt) and save raw events by extracted index
    '''
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True).filter(l_freq=70, h_freq=None)
    #raw_data = mne.io.Raw(conf.fpath_raw.format(subj, run, subj), preload=True, verbose='ERROR').filter(l_freq=70, h_freq=None)
    
    events_raw = np.loadtxt(op.join(data_path_raw, raw_name.format(subj, r)), dtype = 'int')
    events = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_autists/Events_autists_test/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    # (3,) -> (1,3)
    if events.shape == (3,):
        events = events[np.newaxis, :]
    print('events before',events)
    print(events.shape)
    # список индексов трайлов
    cleaned = []
    for i in range(len(events_raw)):
        for j in range(len(events)):
            if np.all((events_raw[i] - events[j] == 0)):
                cleaned.append(events[j])  
    '''
    epochs = mne.Epochs(raw_data, events, event_id=None, tmin=period_start, tmax=period_end,
        picks=mne.pick_types(raw_data.info, meg=True), preload=True, verbose='ERROR').pick(picks="grad")

    thres = 7 #procedure to remove epochs-outliers based on thres*STD difference
    clean = clean_events(epochs.get_data(), thres)
    if cleaned.any():
        print(subj, thres, str(events.shape[0]) + " ~~~~ " + str(events[clean].shape[0]) )
        cleaned = events[clean]
        mio_corrected_events_file = open('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_test/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), "w")
        np.savetxt(mio_corrected_events_file, cleaned, fmt="%d")
        mio_corrected_events_file.close()
    '''
    cleaned = np.array(cleaned)

    if cleaned.any():
        print('events after', cleaned)
        print(cleaned.shape)
        mio_corrected_events_file = open('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), "w")
        np.savetxt(mio_corrected_events_file, cleaned, fmt="%d")
        mio_corrected_events_file.close()

#subjects = ['P301', 'P304', 'P307',  'P309',  'P312', 'P313', 'P314',
#            'P316', 'P322',  'P323', 'P324', 'P325',
#            'P326', 'P327' , 'P328','P329', 'P331',  'P333', 'P334',
#            'P336', 'P340', 'P341']
subjects = ['P301', 'P304', 'P307', 'P308', 'P311', 'P312', 'P313', 'P314', 'P316', 'P318', 'P320', 'P321', 'P322',   
            'P323', 'P324', 'P325', 'P326', 'P327', 'P328', 'P329', 'P330', 'P331', 'P332', 'P333', 'P334', 'P335',    
            'P336', 'P338', 'P341']

#subjects = ['P341']
#consider only block 1 to pinpoint novelty
rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
##trial_type = ['norisk']

feedback = ['positive', 'negative']
period_start = -1.750
period_end = 2.750
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/'
raw_name = '{0}/{0}_run{1}_mio_free.txt'

'''
extract cleaned events
'''
print('\trun mio_extraction...')
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare/', exist_ok = True)

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                rf = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_autists/Events_autists_test/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb) 
                if pathlib.Path(rf).exists() and os.stat(rf).st_size != 0:
                    call_clean_events(data_path, data_path_raw, raw_name, subj, r, cond, fb)
                else:
                    print('This file: ', rf, 'does not exit')

print('\tmio_extraction completed')
