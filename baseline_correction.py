import mne, os
import numpy as np
import numpy.matlib
from config import *

with open("config.py", "r") as f_in:
    settings = f_in.readlines()

def retrieve_events_for_baseline(raw_data, picks):
    #takes events with fixation cross followed by the events of interest (positive and negative feedback)
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset',
                                 consecutive='increasing', min_duration=0, shortest_event=1,
                                 mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    events_cleaned = np.loadtxt('/home/sasha/MEG/MIO_cleaning/P001_run3_mio_corrected_NEW.txt', dtype=int)
    # extract events with fixation cross followed by positive or negative feedback
    for i in range(len(events_raw)):
        # cross
        if events_raw[i][2] == 1:
            # check
            # ids of event of interet are located in i + 4
            assert(events_raw[i + 4][2] == 50 or
                   events_raw[i + 4][2] == 51 or
                   events_raw[i + 4][2] == 52 or
                   events_raw[i + 4][2] == 53)
            # look up thr
            for j in range(len(events_cleaned)):
                # timing
                if events_cleaned[j][0] == events_raw[i + 4][0]:
                    # check
                    assert(events_cleaned[j][2] == events_raw[i + 4][2])
                    # extract epoch with fix cross for baseline
                    events_with_cross.append(events_raw[i])
                    events_of_interest.append(events_cleaned[j])
                    
    print(events_with_cross)
    print(events_of_interest)
    return events_with_cross, events_of_interest

def reshape_epochs(raw_data, events):
    #  retrieve epochs associated with the events of interest
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True)
    # prepare data for numerical calculations
    epochs = epochs.pick(picks="grad")
    epochs_ar = epochs.get_data()
    # reshape data for calculations -> 3D matrix with the dimensions of N_chans, N_times, N_events
    epochs_ar = epochs_ar.swapaxes(0, 1)  
    epochs_ar = epochs_ar.swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    return N_chans, N_times, N_events, epochs_ar
		    
def compute_baseline(events_with_cross, events_of_interest, raw_data, picks):
    # average each epoch with fixation cross followed by the events of interest
    # substract this average from the relevant epoch of interest
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset',
                                 consecutive='increasing', min_duration=0, shortest_event=1,
                                 mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    
    # prepare data for numerical calculations for events_with_cross
    N_chans, N_times, N_events, epochs_ar = reshape_epochs(raw_data, events_with_cross)
    assert(N_events == len(events_with_cross))
    BASELINE = np.zeros((N_events, N_chans))
    for i in range(N_events):
        #extract data for baseline computation for each event
        baseline_interval_start = -350
        baseline_interval_end = -50
        baseline_chunk = epochs_ar[:, baseline_interval_start:baseline_interval_end, i]
        #baseline computation over the time samples in column data (axis=1)
        BASELINE[i, 0:N_chans] = np.mean(baseline_chunk, axis=1)
    # We need to operate on further data as of (204,2001), so we need to transpose BASELINE as of (2001,25)
    BASELINE = BASELINE.transpose()
    #return array of (N_chan, N_events) with averaged value over the baseline time interval
    return BASELINE

def correct_baseline(BASELINE, events_of_interest, raw_data, picks):
    # for results
    f_name = "P001_run3_baseline_corrected_epoch_ev{}.txt"

    # prepare data for numerical calculations for events_of_interest
    N_chans, N_times, N_events, epochs_ar = reshape_epochs(raw_data, events_of_interest)
    assert(N_events == len(events_of_interest))
    for i in range(N_events):
        # spread the baseline for current event over the time samples of the epoch -> 2D matrix of N chan, N_times
        BASELINE_CUR = np.matlib.repmat(BASELINE[:,i], N_times, 1)
        # we want to broadcast together epochs_ar[:, :, i] as of (204,2001) and BASELINE_CUR as of (2001,204)
        # so we need to transpose BASELINE_CUR
        BASELINE_CUR = BASELINE_CUR.transpose()
        #correct data in each event of interest
        CORRECTED_DATA_CUR = epochs_ar[:, :, i]  - BASELINE_CUR
        CORRECTED_DATA_file = open(f_name.format(i), "w")
        np.savetxt(CORRECTED_DATA_file, CORRECTED_DATA_CUR, fmt="%e")
        CORRECTED_DATA_file.close()

#an example of data to be corrected
raw_file = '/home/sasha/MEG/MIO_cleaning/P001_run3_raw_tsss_mc.fif' 
raw_data = mne.io.Raw(raw_file, preload=True)
picks = mne.pick_types(raw_data.info, meg = True)

events_with_cross = []
events_of_interest = []

events_with_cross, events_of_interest = retrieve_events_for_baseline(raw_data, picks)

BASELINE = compute_baseline(events_with_cross, events_of_interest, raw_data, picks)
correct_baseline(BASELINE, events_of_interest, raw_data, picks)

