import mne
import os
import os.path as op
import numpy as np
from function import make_beta_signal

from function import make_fix_cross_signal
from function import make_response_signal
from function import make_fix_cross_signal_baseline
from function import make_response_signal_baseline

L_freq = 4
H_freq = 8
f_step = 1

period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)



subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'risk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS', exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE', exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS_BASELINE', exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE_BASELINE', exist_ok = True)
for subj in subjects:
    for r in rounds:
        for cond in trial_type:
            try:
                epochs_tfr_fix_cross = make_fix_cross_signal(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline)
                epochs_tfr_response = make_response_signal(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline)
                epochs_tfr_fix_cross_baseline = make_fix_cross_signal_baseline(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline)
                epochs_tfr_response_baseline = make_response_signal_baseline(subj, r, cond, data_path, L_freq, H_freq, f_step, period_start, period_end, baseline)
                epochs_tfr_fix_cross.save('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS/{0}_run{1}_{2}_fb_cur_theta_4_8-epo.fif'.format(subj, r, cond), overwrite=True)
                epochs_tfr_response.save('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE/{0}_run{1}_{2}_fb_cur_theta_4_8-epo.fif'.format(subj, r, cond), overwrite=True)
                epochs_tfr_fix_cross_baseline.save('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS_BASELINE/{0}_run{1}_{2}_fb_cur_theta_4_8-epo.fif'.format(subj, r, cond), overwrite=True)
                epochs_tfr_response_baseline.save('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE_BASELINE/{0}_run{1}_{2}_fb_cur_theta_4_8-epo.fif'.format(subj, r, cond), overwrite=True)
            except (OSError):
               print('This file not exist')


