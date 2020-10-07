import os
import numpy as np

L_freq = 4
H_freq = 8
f_step = 1

freqs = np.arange(L_freq, H_freq+1, f_step)

mode = 'server'

period_start = -2.350 #epoch start
period_end = 1.850 #epoch end

# time interval before the appearance of the fixation cross
baseline_interval_start_power = -0.350
baseline_interval_end_power = -0.50

baseline_interval_start_sub = -350
baseline_interval_end_sub = -50

kind = 'negative'

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

runs = ['1']

'''
subjects = [
    'P002']

runs = ['1','2','3','4','5','6']
'''
