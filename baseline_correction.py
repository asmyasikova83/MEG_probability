import mne, os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from config import *
from mne.time_frequency import tfr_morlet, psd_multitaper

with open("config.py", "r") as f_in:
    settings = f_in.readlines()

def retrieve_events_for_baseline(conf, raw_data, fpath_events, kind, subject, run, picks):
    prefix_out = conf.prefix_out
    events_with_cross = []
    events_of_interest = []
    #takes events with fixation cross followed by the events of interest (positive and negative feedback)
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset',
                                 consecutive='increasing', min_duration=0, shortest_event=1,
                                 mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    print('fpath_events', fpath_events)
    events_cleaned = np.loadtxt(fpath_events, dtype=int)
    print(kind)
    print('events cl')
    print(events_cleaned)
    print(events_raw)
    if kind == 'negative' or kind ==  'positive':
        p = 3
    if kind == 'prerisk' or kind == 'risk' or kind == 'postrisk' or kind == 'norisk' or kind == 'fb_negative_norisk' or kind == 'fb_positive_norisk' or kind == 'fb_negative_risk' or kind == 'fb_positive_risk' or  kind == 'risk_fb_negative' or kind == 'risk_fb_positive':
        # kind == 'norisk_fb_negative' or kind == 'norisk_fb_positive'
        if stim:
            p = 1
        if response:
            p = 2
    # extract events with fixation cross followed by positive or negative feedback
    for i in range(len(events_raw)):
        for j in range(len(events_cleaned)):
            # check the fixation cross and find the response after the fix cross
            if events_raw[i][2] == 1:
                str_digit1 = str(events_raw[i + 2][2])
                str_digit2 = str(events_raw[i + 3][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                if d1[0] == 4:
                    factor = 'k'
                    if factor == 'k' and events_cleaned.shape != (3,) and events_cleaned[j][0] == events_raw[i + p][0]:
                        assert(events_cleaned[j][2] == events_raw[i + p][2])
                        if baseline == 'fixation_cross_general':
                            events_with_cross.append(events_raw[i])
                        events_of_interest.append(events_cleaned[j])
                        print('extracting event of interest', events_cleaned[j])
                    elif factor == 'k' and events_cleaned.shape == (3,) and events_cleaned[j] == events_raw[i + p][0]:
                        assert(events_cleaned[2] == events_raw[i + p][2])
                        if baseline == 'fixation_cross_general':
                            events_with_cross.append(events_raw[i])
                        events_of_interest.append(events_cleaned)
                        print('extracting event of interest', events_cleaned[j])
                    else:
                        continue
                if d2[0] == 4:
                    factor = 'l'
                    if factor == 'l' and events_cleaned.shape != (3,) and events_cleaned[j][0] == events_raw[i + p + 1][0]:
                        assert(events_cleaned[j][2] == events_raw[i + p + 1][2])
                        if baseline == 'fixation_cross_general':
                            events_with_cross.append(events_raw[i])
                        events_of_interest.append(events_cleaned[j])
                        print('extracting event of interest', events_cleaned[j])
                    elif factor == 'l' and events_cleaned.shape == (3,) and events_cleaned[j] == events_raw[i + p + 1][0]:
                        assert(events_cleaned[2] == events_raw[i + p + 1][2])
                        if baseline == 'fixation_cross_general':
                            events_with_cross.append(events_raw[i])
                        events_of_interest.append(events_cleaned)
                        print('extracting event of interest', events_cleaned[j])
                    else:
                        continue
    if baseline == 'fixation_cross_norisks':
        fpath_events = f'{prefix_out}/{mio_dir}/mio_out_norisk/{subject}_run{run}_mio_corrected_norisk.txt'
        print('fpath events norisk', fpath_events)
        events_cleaned = np.loadtxt(fpath_events, dtype=int)
        print('baseline fix cross norisks')
        print(events_cleaned)
        print(events_raw)
        p = 2
        for i in range(len(events_raw)):
            for j in range(len(events_cleaned)):
                #check the fixation cross and the type of response after it: supposed to be norisk
                if events_raw[i][2] == 1:
                    str_digit1 = str(events_raw[i + 2][2])
                    str_digit2 = str(events_raw[i + 3][2])
                    d1 = [int(d) for d in str_digit1]
                    d2 = [int(d) for d in str_digit2]
                    if d1[0] == 4 and d1[1] == 0 or d1[0] == 4 and d1[1] == 1 or d1[0] == 4 and d1[1] == 6 or d1[0] == 4 and d1[1] == 7:
                        #pick out fix cross preceding norisks
                        factor = 'm'
                        #events_with_cross, events_of_interest = pick_events(i, j, factor, events_raw, events_cleaned, kind)
                        if factor == 'm' and events_cleaned.shape != (3,) and events_cleaned[j][0] == events_raw[i + p][0]:
                            assert(events_cleaned[j][2] == events_raw[i + p][2])
                            events_with_cross.append(events_raw[i])
                            print('ev with cross found')
                            print('1')
                            print(events_with_cross)
                        elif factor == 'm' and events_cleaned.shape == (3,) and events_cleaned[j] == events_raw[i + p][0]:
                            assert(events_cleaned[2] == events_raw[i + p][2])
                            events_with_cross.append(events_raw[i])
                            print('ev with cross found')
                            print('2')
                            print(events_with_cross) 
                        else:
                            continue
                if events_raw[i][2] == 1:
                    str_digit1 = str(events_raw[i + 2][2])
                    str_digit2 = str(events_raw[i + 3][2])
                    d1 = [int(d) for d in str_digit1]
                    d2 = [int(d) for d in str_digit2]
                    if d2[0] == 4 and d2[1] == 0 or d2[0] == 4 and d2[1] == 1 or d2[0] == 4 and d2[1] == 6 or d2[0] == 4 and d2[1] == 7:
                        factor = 'n'
                        #events_with_cross, events_of_interest = pick_events(i, j, factor, events_raw, events_cleaned, kind)
                        if factor == 'n' and events_cleaned.shape != (3,) and events_cleaned[j][0] == events_raw[i + p + 1][0]:
                            assert(events_cleaned[2] == events_raw[i + p + 1][2])
                            events_with_cross.append(events_raw[i])
                        elif factor == 'n' and events_cleaned.shape == (3,) and events_cleaned[j] == events_raw[i + p + 1][0]:
                            assert(events_cleaned[2] == events_raw[i + p + 1][2])
                            events_with_cross.append(events_raw[i])
                        else:
                            continue
    print('ev of interest2')
    print(events_of_interest)
    print('events_with_cross', events_with_cross)
    print('events_of interest', events_of_interest)
    print('\nevents_for_baseline retrieved\n')
    return events_with_cross, events_of_interest

def reshape_epochs(conf, raw_data, events, picks):
    period_start = conf.period_start
    period_end = conf.period_end
    #  retrieve epochs associated with the events of interest
    print('events', events)
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True)
    #epochs = epochs.pick(picks="meg")
    epochs_ar = epochs.get_data()
    # reshape data for calculations -> 3D matrix with the dimensions of N_chans, N_times, N_events
    epochs_ar = epochs_ar.swapaxes(0, 1)
    epochs_ar = epochs_ar.swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    return N_chans, N_times, N_events, epochs_ar

def create_mne_epochs_evoked(conf, kind, subject, run, CORRECTED_DATA, events_of_interest, plot, raw, picks):
    #create an Epoch object from data array using info from raw_file, downsample it, creates and returns evoked
    #data in shape (n_epochs, n_channels, n_times)
    period_start = conf.period_start
    period_end = conf.period_end
    epochs_data = CORRECTED_DATA
    # create info for the Epoch object
    info = raw.info
    meg_indices = mne.pick_types(info, meg='grad')
    reduced_info = mne.pick_info(info, meg_indices)
    print(events_of_interest)
    print('subj', subject)
    print('run', run)
    print('CORR DATA shape', CORRECTED_DATA.shape)
    if kind == 'both':
    #explore reinforcement data with both pos and neg feedback
        if subject == 'P005' and run == '1' or subject == 'P003' and run == '1' or subject == 'P003' and run == '3' or subject == 'P004' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 52, 53])
        elif subject == 'P005' and run == '2' or subject == 'P003' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 53])
        elif subject == 'P005' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 53])
        elif subject == 'P005' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 53])
        elif subject == 'P005' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 53])
        elif subject == 'P003' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 52, 53])
        elif subject == 'P004' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 53])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 51, 52, 53])
    if kind == 'positive':
    #explore data with positive feedback
        if subject == 'P005' and run == '1' or subject == 'P003' and run == '1' or subject == 'P003' and run == '3' or subject == 'P004' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P005' and run == '2' or subject == 'P003' and run == '2' or subject == 'P016' and run == '4' or subject == 'P023' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P005' and run == '3' or subject == 'P009' and run == '1' or subject == 'P016' and run == '1' or subject == 'P014' and run == '4' :
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P005' and run == '4' or subject == 'P021' and run == '1' or subject == 'P014' and run == '2' or subject == 'P011' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P005' and run == '5' or subject == 'P018' and run == '2' or subject == 'P008' and run == '3' or subject == 'P007' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P003' and run == '5' or subject == 'P021' and run == '2' or subject == 'P007' and run == '3' or subject == 'P009' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P004' and run == '5' or subject == 'P009' and run == '3' or subject == 'P014' and run == '3' or subject == 'P016' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50])
        elif subject == 'P025' and run == '4' or subject == 'P008' and run == '5' or subject == 'P009' and run == '5' or subject == 'P014' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50] )
        elif subject == 'P020' and run == '5' or subject == 'P025' and run == '5' or subject == 'P023' and run == '5' or subject == 'P007' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50] )
        elif subject == 'P009' and run == '6' or subject == 'P025' and run == '5' or subject == 'P023' and run == '5' or subject == 'P007' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50] )
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [50, 51])
    if kind == 'negative':
    #explore data with negative feedback
        if subject == 'P005' and run == '1' or subject == 'P003' and run == '1' or subject == 'P003' and run == '3' or subject == 'P004' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [52, 53])
        elif subject == 'P005' and run == '2' or subject == 'P003' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [53])
        elif subject == 'P005' and run == '3' or subject == 'P009' and run == '3' or subject == 'P007' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [53])
        elif subject == 'P005' and run == '4' or subject == 'P009' and run == '4' or subject == 'P016' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [53])
        elif subject == 'P005' and run == '5' or subject == 'P009' and run == '5' or subject == 'P014' and run == '5' or subject == 'P025' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [53])
        elif subject == 'P003' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [52, 53])
        elif subject == 'P004' and run == '5':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [53])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [52, 53])
    if stim == False and kind == 'prerisk':
        if subject == 'P003' and run == '1' or subject == 'P004' and run == '1' or subject == 'P029' and run == '4' or subject == 'P017' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P045' and run == '3' or subject == 'P046' and run == '2' or subject == 'P055' and run == '3' or subject == 'P059' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif  subject == 'P062' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P048' and run == '1' or subject == 'P053' and run == '4': 
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46])
        elif subject == 'P051' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 47])
        elif subject == 'P005'and run == '1' or subject == 'P003' and run == '2' or subject == 'P003' and run == '3' or subject == 'P016' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47])
        elif subject == 'P048'and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47])
        elif subject == 'P059'and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        elif subject == 'P051'and run == '6' or subject == 'P057'and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46, 47])
        elif subject == 'P052'and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        elif subject == 'P055'and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P006'and run == '1' or subject == 'P011' and  run =='4' or subject == 'P042' and run == '1' or subject == 'P031' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46])
        elif subject == 'P007' and run == '1' or subject == 'P009' and run == '1' or subject == 'P011' and run == '1' or subject == 'P024' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P008' and run == '1' or subject == 'P014' and run == '6' or subject == 'P050' and run == '1' or subject == 'P059' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        elif subject == 'P052' and run == '1' or subject == 'P053' and run == '1' or subject == 'P052' and run == '4' or subject == 'P052' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P018' and run == '1' or subject == 'P017' and run =='4' or subject == 'P023' and run == '4' or subject == 'P048' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        elif subject == 'P021' and run == '1' or subject == 'P008' and run == '2' or subject == 'P018' and run == '2' or subject == 'P021' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 47])
        elif subject == 'P025' and run == '1' or subject == 'P032' and run == '1' or subject == 'P041' and run == '2' or subject == 'P035' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P029' and run == '1' or subject == 'P022' and run == '2' or subject == 'P023' and run == '2' or subject == 'P021' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P045' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P007' and run == '2' or subject == 'P011' and run == '2' or subject == 'P015' and run == '2' or subject == 'P017' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P014' and run =='2' or subject == 'P007' and run =='3' or subject == 'P008' and run == '3' or subject == 'P014' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41])
        elif subject == 'P016' and run == '2' or subject == 'P025' and run == '3' or subject =='P039' and run == '3' or subject == 'P040' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P017' and run == '2'  or subject == 'P003' and run =='4' or subject == 'P042' and run == '3' or subject == 'P059' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40])
        elif subject == 'P029' and run == '2' or subject == 'P028' and run == '4' or subject == 'P011' and run == '6' or subject == 'P046' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        elif subject == 'P019' and run == '3' or subject == 'P021' and run == '3' or subject == 'P022' and run == '6' or subject == 'P032' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47, 46])
        elif subject == 'P014' and run == '4' or subject == 'P034' and run == '2' or subject == 'P036' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41])
        elif subject == 'P018' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47, 46])
        elif subject == 'P021' and run == '6' or subject == 'P039' and run == '4' or subject == 'P015' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 47])
        elif subject == 'P030' and run == '2' or subject == 'P029' and run == '3' or subject == 'P006' and run == '4' or subject == 'P050' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 47])
        elif subject == 'P011' and run == '3' or subject == 'P034' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 47])
        elif subject == 'P023' and run == '3' or subject == 'P030' and run == '3' or subject == 'P018' and run == '4' or subject == 'P044' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P004' and run == '4'or subject == 'P008' and run == '4' or subject == 'P037' and run == '2' or subject == 'P048' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47])
        elif subject == 'P020' and run == '4' or subject == 'P059' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P025' and run == '4' or subject == 'P007' and run == '6' or subject == 'P009' and run == '6' or subject == 'P041' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41])
        elif subject == 'P005' and run == '6' or subject == 'P032' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        elif subject == 'P028' and run =='6' or subject == 'P034' and run == '4' or subject == 'P043' and run == '4' or subject == 'P044' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P036' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P036' and run == '2' or subject == 'P039' and run == '2' or subject == 'P032' and run == '4' or subject == 'P041':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46])
        elif subject == 'P044' and run == '3' or subject == 'P031' and run == '6' or subject == 'P051' and run == '2' or subject == 'P053' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P043' and run == '3'or subject == 'P047' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P035' and run == '4' or subject == 'P032' and run == '6' or subject == 'P055' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47, 46])
        elif subject == 'P037' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46, 47])
    if stim == False and kind == 'risk':
        if subject == 'P003' and run == '1' or subject == 'P009' and run == '1' or subject == 'P021' and run == '1' or subject == 'P008' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P014' and run == '2' or subject == 'P017' and run == '2' or subject == 'P018' and run == '2' or subject == 'P021' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P004' and run == '1' or subject == 'P011' and run == '1' or subject == 'P016' and run == '2' or subject == 'P029' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P006' and run == '1' or subject == 'P023' and run == '2' or subject == 'P030' and run == '2' or subject == 'P007' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        elif subject == 'P008' and run == '1' or subject == 'P025' and run == '1' or subject == 'P011' and run == '2' or subject == 'P015' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 45])
        elif subject == 'P016' and run == '1' or subject == 'P003' and run == '3' or subject == 'P020' and run == '4' or subject == 'P025' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P018' and run == '1' or subject == 'P018' and run == '4' or  subject == 'P053' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44])
        elif subject == 'P024' and run == '1' or subject == 'P029' and run == '1' or subject == 'P003' and run == '3' or subject == 'P011' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44])
        elif subject == 'P022' and run =='2' or subject == 'P008' and run == '3' or subject == 'P014' and run == '3' or subject == 'P018' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P048' and run =='1' or subject == 'P047' and run =='3' or subject == 'P048' and run =='3' or subject == 'P055' and run =='4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 45])
        elif subject == 'P050' and run =='1' or subject == 'P059' and run =='1' or subject == 'P051' and run =='4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])

        elif subject == 'P003' and run == '3' or subject == 'P016' and run == '3' or subject == 'P003' and run == '4' or subject == 'P017' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P044' and run == '2' or subject == 'P046' and run == '2' or subject == 'P048' and run == '2' or subject == 'P045' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P052' and run == '1':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 42])
        elif subject == 'P006' and run == '3' or subject == 'P025' and run == '3' or subject == 'P030' and run == '3' or subject == 'P042' and run == '1':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 45])
        elif subject == 'P015' and run == '3' or subject == 'P039' and run == '4':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44])
        elif  subject == 'P059' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 42])
        elif subject == 'P017' and run == '3' or subject == 'P021' and run == '3' or subject == 'P014' and run == '6' or subject == 'P022' and run =='6':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P019' and run == '3' or subject == 'P028' and run == '3' or subject == 'P006' and run == '4' or subject == 'P014' and run == '4':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P023' and run == '3' or subject == 'P029' and run == '4' or subject == 'P028' and run == '6' or subject == 'P062' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 45])
        elif subject == 'P004' and run == '4' or subject == 'P011'  and run == '4' or subject == 'P007' and run == '6':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        elif subject == 'P052' and run == '4':
              epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P021' and run == '4' or subject == 'P031' and run == '6' or subject == 'P053' and run == '4':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 45])
        elif subject == 'P023' and run == '4' or subject == 'P028' and run == '4' or subject == 'P011' and run == '6' or subject == 'P017' and run == '6':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P036' and run == '1' or subject == 'P044' and run == '1' or subject == 'P031' and run == '2' or subject == 'P041' and run == '2':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P006' and run== '6' or subject == 'P021' and run == '6' or subject == 'P040' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 45])
        elif subject == 'P032' and run == '2' or subject == 'P050' and run == '2':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P036' and run == '2':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        elif subject == 'P032' and run == '3' or subject == 'P055' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44])
        elif subject == 'P035' and run == '3' or subject == 'P043' and run == '3' or subject == 'P032' and run == '4' or subject == 'P059' and run == '4':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P059' and run == '2':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 45])
        elif subject == 'P042' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 45])
        elif subject == 'P044' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43])
        elif subject == 'P033' and run == '4' or subject == 'P035' and run == '4' or subject == 'P034' and run == '6':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P034'and run == '4' or subject == 'P043' and run == '4' or subject == 'P050' and run == '2' or  subject == 'P052' and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 44])
        elif subject == 'P051'and run == '3':
             epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P036' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 44, 45])
    if stim == False and kind == 'postrisk':
        if subject == 'P003' and run == '1' or subject == 'P004' and run == '1' or subject == 'P008' and run == '1' or subject == 'P018' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P005' and run == '1' or subject == 'P017' and run == '2' or subject == 'P014' and run == '3' or subject == 'P005' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47])
        elif subject == 'P045' and run == '6' or subject == 'P051' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P006' and run == '1' or subject == 'P014' and run == '2' or subject == 'P003' and run == '3' or subject == 'P007' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40])
        elif subject == 'P007' and run == '1' or subject == 'P011' and run == '1' or subject == 'P007' and run == '2' or subject == 'P059' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P055' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P009' and run == '1' or subject == 'P015' and run == '2' or subject == 'P016' and run == '2' or subject == 'P006' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P016' and run == '1' or subject == 'P022' and run == '2' or subject == 'P023' and run == '2' or subject == 'P048' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P021' and run == '1' or subject == 'P008' and run == '2' or subject == 'P018' and run == '2' or subject == 'P006' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P024' and run == '1' or subject == 'P044' and run == '1' or subject == 'P059' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 47])
        elif subject == 'P025' and run == '2' or subject == 'P011' and run == '2' or subject == 'P029' and run == '2' or subject == 'P014' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P029' and run == '1' or subject == 'P039' and run == '3' or subject == 'P046' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        elif subject == 'P021' and run == '2' or subject == 'P030' and run == '2' or subject == 'P003' and run == '4' or subject == 'P031' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P008' and run == '3' or subject == 'P011' and run == '3' or subject == 'P021' and run == '3' or subject == 'P011' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 47])
        elif subject == 'P015' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40])
        elif subject == 'P017' and run == '3' or subject == 'P004' and run == '4' or subject == 'P008' and run == '4' or subject == 'P017' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41])
        elif subject == 'P018' and run == '3' or subject == 'P030' and run == '3' or subject == 'P018' and run  == '4' or subject == 'P021' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40,41, 46])
        elif subject == 'P019' and run == '3' or subject == 'P023' and run == '3' or subject == 'P028' and run == '3' or subject == 'P006' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40,41])
        elif subject == 'P043' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        elif subject == 'P050' and run == '1' or subject == 'P059' and run == '1' or subject == 'P048' and run == '2' or subject == 'P050' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P052' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P014' and run == '4' or subject == 'P053' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46, 47])
        elif subject == 'P020' and run == '4' or subject == 'P023' and run == '4' or subject == 'P017' and run == '6' or subject == 'P022' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P025' and run == '4' or subject == 'P009' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        elif subject == 'P028'and run == '4' or subject == 'P035' and run == '3' or subject == 'P051' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41])
        elif subject == 'P029' and run == '4' or subject == 'P030' and run == '4' or subject == 'P044' and run == '2' or subject == 'P042' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P007' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47])
        elif subject == 'P031' and run == '6' or subject == 'P041'and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 47])
        elif subject == 'P011' and run == '6' or subject == 'P028' and run == '6' or subject == 'P034' and run == '6' or subject == 'P045' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        elif subject == 'P021' and run == '6' or subject == 'P040' and run == '3' or subject == 'P052' and run == '2' or subject == 'P052' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46])
        elif subject == 'P036' and run == '1' or subject == 'P041' and run == '6' or subject == 'P052' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40])
        elif subject == 'P032' and run == '2' or subject == 'P036' and run == '3' or subject == 'P044' and run == '3' or subject == 'P039' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P032' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P032' and run == '4' or subject == 'P053' and run == '2'or  subject == 'P051' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P033'and run == '4' or subject == 'P034' and run == '4' or subject == 'P059' and run == '3' or subject == 'P062' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P035' and run == '4' or subject == 'P043' and run == '4' or subject == 'P044' and run == '4' or subject == 'P040' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P032' and run == '6' or subject == 'P055' and run == '2' or subject == 'P059' and run == '2' or subject == 'P048' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif  subject == 'P055' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif  subject == 'P055' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46])
        elif  subject == 'P057' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46, 47])
    if stim == False and kind == 'norisk':
        if subject == 'P003' and run == '1' or subject == 'P032' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P006' and run == '1' or subject == 'P040' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40])
        elif subject == 'P016' and run == '1' or subject == 'P018' and run == '1' or subject == 'P025' and run == '1' or subject == 'P042' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P019' and run == '3' or subject == 'P021' and run == '3' or subject == 'P006' and run == '4' or subject == 'P017' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P021' and run == '4' or subject == 'P006' and run == '6' or subject == 'P017' and run == '6' or subject == 'P022' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P021' and run == '6' or subject == 'P014' and run == '6' or subject == 'P040' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P032' and run == '6' or subject == 'P039' and run == '1' or subject == 'P039' and run == '3' or subject == 'P043' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P055' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P052' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46, 47])
    if stim == False and kind == 'norisk_fb_positive':
        if subject == 'P040' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
    if stim == False and kind == 'norisk_fb_negative':
        if subject == 'P003' and run == '1' or subject == 'P018' and run == '1' or subject == 'P042' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [47])
        elif subject == 'P019' and run == '3' or subject == 'P021' and run == '3' or subject == 'P006' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        elif subject == 'P017' and run == '4' or subject == 'P043' and run == '4' or subject == 'P006' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        elif subject == 'P017' and run == '4' or subject == 'P017' and run == '6' or subject == 'P022' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46])
        elif subject == 'P005' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46, 47])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46, 47])
    if stim == False and kind == 'risk_fb_positive':
        if subject == 'P008' and run == '1' or subject == 'P011' and run == '3' or subject == 'P023' and run == '3' or subject == 'P030' and run == '3':
           epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43])
        elif subject == 'P014' and run == '6':
           epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42])
        else:
           epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43])
    if stim == False and kind == 'risk_fb_negative':
        if subject == 'P003' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P016' and run == '1' or subject == 'P024' and run == '1' or subject == 'P029' and run == '1' or subject == 'P039' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P011' and run == '3' or subject == 'P018' and run == '4' or subject == 'P020' and run == '4' or subject == 'P034' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P030' and run == '2' or subject == 'P036' and run == '2' or subject == 'P040' and run == '3' or subject == 'P011' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        elif subject == 'P021' and run == '4' or subject == 'P006' and run == '6' or subject == 'P028' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
    if stim == False and kind == 'fb_negative_norisk':#kind == 'norisk_fb_positive'
        if subject == 'P042' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 47])
        elif subject == 'P039' and run == '3' or subject == 'P020' and run == '4' or subject == 'P021' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        elif subject == 'P021' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46])
        elif subject == 'P015' and run == '2' or subject == 'P023' and run == '3' or subject == 'P034' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41])
        elif subject == 'P029' and run == '2' or subject == 'P032' and run == '2' or subject == 'P037' and run == '2' or subject == 'P018' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P016' and run == '2' or subject ==  'P023' and run == '2' or subject == 'P037' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P030' and run == '2' or subject == 'P017' and run == '3' or subject == 'P019' and run == '3' or subject == 'P032' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 40])
        elif subject == 'P006'and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P005'and run == '6' or subject == 'P011' and run == '6' or subject == 'P017' and run == '6' or subject == 'P041' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        elif subject == 'P007' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 47])
        elif subject == 'P039' and run == '1' or subject == 'P007' and run == '6' or subject == 'P011' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [46, 47])
        elif subject == 'P017' and run == '4' or subject == 'P035' and run == '4' or subject == 'P006' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P044' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 47])
        elif subject == 'P043' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P029' and run == '1' or subject == 'P043' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P018' and run == '2' or subject == 'P029' and run == '3' or subject == 'P030' and run == '3' or subject == 'P043' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        elif subject == 'P042' and run == '1' or subject == 'P029' and run == '4' or subject == 'P030' and run == '4' or subject == 'P033' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P009' and run == '1' or subject == 'P018' and run == '1' or subject == 'P032' and run == '1' or subject == 'P036' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P003' and run == '1' or subject == 'P016' and run == '1' or subject == 'P024' and run == '1' or subject == 'P042' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        elif subject == 'P044' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46, 47])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46, 47])
    if stim == False and kind == 'fb_negative_risk': #kind == 'risk_fb_negative'
        if subject == 'P003' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P034' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44])
        elif subject == 'P028' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 45])
        elif subject == 'P008' and run == '1' or subject == 'P032' and run == '1' or subject == 'P015' and run == '2' or subject == 'P040' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 45])
        elif subject == 'P032' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43])
        elif  subject == 'P029' and run == '3' or subject == 'P014' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 45])
        elif subject == 'P035' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P016' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P029' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44])
        elif subject == 'P006' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 45])
        elif subject == 'P016' and run == '1' or subject == 'P024' and run == '1' or subject == 'P029' and run == '1' or subject == 'P039' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P011' and run == '3' or subject == 'P018' and run == '4' or subject == 'P020' and run == '4' or subject == 'P034' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P030' and run == '2' or subject == 'P036' and run == '2' or subject == 'P040' and run == '3' or subject == 'P011' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        elif subject == 'P021' and run == '4' or subject == 'P028' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
    if stim == False and kind == 'fb_positive_norisk':
        if subject == 'P003' and run == '1' or subject == 'P008' and run == '1' or subject == 'P016' and run == '1' or subject == 'P018' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P032' and run == '1' or subject == 'P042' and run == '1' or subject == 'P020' and run == '4' or subject == 'P040' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 47])
        elif subject == 'P009' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [41, 46, 47])
        elif subject == 'P039' and run == '1' or subject == 'P019' and run == '3' or subject == 'P006' and run == '3' or subject == 'P017' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P018' and run == '4' or subject == 'P021' and run == '4' or subject == 'P037' and run == '4' or subject == 'P006' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P043' and run == '4' or subject == 'P006' and run == '4' or subject == 'P022' and run == '6' or subject == 'P032' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46])
        elif subject == 'P006' and run == '1' or subject == 'P014' and run == '6' or subject == 'P021' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41])
        elif subject == 'P040' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 46])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [40, 41, 46, 47])
    if stim == False and kind == 'fb_positive_risk':
        if subject == 'P003' and run == '1' or subject == 'P009' and run == '1' or subject == 'P021' and run == '1' or subject == 'P036' and run == '1':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P004' and run == '1' or subject == 'P011' and run == '1' or subject == 'P032' and run == '2' or subject == 'P044' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P011' and run == '1' or subject == 'P016' and run == '1' or subject == 'P020' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44])
        elif subject == 'P030' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44, 45])
        elif subject == 'P030' and run == '2' or subject == 'P036' and run == '3' or subject == 'P035' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [45])
        elif subject == 'P011' and run == '3' or subject == 'P015' and run == '3' or subject == 'P030' and run == '3' or subject == 'P042' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44])
        elif subject == 'P024' and run == '1' or subject == 'P039' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44])
        elif subject == 'P018' and run == '1' or subject == 'P018' and run == '4' or subject == 'P014' and run == '6' or subject == 'P022' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 44])
        elif subject == 'P008' and run == '2' or subject == 'P014' and run == '2' or subject == 'P015' and run == '2' or subject == 'P016' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P018' and run == '2' or subject == 'P021' and run == '2' or subject == 'P022' and run == '2' or subject == 'P029' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P021' and run == '3' or subject == 'P028' and run == '3' or  subject == 'P035' and run == '3' or subject == 'P033' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P041' and run == '2' or subject == 'P017' and run == '3' or subject == 'P018' and run == '3' or subject == 'P019' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P023' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 45])
        elif subject == 'P011' and run == '2':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 45])
        elif subject == 'P043' and run == '3' or subject == 'P023' and run == '4' or subject == 'P006' and run == '4' or subject == 'P017' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [44, 45])
        elif subject == 'P032' and run == '1' or subject == 'P043' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 44])
        elif subject == 'P007' and run == '1' or subject == 'P034' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 44])
        elif subject == 'P008' and run == '1' or subject == 'P042' and run == '1' or subject == 'P029' and run == '3' or subject == 'P006' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 44, 45])
        elif subject == 'P035' and run == '3' or subject == 'P021' and run == '6' or subject == 'P006' and run == '6':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [43, 45])
        elif subject == 'P044' and run == '3':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43])
        elif subject == 'P021' and run == '4':
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 45])
        else:
            epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [42, 43, 44, 45])
    if stim == True:
        epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest, tmin=period_start, baseline=None, event_id= [11])
    # downsample to 250 Hz
    epochs_of_interest = epochs.copy().resample(250, npad='auto')
    evoked = epochs_of_interest.average()
    print('ep of interest', epochs_of_interest)

    # plotting options for newly created epochs object, evoked, psd
    if plot:
        print('Plotting after baseline...')
        #plot epochs
        mne.viz.plot_epochs(epochs, picks=picks[0:204], scalings=None)
        #plot PSD
        #epochs.pick_types('grad').plot_psd(fmin = 4, fmax = 40, tmin= -2.000, tmax= 1.500, picks= 'grad', xscale= 'log', dB = True, estimate='power' )
        #evoked.plot_image()
        #plot topomap ERP
        #evoked.pick_types(meg=True).plot_topo(color='r', legend=False)
        evoked.plot_topomap(ch_type='mag', title='mag (original)', time_unit='s')
        plt.show()
        exit()
    return epochs_of_interest, evoked

