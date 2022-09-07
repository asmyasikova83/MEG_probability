
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from mne import set_log_level
from tools import make_subjects_df
from config import *

freq_range = 'beta_16_30_trf_early_log'  

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

# interval of interest (1800 ms +/- 100 ms)
tmin = -0.9
tmax = 2.501
step = 0.2

prefix = '_ignore_train'

if Autists:
    scheme = pd.read_csv('/home/asmyasnikova83/MEG_probability/SCHEME_Autists.csv')
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists_extended'
if Normals:
    scheme = pd.read_csv('/home/asmyasnikova83/MEG_probability/SCHEMES2.csv')
    scheme = scheme.loc[222:]
    prefix_events = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
    prefix_data = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_extended'

os.makedirs('/{0}/{1}{2}_classical_bline/dataframe_for_LMEM_{1}'.format(prefix_data, freq_range, prefix), exist_ok = True)

########################## файл, со входными параметрами ############################################

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin), "tmax = {}".format(tmax), "step = {} усредение сигнала +/- 1,0 step от значения над topomap  ".format(step)]


with open("/{0}/{1}{2}_classical_bline/dataframe_for_LMEM_{1}/config.txt".format(prefix_data, freq_range, prefix), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################
for s in range(102):
    df = pd.DataFrame()
    for subj in subjects:
        for r in rounds:
            for t in trial_type:
                for fb_cur in feedback:
                    try:
                        combined_planar = mne.read_epochs('/{0}/{1}{2}_classical_bline/{1}_epo_comb_planar/{3}_run{4}_{5}_fb_cur_{6}_{1}-epo_comb_planar.fif'.format(prefix_data, freq_range, prefix, subj, r, t, fb_cur), preload = True)
                                        
                        df_subj = make_subjects_df(prefix_events, combined_planar, s, subj, r, t, fb_cur, tmin, tmax, step, scheme)
                        df = df.append(df_subj)            
                    except (OSError, FileNotFoundError):
                        print('This file not exist')
    df.to_csv('/{0}/{1}{2}_classical_bline/dataframe_for_LMEM_{1}/df_LMEM_{3}.csv'.format(prefix_data, freq_range, prefix, s))
                    
	
	
		

