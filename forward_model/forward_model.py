import mne, os
import os.path as op
import numpy as np
from functions import make_epochs_for_fwd, make_fwd_solution

subjects = []
for i in range(0, 63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
subjects.remove('P062')
subjects.remove('P036')
subjects.remove('P052')
subjects.remove('P032')
subjects.remove('P045')

runs = [1, 2, 3, 4, 5, 6]
trial_type = ['norisk', 'risk', 'prerisk', 'postrisk']
feedback = ['positive', 'negative']

period_start = -1.750
period_end = 2.750

os.makedirs('/home/asmyasnikova83/forward_model/', exist_ok = True)
os.makedirs('/home/asmyasnikova83/forward_model/bem/', exist_ok = True)
os.makedirs('/home/asmyasnikova83/forward_model/fwd', exist_ok = True)

path_data = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected'
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned' 
path_epochs = '/home/asmyasnikova83/forward_model'
path_bem =  '/home/asmyasnikova83/forward_model/bem'
path_trans = '/net/server/mnt/Archive/prob_learn/freesurfer'
path_forward = '/home/asmyasnikova83/forward_model/fwd'

prepare_epochs = True
prepare_fwd_solution = False
process_fwd_solution = False

planars = ['planar1', 'planar2']

if prepare_epochs:
    for planar in planars:
        for subj in subjects:
            for r in runs:
                for cond in trial_type:
                    for fb in feedback:
                        try:
                            events_response = np.loadtxt('{0}/{1}_run{2}_{3}_fb_cur_{4}.txt'.format(path_data, subj, r, cond, fb), dtype='int')
                            epochs = make_epochs_for_fwd(subj, r, cond, fb, events_response, planar, period_start, period_end, data_path, path_epochs)
                        except (OSError):
                            print('This file not exist')
if prepare_fwd_solution:
    for planar in planars:
        for subj in subjects:
            for r in runs:
                for cond in trial_type:
                    for fb in feedback:
                        try:
                            epochs = mne.read_epochs('{0}/{1}_run{2}_{3}_fb_cur_{4}_{5}-epo.fif'.format(path_epochs, subj, r, cond, fb, planar), preload = True)                               
                            fwd = make_fwd_solution(subj, r, cond, fb,  planar, epochs.info, path_bem, path_trans, path_forward)
                        except (OSError):
                            print('This file not exist')
if process_fwd_solution:
    for planar in planars:
        fwd_all = []
        for subj in subjects:
            for r in runs:
                for cond in trial_type:
                    for fb in feedback:
                        try:
                            fname = '{0}/{1}_run{2}_{3}_fb_cur_{4}_{5}-fwd.fif'.format(path_forward, subj, r, cond, fb, planar)
                            fwd = mne.read_forward_solution(fname)
                            fwd_all.append(fwd)
                        except (OSError):
                            print('This file not exist')
                            print('{0}/{1}_run{2}_{3}_fb_cur_{4}_{5}-fwd.fif'.format(path_forward, subj, r, cond, fb, planar))
        fwd_averaged = mne.average_forward_solutions(fwd_all, weights=None, verbose=None)
        fname = f'{path_forward}/aver_{planar}_20_63_fwd.fif'
        mne.write_forward_solution(fname, fwd_averaged, overwrite=True, verbose=None)
