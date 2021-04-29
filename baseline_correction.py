import mne, os
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from config import conf, response
from mne.time_frequency import tfr_morlet, psd_multitaper
from make_evoked_freq_data_container import container_results

def find_event(event, events):
    for e in events:
        if e[0] == event[0]:
            assert e[2] == event[2]
            return True
    return False

def retrieve_events(conf, raw_data, path_events, kind_idx, cross):
    events = []
    verbose = conf.verbose
    kind = conf.kind[kind_idx]

    #takes events with fixation cross followed by the events of interest (positive and negative feedback)
    events_raw = mne.find_events(raw_data, stim_channel='STI101', output='onset',
                                 consecutive='increasing', min_duration=0, shortest_event=1,
                                 mask=None, uint_cast=False, mask_type='and', initial_event=False, verbose='ERROR')
    if verbose:
        print('path_events', path_events)
    events_cleaned = np.loadtxt(path_events, dtype=int)
    # (3,) -> (1,3)
    if events_cleaned.shape == (3,):
        events_cleaned = events_cleaned[np.newaxis, :]
    if verbose:
        print(kind)
        print('events cl')
        print(events_cleaned)
        print(events_raw)

    if kind == 'negative' or kind ==  'positive':
        p = 3
    else:
        if conf.stim:
            p = 1
        if conf.response:
            p = 2

    # extract events with fixation cross followed by positive or negative feedback
    for i in range(len(events_raw)):
        # check the fixation cross and find the response after the fix cross
        if events_raw[i][2] == 1:
            if find_event(events_raw[i + p], events_cleaned):
                events.append(events_raw[i] if cross else events_raw[i + p])
            if find_event(events_raw[i + p + 1], events_cleaned):
                events.append(events_raw[i] if cross else events_raw[i + p + 1])
    return events

def reshape_epochs(conf, raw_data, events, picks):
    verbose = conf.verbose
    period_start = conf.period_start
    period_end = conf.period_end
    #  retrieve epochs associated with the events of interest
    if verbose:
        print('events', events)
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True, verbose = 'ERROR')
    epochs_ar = epochs.get_data()
    # reshape data for calculations -> 3D matrix with the dimensions of N_chans, N_times, N_events
    epochs_ar = epochs_ar.swapaxes(0, 1)
    epochs_ar = epochs_ar.swapaxes(1, 2)
    N_chans, N_times, N_events = epochs_ar.shape
    return N_chans, N_times, N_events, epochs_ar

def create_mne_epochs_evoked(conf, CORRECTED_DATA, events_of_interest, plot, raw, picks):
    '''
    create an Epoch object from data array using info from raw_file, downsample it, creates and returns evoked
    data in shape (n_epochs, n_channels, n_times)
    '''
    verbose = conf.verbose

    # create info for the Epoch object
    info = raw.info
    meg_indices = mne.pick_types(info, meg='grad')
    reduced_info = mne.pick_info(info, meg_indices)
    if verbose:
        print('CORR DATA shape', CORRECTED_DATA.shape)
        print(events_of_interest)
    epochs = mne.EpochsArray(CORRECTED_DATA, info=reduced_info, events=events_of_interest,
        tmin=conf.period_start, baseline=None, event_id=sorted(list(set([e[2] for e in events_of_interest]))), verbose='ERROR')

    # downsample to 250 Hz
    epochs_of_interest = epochs.copy().resample(250, npad='auto')
    evoked = epochs_of_interest.average()
    if verbose:
        print('ep of interest', epochs_of_interest)

    # plotting options for newly created epochs object, evoked, psd
    if plot:
        if verbose:
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
                        tmax = period_end, baseline = None, picks=picks, preload = True, verbose = 'ERROR')
    title=' Before baseline'
    mne.viz.plot_epochs(epochs_of_interest_out_BASELINE, picks=picks[0:204], title=title, scalings=None)
    title=' After baseline'
    mne.viz.plot_epochs(epochs_of_interest_w_BASELINE, picks=picks[0:204], title=title, scalings=None)
    plt.show()
    exit()

