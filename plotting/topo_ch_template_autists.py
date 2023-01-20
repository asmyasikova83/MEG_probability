# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import os.path as op
import os
import numpy as np
from function import nocolor_topomaps_line

#we will mark significant channels
template_for_channels = False

group_1700_triple = False
group_1700_triple_fin = True
group_1700_trial = False
triple_500_parapsycho = False
alpha_decision = False

n = 1 # количество говов в ряду
#set time for the pic  plotting
t = 1.7
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
cluster = np.zeros((102, n))
#set significant channels

if group_1700_triple_fin:
    #[3 4 5 7 8 9 10 11 12 19 20 51 54 55 58 59 60 61 62 63 64 70 71 72 73 76 77 78 79 86 87 89]
    #cluster[3,:] = 1
    #cluster[4,:] = 1
    cluster[5,:] = 1
    #cluster[7,:] = 1
    cluster[8,:] = 1
    cluster[9,:] = 1
    cluster[10,:] = 1
    cluster[11,:] = 1
    cluster[12,:] = 1
    cluster[19,:] = 1
    cluster[20,:] = 1
    #cluster[51,:] = 1
    #cluster[54,:] = 1
    #cluster[55,:] = 1
    #cluster[58,:] = 1
    #cluster[59,:] = 1
    #cluster[60,:] = 1
    #cluster[61,:] = 1
    #cluster[62,:] = 1
    #cluster[63,:] = 1
    #cluster[64,:] = 1
    #cluster[70,:] = 1
    #cluster[71,:] = 1
    #cluster[72,:] = 1
    #cluster[73,:] = 1
    #cluster[76,:] = 1
    #cluster[77,:] = 1
    #cluster[78,:] = 1
    #cluster[79,:] = 1
    #cluster[86,:] = 1
    #cluster[87,:] = 1
    #cluster[89,:] = 1
    title = 'triple_late_fb_fin'

if group_1700_triple:
    #[5, 7, 9, 11, 51, 61, 62, 63, 64, 70, 71, 72, 73, 77, 78, 79]
    cluster[5,:] = 1
    cluster[11,:] = 1
    cluster[9,:] = 1
    cluster[61,:] = 1
    cluster[62,:] = 1
    cluster[63,:] = 1
    cluster[64,:] = 1
    cluster[70,:] = 1
    cluster[71,:] = 1
    cluster[72,:] = 1
    cluster[73,:] = 1
    cluster[77,:] = 1
    cluster[78,:] = 1
    cluster[79,:] = 1
    title = 'triple_late_fb'
if group_1700_trial:
    #cluster[7,:] = 1
    #cluster[52,:] = 1
    #cluster[53,:] = 1
    #cluster[58,:] = 1
    #cluster[62,:] = 1
    cluster[63,:] = 1
    cluster[64,:] = 1
    cluster[76,:] = 1
    cluster[86,:] = 1
    cluster[87,:] = 1
    cluster[88,:] = 1
    cluster[89,:] = 1
    cluster[92,:] = 1
    cluster[93,:] = 1
    #cluster[98,:] = 1
    title = 'double_group_late_fb'

if triple_500_parapsycho:
    #cluster[28,:] = 1
    #cluster[30,:] = 1
    #cluster[51,:] = 1
    cluster[63,:] = 1
    cluster[64,:] = 1
    cluster[71,:] = 1
    cluster[75,:] = 1
    cluster[87,:] = 1
    cluster[92,:] = 1
    cluster[94,:] = 1
    cluster[95,:] = 1
    cluster[100,:] = 1
    cluster[101,:] = 1
    title = 'triple_500'
if alpha_decision:
    cluster[52,:] = 1
    cluster[56,:] = 1
    cluster[60,:] = 1
    cluster[61,:] = 1
    cluster[62,:] = 1
    cluster[63,:] = 1
    cluster[64,:] = 1
    cluster[65,:] = 1
    cluster[69,:] = 1
    cluster[70,:] = 1
    cluster[71,:] = 1
    cluster[72,:] = 1
    cluster[73,:] = 1
    cluster[74,:] = 1
    cluster[75,:] = 1
    cluster[76,:] = 1
    cluster[77,:] = 1
    cluster[78,:] = 1
    cluster[79,:] = 1
    cluster[80,:] = 1
    cluster[81,:] = 1
    cluster[84,:] = 1
    cluster[86,:] = 1
    cluster[87,:] = 1
    cluster[88,:] = 1
    cluster[92,:] = 1
    cluster[94,:] = 1
    cluster[95,:] = 1
    cluster[96,:] = 1
    cluster[97,:] = 1
    cluster[99,:] = 1
    cluster[100,:] = 1
    title = 'trial_group_decis'
stat_sensors = np.array(cluster)
print(title)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors_autists/', exist_ok = True)
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = False, extrapolate = "local", mask = np.bool_(stat_sensors), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))
fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors_autists/{title}.jpeg', dpi = 900)
