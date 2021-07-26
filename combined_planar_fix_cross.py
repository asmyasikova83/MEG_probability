import mne
import os
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
import copy
import pandas as pd
from scipy import stats
from function import combine_planar_Evoked
from config import *

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
        
# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
subjects.remove('P000')
subjects.remove('P020')
subjects.remove('P036')
subjects.remove('P049')
subjects.remove('P056')


trial_type = ['norisk', 'risk']
# donor
donor = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif')

file_dir = ['theta_4_8_epo_FIX_CROSS',
            'theta_4_8_epo_RESPONSE',
            'theta_4_8_epo_FIX_CROSS_BASELINE',
            'theta_4_8_epo_RESPONSE_BASELINE']

for  fi in  file_dir:
    os.makedirs(f'/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/{fi}/ave_comb_planar', exist_ok = True)

    for t in trial_type:
        for subj in subjects:
            try:
                evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/{0}/ave/{1}_{2}_evoked_{3}_resp.fif'.format(fi, subj, t, fr))
                print('EVOKED', evoked)
                _, _, comb_planar = combine_planar_Evoked(evoked)
                comb = mne.EvokedArray(comb_planar, info = donor.info, tmin = -0.350)
                comb.save('/net/server/data/Archive/prob_learn/asmyasnikova83/theta_4_8_FIX_CROSS/{0}/ave_comb_planar/{1}_{2}_evoked_{3}_resp_comb_planar.fif'.format(fi, subj, t, fr))
            except (OSError):
                print('This file not exist')
            

