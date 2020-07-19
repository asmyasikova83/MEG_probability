import mne, os
import numpy as np
import numpy.matlib
from configure import *

os.makedirs("baseline", exist_ok=True)
init()

with open("configure.py", "r") as f_in:
    settings = f_in.readlines()

def compute_baseline(raw_data, picks):
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    events = mne.pick_events(events_raw, include = [1])
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start, tmax = period_end, baseline = None, picks=picks, preload = True)
    epochs = epochs.pick(picks="grad")
    epochs_ar = epochs.get_data()
    epochs_ar = epochs_ar.swapaxes(0, 1)  
    epochs_ar = epochs_ar.swapaxes(1, 2) 
    baseline_chunk = epochs_ar[:, baseline_interval_start:baseline_interval_end,:]
    BASELINE = np.mean(np.mean(baseline_chunk, axis=1), axis=1)
    BASELINE = np.array(BASELINE)[np.newaxis]
    BASELINE = np.transpose(BASELINE)
    return BASELINE.transpose()

def correct_baseline(raw_data, picks, BASELINE):
    events = np.loadtxt('/home/sasha/MEG/MIO_cleaning/P001_run3_events.txt', dtype=int) #events of interest after MIO cleaning
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start, tmax = period_end, picks=picks, preload = True)
    epochs = epochs.pick(picks="grad")   
    epochs_ar = epochs.get_data()
    epochs_ar = epochs_ar.swapaxes(0, 1)  
    epochs_ar = epochs_ar.swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    
    RESH_DATA = epochs_ar.reshape(N_chans,  N_events*N_times)
    BASELINE = np.matlib.repmat(BASELINE, N_events*N_times, 1)
    print(N_events)

    BASELINE_CORRECTED_DATA = RESH_DATA - np.transpose(BASELINE)
    print(BASELINE_CORRECTED_DATA.shape)
    print(BASELINE_CORRECTED_DATA)
    return BASELINE_CORRECTED_DATA

raw_file = 'P001_run3_raw_tsss_mc.fif' #an example of data to be corrected
raw_data = mne.io.Raw(raw_file, preload=True)
picks = mne.pick_types(raw_data.info, meg = True)
          
    
BASELINE = compute_baseline(raw_data, picks)
BASELINE_CORRECTED_DATA = correct_baseline(raw_data, picks, BASELINE)

with open(f"baseline/{subj}_run{run[0]}_baseline_corrected.txt", "w") as ff:
    np.savetxt(ff, BASELINE_CORRECTED_DATA, fmt="%d")

