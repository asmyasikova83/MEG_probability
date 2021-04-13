import mne, os, sys, numpy as np
from config import conf
import pathlib

def container_results(plot_spectrogram, freq_data, data, donor, out_file, verbose):
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
    if plot_spectrogram:
        freq_data.save(out_file, overwrite=True)
    else:
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
    plot_spectrogram = conf.plot_spectrogram

    #get rid of runs, leave frequency data for pos and neg feedback for time course plotting 
    for i in range(len(kind)):
        for subject in conf.subjects:
            data = []
            processing_done = False
            if not plot_spectrogram:
                out_file = conf.path_container + "{}_{}{}_{}{}-ave.fif".format(subject, spec, kind[i], frequency, train)
            else:
                out_file = conf.path_container + "{0}_{1}{2}_{3}{4}-50ms-tfr.h5".format(subject, spec, kind[i], frequency, train)
            for run in conf.runs:
                print('\t\t', kind[i], run, subject)
                path_events = fpath_events.format(kind[i], subject, run, kind[i], train)
                if pathlib.Path(path_events).exists():
                    if verbose:
                        print('This file is being processed: ', path_events)

                    freq_file = conf.path_tfr + data_path.format(subject, run, spec, frequency, kind[i], train)
                    old_level = mne.set_log_level(verbose='ERROR', return_old_level=True)
                    freq_data = mne.time_frequency.read_tfrs(freq_file)[0]
                    mne.set_log_level(verbose=old_level)
                    data.append(freq_data.data)

                    processing_done = True

                if run == conf.runs[-1] and processing_done:
                    container_results(plot_spectrogram, freq_data, data, donor, out_file, verbose)

    if plot_spectrogram:
        sdata = []
        for subject in conf.subjects:
            out_file = conf.path_container + "{0}_{1}{2}_{3}{4}-50ms-tfr.h5".format(subject, spec, kind[0], frequency, train)
            if pathlib.Path(out_file).exists():
                freq_subject_data = mne.time_frequency.read_tfrs(out_file)[0]
                sdata.append(freq_subject_data)

        freq_spec_data = mne.grand_average(sdata)
        title = f'Spectrogram ~{conf.L_freq}-{conf.H_freq} Hz TFR in {kind[0]}'
        PM = freq_spec_data.plot(picks='meg', fmin=conf.L_freq, fmax=conf.H_freq, vmin=-0.15, vmax=0.15, title=title)
        os.chdir('/home/asmyasnikova83/')
        PM.savefig('output.png')
        print('\tSpectrogramm completed')

    print('\ttfr container completed')

