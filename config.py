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
#parameter3 = 'negative'
#parameter4 = 'positive'
parameter3 = None
parameter4 = None
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
planars = ['comb_planar']

freq_range = 'beta_16_30_trf_early_log'
data_path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_into_subj'
#path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/stim/{0}/timecourses_aver_all_ch/'.format(freq_range)

Autists = False
Normals = False
Normals_Autists = True

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
    Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
                'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
                'P048', 'P053', 'P055', 'P058', 'P059', 'P060', 
                'P061', 'P063', 'P064', 'P065', 'P067']
    sample_full = 'full (40) Norm'
    sample = 'short Norm'
if Autists:
    Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
               'P316',  'P320', 'P321', 'P322', 'P323', 'P324', 
               'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
               'P334',  'P335', 'P338', 'P341', 'P342']
    sample = 'Autists'
if Normals_Autists:
    Normals = ['P001', 'P004', 'P019', 'P021', 'P022', 'P032',
               'P034', 'P035', 'P039', 'P040', 'P044', 'P047',
               'P048', 'P053', 'P055', 'P058', 'P059', 'P060',
               'P061', 'P063', 'P064', 'P065', 'P067']
    Autists = ['P301', 'P304', 'P307', 'P312', 'P313', 'P314',
               'P316',  'P320', 'P321', 'P322', 'P323', 'P324',
               'P325',  'P326', 'P327', 'P328', 'P329', 'P333',
               'P334', 'P335', 'P338', 'P341', 'P342']
#time points 
t = 1051
#tmin for corrected time course (cut off the beginning and the end of the timecourse)
t_min = -1.4
t_max = 2.1

