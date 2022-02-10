
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from mne import set_log_level
from make_freq_stim import make_subjects_df

#set_log_level("ERROR")
freq_range = 'beta_16_30_trf_no_log_division_stim'

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

# interval of interest (1800 ms +/- 100 ms)
tmin = -0.9
tmax = 2.501
step = 0.2

a = np.arange(tmin, tmax, step)
print(len(a))
scheme = pd.read_csv('/home/asmyasnikova83/MEG_probability/SCHEMES2.csv')
scheme = scheme.loc[222:]
prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83'
os.makedirs('/{0}/stim_check/{1}_feedback/dataframe_for_LMEM'.format(prefix, freq_range), exist_ok = True)

########################## файл, со входными параметрами ############################################

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin), "tmax = {}".format(tmax), "step = {} усредение сигнала +/- 1,0 step от значения над topomap  ".format(step)]


with open("/{0}/stim_check/{1}_feedback/dataframe_for_LMEM/config.txt".format(prefix, freq_range), "w") as file:
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
                        print('/{0}/stim_check/{1}_feedback/{1}_epo_comb_planar/{2}_run{3}_{4}_fb_cur_{5}_{1}-epo_comb_planar.fif'.format(prefix, freq_range, subj, r, t, fb_cur))
                        combined_planar = mne.read_epochs('/{0}/stim_check/{1}_feedback/{1}_epo_comb_planar/{2}_run{3}_{4}_fb_cur_{5}_{1}-epo_comb_planar.fif'.format(prefix, freq_range, subj, r, t, fb_cur), preload = True)
                        
                        df_subj = make_subjects_df(combined_planar, s, subj, r, t, fb_cur, tmin, tmax, step, scheme)
                        df = df.append(df_subj)
                    except (OSError, FileNotFoundError):
                        print('This file not exist')
    df.to_csv('/{0}/stim_check/{1}_feedback/dataframe_for_LMEM/df_LMEM_{1}.csv'.format(prefix, freq_range, s))
                    
	
	
		

