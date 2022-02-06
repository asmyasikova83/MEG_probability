# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import os.path as op
import os
import numpy as np
from function import nocolor_topomaps_line

path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/signif_sensors/'


template_for_channels = False
decision_pre_resp_900_200 = False
post_resp_100_500 = True
fb_anticip_800 = False
early_fb_1100_1500 = False
late_fb_1500_1900 = False


if decision_pre_resp_900_200 == True:
    t = -0.5 
    f_name = path +  "sensors_decision_pre_resp_900_200.txt"
    title = "decisionpreresp"
if post_resp_100_500 == True:
    #set time to plot
    t = 0.2 
    f_name = path +  "sensors_100_500_post_resp.txt"
    title = "postresp100500"
if fb_anticip_800 == True:
    t = 0.8 
    f_name = path +  "sensors_fb_anticip_600_800.txt"
    title = "fbant600800"
if early_fb_1100_1500 == True:
    t = 1.3 
    f_name = path +  "sensors_early_fb_1100_1500.txt"
    title = "earlyfb11001500"
if late_fb_1500_1900 == True:
    t = 1.7 
    f_name = path +  "sensors_late_fb_1500_1900.txt"
    title = "latefb15001900"

sensors = np.loadtxt(f_name, dtype = int)
cluster = np.zeros((102, 1))
for s in sensors:
    cluster[s] = 1


print('cluster', cluster)



n = 1 # количество говов в ряду
#set time for the pic  plotting
#time_to_plot = np.linspace(-0.8, 2.4, num = 17)
time_to_plot = np.linspace(t, t + 0.1, num = n)
# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

# задаем временные точнки, в которых будем строить головы, затем мы присвоим их для донора (template)
times_array = np.array([t])

data_path = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/P061/run4_P061_raw_ica.fif'
raw = mne.io.read_raw_fif(data_path)
ch_names = raw.ch_names
##############  empty topomaps line (without color) ##################
temp = nocolor_topomaps_line(n, temp, times_array, template_for_channels)
############### cluster #####################################
#set significant channels
 
stat_sensors = np.array(cluster)

os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/', exist_ok = True)
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = False, extrapolate = "local", mask = np.bool_(stat_sensors), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))
fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/{title}.jpeg', dpi = 900)
