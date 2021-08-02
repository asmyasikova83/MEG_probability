# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
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
##############  empty topomaps line (without color) ##################
temp = nocolor_topomaps_line(n, temp, times_array, template_for_channels)
############### cluster #####################################
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/P061/run4_P061_raw_ica.fif'
raw = mne.io.read_raw_fif(data_path)


if central_cluster:
    fig = temp.plot_sensors(title = 'Central Cluster', show_names=['MEG0432', 'MEG0732', 'MEG0742', 'MEG1632', 'MEG1822', 'MEG1842'], show=False)
if occipital_cluster:
    fig = temp.plot_sensors(title = 'Occipital Cluster', show_names = ['MEG1742', 'MEG1932', 'MEG2112', 'MEG2132'], show=False)

fig.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/head_templates_channels/sensors.jpeg', dpi = 300)
