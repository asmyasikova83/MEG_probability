import mne
import os
import os.path as op
import numpy as np
from function import make_beta_signal


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

subjects_bk = ['P301', 'P304', 'P307',  'P309',  'P312', 'P313', 'P314',
            'P316', 'P322',  'P323', 'P324', 'P325',
            'P326', 'P329', 'P331',  'P333', 'P334',
            'P336', 'P340']
#subjects = ['P341']
subjects = ['P301', 'P304', 'P307', 'P308', 'P311', 'P312', 'P313', 'P314', 'P316', 'P318', 'P320', 'P321', 'P322',
            'P323', 'P324', 'P325', 'P326', 'P327', 'P328', 'P329', 'P330', 'P331', 'P332', 'P333', 'P334', 'P335',
            'P336', 'P338', 'P341']
subjects.remove('P328') #bad segmentation
subjects.remove('P327') #no bem
subjects.remove('P341') #no mri

rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}'.format(freq_range), exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_epo'.format(freq_range), exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = ["freq_range = {}".format(freq_range), description, "L_freq = {}".format(L_freq), "H_freq = {}, в питоне последнее число не учитывается, т.е. по факту частота (H_freq -1) ".format(H_freq), "f_step = {}".format(f_step), "time_bandwidth = {}".format(time_bandwidth), "period_start = {}".format(period_start), "period_end = {}".format(period_end), "baseline = {}".format(baseline)]


with open("/net/server/data/Archive/prob_learn//asmyasnikova83/Autists/{0}/{0}_epo/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################


for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    epochs_tfr = make_beta_signal(subj, r, cond, fb, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline, n_cycles, time_bandwidth = time_bandwidth)
                    epochs_tfr.save('/net/server/data/Archive/prob_learn//asmyasnikova83/Autists/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}_epo.fif'.format(freq_range, subj, r, cond, fb), overwrite=True)
                except (OSError):
                    print('This file not exist')


