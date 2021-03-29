import os
import numpy as np
import mne
from pathlib import Path

def correct_response(event):
    return event[2] == 40 or event[2] == 41 or event[2] == 46 or event[2] == 47

def incorrect_response(event):
    return event[2] == 42 or event[2] == 43 or event[2] == 44 or event[2] == 45

def response(event):
    return correct_response(event) or incorrect_response(event)

class conf():
    def __init__(self, mode, kind, subjects=None, runs=None, frequency=None, work_dir='WORK/', verbose=False):
        # FIXME P042
        default_subj_list = [
        'P000','P001','P002','P003','P004','P005','P006','P007','P008','P009',
        'P010','P011','P012',       'P014','P015','P016','P017','P018','P019',
        'P020','P021','P022','P023','P024',       'P026',       'P028','P029',
        'P030','P031','P032','P033','P034','P035','P036','P037',       'P039',
        'P040','P041',       'P043','P044','P045','P046','P047','P048','P049',
        'P050','P051','P052','P053','P054','P055','P056','P057','P058','P059',
        'P060','P061','P062']
        self.subjects = subjects if subjects else default_subj_list #['P045','P049','P062']
        default_runs_list = ['1', '2', '3', '4', '5', '6'] 
        self.runs = runs if runs else default_runs_list #['1','3']

        #kind = ['norisk', 'risk'] #'positive', 'negative', 'prerisk', 'risk', 'postrisk', 'norisk_fb_positive','norisk_fb_negative', 'fb_negative_norisk'
        self.kind = kind

        #settings for averaging over stimulus and over response
        self.stim = False
        self.response = True
        assert self.stim and not self.response or self.response and not self.stim

        #setting for legends
        self.zero_point = 'averaged_over_response'

        #type of analysis
        #if trained set train = '', in nontrained, set train = '_no_train'
        self.train = ''
        #plot_spectrogram param, if plot_spectrogram = True, spec = '_spec'
        self.spec = ''
        self.plot_spectrogram = False
        #'fixation_cross_general'# 'fixation_cross_norisks'# 'fixation_cross_general'
        self.baseline =  'fixation_cross_norisks'
        # time interval before the appearance of the fixation cross
        self.baseline_interval_start_power = -0.350
        self.baseline_interval_end_power = -0.50

        self.baseline_interval_start_sub = -350
        self.baseline_interval_end_sub = -50
        self.random_comp = False
        self.check_num_sens = False

        assert len(self.kind) >= 2
        self.legend = [kind[0], kind[1]]

        self.verbose = verbose

        self.path_home = str(Path.home()) + '/'
        self.fpath_raw = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
        prefix_out = self.path_home + work_dir
        if not os.path.exists(prefix_out) or not os.path.isdir(prefix_out):
            os.makedirs(prefix_out)
        self.prefix_out = prefix_out

        events_dir = 'events/'
        mio_dir = 'MIO/'
        tfce_dir = 'TFCE/'
        pdf_dir = 'TFCE_PDF/'
        fdr_dir = 'FDR/'
        fdr_pdf_dir = 'FDR_PDF/'

        self.path_events = prefix_out + events_dir
        self.path_mio = prefix_out + mio_dir

        if mode == 'grand_average':
            GA_dir = 'GA/'
            self.path_GA = prefix_out + GA_dir
            self.path_tfce = prefix_out + tfce_dir + GA_dir
            self.path_pdf = prefix_out + pdf_dir + GA_dir
            self.path_fdr = prefix_out + fdr_dir + GA_dir
            self.path_fdr_pdf = prefix_out + fdr_pdf_dir + GA_dir

            self.grand_average = True

            self.period_start = -1.400 #epoch start. for GA period_start = -1.400, for tfr period_start = -1.750
            self.period_end = 2.000 #epoch end for GA period_end = 2.000, for tfr period_end = 2.350
            self.time = np.arange(-1.400, 2.000, 0.004)
            self.times_to_plot = np.arange(-1.4, 2.0, 0.2)
            self.p_mul = 0.000000000005
            self.p_mul_topo = 0.0000000000006
            self.p_mul_topo_contrast = 0.0000000000005
            self.p_mul_topo_fdr_contrast = 0.0000000000005
            self.ERF = 'event related fields'
        elif mode == 'tfr':
            tfr_dir = 'TFR/'
            self.path_tfr = prefix_out + tfr_dir
            container_dir = 'evoked/'
            self.path_container = prefix_out + container_dir
            self.path_tfce = prefix_out + tfce_dir + tfr_dir
            self.path_pdf = prefix_out + pdf_dir + tfr_dir
            self.path_fdr = prefix_out + fdr_dir + tfr_dir
            self.path_fdr_pdf = prefix_out + fdr_pdf_dir + tfr_dir

            self.grand_average = False
            #do not use built-in baseline correction
            self.b_line_manually = True
            self.baseline == 'fixation_cross_norisks'
            self.data_path = '{}_run{}{}_{}_{}{}_int_50ms-tfr.h5'
            self.period_start = -1.750
            #if self.baseline == 'fixation_cross_general':
            #self.tfr_path_dir = '{0}TFR_av/{1}/'
            self.period_end = 2.350
            self.time = np.arange(-1.400, 2.002, 0.004)
            self.times_to_plot = np.arange(-1.4, 2.0, 0.2)

            self.frequency = frequency
            if self.frequency == 'theta':
                self.L_freq = 4
                self.H_freq = 8
                self.f_step = 1
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
            elif self.frequency == 'alpha':
                self.L_freq = 8
                self.H_freq = 14
                self.f_step = 1
                self.p_mul = 1.0
                self.p_mul_topo = 0.6
                self.p_mul_topo_contrast= 0.2
                self.p_mul_topo_fdr_contrast = 0.2
            elif self.frequency == 'beta':
                self.L_freq = 16
                self.H_freq = 30
                self.f_step = 2
                self.p_mul = 1.0
                self.p_mul_topo = 0.5
                self.p_mul_topo_contrast = 0.1
                self.p_mul_topo_fdr_contrast = 0.1
            elif self.frequency == 'gamma':
                self.L_freq = 30
                self.H_freq = 50
                self.f_step = 2
                self.p_mul = 0.4
                self.p_mul_topo = 0.15
                self.p_mul_topo_contrast = 0.05
                self.p_mul_topo_fdr_contrast = 0.05
            elif self.frequency == 'delta':
                self.L_freq = 2
                self.H_freq = 4
                self.f_step = 1
                self.p_mul = 0.6
                self.p_mul_topo = 0.3
                self.p_mul_topo_contrast = 0.2
                self.p_mul_topo_fdr_contrast = 0.2
            else:
                print('freq range is over')
                assert 0
            self.freqs = np.arange(self.L_freq, self.H_freq+1, self.f_step)

        else:
             print('mode range is over')
             assert 0

#settings for topomap plotting
topomap_plotting = True

#grand average plotting
topomap = True
butterfly = False

#settings for visualization
sign_sensors = False
save_t_stat = False
stat_over_subjects = False
stat_over_runs = True

