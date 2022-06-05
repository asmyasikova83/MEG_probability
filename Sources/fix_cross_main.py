import mne
import os
import os.path as op
import numpy as np
from find_fix_cross import fixation_cross_events

rounds = [1, 2, 3, 4, 5, 6]


#rial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['norisk']

feedback = ['positive', 'negative']
#set type of sample - Autists or Normals with a list of subjects- in config

if Autists:
    data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/'
    raw_name = '{0}/{0}_run{1}_mio_free.txt'
    data_path_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare/'
    name_events = '{0}_run{1}_norisk_fb_{2}.txt' 
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr/', exist_ok = True)
if Normals:
    subjects = ['P063', 'P064', 'P065', 'P066']
    data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/mio_free_events/'
    raw_name = '{0}/{0}_run{1}_mio_free.txt'
    data_path_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_mio_list_compare/'
    name_events = '{0}_run{1}_norisk_fb_{2}.txt' 
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/fix_cross_mio_corr/', exist_ok = True)


for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                
                try:
                    event_fixation_cross_norisk = fixation_cross_events(data_path_raw, raw_name, data_path_events, name_events, subj, r, fb)
                    if Autists:
                        f = "/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt".format(subj, r, t, fb)
                        np.savetxt("/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt".format(subj, r, t, fb), event_fixation_cross_norisk, fmt="%s")
                    if Normals:
                        f = "/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/fix_cross_mio_corr/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt".format(subj, r, t, fb)
                        np.savetxt("/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/fix_cross_mio_corr/{0}_run{1}_{2}_fb_cur_{3}_fix_cross.txt".format(subj, r, t, fb), event_fixation_cross_norisk, fmt="%s")
                    print('Saved!')
                    print(f)
                except OSError:
                   print('This file not exist')
                    

                    
                    