def plot_epochs_with_without_BASELINE(events_of_interest, epochs_of_interest_w_BASELINE, raw_data, picks):
    epochs_of_interest_out_BASELINE = mne.Epochs(raw_data, events_of_interest, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True)
    title=' Before baseline'
    mne.viz.plot_epochs(epochs_of_interest_out_BASELINE, picks=picks[0:204], title=title, scalings=None)
    title=' After baseline'
    mne.viz.plot_epochs(epochs_of_interest_w_BASELINE, picks=picks[0:204], title=title, scalings=None)
    plt.show()
    exit()

def compute_baseline_substraction_and_power(conf, raw_data, events_with_cross, events_of_interest, picks):
    # average each epoch with fixation cross followed by the events of interest
    # substract this average from the relevant epoch of interest
    # prepare data for numerical calculations for events_with_cross
    period_start = conf.period_start
    period_end = conf.period_end
    N_chans, N_times, N_events, epochs_ar = reshape_epochs(conf, raw_data, events_with_cross, picks)
    N_chan_interests, N_times_interest, N_events_interest, epochs_ar_interest = reshape_epochs(conf, raw_data, events_of_interest, picks)
    assert(N_events == len(events_with_cross))
    BASELINE = np.zeros((N_events, N_chans))
    for i in range(N_events):
        #extract data for baseline computation for each event
        #baseline_interval_start = -350, baseline_interval_end = -50 from config
        baseline_chunk = epochs_ar[:, baseline_interval_start_sub:baseline_interval_end_sub, i]
        #baseline computation over the time samples in column data (axis=1)
        BASELINE[i, 0:N_chans] = np.mean(baseline_chunk, axis=1)
    if baseline == 'fixation_cross_norisks':
        #adjust the num ov events to that of events_of_interest
        NEW_BASELINE = np.mean(BASELINE, axis=0)
        #add new dim according to events_of_interest
        BASELINE = np.tile(NEW_BASELINE, (N_events_interest, 1))
    # We need to operate on further data as of (204,2001), so we need to transpose BASELINE as of (2001,25)
    BASELINE = BASELINE.transpose()
    #compute baseline II for power correction: mean  picks = picks!
    epochs_with_cross = mne.Epochs(raw_data, events_with_cross, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True)
    #epochs_with_cross = epochs_with_cross.pick(picks="meg")
    epochs_with_cross = epochs_with_cross.copy().resample(250, npad='auto')
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs_with_cross, freqs = freqs, n_cycles = freqs//2, use_fft = False,
                                                           return_itc = False).crop(tmin= baseline_interval_start_power-0.350, tmax=baseline_interval_end_power+0.350, include_tmax=True)
    #remove artifacts
    freq_show_baseline = freq_show_baseline.crop(tmin=-0.350, tmax=-0.050, include_tmax=True)
    b_line  = freq_show_baseline.data.mean(axis=-1)
    #return array of (N_chan, N_events) with averaged value over the baseline time interval
    return BASELINE, b_line

