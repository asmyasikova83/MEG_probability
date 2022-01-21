import mne
import os
import os.path as op
import numpy as np
from make_freq_stim import combine_planar_Evoked


subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
        
# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
#subjects.remove('P000')
#subjects.remove('P020')
#subjects.remove('P036')
#subjects.remove('P049')
#subjects.remove('P056')

freq_range = 'beta_16_30_trf_no_log_division_stim'
prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83'

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']

# donor
donor = mne.Evoked('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif')
os.makedirs('{0}/stim_check/{1}/{1}_ave_comb_planar'.format(prefix, freq_range), exist_ok = True)

for t in trial_type:
    for subj in subjects:
        try:
            evoked = mne.Evoked('{0}/stim_check/{1}/{1}_ave_into_subj/{2}_{3}_evoked_{1}_resp.fif'.format(prefix, freq_range, subj, t))
            print(evoked)
            _, _, comb_planar = combine_planar_Evoked(evoked)
            donor.data = comb_planar
            donor.save('{0}/stim_check/{1}/{1}_ave_comb_planar/{2}_{3}_evoked_beta_16_30_resp_comb_planar.fif'.format(prefix, freq_range, subj, t))
        except (OSError):
            print('This file not exist')
            

