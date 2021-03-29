import mne, os
import numpy as np
import matplotlib.pyplot as plt
from baseline_correction import retrieve_events
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline_substraction
from baseline_correction import compute_baseline_power
from baseline_correction import correct_baseline_substraction
from baseline_correction import correct_baseline_power_and_save
from baseline_correction import topomap_one
from config import conf
import pathlib

def tfr_process(conf):
    print('\trun tfr...')
    kind = conf.kind
    train = conf.train
    verbose = conf.verbose
    fpath_raw = conf.fpath_raw
    fpath_events = f'{conf.path_mio}/' + 'mio_out_{}/{}_run{}_mio_corrected_{}{}.txt'
    freq_path = conf.data_path
    data = []
    
    for i in range(len(kind)):
        for run in conf.runs:
            for subject in conf.subjects:
                print('\t\t', kind[i], run, subject)

                path_events = fpath_events.format(kind[i],subject, run, kind[i], train)
                if conf.baseline == 'fixation_cross_norisks':
                    path_events_with_cross = f'{conf.path_mio}/mio_out_norisk/{subject}_run{run}_mio_corrected_norisk.txt'
                else:
                    path_events_with_cross = path_events
                if pathlib.Path(path_events).exists() and os.stat(path_events).st_size != 0 and \
                    pathlib.Path(path_events_with_cross).exists() and os.stat(path_events_with_cross).st_size != 0:
                    if verbose:
                        print('This file is being processed: ', path_events)

                    raw_file = fpath_raw.format(subject, run, subject)
                    raw_data = mne.io.Raw(raw_file, preload=True, verbose = 'ERROR')
                    # filter 1-50 Hz
                    # for low frequencies, below the peaks of power-line noise low pass filter the data
                    raw_data = raw_data.filter(None, 50, fir_design='firwin')
                    # remove slow drifts
                    raw_data = raw_data.filter(1., None, fir_design='firwin')
                    picks = mne.pick_types(raw_data.info, meg = 'grad')

                    events_of_interest = retrieve_events(conf, raw_data, path_events, i, False)
                    events_with_cross = retrieve_events(conf, raw_data, path_events_with_cross, i, True)
                    if verbose:
                        print('\n\nDone with the events!')

                    BASELINE = compute_baseline_substraction(conf, raw_data, events_with_cross, events_of_interest, picks)
                    b_line = compute_baseline_power(conf, raw_data, events_with_cross, picks)
                    if verbose:
                        print('\n\nDone with the BASELINE I!')
                    if BASELINE.all== 0:
                        if verbose:
                            print('Yes, BASELINE is dummy')
                        continue

                    CORRECTED_DATA = correct_baseline_substraction(conf, BASELINE, events_of_interest, raw_data, picks)
                    if verbose:
                        print('\n\nDone with the CORRECTED!')

                    plot_created_epochs_evoked = False
                    epochs_of_interest, evoked = create_mne_epochs_evoked(conf, CORRECTED_DATA,
                            events_of_interest, plot_created_epochs_evoked, raw_data, picks)

                    # for time frequency analysis we need baseline II (power correction)
                    data_path = conf.data_path.format(subject, run, conf.spec, conf.frequency, kind[i], train)
                    freq_show = correct_baseline_power_and_save(conf, epochs_of_interest, b_line, data_path, conf.b_line_manually, conf.plot_spectrogram)
                    if verbose:
                        print('\n\nDone with the BASELINE II!')

                    #plot an example of topomap
                    show_one = False
                    if show_one:
                        topomap_one(freq_show)
                        freq_file = freq_fpath.format(prefix, kind[i], subject, run, spec, frequency, subject, KIND, train)
                        #read tfr data from (freq_file)[0]
                        freq_show = mne.time_frequency.read_tfrs(freq_file)[0]
                        #fix the hack array[5] for changed freq dim
                        freq_show.freqs  = freqs
                        data.append(freq_show)

                else:
                    if verbose:
                        print('This file: ', path_events, 'does not exit')

    print('\ttfr completed')

'''
print('\n\nGrand_average:')
freq_data = mne.grand_average(data)

print('\n\nPlot poto:')

if mode == 'server':
    #topomap for the general time inerval
    PM = freq_data.plot_topo(picks='meg', title='Theta average power in Negative Feedback')
    #topographic maps of time-frequency intervals of TFR data
    PM = freq_data.plot_topomap(tmin= 0.20, tmax=0.60, fmin=4, fmax=8, ch_type='grad')
    os.chdir('/home/asmyasnikova83/DATA')
    PM.savefig('output.png')
else:
    PM = freq_data.plot_topomap(tmin= 0.20, tmax=0.60, fmin=4, fmax=8, ch_type='grad')
    plt.show()
'''
