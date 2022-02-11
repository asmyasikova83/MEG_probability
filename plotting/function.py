import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
import matplotlib.pyplot as plt

###############################################################################################
######## Resample before doing stat #############
def  resample_before_stat(t_min, t_max):
    original_time = np.arange(-1.4, 2.1+1.0/300, 1.0/300)
    correct_time = np.arange(-1.4, 2.1, 1.0/40)
    ticks_array = np.zeros((len(correct_time)))
    idx_array = np.zeros((len(correct_time)))
    for i in range(len(correct_time)):
        min_val = 1.0
        for g in range(len(original_time)):
            if abs(original_time[g] - correct_time[i]) < min_val:
                min_val = abs(original_time[g] - correct_time[i])
                min_ind = g
        ticks_array[i] = original_time[min_ind]
        idx_array[i] = min_ind
    #add last element_array
    ticks_array_extended = np.append(ticks_array, 2.1)
    idx_array_extended = np.append(idx_array, 1050.0)
    time = ticks_array_extended
    return time, idx_array_extended

######## Функция для поиска меток фиксационного креста (по ним ищется baseline)######

def fixation_cross_events(trial_type, data_path_raw, raw_name, data_path_events, name_events, subj, r, fb):
    print(trial_type)
    # для чтения файлов с events используйте либо np.loadtxt либо read_events либо read_events_N
    no_risk = np.loadtxt(op.join(data_path_events, name_events.format(subj, r, trial_type, fb)), dtype='int')
    #no_risk = read_events(op.join(data_path_events, name_events.format(subj, r)))
    
    # Load raw events without miocorrection
    events_raw = read_events(op.join(data_path_raw, raw_name.format(subj, r)))        
    
    # Load data

    #raw_fname = op.join(data_path_raw, raw_name.format(subj, r))

    #raw = mne.io.Raw(raw_fname, preload=True)

    #events_raw = mne.find_events(raw, stim_channel='STI101', output='onset', 
    #                                 consecutive='increasing', min_duration=0, shortest_event=1, mask=None, 
    #                                 uint_cast=False, mask_type='and', initial_event=False, verbose=None)
    
    if no_risk.shape == (3,):
        no_risk = no_risk.reshape(1,3)
    # список индексов трайлов
    x = []
    for i in range(len(events_raw)):
	    for j in range(len(no_risk)):
		    if np.all((events_raw[i] - no_risk[j] == 0)):
			    x+=[i]

    x1 = 1 #fixation cross

    full_ev = []
    for i in x:
        full_ev += [list(events_raw[i])] # список из 3ех значений время х 0 х метка
        j = i - 1
        ok = True      
        while ok:
            full_ev += [list(events_raw[j])]
            if events_raw[j][2] == x1:
                ok = False
            j -= 1 

                
    event_fixation_cross_norisk = []

    for i in full_ev:
        if i[2] == x1:
            event_fixation_cross_norisk.append(i)
                    
    event_fixation_cross_norisk = np.array(event_fixation_cross_norisk)
     
    return(event_fixation_cross_norisk)

###########################################################################
###### Функция для получения эпохированных tfr сингл трайлс ###############
def make_fix_cross_signal(subj, r, fb, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline):
    freqs = np.arange(L_freq, H_freq, f_step)
    # download marks of positive feedback
    if cond == 'norisk':      
        events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
        events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    if cond == 'risk':      
        events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/probability/events_fix_cross/{0}_run{1}_risk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
        events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/probability/events_fix_cross/{0}_run{1}_risk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    if cond == 'prerisk':      
        events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/probability/events_fix_cross/{0}_run{1}_prerisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
        events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/probability/events_fix_cross/{0}_run{1}_prerisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    if cond == 'postrisk':      
        events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/probability/events_fix_cross/{0}_run{1}_postrisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
        events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/probability/events_fix_cross/{0}_run{1}_postrisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_pos.shape == (3,):
        events_pos = events_pos.reshape(1,3)
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_neg.shape == (3,):
        events_neg = events_neg.reshape(1,3) 
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events = np.vstack([events_pos, events_neg])
    events = np.sort(events, axis = 0) 
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True)
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, 
		                baseline = None, picks = picks, preload = True)
    epochs.resample(300) 
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True)
    temp = freq_show.data.sum(axis=2)
    print('DATA from make_fix_cross_signal', temp)
    freq_show.data = temp
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = baseline[0], events = events)
    return (epochs_tfr)   
