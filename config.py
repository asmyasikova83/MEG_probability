import os
import numpy as np
import mne

L_freq = 32
H_freq = 100
f_step = 2

freqs = np.arange(L_freq, H_freq+1, f_step)
frequency = 'alpha'

mode = 'server'

period_start = -2.350 #epoch start
period_end = 1.850 #epoch end

# time interval before the appearance of the fixation cross
baseline_interval_start_power = -0.350
baseline_interval_end_power = -0.50

baseline_interval_start_sub = -350
baseline_interval_end_sub = -50

kind = ['prerisk', 'risk', 'postrisk'] #'positive', 'negative'

#if trained set ytain = '', in nontrained, set train = 'no_train'
train = ''
#settings for visualization
out_path = '/home/asmyasnikova83/DATA/evoked_ave/'
sign_sensors = True
check_num_sens = True

if frequency == 'theta':
    p_mul = 0.3
    p_mul_topo = 0.3
    p_mul_topo_contrast = 0.1
    p_mul_topo_fdr_contrast = 0.1
if frequency == 'alpha':
    p_mul = 1.0
    p_mul_topo = 0.6
    p_mul_topo_contrast= 0.2
    p_mul_topo_fdr_contrast = 0.2
if frequency == 'beta':
    p_mul = 1.0
    p_mul_topo = 0.5
    p_mul_topo_contrast = 0.1
    p_mul_topo_fdr_contrast = 0.1
if frequency == 'gamma':
    p_mul = 0.4 #gamma
    p_mul_topo = 0.15
    p_mul_topo_contrast = 0.05
    p_mul_topo_fdr_contrast = 0.05
'''
runs = ['1']

subjects = [
    'P003']
'''
#P008 P025 neg negative removed

subjects = [
    'P000',  
    'P002',
    'P003',
    'P004',
    'P005',
    'P006',
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
    'P025',
    'P026',
    'P028',
    'P029',
    'P030']

runs = ['1','2','3','4','5','6']
