import mne
import os
import os.path as op
import numpy as np
from tools import prev_feedback, read_events
from config import *



freq_range = 'beta_16_30_trf_early_log_stim'
if Autists:
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists_extended'
    '/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/'
if Normals:
    subjects = ['P063', 'P064', 'P065', 'P066', 'P067']
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended'

os.makedirs('/{0}/prev_fb_mio_corrected'.format(prefix_events, freq_range), exist_ok = True)

FB = [50, 51, 52, 53]   

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'

for subj in subjects:
    for r in rounds:
        for t in trial_type:
            for fb in feedback:
                try:
                    tials_of_interest = np.loadtxt('/{0}/Events_mio_list_compare/{1}_run{2}_{3}_fb_{4}.txt'.format(prefix_events, subj, r, t, fb), dtype='int')
                    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
                    if tials_of_interest.shape == (3,):
                        tials_of_interest = tials_of_interest.reshape(1,3)
                
                        # Load raw event with miocorection
                    if Normals:
                        #for P001 - P062
                        #events_raw = read_events('/net/server/data/home/inside/Events_probability/Events_clean/{0}_run{1}_events_clean.txt'.format(subj, r))
                        #events_raw =np.loadtxt('/net/server/data/home/inside/Events_probability/Events_clean/{0}_run{1}_events_clean.txt'.format(subj, r))
                        #for P063-P067 and Autists
                        events_raw =np.loadtxt('/net/server/data/Archive/prob_learn/data_processing/mio_free_events/{0}/{0}_run{1}_mio_free.txt'.format(subj, r), dtype='int')
                    if Autists:
                        #events_raw = read_events('/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/{0}/{0}_run{1}_mio_free.txt'.format(subj, r))
                        events_raw =np.loadtxt('/net/server/data/Archive/prob_learn/data_processing/Autists/mio_free_events/{0}/{0}_run{1}_mio_free.txt'.format(subj, r), dtype='int')
                    prev_fb = prev_feedback(events_raw, tials_of_interest, FB)    
                    np.savetxt("/{0}/prev_fb_mio_corrected/{1}_run{2}_{3}_fb_cur_{4}_prev_fb.txt".format(prefix_events, subj, r, t, fb), prev_fb, fmt="%s")
                    
                except OSError:
                    print('This file not exist')    
   