def make_fix_cross_signal_baseline(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline):
    #compute power for ti interval before fix cross    
    freqs = np.arange(L_freq, H_freq, f_step)
    # download marks of positive feedback      
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_pos.shape == (3,):
        events_pos = events_pos.reshape(1,3)
    # download marks of negative feedback      
    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_neg.shape == (3,):
        events_neg = events_neg.reshape(1,3) 
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events_norisk = np.vstack([events_pos, events_neg])
    events_norisk = np.sort(events_norisk, axis = 0)
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True)
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
    epochs_baseline = mne.Epochs(raw_data, events_norisk, event_id = None, tmin = -1.0, tmax = 1.0, 
		                baseline = None, picks = picks, preload = True)
    epochs_baseline.resample(300) 
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs_baseline, freqs = freqs, n_cycles = freqs//2, use_fft = False, 
                                return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	    
    #add up all values according to the frequency axis
    #b_line = freq_show_baseline.data.sum(axis=-2)
    b_line = freq_show_baseline.data
    # Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
    #b_line = np.swapaxes(b_line, 3, 2) #for check
    # выстраиваем в ряд бейзлайныbeta_16_30_epo_comb_planar для каждого из эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    b_line = b_line.reshape(a, b * c)
    #a, b, c, d  = b_line.shape
    #b_line = b_line.reshape(a, b * c, d)
    #print(b_line.shape)
    ####### ДЛЯ ДАННЫХ ##############
    if cond == 'norisk':
        events = events_norisk
    if cond != 'norisk':
        if fb == 'positive':
            events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_positive_fix_cross.txt".format(subj, r, cond), dtype='int') 
            # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
            if events_pos.shape == (3,):
                events = events_pos.reshape(1,3)
            print('fb', fb)
            print('cond', cond)
            exit()
        if fb == 'negative':
            events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_negative_fix_cross.txt".format(subj, r, cond), dtype='int')
            # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
            if events_neg.shape == (3,):
                events = events_neg.reshape(1,3) 
            print('fb', fb)
            print('cond', cond)
            exit(
            exit())
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    #events = np.vstack([events_pos, events_neg])
    #events = np.sort(events, axis = 0)
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, 
		                baseline = None, picks = picks, preload = True)
    epochs.resample(300) 
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, 
                                return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True)
    print('FREQ SHOW data sh', freq_show.data.shape )
    temp = freq_show.data.sum(axis=2)
	####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    #temp = freq_show.data
    #data = np.swapaxes(temp, 0, 1)
    #data = np.swapaxes(data, 3, 2) #for check
    print('DATA SHAPE', data.shape)
    data = np.swapaxes(data, 1, 2)
    print('DATA SHAPE2', data.shape)
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1) #no need in check where we do the summation after b_lining)
    print('B_LINE SHAPe', b_line.shape)
    #b = b_line.mean(axis=-2)# do if check sum
    print('B_LINE SHAPe', b_line.shape)
    #b_line_new_shape = b[:, np.newaxis, np.newaxis, :] #leave the tapers
    b_line_new_shape = b[:, np.newaxis, np.newaxis]
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    print('data shape after b_lining', data.shape)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    freq_show.data = data
    #freq_show.data = freq_show.data[:, :, np.newaxis, :] #keep consistent with the previous workflow
    #freq_show.data = freq_show.data.sum(axis = -1) #sum over freq tapers
    print('data shapeafter', freq_show.data.shape)
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = baseline[0], events = events)
    return (epochs_tfr)   
def make_response_signal(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline):
    #compute power for ti interval before fix cross    
    freqs = np.arange(L_freq, H_freq, f_step)
    events_resp_pos = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_positive.txt'.format(subj, r, cond), dtype='int')
    events_resp_neg = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_negative.txt'.format(subj, r, cond), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_resp_pos.shape == (3,):
        events_resp_pos = events_resp_pos.reshape(1,3)
    if events_resp_neg.shape == (3,):
        events_resp_neg = events_resp_neg.reshape(1,3)
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания   
    events_resp = np.vstack([events_resp_pos, events_resp_neg])
    events_resp = np.sort(events_resp, axis = 0) 
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True)
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
    epochs = mne.Epochs(raw_data, events_resp, event_id = None, tmin = -1.0, tmax = 1.0, 
		                 baseline = None, picks = picks, preload = True)
    epochs.resample(300) 
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True)
    temp = freq_show.data.sum(axis=2)
    freq_show.data = temp
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = baseline[0], events = events_resp)
    return (epochs_tfr)   
