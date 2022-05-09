import mne
import os
import os.path as op
import numpy as np
import pandas as pd
from functions import make_inverse_operator

period_start = -1.750
period_end = 2.750
baseline = (-0.35, -0.05)

#freq_range = 'beta_16_30'

description = 'Inverse operators for each subject and each run'

# This code sets an environment variable called SUBJECTS_DIR
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

subjects = ['P301', 'P304', 'P307',  'P309',  'P312', 'P313', 'P314',
            'P316', 'P322',  'P323', 'P324', 'P325',
            'P326',  'P328','P329', 'P331',  'P333', 'P334',
            'P336', 'P340']
subjects.remove('P328')
#subjects = ['P304']
rounds = [1, 2, 3, 4, 5, 6]

trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']

feedback = ['positive', 'negative']

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
out_path = os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/inverse_operators', exist_ok = True)

########################## Обязательно делать файл, в котором будет показано какие параметры были заданы, иначе проверить вводные никак нельзя, а это необходимо при возникновении некоторых вопросов ############################################

lines = [description, "baseline = {}".format(baseline)]


with open("/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/inverse_operators/config.txt", "w") as file:
    for  line in lines:
        file.write(line + '\n')


##############################################################################################################


for subj in subjects:
    bem = mne.read_bem_solution('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/bem/{0}_bem.h5'.format(subj), verbose=None)
    src = mne.setup_source_space(subject =subj, spacing='ico5', add_dist=False ) # by default - spacing='oct6' (4098 sources per hemisphere)
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                try:
                    inv = make_inverse_operator(subj, r, cond, fb, data_path, baseline, period_start, period_end, bem, src)
                    print('INV', inv)
                    fname = '/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/inverse_operators/{0}_run{1}_{2}_fb_cur_{3}-inv.fif'.format(subj, r, cond, fb)
                    mne.minimum_norm.write_inverse_operator(fname, inv, verbose=None)
                                        
                except (OSError):
                    print('This file not exist')

    

