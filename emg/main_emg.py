import mne
import os
import os.path as op
import numpy as np
from function import make_beta_signal_mio


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

freq_range = 'beta_16_30_trf_early_log'

description = 'И для данных и для бейзлайн логарифмирование проводим на самых ранных этапах - сразу после суммирования по частотам.'

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]
#rounds = [2]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk','risk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}'.format(freq_range), exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_epo'.format(freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "time_bandwidth = {}".format(time_bandwidth), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open("net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_epo/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################


for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_tfr = make_beta_signal_mio(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = time_bandwidth)
                    epochs_tfr.save('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}_epo.fif'.format(freq_range, subj, r, cond, fb), overwrite=True)
                except (OSError):
                    print('This file not exist')