def make_response_signal_baseline(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline):
    #compute power for ti interval before fix cross    
    freqs = np.arange(L_freq, H_freq, f_step)
    # download marks of positive feedback      
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_pos.shape == (3,):
        events_pos = events_pos.reshape(1,3)
    # download marks of negative feedback      
    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_neg.shape == (3,):
        events_neg = events_neg.reshape(1,3) 
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events = np.vstack([events_pos, events_neg])
    events = np.sort(events, axis = 0) 
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True)
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
    epochs_baseline = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, 
		                baseline = None, picks = picks, preload = True)
    epochs_baseline.resample(300) 
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs_baseline, freqs = freqs, n_cycles = freqs//2, use_fft = False, 
                                return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	    
    #add up all values according to the frequency axis
    b_line = freq_show_baseline.data.sum(axis=-2)
    # Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
    # выстраиваем в ряд бейзлайныbeta_16_30_epo_comb_planar для каждого из эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    b_line = b_line.reshape(a, b * c)
    events_resp_pos = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_positive.txt'.format(subj, r, cond), dtype='int')
    events_resp_neg = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_negative.txt'.format(subj, r, cond), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_resp_pos.shape == (3,):
        events_resp_pos = events_resp_pos.reshape(1,3)
    if events_resp_neg.shape == (3,):
        events_resp_neg = events_resp_neg.reshape(1,3)
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events_resp = np.vstack([events_resp_pos, events_resp_neg])
    events_resp = np.sort(events_resp, axis = 0) 
    epochs = mne.Epochs(raw_data, events_resp, event_id = None, tmin = -1.0, tmax = 1.0, 
		                 baseline = None, picks = picks, preload = True)
    epochs.resample(300) 
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True)
    temp = freq_show.data.sum(axis=2)
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
    # Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)
    b_line_new_shape = b[:, np.newaxis, np.newaxis]
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    freq_show.data = data
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = baseline[0], events = events_resp)
    return (epochs_tfr)   
def make_beta_signal(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline):
    freqs = np.arange(L_freq, H_freq, f_step)
    
    #read events
	#events for baseline
	# download marks of positive feedback
	
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int') 
    #events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/PREV_FB/fix_cross_mio_corr/{0}_run{1}_norisk_fb_prev_positive_fix_cross.txt".format(subj, r), dtype='int')
    '''
    ####################################################
    #проверка скрипта Александры - нериск вместо фикс креста
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/ksayfulina/events_clean_after_mio/{0}_run{1}_norisk_fb_positive.txt".format(subj, r), dtype='int')
    #################################################
    '''
        # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_pos.shape == (3,):
        events_pos = events_pos.reshape(1,3)
        
    # download marks of negative feedback      
    
    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    #events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/PREV_FB/fix_cross_mio_corr/{0}_run{1}_norisk_fb_prev_negative_fix_cross.txt".format(subj, r), dtype='int')
    '''
    ####################################################
    #проверка скрипта Александры - нериск вместо фикс креста
    
    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/ksayfulina/events_clean_after_mio/{0}_run{1}_norisk_fb_negative.txt".format(subj, r), dtype='int')
    #################################################
    '''
    
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_neg.shape == (3,):
        events_neg = events_neg.reshape(1,3) 
    
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events = np.vstack([events_pos, events_neg])
    events = np.sort(events, axis = 0) 
    
    #events, which we need
    fix_cross = False
    if fix_cross:
        print('in fix cross')
        print('cond', cond)
        print('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt'.format(subj, r, cond, fb))
        events_response = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt'.format(subj, r, cond, fb), dtype='int') 
        print('eve response',  events_response)
    else:
        events_response = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    #vents_response = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/PREV_FB/PREV_FB_events/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    
	           
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
        
    picks = mne.pick_types(raw_data.info, meg = True, eog = True, emg = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)
    print('Epochs', epochs)
    #average False
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	    
        #add up all values according to the frequency axis
    b_line = freq_show_baseline.data.sum(axis=-2)
    #print('BASELINE',  b_line)
	    
	    # Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
        
        # выстраиваем в ряд бейзлайныbeta_16_30_epo_comb_planar для каждого из эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    b_line = b_line.reshape(a, b * c)
	    

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline=None, picks = picks, preload = True)
    print('epochs', epochs)		       
    epochs.resample(300) 
    
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = freqs//2, use_fft = False, return_itc = False, average=False)
    #average = False
    temp = freq_show.data.sum(axis=2)
    #print('DATA BEFORE BASELIINE', temp)
    #exit()	    
	####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
	    
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
	    
    b = b_line.mean(axis=-1)
	    
    b_line_new_shape = b[:, np.newaxis, np.newaxis]
            
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
        
    freq_show.data = data
        
    freq_show.data = freq_show.data[:, :, np.newaxis, :]
        
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2)
    print('freq show shape', freq_show.data.shape)   
    #epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = period_start, events = events_response)
        
    #return (epochs_tfr)
    
    return freq_show


