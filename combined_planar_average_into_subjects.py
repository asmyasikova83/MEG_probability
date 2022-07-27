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

print(subjects)
freq_range = 'beta_16_30_trf_early_log'

fr = 'beta_16_30'
trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['norisk', 'prerisk', 'postrisk']
feedback = ['positive', 'negative']
# donor

print('donor')
fb_split = False
donor = mne.Evoked(f'/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/{fr}_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif')

if Autists:
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subjects_comb_planar/'.format(freq_range), exist_ok = True)
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/'.format(freq_range), exist_ok = True)
if Normals:
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subjects_comb_planar/'.format(freq_range), exist_ok = True)
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_ave_into_subjects_comb_planar/'.format(fr), exist_ok = True)
print('loop is beginning')
for t in trial_type:
    for fb in feedback:
        for subj in subjects:
            print('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp_fb_cur_{3}.fif'.format(fr, subj, t, fb))
            try:
                #if fb_split:
                #if Normals:
                #print('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_ave_into_subjects/{1}_{2}_evoked_{0}_resp_fb_cur_{3}.fif'.format(fr, subj, t, fb))
                evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                print('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                #if Autists:
                #evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subj/{1}_{2}_{0}_resp_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                #print(evoked)
                #if not fb_split:
                #if Normals:
                #evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_ave_into_subjects/{1}_{2}_evoked_{0}_resp.fif'.format(fr, subj, t))
                #evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_ave_into_subjects/{1}_{2}_evoked_{0}_resp_fb_cur_{3}.fif'.format(fr, subj, t, fb))
                #if Autists:
                #print('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
                #evoked = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, t))
                _, _, comb_planar = combine_planar_Evoked(evoked)
                donor.data = comb_planar
                #if fb_split:
                #print('saving')
                #if Normals:
                #donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subjects_comb_planar_classic_bline/{1}_{2}_evoked_{0}_resp_comb_planar_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                #if Autists:
                #donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/beta_by_feedback/{0}_ave_into_subjects_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))

                #if not fb_split:
                #if Normals:
                #donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/{0}_ave_into_subjects_comb_planar/{1}_{2}_evoked_{3}_resp_comb_planar.fif'.format(fr, subj, t, freq_range))
                donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/beta_by_feedback/{0}_ave_into_subjects_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar_fb_cur_{3}.fif'.format(freq_range, subj, t, fb))
                #if Autists:
                #donor.save('/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/{0}/{0}_ave_into_subj_comb_planar/{1}_{2}_evoked_{0}_resp_comb_planar.fif'.format(freq_range, subj, t))
                print('SAVED')
            except (OSError):
                print('This file not exist')

