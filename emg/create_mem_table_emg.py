
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from mne import set_log_level
from function import make_subjects_df

#set_log_level("ERROR")

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
freq_range = 'beta_16_30_trf_early_log'  

rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
feedback = ['positive', 'negative']

# interval of interest (1800 ms +/- 100 ms)
tmin = -0.9
tmax = 2.1
step = 0.2

scheme = pd.read_csv('/home/asmyasnikova83/MEG_probability/SCHEMES2.csv')
scheme = scheme.loc[222:]

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/dataframe_for_LMEM'.format(freq_range), exist_ok = True)

########################## файл, со входными параметрами ############################################

lines = ["freq_range = {}".format(freq_range), "rounds = {}".format(rounds), "trial_type = {}".format(trial_type), "feedback = {}".format(feedback), "tmin = {}".format(tmin), "tmax = {}".format(tmax), "step = {} усредение сигнала +/- 1,0 step от значения над topomap  ".format(step)]


with open("/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/dataframe_for_LMEM/config.txt".format(freq_range), "w") as file:
    for  line in lines:
        file.write(line + '\n')

#####################################################################################################
# emg channel only

for s in range(1):
    df = pd.DataFrame()
	
    for subj in subjects:
        for r in rounds:
            for t in trial_type:
                for fb_cur in feedback:
                    try:
                        combined_planar = mne.read_epochs('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_epo/{1}_run{2}_{3}_fb_cur_{4}_{0}_epo.fif'.format(freq_range, subj, r, t, fb_cur), preload = True)
                        
                        df_subj = make_subjects_df(combined_planar, s, subj, r, t, fb_cur, tmin, tmax, step, scheme)
                        df = df.append(df_subj)
                        print(df)
                    except (OSError, FileNotFoundError):
                        print('This file not exist')
    df.to_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/dataframe_for_LMEM/df_LMEM_{1}.csv'.format(freq_range, s))
                    
	
	
		

