import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

###############################################################################################
######## File with events was made by Lera, you need this function for reading it #############

def read_events(filename):
    with open(filename, "r") as f:
        b = f.read().replace("[","").replace("]", "").replace("'", "")
        b = b.split("\n")
        b = list(map(str.split, b))
        b = list(map(lambda x: list(map(int, x)), b))
        return np.array(b[:])

#####################################################################################
######## Функция для поиска меток фиксационного креста (по ним ищется baseline)######

def fixation_cross_events(data_path_raw, raw_name, data_path_events, name_events, subj, r, fb):
    
    # для чтения файлов с events используйте либо np.loadtxt либо read_events либо read_events_N
    print(op.join(data_path_events, name_events.format(subj, r, fb)))
    no_risk = np.loadtxt(op.join(data_path_events, name_events.format(subj, r, fb)), dtype='int')
    print(no_risk) 
    #no_risk = read_events(op.join(data_path_events, name_events.format(subj, r)))
    
    # Load raw events without miocorrection
    events_raw = read_events(op.join(data_path_raw, raw_name.format(subj, r)))        
    print(events_raw) 
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
    print(event_fixation_cross_norisk) 
    return(event_fixation_cross_norisk)


###################################################################################################################
# функция получения эпох с выделенными частотами с применение раннего логарифмирования, сразу после сложения частот
def make_beta_signal(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = 4):
    freqs = np.arange(L_freq, H_freq, f_step)
    #read events
	#events for baseline
	# download marks of positive feedback
    events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/fix_cross_mio_corr_prev_pos/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int')
    print(events_pos)
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_pos.shape == (3,):
        events_pos = events_pos.reshape(1,3)
        
    # download marks of negative feedback      
    events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/fix_cross_mio_corr_prev_pos/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
    
    print(events_neg)
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводим shape к виду (N,3)
    if events_neg.shape == (3,):
        events_neg = events_neg.reshape(1,3) 
    
    #объединяем негативные и позитивные фидбеки для получения общего бейзлайна по ним, и сортируем массив, чтобы времена меток шли в порядке возрастания    
    events = np.vstack([events_pos, events_neg])
    events = np.sort(events, axis = 0) 
    #events, which we need
    events_response = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/mio_cond_prev_fb_pos/Events_mio/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), dtype='int')
    print('all events response', events_response)
    #events_response = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/mio_cond_prev_fb_pos/Events_mio/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), dtype='int')

    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    print(events_response) 
    #fromm events_response pick only early 10 trials to pinpoint novelty
    counter = 0
    short_ev_resp = []
    for e in events_response:
        short_ev_resp.append(e)
        counter = counter + 1
        if counter == 10:
             break
        else:
             pass
    events_response = short_ev_resp
    print('events_resp', events_response)
    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

    raw_data = mne.io.Raw(raw_fname, preload=True)
        
    
    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		    
	   	    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)
    
        
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	    
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
		       
    epochs.resample(300) 

    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, average=False)

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
        
    #freq_show.data = freq_show.data[:, :, np.newaxis, :]
        
    #33 is an arbitrary number. We have to set some frequency if we want to save the file
    freq_show.freqs = np.array([33])
        
    #getting rid of the frequency axis	
    freq_show.data = freq_show.data.mean(axis=2) 
        
    epochs_tfr = mne.EpochsArray(freq_show.data, freq_show.info, tmin = period_start, events = events_response)
        
    return (epochs_tfr)   
    
    

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


