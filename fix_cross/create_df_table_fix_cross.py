
import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from mne import set_log_level
from function import make_subjects_df
from function import make_fix_cross_df
from config import *
#set_log_level("ERROR")

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
   

#rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'risk']
#feedback = ['positive', 'negative']

# interval of interest (1800 ms +/- 100 ms)
tmin = -0.35
tmax = 0
step = 0.3

#scheme = pd.read_csv('/net/server/data/Archive/prob_learn/vtretyakova/for_Aleksandra/SCHEMES2.csv')
#scheme = scheme.loc[222:]
file_dir = ['theta_4_8_epo_FIX_CROSS',
            'theta_4_8_epo_RESPONSE',
            'theta_4_8_epo_FIX_CROSS_BASELINE',
            'theta_4_8_epo_RESPONSE_BASELINE']

df = pd.DataFrame()

for s in subjects:
    try:
        print('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[0], fr))
        fix_cross_norisk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[0], fr))
        resp_norisk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[0], fr))
        fix_cross_bslne_norisk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS_BASELINE/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[0], fr))
        resp_bslne_norisk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE_BASELINE/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[0], fr))
        fix_cross_risk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[1], fr))
        resp_risk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[1], fr))
        fix_cross_bslne_risk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_FIX_CROSS_BASELINE/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[1], fr))
        resp_bslne_risk = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/theta_4_8_epo_RESPONSE_BASELINE/ave_comb_planar/{0}_{1}_evoked_{2}_resp_comb_planar.fif'.format(s, trial_type[1], fr))
        df_subj = make_fix_cross_df(fix_cross_norisk, resp_norisk, fix_cross_bslne_norisk, resp_bslne_norisk, fix_cross_risk, resp_risk,  fix_cross_bslne_risk, resp_bslne_risk, s, trial_type, tmin, tmax, step)
        df = df.append(df_subj)
       # print(df)
    except (OSError, FileNotFoundError):
            print('This file not exist')
    df.to_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/df_ANOVA.csv')
                    
	
	
		

