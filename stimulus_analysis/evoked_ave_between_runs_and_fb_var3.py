import mne
import os
import os.path as op
import numpy as np

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

rounds = [1, 2, 3, 4, 5, 6]
#rounds = [2]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
#trial_type = ['risk']
# донор
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P001_norisk_evoked_beta_16_30_resp.fif")

n = temp.data.shape[1] # количество временных точек (берем у донора, если донор из тех же данных.
freq_range = 'beta_16_30_trf_no_log_division_stim'
prefix = '/net/server/data/Archive/prob_learn/asmyasnikova83/Events_normals'
#создаем папку, куда будут сохраняться полученные комбайны
os.makedirs('{0}/stim_check/{1}/{1}_ave_into_subj'.format(prefix, freq_range), exist_ok = True)


for subj in subjects:
    for t in trial_type:
        ################################ Positive feedback ################################
        epochs_stack = np.empty((0, 306, n))
        for r in rounds:
            try:
                epochs = mne.read_epochs('{0}/stim_check/{1}/{1}_second_bl_epo/{2}_run{3}_{4}_{1}_epo.fif'.format(prefix, freq_range, subj, r, t), preload = True)             
                epochs_stack = np.vstack([epochs_stack, epochs.get_data()])
            except (OSError):
                print('This file not exist')
        ###### Шаг 1. Усреднили все блоки 1 -6#################
        if epochs_stack.size != 0:
            data_into_subj = epochs_stack.mean(axis = 0)
            temp.data = data_into_subj
            temp.save('{0}/stim_check/{1}/{1}_ave_into_subj/{2}_{3}_evoked_{1}_resp.fif'.format(prefix, freq_range, subj, t))
        else:
            print('Subject has no data in this condition')
            pass
