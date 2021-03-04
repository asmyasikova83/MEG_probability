import os
import numpy as np
import mne

class conf():
    def __init__(self, mode, kind, frequency = None):
        #kind = ['norisk', 'risk'] #'positive', 'negative', 'prerisk', 'risk', 'postrisk', 'norisk_fb_positive','norisk_fb_negative', 'fb_negative_norisk'
        self.kind = kind
        self.path_home = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
        self.work_dir = 'WORK/'
        self.prefix_out = self.path_home + self.work_dir
        self.tfce_dir = 'TFCE/'

        if mode == 'grand_average':
            self.GA_dir = 'GA/'
            self.path_tfce = self.prefix_out + self.tfce_dir + self.GA_dir
            self.grand_average = True
            self.period_start = -1.400 #epoch start. for GA period_start = -1.400, for tfr period_start = -1.750
            self.period_end = 2.000 #epoch end for GA period_end = 2.000, for tfr period_end = 2.350
            self.time = np.arange(-1.400, 2.000, 0.004)
            self.times_to_plot = np.arange(-1.4, 2.0, 0.2)
            self.p_mul = 0.000000000005
            self.p_mul_topo = 0.0000000000006
            self.p_mul_topo_contrast = 0.0000000000005
            self.p_mul_topo_fdr_contrast = 0.0000000000005
        elif mode == 'tfr':
            self.tfr_dir = 'TFR/'
            self.path_tfce = self.prefix_out + self.tfce_dir + self.tfr_dir
            self.frequency = frequency
            self.grand_average = False
            self.period_start = -1.750
            self.period_end = 2.350
            self.time = np.arange(-1.400, 2.002, 0.004)
            self.times_to_plot = np.arange(-1.4, 2.0, 0.2)
            if frequency == 'theta':
                self.p_mul = 0.5
                self.p_mul_topo = 0.2
                if kind[0] == 'prerisk':
                    self.p_mul_topo_contrast = 0.15
                    self.p_mul_topo_fdr_contrast = 0.15
                elif kind[0] == 'norisk':
                    self.p_mul_topo_contrast = 0.1
                    self.p_mul_topo_fdr_contrast = 0.1
                elif kind[0] == 'postrisk':
                    self.p_mul_topo_contrast = 0.15
                    self.p_mul_topo_fdr_contrast = 0.15
                elif kind[0] == 'norisk_fb_positive':
                    self.p_mul_topo_contrast = 0.1
                    self.p_mul_topo_fdr_contrast = 0.1
                elif kind[0] == 'fb_positive_norisk' or grand_average == False and kind[0] == 'fb_negative_norisk':
                    self.p_mul_topo_contrast = 0.1
                    self.p_mul_topo_fdr_contrast = 0.1
                else:
                    print('The options in the theta range are over')
                    assert 0
            elif frequency == 'alpha':
                self.p_mul = 1.0
                self.p_mul_topo = 0.6
                self.p_mul_topo_contrast= 0.2
                self.p_mul_topo_fdr_contrast = 0.2
            elif frequency == 'beta':
                self.p_mul = 1.0
                self.p_mul_topo = 0.5
                self.p_mul_topo_contrast = 0.1
                self.p_mul_topo_fdr_contrast = 0.1
            elif frequency == 'gamma':
                self.p_mul = 0.4 #gamma
                self.p_mul_topo = 0.15
                self.p_mul_topo_contrast = 0.05
                self.p_mul_topo_fdr_contrast = 0.05
            else:
                print('freq range is over')
                assert 0
        else:
             print('mode range is over')
             assert 0

L_freq = 4
H_freq = 8
f_step = 1

freqs = np.arange(L_freq, H_freq+1, f_step)
legend = ['norisk', 'risk']
mode = 'server'
#prefix = '/home/asmyasnikova83/DATA/'
prefix_in = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
path_home = '/net/server/data/Archive/prob_learn/asmyasnikova83/'
work_dir = 'WORK/'
prefix_out = path_home + work_dir
events_dir = 'events/'
out_path = prefix_out
mio_dir = 'MIO/'
container_dir = 'evoked/'
pdf_dir = 'TFCE_PDF/'
fdr_dir = 'FDR/'
fdr_pdf_dir = 'FDR_PDF/'

#remove trend from GA
GA_correction = False
#settings for topomap plotting
topomap_plotting = True

# time interval before the appearance of the fixation cross
baseline_interval_start_power = -0.350
baseline_interval_end_power = -0.50

baseline_interval_start_sub = -350
baseline_interval_end_sub = -50
baseline =  'fixation_cross_norisks'#'fixation_cross_general'# 'fixation_cross_norisks'# 'fixation_cross_general'
if baseline == 'fixation_cross_norisks':
    data_path = '{0}_run{1}{2}_{3}_{4}{5}{6}_int_50ms-tfr.h5'
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

