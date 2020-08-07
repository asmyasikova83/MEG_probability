import mne, os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from config import *

with open("config.py", "r") as f_in:
    settings = f_in.readlines()

def retrieve_events_for_baseline(raw_data, fpath_events, picks):
    events_with_cross = []
    events_of_interest = []
    #takes events with fixation cross followed by the events of interest (positive and negative feedback)
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset',
                                 consecutive='increasing', min_duration=0, shortest_event=1,
                                 mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    events_cleaned = np.loadtxt(fpath_events, dtype=int)
    # extract events with fixation cross followed by positive or negative feedback
    for i in range(len(events_raw)):
        # check the fixation cross
        if events_raw[i][2] == 1:
            str_digit1 = str(events_raw[i + 2][2])
            str_digit2 = str(events_raw[i + 3][2])
            d1 = [int(d) for d in str_digit1]
            d2 = [int(d) for d in str_digit2]
            for j in range(len(events_cleaned)):
            # check that then follows the response (starting with 4*)
            # if the timing of feedback in the events after learning is equal to that of in the set with fix cross
            # retrieve those feedback events and put them into  events_of_interest
            # also put the relevant fix cross events into events_with_cross  - we will need them for baseline
                if d1[0] == 4 and events_cleaned[j][0] == events_raw[i + 3][0]:
                    assert(events_cleaned[j][2] == events_raw[i + 3][2])
                    events_with_cross.append(events_raw[i])
                    events_of_interest.append(events_cleaned[j])
                elif d2[0] == 4 and events_cleaned[j][0] == events_raw[i + 4][0]:
                    assert(events_cleaned[j][2] == events_raw[i + 4][2])
                    events_with_cross.append(events_raw[i])
                    events_of_interest.append(events_cleaned[j])
                else:
                    print('Skip the event...')
                    continue
    return events_with_cross, events_of_interest

def reshape_epochs(raw_data, events, picks):
    #  retrieve epochs associated with the events of interest
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True)
    epochs = epochs.pick(picks="meg")
    epochs_ar = epochs.get_data()
    # reshape data for calculations -> 3D matrix with the dimensions of N_chans, N_times, N_events
    epochs_ar = epochs_ar.swapaxes(0, 1)  
    epochs_ar = epochs_ar.swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    return N_chans, N_times, N_events, epochs_ar

def create_mne_epochs_evoked(CORRECTED_DATA, events_of_interest, plot, raw, picks):
    #create an Epoch object from data array using info from raw_file, downsample it, creates and returnss evoked
    n_time_samps = raw.n_times
    time_secs = raw.times
    ch_names = raw.ch_names[0:306] #take grad + mag channels for further plotting
    #ch_names = raw.ch_names
    sfreq = raw.info['sfreq']
    # Channels: 204 grad, 102 mag
    ch_types = ['grad']*204 + ['mag']*102
    events = events_of_interest
    #data in shape (n_epochs, n_channels, n_times)
    epochs_data = CORRECTED_DATA
    # create info for the Epoch object
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    events = np.array(events)
    # don't forget to set a correct tminl (from config)!
    epochs = mne.EpochsArray(epochs_data, info=info, events=events, tmin = -2.000, baseline=None,
                         event_id = None)

    # downsample to 250 Hz
    epochs_resampled = epochs.copy().resample(250, npad='auto')
    evoked = epochs_resampled.average()
    # Plotting options for newly created epochs object, evoked, psd
    if plot:
        print('Plotting after baseline...')
        #plot epochs
        mne.viz.plot_epochs(epochs, picks=picks[0:204], scalings=None)
        #plot PSD
        #epochs.pick_types('grad').plot_psd(fmin = 4, fmax = 40, tmin= -2.000, tmax= 1.500, picks= 'grad', xscale= 'log', dB = True, estimate='power' )
        #evoked.plot_image()
        #plot topomap ERP
        #evoked.pick_types(meg=True).plot_topo(color='r', legend=False)
        plt.show()
    return evoked
		    
def compute_baseline(raw_data, events_with_cross, picks):
    # average each epoch with fixation cross followed by the events of interest
    # substract this average from the relevant epoch of interest
    # prepare data for numerical calculations for events_with_cross
    N_chans, N_times, N_events, epochs_ar = reshape_epochs(raw_data, events_with_cross, picks)
    assert(N_events == len(events_with_cross))
    BASELINE = np.zeros((N_events, N_chans))
    for i in range(N_events):
        #extract data for baseline computation for each event
        #baseline_interval_start = -350, baseline_interval_end = -50 from config
        baseline_chunk = epochs_ar[:, baseline_interval_start:baseline_interval_end, i]
        #baseline computation over the time samples in column data (axis=1)
        BASELINE[i, 0:N_chans] = np.mean(baseline_chunk, axis=1)
    # We need to operate on further data as of (204,2001), so we need to transpose BASELINE as of (2001,25)
    BASELINE = BASELINE.transpose()
    #return array of (N_chan, N_events) with averaged value over the baseline time interval
    return BASELINE

def correct_baseline(BASELINE, events_of_interest, raw_data, picks):
    # prepare data for numerical calculations for events_of_interest
    N_chans, N_times, N_events, epochs_ar = reshape_epochs(raw_data, events_of_interest, picks)
    assert(N_events == len(events_of_interest))
    #any data in shape (n_epochs, n_channels, n_times) can be used
    CD = (N_events,  N_chans, N_times)
    CORRECTED_DATA = np.zeros(CD)
    for i in range(N_events):
        # spread the baseline for current event over the time samples of the epoch -> 2D matrix of N chan, N_times
        BASELINE_CUR = np.matlib.repmat(BASELINE[:,i], N_times, 1)
        # we want to broadcast together epochs_ar[:, :, i] as of (204,2001) and BASELINE_CUR as of (2001,204)
        # so we need to transpose BASELINE_CUR
        BASELINE_CUR = BASELINE_CUR.transpose()
        #correct data in each event of interest
        CORRECTED_DATA_CUR = epochs_ar[:, :, i]  - BASELINE_CUR
        CORRECTED_DATA[i, :, :] = CORRECTED_DATA_CUR
    return CORRECTED_DATA
