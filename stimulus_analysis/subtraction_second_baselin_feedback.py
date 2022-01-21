#на вход подаются данные скорректированные на бейслайн первый раз делением, без логорифмирования (при выделении частот)

import mne
import os
import os.path as op
import numpy as np
from os.path import exists

L_freq = 16
H_freq = 31
f_step = 2

time_bandwidth = 4 #(by default = 4)
# if delta (1 - 4 Hz) 
#n_cycles = np.array([1, 1, 1, 2]) # уточнить

#for others
freqs = np.arange(L_freq, H_freq, f_step)
n_cycles = freqs//2

period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)

freq_range = 'beta_16_30_trf_no_log_division_stim'
prefix_vera = '/net/server/data/Archive/prob_learn/vtretyakova'
prefix_sasha = '/net/server/data/Archive/prob_learn/asmyasnikova83'

description = 'Усредение от реакции. Выделяем частоты и при корректировке на бейзлан, каждое значение данных делим на бейзлан, но без логарифмирования. Логарифмирование проводим на последних этапах: перед рисованием, либо перед статистикой'

subjects = []
for i in range(35,36):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]
#rounds = [5]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']
feedback = ['positive', 'negative']
#feedback = ['positive']

data_path = '{0}/ICA_cleaned'.format(prefix_vera)
os.makedirs('{0}/stim_check/{1}_feedback/{1}_second_bl_epo'.format(prefix_sasha, freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "time_bandwidth = {}".format(time_bandwidth), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open('{0}/stim_check/{1}_feedback/{1}_second_bl_epo/config.txt'.format(prefix_sasha, freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################


for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    #fix cross data from nolog bline step (for fb use fb_cur) 
                    print('{0}/stim_check/{1}_feedback/{1}_epo/{2}_run{3}_{4}_fb_cur_{5}_{1}_epo.fif'.format(prefix_sasha, freq_range, subj, r, cond, fb))
                    #print('/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/{0}/{0}_epo/{1}_run{2}_{3}_{0}_epo.fif'.format(freq_range, subj, r, cond))
                    epochs_tfr = mne.read_epochs('{0}/stim_check/{1}_feedback/{1}_epo/{2}_run{3}_{4}_fb_cur_{5}_{1}_epo.fif'.format(prefix_sasha, freq_range, subj, r, cond, fb), preload = True)    
                    #epochs_tfr = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/{0}/{0}_epo/{1}_run{2}_{3}_{0}_epo.fif'.format(freq_range, subj, r, cond), preload = True)    
                    data = epochs_tfr.get_data()         
                    # логарифмируем и умножаем на 10 для перевода в дБ
                    data_dB = 10*np.log10(data)
                    
                    # меняем оси местами, чтобы первыми шли сенсоры
                    data_dB = np.swapaxes(data_dB, 0, 1)
                    data_dB = np.swapaxes(data_dB, 1, 2)
                    
                    
                    # подготавливаем бейзлан для вычитания
                    freqs = np.arange(L_freq, H_freq, f_step)
    
                    #read events
	            #events for baseline
	            # download marks of positive and negative feedback, if exist
                    events_pos = []
                    events_neg = []
                    events = []
                    if exists('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_positive_fix_cross.txt'.format(prefix_vera, subj, r)):
                        events_pos = np.loadtxt('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_positive_fix_cross.txt'.format(prefix_vera, subj, r), dtype='int')
                    elif os.path.exists('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_negative_fix_cross.txt'.format(prefix_vera, subj, r)):
                         events = np.loadtxt('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_negative_fix_cross.txt'.format(prefix_vera, subj, r), dtype='int')
                    else:
                         print('norisk trials for bline not found')
                    if exists('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_negative_fix_cross.txt'.format(prefix_vera, subj, r)):
                        events_neg = np.loadtxt('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_negative_fix_cross.txt'.format(prefix_vera, subj, r), dtype='int')
                    elif exists('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_positive_fix_cross.txt'.format(prefix_vera, subj, r)):
                        events = np.loadtxt('{0}/Nikita_mio_cleaned/fix_cross_mio_corr/{1}_run{2}_norisk_fb_cur_positive_fix_cross.txt'.format(prefix_vera, subj, r), dtype='int')
                    else:
                        print('norisk trials for bline not found')
                    if len(events) != 0:
                        if events.shape == (3,):
                            events = events.reshape(1,3)
                    #combine both fb for blining
                    if len(events_pos) != 0 and len(events_neg) != 0:
                        if events_neg.shape == (3,):
                            events_neg = events_neg.reshape(1,3)
                        if events_pos.shape == (3,):
                            events_pos = events_pos.reshape(1,3)
                        events = np.vstack([events_pos, events_neg])
                        events = np.sort(events, axis = 0)
                    if len(events) == 0:
                        continue
                  	            
                    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))

                    raw_data = mne.io.Raw(raw_fname, preload=True)
                            
                        
                    picks = mne.pick_types(raw_data.info, meg = True, eog = True)
		                        
	                       	    
                    #epochs for baseline
                    # baseline = None, чтобы не вычитался дефолтный бейзлайн
                    epochs = mne.Epochs(raw_data, events, event_id = None, tmin = -1.0, tmax = 1.0, baseline = None, picks = picks, preload = True)
                    epochs.resample(300)

                    freq_show_baseline = mne.time_frequency.tfr_multitaper(epochs, freqs = freqs, n_cycles = n_cycles, use_fft = False, return_itc = False, average=False).crop(tmin=baseline[0], tmax=baseline[1], include_tmax=True) #frequency of baseline
	                        
                    #add up all values according to the frequency axis
                    b_line = freq_show_baseline.data.sum(axis=-2)
	                        
	            # Для бейзлайна меняем оси местами, на первом месте число каналов
                    b_line = np.swapaxes(b_line, 0, 1)
                            
                    # выстраиваем в ряд бейзлайны для каждого из эвентов, как будто они происходили один за другим
                    a, b, c = b_line.shape
                    b_line_ave = b_line.reshape(a, b * c)

                    # Усредняем бейзлайн по всем точкам, получаем одно число (которое будем вычитать из data для каждого канала)
	                        
                    b = b_line_ave.mean(axis=-1)
	                        
                    b_line_new_shape = b[:, np.newaxis, np.newaxis]    
                    #b_line_new_shape       
                
                    second_baseline = 10*np.log10(b_line/b_line_new_shape) # 10* - для перевода в дБ
                    
                    # усредняем между эпохами
                    second_baseline = second_baseline.mean(axis=-2)
                    
                    # усредняем между временными точками
                    second_baseline = second_baseline.mean(axis=-1)
                    
                    # Добавляем ось времени и эпох                    
                    second_baseline_new_shape = second_baseline[:, np.newaxis, np.newaxis]
                    
                    # корректируем данные на бейзлайн второй раз (вычитаем)
                    
                    data_second_bl = data_dB - second_baseline_new_shape
                    
                    data_second_bl = np.swapaxes(data_second_bl, 1, 2)
                    data_second_bl = np.swapaxes(data_second_bl, 0, 1)
                                       
                    
                    epochs_second_bl = mne.EpochsArray(data_second_bl, epochs_tfr.info, tmin = period_start, events = epochs_tfr.events)
                
                    epochs_second_bl.save('{0}/stim_check/{1}_feedback/{2}_second_bl_epo/{2}_run{3}_{4}_fb_cur_{5}_{1}_epo.fif'.format(prefix_sasha, freq_range, subj, r, cond, fb), overwrite=True)
                    #epochs_second_bl.save('/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/{0}/{0}_second_bl_epo/{1}_run{2}_{3}_{0}_epo.fif'.format(freq_range, subj, r, cond), overwrite=True)
                except (OSError):
                    print('This file not exist')
                
