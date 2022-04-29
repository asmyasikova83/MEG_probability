import mne
import os
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
import copy
import pandas as pd
from scipy import stats
from function import combine_planar_Evoked


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

freq_range = 'beta_16_30_trf_early_log'

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk', 'prerisk', 'postrisk']
feedback = ['positive', 'negative']
# donor
donor = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif')

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range), exist_ok = True)
for t in trial_type:
    for fb in feedback:
        for subj in subjects:
            try:
                evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                #evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/hp_early_trials_check/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
                _, _, comb_planar = combine_planar_Evoked(evoked)
                donor.data = comb_planar
                donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                #donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/hp_early_trials_check/{0}/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar.fif'.format(freq_range, subj, t))
            except (OSError):
                print('This file not exist')