def compute_baseline_substraction(conf, raw_data, events_with_cross, events_of_interest, picks):
    '''
    average each epoch with fixation cross followed by the events of interest
    substract this average from the relevant epoch of interest
    prepare data for numerical calculations for events_with_cross
    '''
    baseline_interval_start_sub = conf.baseline_interval_start_sub
    baseline_interval_end_sub = conf.baseline_interval_end_sub

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

    if conf.baseline == 'fixation_cross_norisks':
        #adjust the num ov events to that of events_of_interest
        NEW_BASELINE = np.mean(BASELINE, axis=0)
        #add new dim according to events_of_interest
        BASELINE = np.tile(NEW_BASELINE, (N_events_interest, 1))

    # We need to operate on further data as of (204,2001), so we need to transpose BASELINE as of (2001,25)
    BASELINE = BASELINE.transpose()

    return BASELINE

def compute_baseline_power(conf, raw_data, events_with_cross, picks):
    period_start = conf.period_start
    period_end = conf.period_end
    baseline_interval_start_power = conf.baseline_interval_start_power
    baseline_interval_end_power = conf.baseline_interval_end_power
    freqs = conf.freqs
    single_trial = conf.single_trial
    print('events with cross shape', len(events_with_cross))
    #compute baseline II for power correction: mean  picks = picks!
    epochs_with_cross = mne.Epochs(raw_data, events_with_cross, event_id = None, tmin = period_start,
                        tmax = period_end, baseline = None, picks=picks, preload = True, verbose = 'ERROR')

    #epochs_with_cross = epochs_with_cross.pick(picks="meg")
    epochs_with_cross = epochs_with_cross.copy().resample(250, npad='auto')
    if single_trial:
    #no averaging in single trial
        freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs_with_cross, freqs = freqs, n_cycles = freqs//2, use_fft = False,
                                                           return_itc = False,average = False,
                                                           verbose = 'ERROR').crop(tmin= baseline_interval_start_power-0.350,
                                                           tmax=baseline_interval_end_power+0.350, include_tmax=True)
    else:
        freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs_with_cross, freqs = freqs, n_cycles = freqs//2, use_fft = False,
                                                           return_itc = False, verbose = 'ERROR').crop(tmin= baseline_interval_start_power-0.350,
                                                           tmax=baseline_interval_end_power+0.350, include_tmax=True)
    #remove artifacts
    freq_show_baseline = freq_show_baseline.crop(tmin=-0.350, tmax=-0.050, include_tmax=True)
    if single_trial:
        #add up all values according to the frequency axis
        b_line_raw = freq_show_baseline.data.sum(axis=-2)
        print('bline shape dd up all values according to the frequency axis', b_line_raw.shape)
	# Для бейзлайна меняем оси местами, на первом месте число каналов
        b_line_raw = np.swapaxes(b_line_raw, 0, 1)
        # выстраиваем в ряд бейзлайны для каждого из 28 эвентов, как будто они происходили один за другим
        a, b, c = b_line_raw.shape
        b_line_raw = b_line_raw.reshape(a, b * c)
        print('baseline shape for single trials', b_line_raw.shape)
        b = b_line_raw.mean(axis=-1)
        b_line = b[:, np.newaxis, np.newaxis]
        print('b_line last', b_line.shape)
    else:
        b_line  = freq_show_baseline.data.mean(axis=-1)
    #return array of (N_chan, N_events) with averaged value over the baseline time interval
    return b_line

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

