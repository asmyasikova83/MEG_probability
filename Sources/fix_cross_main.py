import mne
import os
import os.path as op
import numpy as np
from find_fix_cross import fixation_cross_events
from config import *

rounds = [1, 2, 3, 4, 5, 6]
#rounds = [4]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']

feedback = ['positive', 'negative']
#set type of sample - Autists or Normals with a list of subjects- in config

#prefix = '_not_trained'
prefix = '_ignore_train'

if Autists:
    #subjects = ['P342']
    data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/'
    raw_name = '{0}/{0}_run{1}_mio_free.txt'
    #data_path_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare/'
    #{subject}_run{r}_{trial_type}_fb_{fb}.txt'
    data_path_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio_list_compare{0}/'.format(prefix)
    name_events = '{0}_run{1}_{2}_fb_{3}.txt'
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr{0}/'.format(prefix), exist_ok = True)
if Normals:
    #subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    data_path_raw = '/net/server/data/Archive/prob_learn/data_processing/mio_free_events/'
    raw_name = '{0}/{0}_run{1}_mio_free.txt'
    #data_path_raw = '/net/server/data/home/inside/Events_probability/Events_clean'
    #raw_name = '{0}_run{1}_events_clean.txt'
    #data_path_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_mio_list_compare/'
    data_path_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/Events_mio_list_compare{0}/'.format(prefix)
    name_events = '{0}_run{1}_{2}_fb_{3}.txt'
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/fix_cross_mio_corr{0}/'.format(prefix), exist_ok = True)


for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                
                try:
                    event_fixation_cross_norisk = fixation_cross_events(data_path_raw, raw_name, data_path_events, name_events, subj, r, t, fb)
                    if Autists:
                        f = "/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr{0}/{1}_run{2}_{3}_fb_cur_{4}_fix_cross.txt".format(prefix, subj, r, t, fb)
                        np.savetxt("/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr{0}/{1}_run{2}_{3}_fb_cur_{4}_fix_cross.txt".format(prefix, subj, r, t, fb), event_fixation_cross_norisk, fmt="%s")
                    if Normals:
                        f = "/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/fix_cross_mio_corr{0}/{1}_run{2}_{3}_fb_cur_{4}_fix_cross.txt".format(prefix, subj, r, t, fb)
                        np.savetxt("/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals/fix_cross_mio_corr{0}/{1}_run{2}_{3}_fb_cur_{4}_fix_cross.txt".format(prefix, subj, r, t, fb), event_fixation_cross_norisk, fmt="%s")
                    print('Saved!')
                except OSError:
                   print('This file not exist')
                    

                    
                    
