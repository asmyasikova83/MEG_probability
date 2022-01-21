
import mne
import os
import os.path as op
import numpy as np
from make_freq_stim import make_beta_signal, read_events_N
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

description = 'Усреденение от стимула /n Выделяем частоты и при корректировке на бейзлайн, каждое значение данных делим на бейзлайн, но без логарифмирования. Логарифмирование проводим на последних этапах: перед рисованием, либо перед статистикой'

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]


#rounds = [5]
rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']
feedback = ['positive', 'negative']
#feedback = ['positive']

prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83'
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('{0}/stim_check/{1}'.format(prefix, freq_range), exist_ok = True)
os.makedirs('{0}/stim_check/{1}/{1}_epo'.format(prefix, freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "time_bandwidth = {}".format(time_bandwidth), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open('{0}/stim_check/{1}/{1}_epo/config.txt'.format(prefix, freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################

#we make signals for trial types irrespective of the feedback sign
for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    eve_pos = []
                    eve_neg = []
                    events_of_interest = []
                    data_path1 = '{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_positive_fix_cross.txt'.format(prefix, subj, r, cond)
                    if exists(data_path1):
                        eve_pos = np.loadtxt('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_positive_fix_cross.txt'.format(prefix, subj, r, cond), dtype='int')
                        print(eve_pos)
                    elif os.path.exists('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_negative_fix_cross.txt'.format(prefix, subj, r, cond)):
                        events_of_interest = np.loadtxt('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_negative_fix_cross.txt'.format(prefix, subj, r, cond), dtype='int')
                    else:
                        print('Empty trial!')
                        continue
                    print(events_of_interest)
                    if os.path.exists('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_negative_fix_cross.txt'.format(prefix, subj, r, cond)):
                        eve_neg = np.loadtxt('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_negative_fix_cross.txt'.format(prefix, subj, r, cond), dtype='int')
                    elif os.path.exists('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_positive_fix_cross.txt'.format(prefix, subj, r, cond)):
                        events_of_interest = np.loadtxt('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_positive_fix_cross.txt'.format(prefix, subj, r, cond), dtype='int')
                    else:
                        print('Empty trial')
                        continue
                    if len(eve_pos) != 0 and len(eve_neg) != 0:
                        events = np.vstack([eve_pos, eve_neg])
                        events_of_interest = np.sort(events, axis = 0)
                        print('in both', events_of_interest)
                    if len(eve_pos) != 0 or len(eve_neg) != 0:
                        if len(eve_pos) != 0:
                            events_of_interest = eve_pos
                        if len(eve_neg) != 0:
                            events_of_interest = eve_neg
                    if len(events_of_interest) == 0:
                        continue
                    else:
                        if events_of_interest.shape == (3,):
                            events_of_interest = events_of_interest.reshape(1,3)
                    print(events_of_interest)
                    tfr_stim = make_beta_signal(subj, r, cond, fb, data_path, events_of_interest, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = time_bandwidth)
                    if tfr_stim == 0:
                        continue
                    else:
                        tfr_stim.save('{0}/stim_check/{1}/{1}_epo/{2}_run{3}_{4}_{1}_epo.fif'.format(prefix, freq_range, subj, r, cond))
                except (OSError):
                    print('This file not exist')

