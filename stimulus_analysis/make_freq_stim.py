import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from os.path import exists


def make_beta_signal(subj, r, cond, fb, data_path, events_of_interest, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = 4):
    freqs = np.arange(L_freq, H_freq, f_step)
    #read events
    #events for baseline
    # download marks of positive and negative feedback, if exist
    events_pos = []
    events_neg = []
    events = []
    if exists('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt'.format(subj, r)):
        events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int')
    elif os.path.exists("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r)):
        events = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    else:
        print('norisk trials for bline not found')
    if exists("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r)):
        events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    elif exists("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r)):
        events = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int')
    else:
        print('norisk trials for bline not found')
    
    if len(events) != 0:
        if events.shape == (3,):
            events = events.reshape(1,3)
    #combine both fb for blining
    if len(events_pos) != 0 and len(events_neg) != 0:
        if events_neg.shape == (3,):
        # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
            events_neg = events_neg.reshape(1,3)
        if events_pos.shape == (3,):
            events_pos = events_pos.reshape(1,3)
        events = np.vstack([events_pos, events_neg])
        events = np.sort(events, axis = 0)
    if len(events) == 0:
        return 0
    '''
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    
	'''           
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
        
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)


    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	    
        #add up all values according to the frequency axis
    b_line  = freq_show_baseline.data.mean(axis=-1)
    b_line = b_line.sum(axis=1)


	####### ДЛЯ ДАННЫХ ##############

    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_of_interest, event_id = sorted(list(set([e[2] for e in events_of_interest]))), tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		                
    events_stim = epochs.events
		       
    epochs.resample(300) 

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False)

    temp = freq_show.data.sum(axis=2)
	    
	####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
	    
	
	    
    b_line_new_shape = b_line.reshape(temp.shape[1], 1, 1)
            
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    #data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    
    ####################### не используем логарифм ######################
    data = data/b_line_new_shape
    
    
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
        
    freq_show.data = data
        
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
        
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
        
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = period_start, events = events_stim)
        
    return (epochs_tfr)   
#############################################################################################################
##############################  Получение комбинированных планаров для Evoked  ###############################

def combine_planar_Evoked(evoked):
    planar1 = evoked.copy()
    planar2 = evoked.copy()
    planar1.pick_types(meg='planar1')
    planar2.pick_types(meg='planar2')
    combined = planar1.data + planar2.data
    return planar1, planar2, combined #возвращает планары, которые можно сохранить .fif в файл и np.array() из суммы планаров

##########################################################################################################
########################### Получение комбинированных планаров для эпох  #################################

def combine_planar_Epoches_TFR(EpochsTFR, tmin):
    ep_TFR_planar1 = EpochsTFR.copy();
    ep_TFR_planar2 = EpochsTFR.copy()
    ep_TFR_planar1.pick_types(meg='planar1')
    ep_TFR_planar2.pick_types(meg='planar2')

    #grad_RMS = np.power((np.power(evk_planar1.data, 2) + np.power(evk_planar2.data, 2)), 1/2)
    combine = ep_TFR_planar1.get_data() + ep_TFR_planar2.get_data()
    ep_TFR_combined = mne.EpochsArray(combine, ep_TFR_planar1.info, tmin = tmin, events = EpochsTFR.events)

    return ep_TFR_combined #возвращает эпохи, которые можно сохранить .fif в файл
def make_subjects_df(combined_planar, s, subj, r, t, fb_cur, tmin, tmax, step, scheme):
    time_intervals = np.arange(tmin, tmax, step)
    list_of_time_intervals = []
    i = 0
    while i < (len(time_intervals) - 1):
        interval = time_intervals[i:i+2]
        list_of_time_intervals.append(interval)
        #print(interval)
        i = i+1
    list_of_beta_power = []
    for i in list_of_time_intervals:
        combined_planar_in_interval = combined_planar.copy()
        combined_planar_in_interval = combined_planar_in_interval.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        mean_combined_planar = combined_planar_in_interval.get_data().mean(axis=-1)
        beta_power = []
        for j in range(len(mean_combined_planar)):
            a = mean_combined_planar[j][s]
            beta_power.append(a)
        list_of_beta_power.append(beta_power)
    trial_number = range(len(mean_combined_planar))
    subject = [subj]*len(mean_combined_planar)
    run = ['run{0}'.format(r)]*len(mean_combined_planar)
    trial_type = [t]*len(mean_combined_planar)
    feedback_cur = [fb_cur]*len(mean_combined_planar)
    #in stim we don't need prev data not supported
    #feedback_prev_data = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/prev_fb_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}_prev_fb.txt".format(subj, r, t, fb_cur), dtype='int')
    #if feedback_prev_data.shape == (3,):
    #    feedback_prev_data = feedback_prev_data.reshape(1,3)
    FB_rew = [50, 51]
    FB_lose = [52, 53]
    '''
    feedback_prev = []
    for i in feedback_prev_data:
        if i[2] in FB_rew:
            a = 'positive'
        else:
            a = 'negative'
        feedback_prev.append(a)
    ''' 
    # схема подкрепления 
    a = scheme.loc[(scheme['fname'] == subj) & (scheme['block'] == r)]['scheme'].tolist()[0]
    sch = [a]*len(mean_combined_planar)
    df = pd.DataFrame()
    df['trial_number'] = trial_number
    # beta на интервалах
    for idx, beta in enumerate(list_of_beta_power):
        df['beta power %s'%list_of_time_intervals[idx]] = beta
        df['subject'] = subject
        df['round'] = run
        df['trial_type'] = trial_type
        df['feedback_cur'] = feedback_cur
        #df['feedback_prev'] = feedback_prev
        df['scheme'] = sch
    return (df)
