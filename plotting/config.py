import os

feedb = 'CUR_FB' #PREV_FB
#fr = 'low_beta_12_20'
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
donor = False
cond1 = 'postrisk'
cond2 = 'norisk'
#cond1 = 'risk'
#cond2 = 'norisk'
parameter1 = cond1
parameter2 = cond2
#parameter3 = 'negative'
#parameter4 = 'positive'
parameter3 = None
parameter4 = None
#TODO in plot_topomaps_line_LMEM
#planars = ['planar1', 'planar2', 'combined_planars']
planars = ['comb_planar']

#path = f'/net/server/data/Archive/prob_learn/asmyasnikova83/bline_nolog_div_{fr}/timecourses/'
#path = f'/net/server/data/Archive/prob_learn/asmyasnikova83/beta/timecourses_early_log/'
freq_range = 'beta_16_30_trf_no_log_division'
path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/stim/{0}/timecourses_aver_all_ch/'.format(freq_range)
os.makedirs(path, exist_ok = True)
path_pdf = path + 'output' +  '/all_pdf/'

subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]

# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
subjects.remove('P000')
subjects.remove('P020')
subjects.remove('P036')
subjects.remove('P049')
subjects.remove('P056')

'''
# у следующих испытуемых риски удалились после коррекции меток (удаления технических артефактов и восставновления недостающих (Лера)).
У этих испытуемых "Риски" были повторными, а мы брали, только одиночные
subjects.remove('P005')
subjects.remove('P037')
subjects.remove('P061')

'''

if feedb == 'CUR_FB':
    cond_list = ['_norisk_fb_cur_positive',
                 '_prerisk_fb_cur_positive',
                 '_risk_fb_cur_positive',
                 '_postrisk_fb_cur_positive',
                 '_norisk_fb_cur_negative',
                 '_prerisk_fb_cur_negative',
                 '_risk_fb_cur_negative',
                 '_postrisk_fb_cur_negative'
                 ]
    #rm P023  31 35 45 57 for risk TODO stim
    #rm 35 for risk_pos TODD sti?
    #rm 57 for prerisk sti
    if response == False and parameter3 == None:
        if cond1 == 'risk':
            subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022',        'P024', 'P025',  'P028', 'P029', 'P030',       'P032',
                'P033', 'P034',       'P039', 'P040', 'P042', 'P043', 'P044',          'P047',
                'P048', 'P052', 'P053', 'P055',      'P059', 'P060', 'P062']
        if cond1 == 'prerisk':
            subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022','P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                'P048', 'P052', 'P053', 'P055',      'P059', 'P060', 'P062']
        if cond1 == 'postrisk':
            subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022','P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                'P048', 'P052', 'P053', 'P055',        'P059', 'P060', 'P062']
    if response == True:
            subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022','P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']
    if response == False and parameter3 == 'negative':
        if cond1 == 'risk':
            subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022','P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                'P033', 'P034',       'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']
        else:
            subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
                'P021', 'P022', 'P023', 'P024', 'P025',  'P028', 'P029', 'P030','P031',  'P032',
                'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044','P045',  'P047',
                'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']

if feedb == 'PREV_FB':
    cond_list = ['_norisk_fb_prev_positive',
                 '_prerisk_fb_prev_positive',
                 '_risk_fb_prev_positive',
                 '_postrisk_fb_prev_positive',
                 '_norisk_fb_prev_negative',
                 '_prerisk_fb_prev_negative',
                 '_risk_fb_prev_negative',
                 '_postrisk_fb_prev_negative'
                 ]
    subj_list = subjects.copy()
    for i,subject in enumerate(subjects):
        subject_files = [file for file in f if subject in file] #make list with all subject files
        for j in cond_list: #check if subject has all conditions
            if not any(j in s for s in subject_files):
                if subject in subj_list:
                    subj_list.remove(subject)
    subjects = subj_list