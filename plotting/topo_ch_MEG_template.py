# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import numpy as np
from function import nocolor_topomaps_line

#we will mark significant channels
template_for_channels = True

all_channels = False
frontal_cluster = False
fronto_central_cluster = False
central_cluster = False
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

if all_channels:
    #fig = temp.plot_sensors(title = 'Beta (12-20 hz),1800 ms', show_names=['MEG0222','MEG0232', 'MEG0322', 'MEG0332', "MEG0342", "MEG0422", "MEG0432", "MEG0442", "MEG0612", "MEG0632", "MEG0712",
    #                                                                       "MEG0742", "MEG1012", "MEG1422", "MEG1512", "MEG1522", "MEG1532", "MEG1542", "MEG1622", "MEG1632", "MEG1642", "MEG1712",
    #                                                                       "MEG1722", "MEG1732", "MEG1742", "MEG1812", "MEG1822", "MEG1832", "MEG1842", "MEG1912", "MEG1922", "MEG2012", "MEG2112",
    #                                                                       "MEG2142", "MEG2232", "MEG2422", "MEG2512"], show=False)
    fig = temp.plot_sensors(title = 'Beta (12-20 hz)', show_names= True, show = False)  
if central_cluster:
    fig = temp.plot_sensors(title = 'Central Cluster', show_names=['MEG0432', 'MEG0732', 'MEG0742', 'MEG1632', 'MEG1822', 'MEG1842'], show=False)
if frontal_cluster:
    fig = temp.plot_sensors(title = 'Frontal_cluster', show_names=  ['MEG0532', 'MEG0822', 'MEG1012', 'MEG0522', 'MEG0812' ], show=False)
if central_cluster:
    fig = temp.plot_sensors(title = 'Central Cluster', show_names=['MEG0432', 'MEG0732', 'MEG0742', 'MEG1632', 'MEG1822', 'MEG1842'], show=False)
if fronto_central_cluster:
    fig = temp.plot_sensors(title = 'Fronto-central Cluster', show_names=['MEG1042', 'MEG0722', 'MEG0712', 'MEG0612', 'MEG0622', 'MEG0642', 'MEG1012', 'MEG1022',  'MEG1032', 'MEG1112', 'MEG0632', 'MEG1142',
                           'MEG0432',  'MEG0422'], show=False)
if occipital_cluster:
    fig = temp.plot_sensors(title = 'Occipital Cluster', show_names = ['MEG1742', 'MEG1932', 'MEG2112', 'MEG2132'], show=False)

fig.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/head_templates_channels/sensors.jpeg', dpi = 300)
