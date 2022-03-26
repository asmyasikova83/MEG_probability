import mne, os
import os.path as op
import numpy as np
from functions import make_fwd_solution

os.environ["SUBJECTS_DIR"] = "/net/server/data/Archive/prob_learn/freesurfer/"

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned' 

os.makedirs('/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward/fwd/', exist_ok = True)
#path_forward = '/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward'
subjects_dir = '/net/server/data/Archive/prob_learn/experiment/P011/170214/ORIGINAL_TSSS/'

subjects = []
for i in range(20,30):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
#subjects.remove('P062')
#subjects.remove('P036')
#subjects.remove('P052')
#subjects.remove('P032')
#subjects.remove('P045')

#rounds = [1, 2, 3, 4, 5, 6]
rounds = ['6']
#rial_type = ['norisk', 'risk', 'prerisk', 'postrisk']
trial_type = ['risk']
feedback = ['positive', 'negative']

period_start = -1.750
period_end = 2.750

prepare_fwd_solution = False
process_fwd_solution = False


if prepare_fwd_solution:
    for subj in subjects:
        events_response = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/P061_run5_norisk_fb_cur_positive.txt', dtype='int')
        # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
        if events_response.shape == (3,):
            events_response = events_response.reshape(1,3)
        raw_fname = op.join(data_path, '{0}/run2_{0}_raw_ica.fif'.format(subj))

        raw_data = mne.io.Raw(raw_fname, preload=True)
        picks = mne.pick_types(raw_data.info, meg = True, eog = True)
        epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, 
                        tmax = period_end, baseline = None, picks = picks, preload = True)

        bem = mne.read_bem_solution('/net/server/data/Archive/prob_learn/asmyasnikova83/forward_model/bem/{0}_bem.h5'.format(subj), verbose=None)
        src = mne.setup_source_space(subject =subj, spacing='ico5', add_dist=False ) # by default - spacing='oct6' (4098 sources per hemisphere)
        trans = '/net/server/mnt/Archive/prob_learn/freesurfer/{0}/mri/T1-neuromag/sets/{0}-COR.fif'.format(subj)
        fwd = make_fwd_solution(subj, bem, src, trans, epochs.info)
        print(fwd)
        fname = f'/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward/fwd/{subj}-fwd.fif'
        mne.write_forward_solution(fname, fwd, overwrite=True, verbose=None)
if process_fwd_solution:
    fwd_all = []
    for subj in subjects:
        fname = f'/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward/fwd/{subj}-fwd.fif'
        fwd = mne.read_forward_solution(fname)
        fwd_all.append(fwd)
    fwd_aver = mne.average_forward_solutions(fwd_all, weights=None, verbose=None)
    print(fwd_aver)
    fname = f'/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward/fwd/aver-fwd.fif'
    mne.write_forward_solution(fname, fwd_aver, overwrite=True, verbose=None)

fname = f'/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward/fwd/aver-fwd.fif'
fwd = mne.read_forward_solution(fname)
leadfield = fwd['sol']['data']
print("Leadfield size : %d sensors x %d dipoles" % leadfield.shape)
#print(leadfield[4, 30:650])
#rint(fwd['src'])
