import mne
import os
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
import copy
import pandas as pd
from scipy import stats
from function import combine_planar_Evoked

subjects = ['P301', 'P304', 'P307',  'P309',  'P312', 'P313', 'P314',
            'P316', 'P322',  'P323', 'P324', 'P325',
            'P326', 'P329', 'P331',  'P333', 'P334',
            'P336', 'P340', 'P341']
'''
subjects = ['P341']
'''
freq_range = 'beta_16_30_trf_early_log'

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk', 'prerisk', 'postrisk']
feedback = ['positive', 'negative']
# donor

fb_split = True
donor = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif')

if fb_split:
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/'.format(freq_range), exist_ok = True)
if not fb_split:
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/'.format(freq_range), exist_ok = True)

for t in trial_type:
    for fb in feedback:
        for subj in subjects:
            try:
                if fb_split:
                    evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                if not fb_split:
                    print('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
                    evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
                #evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/hp_early_trials_check/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
                _, _, comb_planar = combine_planar_Evoked(evoked)
                donor.data = comb_planar
                if fb_split:
                    donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                if not fb_split:
                    donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar.fif'.format(freq_range, subj, t))
                    print('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar.fif'.format(freq_range, subj, t))
                    print('SAVED')
                #donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/hp_early_trials_check/{0}/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar.fif'.format(freq_range, subj, t))
            except (OSError):
                print('This file not exist')