##########################################################################################        
################### Фукнция для получения предыдущего фидбека ############################
def prev_feedback(events_raw, tials_of_interest, FB):
    
    #Получаем индексы трайлов, которые нас интересуют
    
    x = []
    for i in range(len(events_raw)):
	    for j in range(len(tials_of_interest)):
		    if np.all((events_raw[i] - tials_of_interest[j] == 0)):
			    x+=[i]
    
    prev_fb = []

    for i in x:
        ok = True
        while ok:
            #print(i)
            if events_raw[i-1][2] in FB:
                a = events_raw[i-1].tolist()
                prev_fb.append(a)
                ok = False
            else:
                pass
            i = i - 1
            
    prev_fb = np.array(prev_fb)
    
    return(prev_fb)
    
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

#############################################################################################################	
##############################  Получение комбинированных планаров для Evoked  ###############################	
def combine_planar_Evoked(evoked):
	planar1 = evoked.copy(); 
	planar2 = evoked.copy()
	planar1.pick_types(meg='planar1')
	planar2.pick_types(meg='planar2')

	#grad_RMS = np.power((np.power(evk_planar1.data, 2) + np.power(evk_planar2.data, 2)), 1/2)
	combined = planar1.data + planar2.data
	
	return planar1, planar2, combined #возвращает планары, которые можно сохранить .fif в файл и np.array() из суммы планаров

###########################################################################################################	
################################ Сборка таблицы для LMEM ###############################
    
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
    FB_rew = [50, 51]
    FB_lose = [52, 53]
    feedb = 'CUR_FB'
    if feedb == 'PREV_FB':
        print('PREV_FB: Extracting cur fb for dataframe')
        feedback_prev = [fb_cur]*len(mean_combined_planar)
        feedback_cur_data = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/PREV_FB/CUR_FB_for_tables/{0}_run{1}_{2}_fb_cur_for_prev_{3}.txt".format(subj, r, t, fb_cur), dtype='int')
        if feedback_cur_data.shape == (3,):
            feedback_cur_data = feedback_cur_data.reshape(1,3)
        feedback_cur = []
        for i in feedback_cur_data:
            if i[2] in FB_rew:
                a = 'positive'
            else:
                a = 'negative'
            feedback_cur.append(a)
    if feedb == 'CUR_FB':
        feedback_cur = [fb_cur]*len(mean_combined_planar)
        feedback_prev_data = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/prev_fb_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}_prev_fb.txt".format(subj, r, t, fb_cur), dtype='int')
        if feedback_prev_data.shape == (3,):
            feedback_prev_data = feedback_prev_data.reshape(1,3)
        feedback_prev = []
        for i in feedback_prev_data:
            if i[2] in FB_rew:
                a = 'positive'
            else:
                a = 'negative'
            feedback_prev.append(a)   
    # схема подкрепления   
    a = scheme.loc[(scheme['fname'] == subj) & (scheme['block'] == r)]['scheme'].tolist()[0]
    sch = [a]*len(mean_combined_planar)    
    
    
    df = pd.DataFrame()
    
    
    df['trial_number'] = trial_number
    
    # beta на интервалах
    for idx, beta in enumerate(list_of_beta_power):
        df['beta power %s'%list_of_time_intervals[idx]] = beta
    

    #df['beta_power'] = beta_power
    df['subject'] = subject
    df['round'] = run
    df['trial_type'] = trial_type
    df['feedback_cur'] = feedback_cur
    df['feedback_prev'] = feedback_prev
    df['scheme'] = sch
        
    return (df)
    
