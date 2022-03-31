import mne
import os
import os.path as op

def make_epochs_for_fwd(subj, r, cond, fb, events_response, planar, period_start, period_end, data_path, path_epochs):
    # если только одна метка, т.е. одна эпоха, то выдается ошибка, поэтому приводи shape к виду (N,3)
    if events_response.shape == (3,):
        events_response = events_response.reshape(1,3)
    raw_fname = op.join(data_path,'{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
    raw_data = mne.io.Raw(raw_fname, preload=True)
    #pick a type: planar1 or planar2
    picks = mne.pick_types(raw_data.info, meg =  planar , eog = True)
    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start,
            tmax = period_end, baseline = None, picks = picks, preload = True)
    print(epochs)
    print('{0}/{1}_run{2}_{3}_fb_cur_{4}_{5}-epo.fif'.format(path_epochs, subj, r, cond, fb, planar))
    epochs.save('{0}/{1}_run{2}_{3}_fb_cur_{4}_{5}-epo.fif'.format(path_epochs, subj, r, cond, fb, planar))
    print('EPOCHS SAVED')
    return epochs




def make_fwd_solution(subj, r, cond, fb, planar, epochs_info, path_bem, path_trans, path_forward):
    os.environ["SUBJECTS_DIR"] = "/net/server/data/Archive/prob_learn/freesurfer/"
    #use make_bem.py to creare bem model
    bem = mne.read_bem_solution('{0}/{1}_bem.h5'.format(path_bem, subj), verbose=None)
    src = mne.setup_source_space(subject =subj, spacing='ico5', add_dist=False ) # by default - spacing='oct6' (4098 sources per hemisphere)
    trans = '{0}/{1}/mri/T1-neuromag/sets/{1}-COR.fif'.format(path_trans, subj)
    fwd = mne.make_forward_solution(info = epochs_info, trans = trans, src = src, bem = bem)
    fname = '{0}/{1}_run{2}_{3}_fb_cur_{4}_{5}-fwd.fif'.format(path_forward, subj, r, cond, fb, planar)
    mne.write_forward_solution(fname, fwd, overwrite=True, verbose=None)
    print('saved fwd')
    return fwd