def correct_baseline_substraction(conf, BASELINE, events_of_interest, raw_data, picks):
    # prepare data for numerical calculations for events_of_interest
    N_chans, N_times, N_events, epochs_ar = reshape_epochs(conf, raw_data, events_of_interest, picks)
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

def correct_baseline_power(conf, epochs_of_interest, b_line, kind, b_line_manually, subject, run, plot_spectrogram):
    prefix_out = conf.prefix_out
    tfr_dir = conf.tfr_dir
    # baseline power correction of TFR data after baseline I substraction from the signal
    #for theta n_cycles = 2
    #average over epochs to eliminate inconsistency in the number of epochs over conditions (i.e., risk_vs_norisk)
    #epochs_of_interest = epochs_of_interest.average(method='mean')
    #print('averaging epochs of interest', epochs_of_interest)

    period_start = conf.period_start
    period_end = conf.period_end
    frequency = conf.frequency

    freq_show = mne.time_frequency.tfr_multitaper(epochs_of_interest, freqs = freqs, n_cycles =  freqs//2, use_fft = False, return_itc = False)
    #remove artifacts
    freq_show = freq_show.crop(tmin=period_start+0.350, tmax=period_end-0.350, include_tmax=True)
    #summarize power in tapers of theta freq
    print('plot_spectrogram', plot_spectrogram)
    if plot_spectrogram:
        freq_show.freqs = freqs
    else:
        print('b_line with sum')
        temp = freq_show.data.sum(axis=1)
        freq_show.freqs  = np.array([5])
        freq_show.data = temp.reshape(temp.shape[0],1,temp.shape[1])
    # now fred dim == 1
    #b_line mean (306, 2) ->freq data sum (306, 875)->b_line sum reshape (306, 1)->
    #freq data reshape (306, 1, 875) ->freq data b_line corrected (306, 1, 875)
    #compute power baseline from epochs of interest: mean->sum->divide->log
    if b_line_manually:
        if plot_spectrogram:
            print('before b_line', freq_show.data.shape)
            print('b_line shape', b_line.shape)
            #spread b_line over N_times = 876
            b_line = np.repeat(b_line[:, :, np.newaxis], 876, axis=2)
            print('b_line rep', b_line.shape)
            freq_show.data = np.log10(freq_show.data/b_line)
        else:
            print('b_line with sum')
            b_line = b_line.sum(axis=1).reshape(temp.shape[0],1)
            freq_show.data = np.log10(freq_show.data/b_line[:, np.newaxis])
    else:
        freq_show.apply_baseline(baseline=(-0.5,-0.1), mode="logratio")
    #avrage the trials
    #tfr_path = data_path
    freq_show.save(prefix_out + tfr_dir + data_path.format(subject, run, spec, frequency, stimulus, kind, train), overwrite=True)
    print(prefix_out + tfr_dir)
    print(data_path.format(subject, run, spec, frequency, stimulus, kind, train))
    return freq_show

def topomap_one(freq_show, reduced_info, events_of_interest, raw):
    # use this function to create timecourse of freq power
    freq_timecourse = False
    if freq_timecourse:
        info = raw.info
        info['sfreq'] = 250
        #meg_indices = mne.pick_types(info, meg='grad')
        #reduced_info = mne.pick_info(info, meg_indices)
        freq_show.freqs = freqs
        freq_show.data = freq_show.data.reshape(freq_show.data.shape[0],freq_show.data.shape[2])
        #for P003 run 3 negative
        evoked = mne.EvokedArray(freq_show.data, info=reduced_info, tmin=period_start, comment='', nave=1, kind='average', verbose=None)
        evoked.plot_topo()
        plt.show()
        exit()
    example_topomap = False
    if example_topomap:
        #see the topomap for one subj one run
        fig = freq_show.plot_topo()
        os.chdir('/home/asmyasnikova83/DATA/')
        save = True
        if save:
            fig.savefig('output.png')
            print('Figure saved!')
        else:
            plt.show()
            exit()
