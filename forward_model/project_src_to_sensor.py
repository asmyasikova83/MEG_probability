import os.path as op
import os
import numpy as np

import mne
from mne.datasets import sample


print(__doc__)

# For this example, we will be using the information of the sample subject.
# This will download the data if it not already on your machine. We also set
# the subjects directory so we don't need to give it to functions.
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'
#a template
subject = 'P055' 
# First, we get an info structure from the test subject.
#evoked_fname = op.join(data_path, 'MEG', subject, 'sample_audvis-ave.fif')
evoked_fname = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects/P024_norisk_evoked_beta_16_30_resp.fif'
#info = mne.io.read_info(evoked_fname)

#info = evoked_fname.info
raw = mne.io.read_raw_fif('/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/P015/run3_P015_raw_ica.fif')
info  = raw.info
tstep = 1. / info['sfreq']
#print(raw.info["dev_head_t"])
# To simulate sources, we also need a source space. It can be obtained from the
# forward solution of the sample subject.
#fwd_fname = op.join(data_path, 'MEG', subject,
#                            'sample_audvis-meg-eeg-oct-6-fwd.fif')

fwd_fname = '/home/asmyasnikova83/Archive/prob_learn/asmyasnikova83/forward/fwd/aver-fwd.fif'
fwd = mne.read_forward_solution(fwd_fname)
src = fwd['src']
#we have averaged thee data and therefore the head parameters differ
info["dev_head_t"] = fwd["info"]["dev_head_t"]

brain_areas = ['audalanteriorcingulate', 'caudalmiddlefrontal', 'cuneus', 'entorhinal', 'frontalpole', 'fusiform', 'inferiorparietal', 'inferiortemporal',
              'insula', 'isthmuscingulate', 'lateraloccipital', 'lateralorbitofrontal', 'lingual', 'medialorbitofrontal', 'middletemporal', 'paracentral',
              'parahippocampal', 'parsopercularis', 'parsorbitalis', 'parstriangularis', 'pericalcarine', 'postcentral', 'posteriorcingulate', 'precentral',
              'precuneus', 'rostralanteriorcingulate', 'rostralmiddlefrontal', 'superiorfrontal', 'superiorparietal', 'superiortemporal','supramarginal',
              'temporalpole', 'transversetemporal']
for area in brain_areas:
    # To select a region to activate, we use -----
    # a region of interest.
    selected_label = mne.read_labels_from_annot(
            subject, regexp=area, subjects_dir=subjects_dir)[0]
    location = 'center'  # Use the center of the region as a seed.
    extent = 10.  # Extent in mm of the region.
    label = mne.label.select_sources(
            subject, selected_label, location=location, extent=extent,
                subjects_dir=subjects_dir)
    print(label)
    # Define the time course of the activity for each source of the region to
    # activate. Here we use a sine wave at 18 Hz with a peak amplitude
    # of 10 nAm.
    source_time_series = np.sin(2. * np.pi * 18. * np.arange(100) * tstep) * 10e-9

    # Define when the activity occurs using events. The first column is the sample
    # of the event, the second is not used, and the third is the event id. Here the
    # events occur every 200 samples.
    n_events = 50
    events = np.zeros((n_events, 3), int)
    events[:, 0] = 100 + 200 * np.arange(n_events)  # Events sample.
    events[:, 2] = 1  # All events have the sample id.
    # Create simulated source activity. Here we use a SourceSimulator whose
    # add_data method is key. It specified where (label), what
    # (source_time_series), and when (events) an event type will occur.
    source_simulator = mne.simulation.SourceSimulator(src, tstep=tstep)
    source_simulator.add_data(label, source_time_series, events)

    # Project the source time series to sensor space and add some noise. The source
    # simulator can be given directly to the simulate_raw function.
    raw = mne.simulation.simulate_raw(info, source_simulator, forward=fwd)
    cov = mne.make_ad_hoc_cov(raw.info)
    mne.simulation.add_noise(raw, cov, iir_filter=[1.0, -1.0, 0.04])
    epochs = mne.Epochs(raw, events, event_id = 1.0, tmin = -1.0, tmax = 1.0, proj=True,
                            picks='mag')
    evoked = epochs.average()
    #plot  the projection onto the sensor space
    pic = evoked.plot_topomap(ch_type='mag', time_unit='s')
    pic.savefig(f'{area}.png')
    print(f'{area} is done!')



