import mne, os, sys, numpy as np
from config import conf
import pathlib

def container_results(freq_data, data, donor, out_file, verbose):
    new_evoked = donor.copy()
    new_evoked.info = freq_data.info
    new_evoked.nave = 98  #all
    new_evoked.kind = "average"
    new_evoked.times = freq_data.times
    new_evoked.first = 0
    new_evoked.last = new_evoked.times.shape[0] - 1
    new_evoked.comment = freq_data.comment
    fq_data = np.asarray(data)
    if verbose:
        print('fq_data shape', fq_data.shape)
    #mean across runs
    fq_data = fq_data.mean(axis=0).mean(axis=1)
    if verbose:
        print('shape', fq_data.shape)
    new_evoked.data = fq_data
    if verbose:
        print(out_file)
    new_evoked.save(out_file)

def container_process(conf):
    print('\trun tfr container...')
    path_home = conf.path_home
    kind = conf.kind
    train = conf.train
    frequency = conf.frequency
    spec = conf.spec
    data_path = conf.data_path
    verbose = conf.verbose

    donor = mne.Evoked(f'{path_home}donor-ave.fif', verbose = 'ERROR')
    fpath_events = conf.path_mio + '/mio_out_{}/{}_run{}_mio_corrected_{}{}.txt'

    #get rid of runs, leave frequency data for pos and neg feedback for time course plotting 
    for i in range(len(kind)):
        for subject in conf.subjects:
            stc_list = []
            processing_done = False
            out_file = '{subject}_morphed'
            for run in conf.runs:
                print('\t\t', kind[i], run, subject)
                path_events = fpath_events.format(kind[i], subject, run, kind[i], train)
                if pathlib.Path(path_events).exists():
                    if verbose:
                        print('This file is being processed: ', path_events)

                    stc_file = '{subject}_run{run}morphed'
                    old_level = mne.set_log_level(verbose='ERROR', return_old_level=True)
                    stc_morph_data = mne.read_source_estimate(stc_file)
                    mne.set_log_level(verbose=old_level)
                    data.append(freq_data.data)

                    processing_done = True

                if run == conf.runs[-1] and processing_done:
                    container_results(freq_data, data, donor, out_file, verbose)

                    #inverse operator
                    inverse_operator = mne.minimum_norm.make_inverse_operator(epochs_of_interest.info, fwd, noise_cov=noise_covv,
                               loose=0.2, depth=0.8, verbose=True)
                    print('Inverse operator ready')
                    #bands = dict(theta=[4,8])
                    #f_step = 1
                    #stc = mne.minimum_norm.source_band_induced_power(epochs_of_interest.pick('grad'), inverse_operator,\
                    #                          bands, use_fft=False, df = f_step, n_cycles = 2)["theta"]
                    #sourse estimates on each epoch
                    stc = mne.minimum_norm.apply_inverse_epochs(epochs_of_interest, inverse_operator, method=method,\
                           lambda2=lambda2, pick_ori='normal')
                    stc=np.mean(stc)
                    morph = mne.compute_source_morph(stc, subject_from=subject, subject_to='fsaverage')
                    stc_fsaverage = morph.apply(stc)
                    print('Morphing done!')
                    print(stc_fsaverage)
                    stc_morph_name = '/MORPH/{subject}_run{run}morphed'
                    stc_fsaverage.save(stc_morph_name)
                    print('Morphing saved')
                    '''
                    stc_morph0 = mne.read_source_estimate(stc_morph_name)
                    stc_list.append(stc_morph0)
                    V_all = np.mean([stc_list[0].data], axis=0)
                    stc_av = (stc_list[0])/2
                    #V_all = np.mean([stc_list[0].data, stc_list[1].data], axis=0)
                    #stc_av = (stc_list[0] + stc_list[1])/2
                    stc_new = mne.SourceEstimate(V_all, [stc_list[0].lh_vertno, stc_list[0].rh_vertno], tmin=-1.4, tstep=stc_av.tstep, subject='fsaverage')
                    print(stc_new)
                    V_all = [stc_new.data]
                    num0 = np.argmax(stc_new.data.mean(axis=0))
                    init_time = stc_new.times[num0]
