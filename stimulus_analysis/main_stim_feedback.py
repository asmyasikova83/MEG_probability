
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

prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83'

description = 'Усреденение от стимула /n Выделяем частоты и при корректировке на бейзлайн, каждое значение данных делим на бейзлайн, но без логарифмирования. Логарифмирование проводим на последних этапах: перед рисованием, либо перед статистикой'

subjects = []
for i in range(35,36):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]


#rounds = [5]
rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']
feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('{0}/stim_check/{1}_feedback'.format(prefix, freq_range), exist_ok = True)
os.makedirs('{0}/stim_check/{1}_feedback/{1}_epo'.format(prefix, freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "time_bandwidth = {}".format(time_bandwidth), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open('{0}/stim_check/{1}_feedback/{1}_epo/config.txt'.format(prefix, freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################

#we make signals for trial types irrespective of the feedback sign
for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    events_of_interest = []
                    data_path1 = '{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_{4}_fix_cross.txt'.format(prefix, subj, r, cond, fb)
                    print(data_path1)
                    if exists(data_path1):
                        events_of_interest = np.loadtxt('{0}/fix_cross_mio_corr/{1}_run{2}_{3}_fb_cur_{4}_fix_cross.txt'.format(prefix, subj, r, cond, fb), dtype='int')
                    else:
                        print('Empty trial!')
                        continue
                    #for cases when the list of events [], needs special processing
                    if len(events_of_interest) == 0:
                        continue
                    else:
                        if events_of_interest.shape == (3,):
                            events_of_interest = events_of_interest.reshape(1,3)
                    tfr_stim = make_beta_signal(subj, r, cond, fb, data_path, events_of_interest, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = time_bandwidth)
                    #for cases when norisk is empty
                    if tfr_stim == 0:
                        continue
                    else:
                        tfr_stim.save('{0}/stim_check/{1}_feedback/{1}_epo/{2}_run{3}_{4}_fb_cur_{4}_{1}_epo.fif'.format(prefix, freq_range, subj, r, cond, fb))
                        #tfr_stim.save('/net/server/data/Archive/prob_learn/asmyasnikova83/stim_check/{0}_feedback/{0}_epo/{1}_run{2}_{3}_{0}_epo.fif'.format(freq_range, subj, r, cond))
                except (OSError):
                    print('This file not exist')

