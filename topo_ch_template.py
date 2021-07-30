# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import os.path as op
import os
import numpy as np
from function import nocolor_topomaps_line

#we will mark significant channels
template_for_channels = True
central_cluster = True
occipital_cluster = False
n = 1 # количество говов в ряду
#set time for plotting
t = 1.8 
#time_to_plot = np.linspace(-0.8, 2.4, num = 17)
time_to_plot = np.linspace(t, t + 0.1, num = n)
# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

# задаем временные точнки, в которых будем строить головы, затем мы присвоим их для донора (template)
times_array = np.array([t])

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/P061/run4_P061_raw_ica.fif'
raw = mne.io.read_raw_fif(data_path)
ch_names = raw.ch_names
#print('The channel for index 14 is:', ch_names[14])
#print('The channel for index 26 is:', ch_names[26])
#print('The channel for index 27 is:', ch_names[27])
#print('The channel for index 60 is:', ch_names[60])
##print('The channel for index 67 is:', ch_names[67])
#print('The channel for index 69 is:', ch_names[69])
##############  empty topomaps line (without color) ##################
temp = nocolor_topomaps_line(n, temp, times_array, template_for_channels)
############### cluster #####################################
cluster = np.zeros((102, n))
#set significant channels
if occipital_cluster:     
    cluster[65,:] = 1
    #cluster[66,:] = 1
    cluster[72,:] = 1
    cluster[78,:] = 1
    cluster[80,:] = 1
    title = 'Occipit cluster'
if central_cluster:
    cluster[14,:] = 1
    cluster[26,:] = 1
    cluster[27,:] = 1
    cluster[60,:] = 1
    cluster[67,:] = 1
    cluster[69,:] = 1
    title = 'Central cluster'

stat_sensors = np.array(cluster)

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/head_templates_channels/', exist_ok = True)
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = False, extrapolate = "local", mask = np.bool_(stat_sensors), mask_params = dict(marker='o', markerfacecolor='red', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))
fig.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/head_templates_channels/cluster.jpeg', dpi = 300)
