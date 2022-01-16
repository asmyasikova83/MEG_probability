import mne
import os
import os.path as op
import numpy as np
import pandas as pd
import copy

    

def make_beta_signal_mio(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = 4):
    freqs = np.arange(L_freq, H_freq, f_step)
    
    #read events
	#events for baseline
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
    
    #events, which we need
    events_response = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    
	           
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
    print(raw_data)    
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True, emg = True, misc = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    #epochs.resample(300)
    
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False, picks= ['EMG064']).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
    #add up all values according to the frequency axis
    b_line = freq_show_baseline.data.sum(axis=-2)
    
    # логарифмируем данные для бейзлайн и получаем бейзлайн в дБ
    b_line = 10*np.log10(b_line)
	    
	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(b_line, 0, 1)
        
    # выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
    a, b, c = b_line.shape
    
    b_line_ave = b_line.reshape(a, b * c)

    # Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала) (то же самое если вместо смены осей усреднить сначала по времени, а потом по эпохам)
	                        
    b = b_line_ave.mean(axis=-1)
	                        
    b_line_new_shape = b[:, np.newaxis, np.newaxis]  
    

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
    print(epochs)		       
    #epochs.resample(300)
   
    #freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False)
    #cut off the edges to remove artifacts   
    freq_show =  mne.time_frequency.tfr_multitaper(epochs, freqs=freqs, n_cycles=n_cycles, time_bandwidth = time_bandwidth, use_fft=False, return_itc = False,average = False, picks= ['EMG064']).crop(tmin = -1.000, tmax = 2.100)
    print(freq_show)
    print(freq_show.data.shape)
    temp = freq_show.data.sum(axis=2)
    
    # логарифмируем данные и получаем данные в дБ
    temp = 10*np.log10(temp)
	    
	####### Для данных так же меняем оси местами
    data = np.swapaxes(temp, 0, 1)
    data = np.swapaxes(data, 1, 2)
	
	
    #Вычитаем из данных в дБ бейзлайн в дБ
    data_dB = data - b_line_new_shape 
    
    # меняем оси обратно   
    data_dB = np.swapaxes(data_dB, 1, 2)
    data_dB = np.swapaxes(data_dB, 0, 1)
    
            
    freq_show.data = data_dB[:, :, np.newaxis, :]
    print(freq_show.data.shape) 
    #freq_show.data = freq_show.data[:, :, np.newaxis, :]
        
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
    print(freq_show.data.shape) 
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = -1.000, events = events_response)
    print(epochs_tfr)
    return (epochs_tfr)   
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
    feedback_cur = [fb_cur]*len(mean_combined_planar)
    
    feedback_prev_data = np.loadtxt("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/prev_fb_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}_prev_fb.txt".format(subj, r, t, fb_cur), dtype='int')
    if feedback_prev_data.shape == (3,):
        feedback_prev_data = feedback_prev_data.reshape(1,3)
    
    FB_rew = [50, 51]
    FB_lose = [52, 53]

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


