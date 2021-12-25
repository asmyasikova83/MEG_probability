import mne
import os
import os.path as op
import numpy as np
from function_emg import make_beta_signal
from mne.time_frequency import tfr_morlet
from matplotlib import pyplot as plt

from mne.time_frequency import tfr_morlet, psd_multitaper

emg = False
veog = True

period_start = -1.750
period_end = 2.750

#baseline = (-0.350, -0.05)



subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
    
rounds = [1, 2, 3, 4, 5, 6]
#ounds = ['2']
#rial_type = ['norisk', 'risk', 'prerisk', 'postrisk']
trial_type = ['risk']

feedback = ['positive', 'negative']
#feedback = ['negative']

temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned'

if emg:
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/emg/', exist_ok = True)
if veog:
    os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/veog/', exist_ok = True)

power = []
#freqs = np.logspace(*np.log10([2,40]), num=8)
freqs = np.arange(2, 41, 2)
n_cycles = freqs / 2.  # different number of cycle per frequency

for subj in subjects:
    for r in rounds: 
        for cond in trial_type:
            for fb in feedback:
                try:
                    events_response = np.loadtxt('/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/{0}_run{1}_{2}_fb_cur_{3}.txt'.format(subj, r, cond, fb), dtype='int')
                    if events_response.shape == (3,):
                        events_response = events_response.reshape(1,3)
                    raw_fname = op.join(data_path, '{0}/run{1}_{0}_raw_ica.fif'.format(subj, r))
                    raw_data = mne.io.Raw(raw_fname, preload=True)
                    picks = mne.pick_types(raw_data.info, meg = True, eog = True, emg = True, misc = True)
                    epochs = mne.Epochs(raw_data, events_response, event_id = None, tmin = period_start, tmax = period_end, baseline=None, picks = picks, preload = True).resample(300)
                    if emg:
                        freq_show =  mne.time_frequency.tfr_multitaper(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=False, return_itc = False,average = True, picks= ['EMG064'], decim=3, n_jobs=1).crop(tmin = period_start+0.750, tmax = period_end-0.750)
                        print(freq_show)
                    if veog:
                        freq_show =  mne.time_frequency.tfr_multitaper(epochs, freqs=freqs, n_cycles=n_cycles, use_fft=False, return_itc = False,average = True, picks= ['MISC301'], decim=3, n_jobs=1).crop(tmin = period_start+0.750, tmax = period_end-0.750)
                    power.append(freq_show)
                except (OSError):
                    print('This file not exist')

freq_spec_data = mne.grand_average(power)
print(freq_spec_data)
#freq_spec_data = power
if veog:
    title = 'VEOG TFR'
    PM = freq_spec_data.plot(picks=['MISC301'], baseline=(-0.5, 0), mode = 'logratio', title=title) 
    os.chdir('/net/server/data/Archive/prob_learn/asmyasnikova83/veog/')
if emg:
    title = 'Miogramm from EMG064'
    PM = freq_spec_data.plot(picks=['EMG064'], baseline=(-0.5, 0), vmin = -0.05, vmax = 0.05, mode = 'logratio', title=title) #EMG064 neck muscles
    print(PM)
    os.chdir('/net/server/data/Archive/prob_learn/asmyasnikova83/emg/')
plt.savefig('output.png')


