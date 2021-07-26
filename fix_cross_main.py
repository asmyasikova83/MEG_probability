import mne
import os
import os.path as op
import numpy as np
from function import fixation_cross_events, read_events


subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

rounds = [1, 2, 3, 4, 5, 6]


trial_type = ['risk']
#trial_type = ['norisk']

feedback = ['positive', 'negative']
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross', exist_ok = True)

data_path_raw = '/net/server/data/home/inside/Events_probability/Events_clean'
raw_name = '{0}_run{1}_events_clean.txt'
data_path_events = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected'
name_events = '{0}_run{1}_{2}_fb_cur_{3}.txt' 

for subj in subjects:
    for r in rounds:
    
        for t in trial_type:
            for fb in feedback:
                
                try:
                    event_fixation_cross_norisk = fixation_cross_events(t, data_path_raw, raw_name, data_path_events, name_events, subj, r, fb)
                    event_fixation_cross_risk = fixation_cross_events(t, data_path_raw, raw_name, data_path_events, name_events, subj, r, fb)
                    event_fixation_cross_prerisk = fixation_cross_events(t, data_path_raw, raw_name, data_path_events, name_events, subj, r, fb)
                    event_fixation_cross_postrisk = fixation_cross_events(t, data_path_raw, raw_name, data_path_events, name_events, subj, r, fb)
                    np.savetxt('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt'.format(subj, r, t, fb), 
                               event_fixation_cross_risk, fmt="%s")
                    np.savetxt('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt'.format(subj, r, t, fb), 
                               event_fixation_cross_prerisk, fmt="%s")
                    np.savetxt('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/events_fix_cross/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt'.format(subj, r, t, fb), 
                               event_fixation_cross_postrisk, fmt="%s")
                except OSError:
                   print('This file not exist')
                    

                    
                    
