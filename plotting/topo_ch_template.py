# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)


import mne
import os.path as op
import os
import numpy as np
from function import nocolor_topomaps_line

#we will mark significant channels
template_for_channels = False
anterior_cluster = False
occipital_cluster = False
decision = False
post_response = False
post_feedback_early = False
post_error = False
by_one_fr = False
by_one = False
super_decision  = False
super_feedback = False
super_early_feedback = False
group =  False
group_sign = False
LFB_groups = False
decision_groups = False
EFB_groups = True

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
if by_one_fr:
    cluster[70,:] = 1
    cluster[10,:] = 1
    cluster[15,:] = 1
    title = 'fr'
if by_one:
    cluster[8,:] = 1
    cluster[9,:] = 1
    cluster[11,:] = 1
    cluster[16,:] = 1
    cluster[17,:] = 1
    cluster[18,:] = 1
    cluster[19,:] = 1
    title = 'post_err'
if group_sign:
    cluster[10,:] = 1
    cluster[26,:] = 1
    cluster[27,:] = 1
    cluster[34,:] = 1
    cluster[59,:] = 1
    cluster[60,:] = 1
    cluster[61,:] = 1
    cluster[66,:] = 1
    cluster[67,:] = 1
    cluster[68,:] = 1
    cluster[69,:] = 1
    cluster[70,:] = 1
    cluster[71,:] = 1
    cluster[74,:] = 1
    cluster[75,:] = 1
    cluster[76,:] = 1
    cluster[77,:] = 1
    cluster[78,:] = 1
    cluster[84,:] = 1
    cluster[85,:] = 1
    cluster[86,:] = 1
    cluster[89,:] = 1
    cluster[90,:] = 1
    cluster[92,:] = 1
    cluster[93,:] = 1
    title = 'LFB'
if group:
    #cluster[6,:] = 1
    # cluster[15,:] = 1
    #cluster[16,:] = 1
    cluster[36,:] = 1
    cluster[38,:] = 1
    cluster[39,:] = 1
    cluster[40,:] = 1
    cluster[41,:] = 1
    cluster[46,:] = 1
    cluster[49,:] = 1
    #cluster[59,:] = 1
    cluster[82,:] = 1
    cluster[83,:] = 1
    #cluster[15,:] = 1
    #cluster[36,:] = 1
    #cluster[38,:] = 1
    #cluster[39,:] = 1
    #cluster[40,:] = 1
    #cluster[46,:] = 1
    #cluster[59,:] = 1
    #cluster[82,:] = 1
    #cluster[15,:] = 1
    #cluster[38,:] = 1
    #cluster[40,:] = 1
    #cluster[41,:] = 1
    #cluster[59,:] = 1
    #cluster[82,:] = 1
    #cluster[83,:] = 1
    title = 'Group_1400'
if occipital_cluster:     
    cluster[60,:] = 1
    cluster[61,:] = 1
    cluster[63,:] = 1
    cluster[64,:] = 1
    cluster[69,:] = 1
    cluster[70,:] = 1
    cluster[71,:] = 1
    cluster[74,:] = 1
    cluster[75,:] = 1
    cluster[76,:] = 1
    cluster[77,:] = 1
    cluster[78,:] = 1
    cluster[84,:] = 1
    cluster[86,:] = 1
    cluster[92,:] = 1
    cluster[93,:] = 1
    title = 'Occipit cluster'
if anterior_cluster:
    cluster[9,:] = 1
    cluster[10,:] = 1
    cluster[11,:] = 1
    cluster[12,:] = 1
    cluster[13,:] = 1
    cluster[20,:] = 1
    cluster[22,:] = 1
    cluster[37,:] = 1
    title = 'LatestAnterior'
