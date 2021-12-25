

import os
from scipy import stats, io
import re
import mne
import os.path as op
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul

###############################################################################################
######## function prepear .h5 files for tfr ploting ###########

def make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs):
        
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
        
    
    #picks = mne.pick_types(raw_data.info, meg = True, eog = True)
    picks = mne.pick_types(raw_data.info, misc = True)
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)
    print(epochs)
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles,  use_fft = False, return_itc = False, average=False, picks= ['MISC301']).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
      
	# Для бейзлайна меняем оси местами, на первом месте число каналов
    b_line = np.swapaxes(freq_show_baseline.data, 0, 1)
    b_line = np.swapaxes(b_line, 1, 2)
	
	# выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
    a, b, c, d = b_line.shape
    print(b_line.shape)
    b_line = b_line.reshape(a, b, c * d)

	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
		       
    epochs.resample(300) 

    freq_show =  mne.time_frequency.tfr_multitaper(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=False, return_itc = False,average = False, picks= ['MISC301']).crop(tmin = -1.000, tmax = 2.100)
    
	####### Для данных так же меняем оси местами
    data = np.swapaxes(freq_show.data, 0, 1)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 2, 3)
    print(data.shape)	
    # Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)
    b_line_new_shape = b[:, :, np.newaxis, np.newaxis]

    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    data = 10*np.log10(data/b_line_new_shape) # 10* - для перевода в дБ
    data = np.swapaxes(data, 2, 3)
    data = np.swapaxes(data, 1, 2)
    data = np.swapaxes(data, 0, 1)
    
    freq_show.data = data
    
    return (freq_show)
    
###############################################################################################    
############################ FUNCTION FOR TTEST ############################
######################### парный ttest #########################################    
    
def ttest_pair_veog(data_path, subjects, cond, parameter1, parameter2, freq, n): # n - количество временных отчетов
    contr = np.zeros((len(subjects), 2, 1, 20, n)) #20 - num of tapers
    print(data_path)
    print(subjects)
    for ind, subj in enumerate(subjects):
        temp1 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_{2}_resp_{3}.h5'.format(subj, cond, freq, parameter1)))[0]
        temp2 = mne.time_frequency.read_tfrs(op.join(data_path, '{0}_{1}_{2}_resp_{3}.h5'.format(subj, cond, freq, parameter2)))[0]
	    
        contr[ind, 0, :, :, :] = temp1.data
        contr[ind, 1, :, :, :] = temp2.data
        		        
		
    comp1 = contr[:, 0, :, :, :]
    comp2 = contr[:, 1, :, :, :]
    t_stat, p_val = stats.ttest_rel(comp2, comp1, axis=0)

    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
	
    return t_stat, p_val, comp1_mean, comp2_mean

###################### строим topomaps со статистикой, для разницы между условиями #########################
# donor creation see make_donor_for_tfr_plot.ipynb
# mean1, mean2 - tfr average between subjects (see def ttest_pair)

def plot_deff_tf_veog(p_val, donor, mean1, mean2, folder_out, title, treshold = 0.05): 	
	
    donor.data = mean2 - mean1
    #MISC301 - 327, MISC302 - 328
    fig = donor.plot(picks = 'MISC302', baseline=None, mode='logratio', title=title, combine = None, mask = p_val.mean(axis = 0 ) < treshold, mask_style = 'contour', show = False);
    
    return fig   







