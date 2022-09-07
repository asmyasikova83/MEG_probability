import mne
import os
import os.path as op
import numpy as np
from function import make_beta_signal
from config import *

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
print(subjects)
rounds = [1, 2, 3, 4, 5, 6]
#rounds = [6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']
feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
assert(not Normals_Autists)

prefix = '_ignore_train'

if Autists:
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists_extended'
if Normals:
    #subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended'

os.makedirs('/{0}/{1}{2}_classical_bline'.format(prefix_data, freq_range, prefix), exist_ok = True)
os.makedirs('/{0}/{1}{2}_classical_bline/{1}_epo'.format(prefix_data, freq_range, prefix), exist_ok = True)
########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "time_bandwidth = {}".format(time_bandwidth), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]

config_name = "/{0}/{1}{2}_classical_bline/{1}_epo/config.txt".format(prefix_data, freq_range, prefix)

with open(config_name, "w") as file:
#with open("/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_epo/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################

print(subjects)

for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_tfr = make_beta_signal(prefix_events, prefix, subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = time_bandwidth)
                    epochs_tfr.save('/{0}/{1}{2}_classical_bline/{1}_epo/{3}_run{4}_{5}_fb_cur_{6}_{1}_epo.fif'.format(prefix_data, freq_range, prefix, subj, r, cond, fb), overwrite=True)
                except (OSError):
                    print('This file not exist')