if decision:
    cluster[5,:] = 1
    cluster[6,:] = 1
    cluster[9,:] = 1
    cluster[10,:] = 1
    cluster[12,:] = 1
    cluster[13,:] = 1
    cluster[14,:] = 1
    cluster[15,:] = 1
    cluster[21,:] = 1
    cluster[22,:] = 1
    cluster[24,:] = 1
    cluster[26,:] = 1
    cluster[27,:] = 1
    cluster[37,:] = 1
    cluster[36,:] = 1
    cluster[38,:] = 1
    cluster[39,:] = 1
    cluster[40,:] = 1
    cluster[41,:] = 1
    cluster[45,:] = 1 
    cluster[59,:] = 1
    cluster[60,:] = 1
    cluster[64,:] = 1
    cluster[66,:] = 1
    cluster[67,:] = 1
    cluster[68,:] = 1
    cluster[69,:] = 1
    cluster[70,:] = 1
    cluster[71,:] = 1
    cluster[73,:] = 1
    cluster[74,:] = 1
    cluster[75,:] = 1
    cluster[76,:] = 1
    cluster[77,:] = 1
    cluster[78,:] = 1
    cluster[79,:] = 1
    cluster[82,:] = 1
    cluster[83,:] = 1
    cluster[84,:] = 1
    cluster[85,:] = 1
    cluster[86,:] = 1
    cluster[87,:] = 1
    cluster[89,:] = 1
    title = 'Decision cluster'
if post_error:
    cluster[8,:] = 1
    cluster[16,:] = 1
    cluster[19,:] = 1
    title = 'Post-error'
if post_feedback_early:
    cluster[60,:] = 1
    cluster[70,:] = 1
    cluster[71,:] = 1
    cluster[73,:] = 1
    cluster[73,:] = 1
    cluster[74,:] = 1
    cluster[75,:] = 1
    cluster[76,:] = 1
    cluster[77,:] = 1
    cluster[86,:] = 1
    title = 'Post-fb early'
if post_response:
    #cluster[7,:] = 1
    cluster[12,:] = 1
    cluster[13,:] = 1
    cluster[14,:] = 1
    cluster[22,:] = 1
    cluster[23,:] = 1
    cluster[24,:] = 1
    cluster[25,:] = 1
    cluster[27,:] = 1
    cluster[38,:] = 1
    cluster[40,:] = 1
    cluster[41,:] = 1
    cluster[49,:] = 1
    cluster[59,:] = 1
    #cluster[63,:] = 1
    cluster[66,:] = 1
    cluster[67,:] = 1
    cluster[68,:] = 1
    cluster[69,:] = 1
    cluster[70,:] = 1
    cluster[74,:] = 1
    cluster[75,:] = 1
    cluster[77,:] = 1
    cluster[82,:] = 1
    cluster[83,:] = 1
    cluster[85,:] = 1
    title = 'Post-resp'
if LFB_groups:
    #cluster[51,:] = 1
    cluster[63,:] = 1
    cluster[64,:] = 1
    cluster[71,:] = 1
    cluster[76,:] = 1
    cluster[78,:] = 1
    #cluster[100,:] = 1
    title = 'LFB_groups'
if EFB_groups:
    cluster[52,:] = 1
    cluster[99,:] = 1
    cluster[100,:] = 1
    title = 'EFB_groups'
if decision_groups:
    cluster[38,:] = 1
    cluster[39,:] = 1
    cluster[43,:] = 1
    cluster[46,:] = 1
    cluster[53,:] = 1
    cluster[98,:] = 1
    #cluster[100,:] = 1
    title = 'Decis_groups'
if super_feedback:
    ##super posterior
    cluster[60,:] = 1
    cluster[69,:] = 1
    cluster[76,:] = 1
    title = 'super_posterior'
    #super anterior
    #cluster[10,:] = 1
    #cluster[20,:] = 1
    #cluster[12,:] = 1
    #title = 'super_anterior'
if super_early_feedback:
    cluster[76,:] = 1
    cluster[77,:] = 1
    cluster[70,:] = 1
    title = 'early_super_fb'

stat_sensors = np.array(cluster)
print(title)
fig = temp.plot_topomap(times = time_to_plot, ch_type='planar1', scalings = 1, units = 'dB', show = False, vmin = -0.9, vmax = 0.9, time_unit='s', title = title, colorbar = False, extrapolate = "local", mask = np.bool_(stat_sensors), mask_params = dict(marker='o', markerfacecolor='green', markeredgecolor='k', linewidth=0, markersize=10, markeredgewidth=2))
fig.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/maps_signif_sensors/{title}.jpeg', dpi = 900)
