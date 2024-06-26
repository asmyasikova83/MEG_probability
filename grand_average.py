import mne, os
import numpy as np
from baseline_correction import retrieve_events
from baseline_correction import create_mne_epochs_evoked
from baseline_correction import compute_baseline_substraction
from baseline_correction import correct_baseline_substraction
from config import conf
import pathlib

def container_results(evoked, evoked_ave, donor, out_file, verbose):
    new_evoked = donor.copy()
    new_evoked.info = evoked.info
    new_evoked.nave = 98  #all
    new_evoked.kind = "average"
    new_evoked.times = evoked.times
    new_evoked.first = 0
    new_evoked.last = evoked.times.shape[0] - 1
    ev_data = np.asarray(evoked_ave)
    ev_data = ev_data[:, np.newaxis]
    if verbose:
        print('ev_data shape', ev_data.shape)
    #mean across runs
    ev_data = ev_data.mean(axis=0).mean(axis=0)
    if verbose:
        print('shape', ev_data.shape)
    new_evoked.data = ev_data
    if verbose:
        print(out_file)
    mne.write_evokeds(out_file, new_evoked)

def grand_average_process(conf):
    print('\trun ERF...')
    kind = conf.kind
    path_home = conf.path_home
    train = conf.train
    spec = conf.spec
    verbose = conf.verbose
    fpath_raw = conf.fpath_raw
    fpath_events = conf.path_mio + '/mio_out_{}/{}_run{}_mio_corrected_{}{}.txt'
    donor = mne.Evoked(f'{path_home}donor-ave.fif', verbose='ERROR')

    for i in range(len(kind)):
        for subject in conf.subjects:
            evoked_ave = []
            processing_done = False
            for run in conf.runs:
                print('\t\t', kind[i], subject, run)

                path_events = fpath_events.format(kind[i], subject, run, kind[i], train)
                if verbose:
                    print('path_events', path_events)
                if conf.baseline == 'fixation_cross_norisks':
                    path_events_with_cross = f'{conf.path_mio}/mio_out_norisk/{subject}_run{run}_mio_corrected_norisk.txt'
                else:
                    path_events_with_cross = path_events
                if pathlib.Path(path_events).exists() and os.stat(path_events).st_size != 0 and \
                    pathlib.Path(path_events_with_cross).exists() and os.stat(path_events_with_cross).st_size != 0:

                    out_file = conf.path_GA + "/{}_{}{}_{}_grand_ave.fif".format(subject, spec, kind[i], train)

                    raw_file = fpath_raw.format(subject, run, subject)
                    if verbose:
                        print('raw file path')
                        print(raw_file)

                    raw_data = mne.io.Raw(raw_file, preload=True, verbose = 'ERROR')
                    # for low frequencies, below the peaks of power-line noise low pass filter the data
                    raw_data = raw_data.filter(None, 50, fir_design='firwin')
                    #remove slow drifts
                    raw_data = raw_data.filter(1., None, fir_design='firwin')
                    picks = mne.pick_types(raw_data.info, meg = 'grad')

                    events_of_interest = retrieve_events(conf, raw_data, path_events, i, False)
                    events_with_cross = retrieve_events(conf, raw_data, path_events_with_cross, i, True)
                    if verbose:
                        print('Done with the events!')
                        print(events_with_cross)
                        print(events_of_interest)

                    BASELINE = compute_baseline_substraction(conf, raw_data, events_with_cross, events_of_interest, picks)
                    if BASELINE.all == 0:
                        if verbose:
                            print('Yes, BASELINE is dummy')
                        if run == conf.runs[-1] and processing_done:
                            container_results(evoked, evoked_ave, donor, out_file, verbose)
                        continue
                    if verbose:
                        print('\n\nDone with the BASELINE I!')

                    CORRECTED_DATA = correct_baseline_substraction(conf, BASELINE, events_of_interest, raw_data, picks)
                    if verbose:
                        print('\n\nDone with the CORRECTED!')

                    plot_created_epochs_evoked = False
                    epochs_of_interest, evoked = create_mne_epochs_evoked(conf, CORRECTED_DATA,
                        events_of_interest, plot_created_epochs_evoked, raw_data, picks)
                    evoked_ave.append(evoked.data)

                    processing_done = True

                if run == conf.runs[-1] and processing_done:
                    container_results(evoked, evoked_ave, donor, out_file, verbose)

    print('\tERF completed')



'''
import matplotlib.pyplot as plt
for subject in subjects:
    sdata = []
    #change kind[0] to kind[1] to get another output.png
    out_file = prefix_out + folder + "/{}_{}{}_{}{}-grand_ave.fif".format(subject, spec, kind[0], frequency, train)
    print(out_file)
    file = pathlib.Path(out_file)
    if file.exists():
        print('This file is being processed: ', out_file)
        evoked = mne.Evoked(out_file)
        print(type(evoked))
        print(evoked)
        sdata.append(evoked)

print('\n\nGrand_average:')
grand_averages = mne.grand_average(sdata)
if butterfly:
    GA = grand_averages.plot(spatial_colors=True, gfp=True, picks=picks, show=False)
if topomap:
    GA = grand_averages.pick_types(meg='grad').plot_topo(color='r', legend=False)
    print('Pic done')
print(grand_averages)
if mode == 'server':
    os.chdir('/home/asmyasnikova83/DATA/evoked_ave')
    GA.savefig('output.png')
else:
    plt.show()
'''