def correct_baseline_power_and_save(conf, epochs_of_interest, b_line, data_path, b_line_manually, plot_spectrogram):
    '''
    baseline power correction of TFR data after baseline I substraction from the signal
    for theta n_cycles = 2
    average over epochs to eliminate inconsistency in the number of epochs over conditions (i.e., risk_vs_norisk)
    epochs_of_interest = epochs_of_interest.average(method='mean')
    '''

    freqs = conf.freqs
    verbose = conf.verbose
    plot_spectrogram = conf.plot_spectrogram
    single_trial = conf.single_trial

    if single_trial:
        freq_show = mne.time_frequency.tfr_multitaper(epochs_of_interest, freqs = freqs, n_cycles =  freqs//2,
            use_fft = False, return_itc = False, average=False, verbose = 'ERROR')
    else:
        freq_show = mne.time_frequency.tfr_multitaper(epochs_of_interest, freqs = freqs, n_cycles =  freqs//2,
            use_fft = False, return_itc = False, verbose = 'ERROR')
    #remove artifacts
    freq_show = freq_show.crop(tmin=conf.period_start+0.350, tmax=conf.period_end-0.350, include_tmax=True)

    #summarize power in tapers of theta freq
    if verbose:
        print('plot_spectrogram', plot_spectrogram)
    if plot_spectrogram:
        freq_show.freqs = freqs
    else:
        if verbose:
            print('b_line with sum')
        if single_trial:
            temp = freq_show.data.sum(axis=2)
            print('data shape in single trial after summation of tapers', temp.shape)
            freq_show.freqs  = np.array([5])
            data = np.swapaxes(temp, 0, 1)
            freq_show.data = np.swapaxes(data, 1, 2)
            print('data shape in single trial after swapping', freq_show.data.shape)
        else:
            temp = freq_show.data.sum(axis=1)
            freq_show.freqs  = np.array([5])
            freq_show.data = temp.reshape(temp.shape[0],1,temp.shape[1])

    # now fred dim == 1
    #b_line mean (306, 2) ->freq data sum (306, 875)->b_line sum reshape (306, 1)->
    #freq data reshape (306, 1, 875) ->freq data b_line corrected (306, 1, 875)
    #compute power baseline from epochs of interest: mean->sum->divide->log
    if b_line_manually:
        if plot_spectrogram:
            if verbose:
                print('before b_line', freq_show.data.shape)
                print('b_line shape', b_line.shape)
            #spread b_line over N_times = 876
            b_line = np.repeat(b_line[:, :, np.newaxis], conf.time.shape[0], axis=2)
            if verbose:
                print('b_line rep', b_line.shape)
            freq_show.data = np.log10(freq_show.data/b_line)
        else:
            if verbose:
                print('b_line with sum')
            if single_trial:
                print('bline single trial shape after swapping', b_line.shape)
                #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
                data = np.log10(data/b_line)
                data = np.swapaxes(data, 1, 2)
                data = np.swapaxes(data, 2, 1)
                data = np.swapaxes(data, 1, 0)
                freq_show.data = data
                #freq_show.data = freq_show.data[:, :, np.newaxis, :]
                print('freq data after b_lining', freq_show.data.shape)
                #averaging over epochs
                freq_show.data = data.mean(axis = 0)
                freq_show.data = freq_show.data[np.newaxis, :, np.newaxis, :]
                print('freq data after averaging: single trial', freq_show.data.shape)
            else:
                b_line = b_line.sum(axis=1).reshape(temp.shape[0],1)
                freq_show.data = np.log10(freq_show.data/b_line[:, np.newaxis])
                print('frew show data shape no single trial', freq_show.data.shape)
    else:
        freq_show.apply_baseline(baseline=(-0.5,-0.1), mode="logratio")

    # save
    #if single_trial:
        #path_home = '/home/asmyasnikova83/'
        #out_file = conf.path_container + data_path
        #print('out file', out_file)
        #donor = mne.Evoked(f'{conf.path_home}donor-ave.fif', verbose = 'ERROR')
        #container_results(plot_spectrogram, single_trial, freq_show, freq_show.data, donor, out_file, verbose)
    #else:
    print(conf.path_tfr + data_path)
    freq_show.save(conf.path_tfr + data_path, overwrite=True)
    if verbose:
        print(data_path)
    return freq_show

def topomap_one(freq_show, reduced_info, events_of_interest, raw):
    # use this function to create timecourse of freq power
    freq_timecourse = False
    if freq_timecourse:
        info = raw.info
        info['sfreq'] = 250
        freq_show.freqs = freqs
        freq_show.data = freq_show.data.reshape(freq_show.data.shape[0],freq_show.data.shape[2])
        #for P003 run 3 negative
        evoked = mne.EvokedArray(freq_show.data, info=reduced_info, tmin=period_start, comment='', nave=1, kind='average', verbose='ERROR')
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
        else:
            plt.show()
            exit()