def make_fix_cross_df(fix_cross_norisk, resp_norisk, fix_cross_bslne_norisk, resp_bslne_norisk, fix_cross_risk, resp_risk,  fix_cross_bslne_risk, resp_bslne_risk, s, t, tmin, tmax, step):
    
    time_intervals = np.arange(tmin, tmax, step)
    print('time intervals', time_intervals)
    list_of_time_intervals = []
    i = 0
    while i < (len(time_intervals) - 1):
        interval = time_intervals[i:i+2]
        list_of_time_intervals.append(interval)
        i = i+1
    print('list_of_time_intervals', list_of_time_intervals) 
    theta_power_fix_cross_norisk = [] 
    theta_power_resp_norisk = []
    theta_power_fix_cross_bslne_norisk = []
    theta_power_resp_bslne_norisk = []
    theta_power_fix_cross_risk = [] 
    theta_power_resp_risk = []
    theta_power_fix_cross_bslne_risk = []
    theta_power_resp_bslne_risk = []
    for i in list_of_time_intervals:
        fix_cross_norisk = fix_cross_norisk.copy()
        fix_cross_norisk = fix_cross_norisk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        #average over time axis=-1 and sensors axis=0
        fix_cross_norisk_mean = fix_cross_norisk.data.mean(axis=-1).mean(axis=0)
        theta_power_fix_cross_norisk.append(fix_cross_norisk_mean)
        resp_norisk = resp_norisk.copy()
        resp_norisk = resp_norisk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        resp_norisk_mean = resp_norisk.data.mean(axis=-1).mean(axis=0)
        theta_power_resp_norisk.append(resp_norisk_mean)
        fix_cross_bslne_norisk = fix_cross_bslne_norisk.copy()
        fix_cross_bslne_norisk = fix_cross_bslne_norisk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        fix_cross_bslne_norisk_mean = fix_cross_bslne_norisk.data.mean(axis=-1).mean(axis=0)
        theta_power_fix_cross_bslne_norisk.append(fix_cross_bslne_norisk_mean)
        resp_bslne_norisk = resp_bslne_norisk.copy()
        resp_bslne_norisk = resp_bslne_norisk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        resp_bslne_norisk_mean = resp_bslne_norisk.data.mean(axis=-1).mean(axis=0)
        theta_power_resp_bslne_norisk.append(resp_bslne_norisk_mean)
        fix_cross_risk = fix_cross_risk.copy()
        fix_cross_risk = fix_cross_risk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        fix_cross_risk_mean = fix_cross_risk.data.mean(axis=-1).mean(axis=0)
        theta_power_fix_cross_risk.append(fix_cross_risk_mean)
        resp_risk = resp_risk.copy()
        resp_risk = resp_risk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        resp_risk_mean = resp_risk.data.mean(axis=-1).mean(axis=0)
        theta_power_resp_risk.append(resp_risk_mean)
        fix_cross_bslne_risk = fix_cross_bslne_risk.copy()
        fix_cross_bslne_risk = fix_cross_bslne_risk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        fix_cross_bslne_risk_mean = fix_cross_bslne_risk.data.mean(axis=-1).mean(axis=0)
        theta_power_fix_cross_bslne_risk.append(fix_cross_bslne_risk_mean)
        resp_bslne_risk = resp_bslne_risk.copy()
        resp_bslne_risk = resp_bslne_risk.crop(tmin=i[0], tmax=i[1], include_tmax=True)
        resp_bslne_risk_mean = resp_bslne_risk.data.mean(axis=-1).mean(axis=0)
        theta_power_resp_bslne_risk.append(resp_bslne_risk_mean)
    
    df = pd.DataFrame()

    subject = [s]
    #trial_type = [t]
    
    df['subject'] = subject
    df['fix_cross_norisk %s'%list_of_time_intervals[0]] = theta_power_fix_cross_norisk
    df['fix_cross_bslne_norisk %s'%list_of_time_intervals[0]] = theta_power_fix_cross_bslne_norisk
    df['response_norisk %s'%list_of_time_intervals[0]] = theta_power_resp_norisk
    df['response_bslne_norisk %s'%list_of_time_intervals[0]] = theta_power_resp_bslne_norisk
    df['fix_cross_risk %s'%list_of_time_intervals[0]] = theta_power_fix_cross_risk
    df['fix_cross_bslne_risk %s'%list_of_time_intervals[0]] = theta_power_fix_cross_bslne_risk
    df['response_risk %s'%list_of_time_intervals[0]] = theta_power_resp_risk
    df['response_bslne_risk %s'%list_of_time_intervals[0]] = theta_power_resp_bslne_risk
    return (df)
###############################################################################################    
############################ FUNCTION FOR TTEST ############################
######################### парный ttest #########################################
def extract_and_av_cond_data(data_path, subjects, fr,  n): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 4, 102, n))

    for ind, subj in enumerate(subjects):
       # temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_resp_{2}.fif'.format(subj, parameter1, planar)))
       # temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_resp_{2}.fif'.format(subj, parameter2, planar)))
       # data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
        temp1 = mne.Evoked(op.join(data_path, '{0}_risk_evoked_{1}_trf_no_log_division_resp_comb_planar.fif'.format(subj, fr)))
        temp2 = mne.Evoked(op.join(data_path, '{0}_norisk_evoked_{1}_trf_no_log_division_resp_comb_planar.fif'.format(subj, fr)))
        temp3 = mne.Evoked(op.join(data_path, '{0}_prerisk_evoked_{1}_trf_no_log_division_resp_comb_planar.fif'.format(subj, fr)))
        temp4 = mne.Evoked(op.join(data_path, '{0}_postrisk_evoked_{1}_trf_no_log_division_resp_comb_planar.fif'.format(subj, fr)))
       # temp1 = mne.Evoked(op.join(data_path, '{0}_risk_evoked_beta_16_30_trf_early_log_resp_comb_planar.fif'.format(subj, fr)))
       # temp2 = mne.Evoked(op.join(data_path, '{0}_norisk_evoked_beta_16_30_trf_early_log_resp_comb_planar.fif'.format(subj, fr)))
       # temp3 = mne.Evoked(op.join(data_path, '{0}_prerisk_evoked_beta_16_30_trf_early_log_resp_comb_planar.fif'.format(subj, fr)))
       # temp4 = mne.Evoked(op.join(data_path, '{0}_postrisk_evoked_beta_16_30_trf_early_log_resp_comb_planar.fif'.format(subj, fr)))
        contr[ind, 0, :, :] = temp1.data
        contr[ind, 1, :, :] = temp2.data
        contr[ind, 2, :, :] = temp3.data
        contr[ind, 3, :, :] = temp4.data
		
    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]
    comp3 = contr[:, 2, :, :]
    comp4 = contr[:, 3, :, :]

    t1_stat, p1_val = stats.ttest_1samp(comp1, 0, axis=0)
    t2_stat, p2_val = stats.ttest_1samp(comp2, 0, axis=0)
    t3_stat, p3_val = stats.ttest_1samp(comp3, 0, axis=0)
    t4_stat, p4_val = stats.ttest_1samp(comp4, 0, axis=0)
    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    comp3_mean = comp3.mean(axis=0)
    comp4_mean = comp4.mean(axis=0)
    return comp1_mean, comp2_mean, comp3_mean, comp4_mean, p1_val, p2_val, p3_val, p4_val

