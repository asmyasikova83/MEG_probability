import mne
import os
import os.path as op
import numpy as np


step = 2

period_start = -1.750
period_end = 2.750

baseline = (-0.35, -0.05)
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

subj = 'P304'
r = 2
cond = 'norisk'
L_freq = 16
H_freq = 31
fb = 'positive'
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'
bem = mne.read_bem_solution('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/bem/{0}_bem.h5'.format(subj), verbose=None)
src = mne.setup_source_space(subject =subj, spacing='ico5', add_dist=False ) # by default - spacing='oct6' (4098 sources per hemisphere) ASK WHY ICO5
bands = dict(beta=[L_freq, H_freq])

events_pos = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_positive_fix_cross.txt".format(subj, r), dtype='int')
events_neg = np.loadtxt("/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/fix_cross_mio_corr/{0}_run{1}_norisk_fb_cur_negative_fix_cross.txt".format(subj, r), dtype='int')
events = np.vstack([events_pos, events_neg])
events = np.sort(events, axis = 0)
events_response = np.loadtxt('/net/server/data/Archive/prob_learn/asmyasnikova83/Events_autists/Events_mio/{0}_run{1}_{2}_fb_{3}.txt'.format(subj, r, cond, fb), dtype='int')
raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
raw_data = mne.io.Raw(raw_fname, preload=True)
picks = mne.pick_types(raw_data.info, meg = True, eog = True)

trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/COR.fif'.format(subj)
epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start,
                                        tmax = period_end, baseline = None, picks = picks, preload = True)
fwd = mne.make_forward_solution(info=epochs.info, trans=trans, src=src, bem=bem)
print(fwd)
