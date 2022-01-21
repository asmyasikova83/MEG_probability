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

def combine_planar_Evoked(evoked):
    planar1 = evoked.copy()
    planar2 = evoked.copy()
    planar1.pick_types(meg='planar1')
    planar2.pick_types(meg='planar2')
    combined = planar1.data + planar2.data
    return planar1, planar2, combined #возвращает планары, которые можно сохранить .fif в файл и np.array() из суммы планаров