def ttest_pair_bk(data_path, subjects, parameter1, parameter2, planar, n): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 2, 102, n))

    for ind, subj in enumerate(subjects):
       # temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_resp_{2}.fif'.format(subj, parameter1, planar)))
       # temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_resp_{2}.fif'.format(subj, parameter2, planar)))
        #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/low_beta_12_20_CORR//beta_12_20_ave_comb_planar/'
        temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_resp_{3}.fif'.format(subj, parameter1, fr, planar)))
        temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_resp_{3}.fif'.format(subj, parameter2, fr, planar)))
        
        contr[ind, 0, :, :] = temp1.data
        contr[ind, 1, :, :] = temp2.data
		
    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]
    t_stat, p_val = stats.ttest_rel(comp2, comp1, axis=0)

    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    return t_stat, p_val, comp1_mean, comp2_mean

def ttest_pair(data_path, response, subjects, fr, parameter1, parameter2, parameter3, parameter4, planar, n): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 2, 102, n))
    for ind, subj in enumerate(subjects):
        if  parameter3 == 'negative':
            #TODO less time points
            if response:
                temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_{3}_resp_{4}.fif'.format(subj, parameter1, fr,  parameter3, planar)))
                temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_{3}_resp_{4}.fif'.format(subj, parameter1, fr, parameter4, planar)))
            else:
                temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_fb_cur_negative_evoked_{2}_resp_{3}.fif'.format(subj, parameter1, fr, planar)))
                temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_fb_cur_positive_evoked_{2}_resp_{3}.fif'.format(subj, parameter1, fr, planar)))
        if parameter3 == None:
            if response:
                temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_beta_16_30_trf_early_log_resp_{3}.fif'.format(subj, parameter1, fr, planar)))
                temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_beta_16_30_trf_early_log_resp_{3}.fif'.format(subj, parameter2, fr, planar)))
            else:
                temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_resp_{2}.fif'.format(subj, parameter1, planar)))
                temp2 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_resp_{2}.fif'.format(subj, parameter2, planar)))
        contr[ind, 0, :, :] = temp1.data
        contr[ind, 1, :, :] = temp2.data
    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]
    t_stat, p_val = stats.ttest_rel(comp2, comp1, axis=0)
    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    return t_stat, p_val, comp1_mean, comp2_mean

#############################################################################
##################### непарный ttest #######################################	
def ttest_vs_zero(data_path, subjects, fr, parameter1, planar, n): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 1, 102, n))
    for ind, subj in enumerate(subjects):
        temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_beta_16_30_trf_no_log_division_resp_{2}.fif'.format(subj,  parameter1, planar)))
        contr[ind, 0, :, :] = temp1.data[:, :]
    comp1 = contr[:, 0, :, :]
    t_stat, p_val = stats.ttest_1samp(comp1, 0, axis=0)
    comp1_mean = comp1.mean(axis=0)
    return t_stat, p_val, comp1_mean	

