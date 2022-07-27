import os

fr = 'beta_16_30'

if fr.split('_')[0] == 'delta':
    L_freq = 2
    H_freq = 4
    f_step = 1
if fr.split('_')[0] == 'theta':
    L_freq = 4
    H_freq = 8
    f_step = 1
if fr.split('_')[0] == 'low' and fr.split('_')[1] == 'beta':
    L_freq = 12
    H_freq = 20
    f_step = 2
if fr.split('_')[0] == 'high' and fr.split('_')[1] == 'beta':
    L_freq = 20
    H_freq = 35
    f_step = 2
if fr.split('_')[0] == 'beta':
    L_freq = 16
    H_freq = 31
    f_step = 2
#TODO issues with poster for IN feedback
poster = False
response = True
donor = True
cond1 = 'risk'
cond2 = 'norisk'
#cond1 = 'risk'
#cond2 = 'norisk'
#parameter1 = cond1
#parameter2 = cond2
parameter3 = 'negative'
parameter4 = 'positive'
#parameter3 = None
#parameter4 = None
if cond1 == 'prerisk':
    cond1_name = 'pre-LP'
if cond1 == 'risk':
     cond1_name = 'LP'
if cond1 == 'postrisk':
    cond1_name = 'post-LP'
if cond1 == 'norisk':
    cond1_name = 'HP'
cond2_name = 'HP'
if parameter3 == 'negative':
    name = cond1_name
    cond1_name = name + '_negative'
    cond2_name = name + '_positive'
comp1_label = cond1_name
comp2_label = cond2_name
#planars = ['planar1', 'planar2', 'combined_planars']
planars = 'comb_planar'

freq_range = 'beta_16_30_trf_early_log'
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_into_subj'
#path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/stim/{0}/timecourses_aver_all_ch/'.format(freq_range)
Autists = False
Normals = True
Normals_Autists = False

if response:
    if Normals:
        #path = '/net/server/data/Archive/prob_learn/asmyasnikova83/timecourses/resp_fewer/{0}/timecourses/'.format(freq_range)
        path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals/timecourses/{0}/'.format(freq_range)
    if Autists:
        path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Autists/timecourses/{0}/'.format(freq_range)
    if Normals_Autists:
        path = '/net/server/data/Archive/prob_learn/asmyasnikova83/Normals_Autists/timecourses/{0}/'.format(freq_range)
else:
    #path = '/net/server/data/Archive/prob_learn/asmyasnikova83/timecourses/stim_fewer/{0}/timecourses/'.format(freq_range)
    path = '/net/server/data/Archive/prob_learn/asmyasnikova83/timecourses/stim/with_contrast/{0}/timecourses_aver_all_ch/'.format(freq_range)
os.makedirs(path, exist_ok = True)
path_pdf = path + 'output' +  '/all_pdf/'


if Normals:
    subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022', 'P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']
    sample_full = 'full (40) Norm'
    #autists for pairs
    subjects_short = ['P023', 'P053', 'P022','P016', 'P040','P065', 'P001', 'P064', 'P055','P060', 'P019', 'P034', 'P004',
                'P039','P035', 'P008','P047', 'P059', 'P021', 'P063','P032', 'P044']
    #prerisk changed bline
    subjects_rerisk_changed_bline = ['P023', 'P053', 'P022','P016',          'P001',        'P055','P060', 'P019', 'P034', 'P004',
                'P039',              'P047', 'P059',      'P063','P032', 'P044']
    #risk changed bline 20 subj
    subjects_risk_changed_bline = ['P023', 'P053', 'P022','P016', 'P040','P065', 'P001', 'P064', 'P055','P060', 'P019', 'P034', 'P004',
                'P039',           'P047', 'P059', 'P021', 'P063','P032', 'P044']
    #prerisk classical_bline
    subjects_prerisk_classical_bline = ['P023', 'P053', 'P022','P016',             'P001',   'P060', 'P019',    'P004',
                'P039',                'P047',      'P063','P032', 'P044']
    #risk classical_bline
    subjects_risk_classical_bline = ['P023', 'P053', 'P022','P016', 'P040','P065', 'P001', 'P064', 'P055','P060', 'P019',     'P004',
                'P039',               'P047', 'P059', 'P021', 'P063','P032', 'P044']
    sample = 'short Norm'
