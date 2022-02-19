import os
from scipy import io
import numpy as np
import mne
from function import nocolor_topomaps_line, plot_stat_comparison, extract_and_av_cond_data
from config import *


freq_range = 'beta_16_30_trf_no_log_division'
# загружаем комбайн планары, усредненные внутри каждого испытуемого
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_no_log_division/beta_16_30_trf_no_log_division_second_bl_comb_planar/'
#data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_comb_planar/' 
# задаем время и донора
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
n = temp.data.shape[1]

risk_mean, norisk_mean, prerisk_mean, postrisk_mean, p1_val, p2_val, p3_val, p4_val  = extract_and_av_cond_data(data_path, subjects, fr,  n)
temp.data = risk_mean +  norisk_mean + prerisk_mean + postrisk_mean
times = np.array([1.7])
tmin = [1.5, 1.7]
tmax = [1.7, 1.9]
#num if intervals
N = 2
data_for_plotting = np.empty((102, 0))
for i in range(N):
    data_in_interval = temp.copy()
    data_in_interval = data_in_interval.crop(tmin=tmin[i], tmax=tmax[i], include_tmax=True)
    data_mean = data_in_interval.data.mean(axis = 1)
    data_mean = data_mean.reshape(102,1)
    data_for_plotting = np.hstack([data_for_plotting, data_mean])
#summarize 2 timeframes and  btain a head
data_to_sum = (data_for_plotting[:,0] + data_for_plotting[:,1])/2
fpath = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/signif_sensors/'
fname = fpath +  "sensors_late_fb_1500_1900.txt"
sensors = np.loadtxt(fname, dtype = int)
print(data_path)
cluster = np.zeros((102, 1))
power = []
counter = 0
k = 0
anterior = False
posterior = True
channels = []
f_name = '/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/threshold/'
for ch in sensors:
    if anterior:
        if data_to_sum[ch] > 1.98: #mean in anterior we observe positive values
            print(data_to_sum[ch])
            print(ch)
            cluster[ch] = 1
            power.append(data_to_sum[ch])
            counter = counter + 1
            channels.append(ch)
            k = k + 1
            print(channels)
        #remove outlier
        cluster[20] = 0
        title = 'Anterior'
    if posterior:
        if data_to_sum[ch] < -6.29: #in posterior we observe negative power
            print(data_to_sum[ch])
            print(ch)
            cluster[ch] = 1
            #power.append(data_to_sum[ch])
            channels.append(ch)
            counter = counter + 1
            k = k + 1
        title = 'Posterior'
channels_to_save = np.array(channels)
channels_to_save = channels_to_save[np.newaxis]
np.savetxt(f_name + f'{title}.txt', channels_to_save, fmt="%s")
#print('meean_', np.mean(power))
#print('sd', np.std(power))
n = 1 # количество говов в ряду
t = 1.7
time_to_plot = np.linspace(t, t+0.01, num = n)

# задаем временные точнки, в которых будем строить головы, затем мы присвоим их для донора (template)
times_array = np.array([t])

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/P061/run4_P061_raw_ica.fif'
raw = mne.io.read_raw_fif(data_path)
ch_names = raw.ch_names
template_for_channels = False
##############  empty topomaps line (without color) ##################
temp = nocolor_topomaps_line(n, temp, times_array, template_for_channels)
############### cluster #####################################
#set significant channels
stat_sensors = np.array(cluster)

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/threshold/', exist_ok = True)
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = False, extrapolate = "local", mask = np.bool_(stat_sensors), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))
fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/threshold/{title}.jpeg', dpi = 900)