##############################################################################################
#################################### FDR CORRECTION ########################################
def compute_p_val(response,data_path, subjects, cond1, cond2, parameter3, parameter4, fr, time, t, idx_array):
    #do ttests for subjects and compute p-values P062_risk_evoked_positive_beta_12_20_resp_comb_planar.fif
    #t = 1051
    #contr = np.zeros((len(subjects), 2, 102, int(time.shape[0])))
    contr = np.zeros((len(subjects), 2, 102, t))
    print(time[0])
    print(round(time[-1], 1))
    print(time.shape)
    for ind, subj in enumerate(subjects):
        if parameter3 == None:
            if response:
            #response TODO FREQ+Range
                cond1_fname = data_path + f'{subj}_{cond1}_evoked_beta_16_30_trf_no_log_division_resp_comb_planar.fif'
                cond2_fname = data_path + f'{subj}_{cond2}_evoked_beta_16_30_trf_no_log_division_resp_comb_planar.fif'
            else:
            #stimulus
                cond1_fname = data_path + f'{subj}_{cond1}_evoked_beta_16_30_resp_comb_planar.fif'
                cond2_fname = data_path +  f'/{subj}_{cond2}_evoked_beta_16_30_resp_comb_planar.fif'
            print(cond1_fname)
        if parameter3 == 'negative':
            if response:
                cond1_fname = data_path + f'{subj}_{cond1}_evoked_{fr}_{parameter3}_resp_comb_planar.fif'
                cond2_fname = data_path + f'{subj}_{cond1}_evoked_{fr}_{parameter4}_resp_comb_planar.fif'
            else:
                cond1_fname = data_path + f'{subj}_{cond1}_fb_cur_{parameter3}_evoked_beta_16_30_resp_comb_planar.fif'
                cond2_fname = data_path + f'{subj}_{cond1}_fb_cur_{parameter4}_evoked_beta_16_30_resp_comb_planar.fif'
            print(cond1_fname)
            print(cond2_fname)
        #here we remove the edges with artifacts
        temp1 = mne.Evoked(cond1_fname, verbose = 'ERROR').pick_types("grad").crop(tmin = time[0], tmax = round(time[-1], 1))
        temp2 = mne.Evoked(cond2_fname, verbose = 'ERROR').pick_types("grad").crop(tmin = time[0], tmax = round(time[-1], 1))
        contr[ind, 0, :, :] = temp1.data
        contr[ind, 1, :, :] = temp2.data
    comp1_before = contr[:, 0, :, :]
    comp2_before = contr[:, 1, :, :]
    comp1 = np.zeros((len(subjects), 102, len(time)))
    comp2 = np.zeros((len(subjects), 102, len(time)))
    #use idx array to resample the data for further stat
    for i, idx in enumerate(idx_array):
        i = int(i)
        idx = int(idx)
        comp1[:, :, i] = comp1_before[:, :, idx]
        comp2[:, :, i] = comp2_before[:, :, idx]
    #p_val over subjects
    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)

    #average the  data over subjects
    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    return comp1_mean, comp2_mean, p_val
     
    print(time.shape)
def plot_stat_comparison(response, path, comp1, comp2, p_mul_min, p_mul_max, p_val, p_fdr, parameter3, time, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2'):
    assert(comp1.shape[0] == comp2.shape[0] == time.shape[0])
    os.makedirs(path+'output/'+ f'{comp1_label}_vs_{comp2_label}/', exist_ok = True)
    print(path)
    plt.figure()
    plt.rcParams['axes.facecolor'] = 'none'
    plt.xlim(time[0], time[-1])
    plt.xticks(np.arange(-1.0,3.0, 1))
    plt.ylim(p_mul_min, p_mul_max)
    #add axis for stimulus-locked data
    plt.plot([0, 0.001], [-50, 50], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([-50, 50], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
    if response:
        #add FB axis if response-locked data
        plt.plot([1, 1.001], [-50, 50], color='k', linewidth=3, linestyle='--', zorder=1)
    if parameter3 == None:
        plt.plot(time, comp1, color='r', linewidth=3, label=comp1_label)
        plt.plot(time, comp2, color='b', linewidth=3, label=comp2_label)
    if parameter3 == 'negative':
        plt.plot(time, comp1, color='r', linewidth=3, label=comp1_label)
        plt.plot(time, comp2, color='b', linewidth=3, label=comp2_label)
    plt.fill_between(time, y1 = p_mul_min, y2 = p_mul_max, where = (p_fdr < 0.05), facecolor = 'm', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul_min, y2 = p_mul_max, where = ((p_val < 0.05) * (p_fdr > 0.05)), facecolor = 'g', alpha = 0.46, step = 'pre')
    # plt.fill_between(time, y1 = p_mul_max, y2 = p_mul_min, where = ((time>-0.350)*(time<-0.050)), facecolor = 'm', alpha = 0.46, step = 'pre')
    plt.tick_params(labelsize = 40)
    #plt.legend(loc='lower left', fontsize = 25)
    plt.title(title, fontsize = 40)
    plt.savefig(path+'output/'+ f'{comp1_label}_vs_{comp2_label}/'+title + '.png', transparent=True)
    plt.close()
#############################################################################
##################### непарный ttest #######################################
def ttest_vs_zero(data_path, subjects, parameter1, freq_range, planar, n): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 1, 102, n))

    for ind, subj in enumerate(subjects):
        temp1 = mne.Evoked(op.join(data_path, '{0}_{1}_evoked_{2}_resp_{3}.fif'.format(subj, parameter1, freq_range, planar)))
        contr[ind, 0, :, :] = temp1.data

    comp1 = contr[:, 0, :, :]
    t_stat, p_val = stats.ttest_1samp(comp1, 0, axis=0)

    comp1_mean = comp1.mean(axis=0)
                                       
    return t_stat, p_val, comp1_mean

def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

def add_pic_time_course_html(filename, pic, pic_folder, pos_n, size):
    x = size[0]
    y = size[1]
    print('in: add_pic_time_course_html', pic)
    print('PIC FOLDER + pic', pic_folder + '/' + pic)
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC=" %s" />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+ pic))
        