if Autists:
    subjects_full= ['P301', 'P304', 'P307', 'P308', 'P311', 'P312', 'P313', 'P314', 'P316', 'P318', 'P320', 'P321', 'P322',
                'P323', 'P324', 'P325', 'P326', 'P327', 'P328', 'P329', 'P330', 'P331', 'P332', 'P333', 'P334', 'P335',
                'P336', 'P338', 'P341']
    #subjects.remove('P308') #autism not confirmed
    #subjects.remove('P336') #not all conditions
    #subjects.remove('P330') #no norisk neg
    #subjects.remove('P331') #not all conditions
    #subjects.remove('P328') #bad segmentation TODO return 328 back to the sample
    #subjects.remove('P327')#'P327' no bem dir in freesurfer
    #subjects.remove('P341')#subjects = ['P341'] no mri

    #autists for pairs
    subjects_short = ['P301','P304','P307','P332','P312', 'P313', 'P314', 'P316','P318', 'P320', 'P321', 'P322', 'P323',
                        'P325', 'P326', 'P327', 'P328', 'P329','P333', 'P334', 'P335', 'P341']
    #prerisk changed bline
    subjects_prerisk_changed_bline = ['P301','P304','P307','P332',               'P314',     'P318', 'P320', 'P321', 'P322', 'P323',
                        'P325',             'P328', 'P329',     'P334', 'P335', 'P341']
    #risk changed bline
    subjects_risk_changed_bline = ['P301','P304','P307','P332','P312', 'P313', 'P314', 'P316','P318', 'P320', 'P321', 'P322', 'P323',
                        'P325',            'P328', 'P329','P333', 'P334', 'P335', 'P341']
    #prerisk classical_bline 
    subjects_prerisk_classical_bline = ['P301','P304','P307','P332',            'P314',               'P320', 'P321',       'P323',
                        'P325',             'P328',               'P334', 'P335', 'P341']
    #risk classical_bline
    subjects_risk_classical_bline = ['P301','P304','P307','P332','P312', 'P313', 'P314', 'P316','P318', 'P320', 'P321',     'P323',
                        'P325',            'P328', 'P329','P333', 'P334', 'P335', 'P341']
    sample = 'Autists'
if Normals_Autists:
    #'P023','P309' for 309 no trained
    #'P058', 'P301','P058', 'P301',
    subjects_norm = ['P058', 'P301', 'P053', 'P304', 'P022','P307','P016','P332', 'P023','P309', 'P040','P312',
                'P055', 'P318', 'P060', 'P320', 'P001', 'P314', 'P034', 'P322', 'P004', 'P323', 'P039', 'P325',
                'P035', 'P326', 'P047', 'P328', 'P059', 'P329', 'P021', 'P333', 'P032', 'P335']
    Normals_full = ['P023', 'P053', 'P022','P016', 'P040','P065', 'P001', 'P064', 'P055','P060', 'P019', 'P034', 'P004',
            'P039','P035', 'P008','P047', 'P059', 'P021', 'P063','P032', 'P044']
    Autists_full = ['P301','P304','P307','P332','P312', 'P313', 'P314', 'P316','P318', 'P320', 'P321', 'P322', 'P323',
            'P325', 'P326', 'P327', 'P328', 'P329','P333', 'P334', 'P335', 'P341']
    #no fb in one of the cond 'P322', 'P322'-'P034', 'P326'-'P008', 'P327'-'P047',  'P313'-'P065'

    #prerisk changed bline _prerisk_changed_bline
    Normals = ['P023', 'P053', 'P022','P016',          'P001',        'P055','P060', 'P019', 'P034', 'P004',
                'P039',              'P047', 'P059',      'P063','P032', 'P044']
    #prerisk changed bline _prerisk_changed_bline
    Autists = ['P301','P304','P307','P332',               'P314',     'P318', 'P320', 'P321', 'P322', 'P323',
                        'P325',             'P328', 'P329',     'P334', 'P335', 'P341']
    #risk changed bline 20 subj
    Normals_risk_changed_bline = ['P023', 'P053', 'P022','P016', 'P040','P065', 'P001', 'P064', 'P055','P060', 'P019', 'P034', 'P004',
                'P039', 'P047', 'P059', 'P021', 'P063','P032', 'P044']
    #risk changed bline
    Autists_risk_changed_bline = ['P301','P304','P307','P332','P312', 'P313', 'P314', 'P316','P318', 'P320', 'P321', 'P322', 'P323',
                        'P325', 'P328', 'P329','P333', 'P334', 'P335', 'P341']
    #risk
    Normals_risk_classical_bline = ['P023', 'P053', 'P022','P016', 'P040','P065', 'P001', 'P064', 'P055','P060', 'P019',     'P004',
                'P039',               'P047', 'P059', 'P021', 'P063','P032', 'P044']
    Autists_risk_classical_bline = ['P301','P304','P307','P332','P312', 'P313', 'P314', 'P316','P318', 'P320', 'P321',     'P323',
                        'P325',            'P328', 'P329','P333', 'P334', 'P335', 'P341']
    sample = 'Norm_Autists'
#time points 
t = 1051
#tmin for corrected time course (cut off the beginning and the end of the timecourse)
t_min = -1.4
t_max = 2.1

