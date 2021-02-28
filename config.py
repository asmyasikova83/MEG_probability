import os
import numpy as np
import mne

L_freq = 4
H_freq = 8
f_step = 1

freqs = np.arange(L_freq, H_freq+1, f_step)
frequency = 'theta'

mode = 'server'
#prefix = '/home/asmyasnikova83/DATA/'
prefix_in = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
path_home = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
work_dir = 'WORK/'
prefix_out = path_home + work_dir
events_dir = 'events/'
out_path = prefix_out
mio_dir = 'MIO/'
tfce_dir = 'TFCE/'


grand_average = True
#remove trend from GA
GA_correction = False
if grand_average:
    period_start = -1.400 #epoch start. for GA period_start = -1.400, for tfr period_start = -1.750
    period_end = 2.000 #epoch end for GA period_end = 2.000, for tfr period_end = 2.350
    time = np.arange(-1.400, 2.000, 0.004)
    times_to_plot = np.arange(-1.4, 2.0, 0.2)
else:
    period_start = -1.750
    period_end = 2.350
    time = np.arange(-1.400, 2.002, 0.004)
#settings for topomap plotting
topomap_plotting = True
if grand_average == False and topomap_plotting:
    time = np.arange(-1.400, 2.002, 0.004)
    times_to_plot = np.arange(-1.4, 2.0, 0.2)

# time interval before the appearance of the fixation cross
baseline_interval_start_power = -0.350
baseline_interval_end_power = -0.50

baseline_interval_start_sub = -350
baseline_interval_end_sub = -50
baseline =  'fixation_cross_norisks'#'fixation_cross_general'# 'fixation_cross_norisks'# 'fixation_cross_general'
if baseline == 'fixation_cross_norisks':
    data_path = '{0}TFR_new_base/{1}/{2}_run{3}{4}_{5}_{6}{7}{8}_int_50ms-tfr.h5'
    tfr_path_dir = '{0}TFR_new_base/{1}/'
if baseline == 'fixation_cross_general':
    data_path = '{0}TFR_av/{2}_run{3}{4}_{5}_{6}{7}{8}_int_50ms-tfr.h5'
    tfr_path_dir = '{0}TFR_av/{1}/'
    #data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/TFR/{1}/{2}_run{3}{4}_{5}_{6}{7}{8}_int_50ms-tfr.h5' 
    #tfr_path_dir = '/net/server/data/Archive/prob_learn/asmyasnikova83/TFR/{}/'
#do not use built-in baseline correction
b_line_manually = True
#plot_spectrogram param, if plot_spectrogram = True, spec = '_spec'
plot_spectrogram = False
#grand average plotting
ERF = 'event related fields'
topomap = True
butterfly = False
spec = ''

#type of analysis
kind = ['norisk', 'risk'] #'positive', 'negative', 'prerisk', 'risk', 'postrisk', 'norisk_fb_positive','norisk_fb_negative', 'fb_negative_norisk'
legend = ['norisk', 'risk']
#if trained set train = '', in nontrained, set train = '_no_train'
train = ''
#if stimulus data. set 'stimulus_', if response, set ''. If stimulus, don't forget to set stim at True!!
stimulus = ''
stim  = False
response = True
zero_point = 'averaged_over_response'
#settings for visualization
sign_sensors = False
check_num_sens = False
save_t_stat = False
random_comp = False
stat_over_subjects = False
stat_over_runs = True



if grand_average == True:
    p_mul = 0.000000000005
    p_mul_topo = 0.0000000000006
    p_mul_topo_contrast = 0.0000000000005
    p_mul_topo_fdr_contrast = 0.0000000000005

if grand_average == False and frequency == 'theta':
    p_mul = 0.5
    p_mul_topo = 0.2
    if kind[0] == 'prerisk':
        p_mul_topo_contrast = 0.15
        p_mul_topo_fdr_contrast = 0.15
    elif kind[0] == 'norisk':
        p_mul_topo_contrast = 0.1
        p_mul_topo_fdr_contrast = 0.1
    elif kind[0] == 'postrisk':
        p_mul_topo_contrast = 0.15
        p_mul_topo_fdr_contrast = 0.15
    elif kind[0] == 'norisk_fb_positive':
        p_mul_topo_contrast = 0.1
        p_mul_topo_fdr_contrast = 0.1
    elif kind[0] == 'fb_positive_norisk' or grand_average == False and kind[0] == 'fb_negative_norisk':
        p_mul_topo_contrast = 0.1
        p_mul_topo_fdr_contrast = 0.1
    else:
        print('The options in the theta range are over')
if grand_average == False and frequency == 'alpha':
    p_mul = 1.0
    p_mul_topo = 0.6
    p_mul_topo_contrast= 0.2
    p_mul_topo_fdr_contrast = 0.2
if grand_average == False and frequency == 'beta':
    p_mul = 1.0
    p_mul_topo = 0.5
    p_mul_topo_contrast = 0.1
    p_mul_topo_fdr_contrast = 0.1
if grand_average == False and frequency == 'gamma':
    p_mul = 0.4 #gamma
    p_mul_topo = 0.15
    p_mul_topo_contrast = 0.05
    p_mul_topo_fdr_contrast = 0.05
#P008 P025 neg negative removed'

subjects = [
    'P045',
    'P049',
    'P062']
'''
subjects = [
    'P000',  
    'P002',
    'P003',
    'P004',
    'P005',
    'P007',
    'P008', 
    'P009',
    'P010',
    'P011',
    'P012',
    'P014',
    'P015',
    'P016',
    'P017',
    'P018',
    'P019',
    'P020',
    'P021',
    'P022',
    'P023',
    'P024',
    'P026',
    'P028',
    'P029',
    'P030',
    'P031',
    'P032',
    'P033',
    'P034',
    'P035',
    'P036',
    'P037',
    'P039',
    'P040',
    'P041',
    'P042',
    'P043',
    'P044',
    'P006',
    'P045',
    'P046',
    'P047',
    'P048',
    'P049',
    'P050',
    'P051',
    'P052',
    'P053',
    'P054',
    'P055',
    'P056',
    'P057',
    'P058',
    'P059',
    'P060',
    'P061',
    'P062',
    'P006']


runs  = ['1', '2', '3', '4', '5', '6'] #'1', '2', '3', '4', '5'
'''
runs = ['1','3']