############ space FDR for each sensor independently ######################################
def space_fdr(p_val_n):
    #print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    for i in range(temp.shape[1]):
        _, temp[:,i] = mul.fdrcorrection(p_val_n[:,i])
    return temp


################## Full FDR -the correction is made once for the intire data array ############
def full_fdr(p_val_n):
    s = p_val_n.shape
    #print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    pval = np.ravel(temp)
    _, pval_fdr = mul.fdrcorrection(pval)
    pval_fdr_shape = pval_fdr.reshape(s)
    return pval_fdr_shape

################ make binary dataframe from pvalue (0 or 1) #########################
def p_val_binary(p_val_n, treshold):
	p_val =  copy.deepcopy(p_val_n)
	for raw in range(p_val.shape[0]):
		for collumn in range(p_val.shape[1]):
			if p_val[raw, collumn] < treshold:
				p_val[raw, collumn] = 1
			else:
				p_val[raw, collumn] = 0
	return p_val


###########################################################################################################
######################################### PLOT TOPOMAPS  ################################################

###################### строим topomaps со статистикой, для разницы между условиями #########################
# temp - donor (see "temp1" in def ttest_pair)
# mean1, mean2 - Evoked average between subjects (see def ttest_pair)
# average - averaging in mne.plot_topomaps

def plot_deff_topo(p_val, temp, mean1, mean2, time_to_plot, title): 	
    #Если мы будем использовать донор Evoked из тех, которые усредняются, то время и так будет то, которое необходимо, тогда менять время нет необходимости и присваиваем только новые данные (see temp.data)
    '''
	temp.first = -206
	temp.last = 1395

	temp.times = np.arange(-0.206, 1.395, 0.001)
    '''
	
    binary = p_val_binary(p_val, treshold = 0.05)
    temp.data = mean2 - mean1

	#temp_shift = temp.shift_time(-0.600, relative=False)
	
    fig1 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.2, units = 'dB', show = False, time_unit='s', title = title);
    fig2 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.2, units = 'dB', show = False, vmin = -1.2, vmax = 1.2, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',			markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))



    return fig1, fig2, temp # temp - "Evoked" for difference mean1 and mean2, which can be save if it is needed   

###################### строим topomaps со статистикой, для разницы между условиями #########################

def plot_topo_vs_zero(p_val, temp, mean1, time_to_plot, title): 	
    #Если мы будем использовать донор Evoked из тех, которые усредняются, то время и так будет то, которое необходимо, тогда менять время нет необходимости и присваиваем только новые данные (see temp.data)
    '''
	temp.first = -206
	temp.last = 1395

	temp.times = np.arange(-0.206, 1.395, 0.001)
    '''
	
    binary = p_val_binary(p_val, treshold = 0.05)
    temp.data = mean1

	#temp_shift = temp.shift_time(-0.600, relative=False)
	
	#fig1 = temp.plot_topomap(times = time_to_plot, ch_type='planar1', average=0.2, show = False,  vmin = -5.0, vmax = 5.0, time_unit='ms', title = title);
    fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, average=0.2, units = 'dB', show = False, vmin = -4.5, vmax = 4.5, time_unit='s', title = title, colorbar = True, extrapolate = "local", mask = np.bool_(binary), mask_params = dict(marker='o',		markerfacecolor='white', markeredgecolor='k', linewidth=0, markersize=7, markeredgewidth=2))



    return fig, temp # temp - "Evoked" , which can be save if it is needed   

########################################################################          
##############  empty topomaps line (without color) ##################



# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
n = 17 # количество говов в ряду

# задаем временные точнки, в которых будем строить головы, затем мы присвоим их для донора (template)
times_array = np.array([-0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4])

def nocolor_topomaps_line (n, temp, times_array, template ):
  
    if template:
        df = np.zeros((102, n))
    else:
        df = np.zeros((102, 17))
    temp.data = df

    # задаем временные точки в которые мы будем строить головы
    temp.times = times_array

    return temp        

