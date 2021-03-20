import os
import numpy as np
import mne

class conf():
    def __init__(self, mode, kind, subjects=None, runs=None, frequency=None, work_dir='WORK/', verbose=False):
        # P036, P055, P044: ValueError: The number of epochs and the number of events must match
        # P048: ValueError: No matching events found for 45 (event id 45)
        # P003, P006, P016, P039, P021, P043, P014, P017, P022 events don't match
        default_subj_list = [
        'P000',       'P002',       'P004','P005',       'P007','P008','P009',
        'P010','P011','P012',              'P015',              'P018','P019',
        'P020',              'P023','P024',       'P026',       'P028','P029',
        'P030','P031','P032','P033','P034','P035',       'P037',
        'P040','P041','P042',              'P045','P046','P047',       'P049',
        'P050','P051','P052','P053','P054',       'P056','P057','P058','P059',
        'P060','P061','P062']
        self.subjects = subjects if subjects else default_subj_list #['P045','P049','P062']
        default_runs_list = ['1', '2', '3', '4', '5', '6'] 
        self.runs = runs if runs else default_runs_list #['1','3']

        #kind = ['norisk', 'risk'] #'positive', 'negative', 'prerisk', 'risk', 'postrisk', 'norisk_fb_positive','norisk_fb_negative', 'fb_negative_norisk'
        self.kind = kind

        #if stimulus data. set 'stimulus_', if response, set ''. If stimulus, don't forget to set stim at True!!
        self.stimulus = ''
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
        self.freqs = np.arange(L_freq, H_freq+1, f_step)
        self.random_comp = False
        self.check_num_sens = False
        self.legend = ['norisk', 'risk']
        self.verbose = verbose
        self.path_home = '/home/asmyasnikova83/'
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

            self.frequency = frequency
            self.grand_average = False
            #do not use built-in baseline correction
            self.b_line_manually = True
            self.baseline == 'fixation_cross_norisks'
            self.data_path = '{0}_run{1}{2}_{3}_{4}{5}{6}_int_50ms-tfr.h5'
            self.period_start = -1.750
            #if self.baseline == 'fixation_cross_general':
            #self.data_path = '{0}TFR_av/{2}_run{3}{4}_{5}_{6}{7}{8}_int_50ms-tfr.h5'
            #self.tfr_path_dir = '{0}TFR_av/{1}/'
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

