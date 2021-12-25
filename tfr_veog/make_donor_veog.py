import os.path as op
import numpy as np
import mne
from mne.time_frequency import psd_multitaper
import os

def make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs, meg = True):
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
    picks = mne.pick_types(raw_data.info, misc = True)		    
    #epochs for baseline
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
    epochs.resample(300)
    # time_bandwidth = 4 , by default
    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, picks= ['MISC301']).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
    # логарифмируем данные для бейзлайн и получаем бейзлайн в дБ
    b_line = 10*np.log10(freq_show_baseline.data)
	####### ДЛЯ ДАННЫХ ##############
    # baseline = None, чтобы не вычитался дефолтный бейзлайн
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
		                tmax = period_end, baseline = None, picks = picks, preload = True)
    epochs.resample(300) 
    # time_bandwidth = 4 , by default
    freq_show = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, time_bandwidth = time_bandwidth, use_fft = False, return_itc = False, picks= ['MISC301']).crop(tmin = -1.000, tmax = 2.100)
    data = 10*np.log10(freq_show.data)
	
	####### Для данных так же меняем оси местами
	# Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
    b = b_line.mean(axis=-1)
    b_line_new_shape = b[:, :, np.newaxis]
    #Вычитаем бейзлайн из данных и приводим оси к изначальному порядку
    
    data = data - b_line_new_shape
    freq_show.data = data
    
    return (freq_show)

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
L_freq = 2
H_freq = 41
f_step = 2

freqs = np.arange(L_freq, H_freq, f_step)

# if delta (1 - 4 Hz) 
#n_cycles = np.array([1, 1, 1, 2])

#for others
n_cycles = freqs//2

period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)

time_bandwidth = 4 #(4 by default)

freq_range = '2_40_step_2_time_bandwidth_by_default_4_early_log'

subjects = ['P001']
rounds = [2]
trial_type = ['risk']
feedback = ['negative']
os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/', exist_ok = True)

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    evoked_tfr_h5 = make_h5_files(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth, freqs)
                    print(evoked_tfr_h5)
                    evoked_tfr_h5.save('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/donor_evoked.h5'.format(freq_range, subj, r, cond, fb), overwrite=True)
                    print('Saved!')
                except (OSError):
                    print('This file not exist')

