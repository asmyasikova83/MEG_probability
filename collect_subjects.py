import os

out_path='/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/' #path to epochs



subjects = [   'P001','P002','P003','P004','P005','P006','P007','P008','P009',
        'P010','P011','P012','P013','P014','P015','P016','P017','P018','P019',
                'P021','P022','P023','P024','P025','P026','P027','P028','P029',
        'P030','P031','P032','P033','P034','P035',      'P037','P038','P039',
        'P040','P041','P042','P043','P044','P045','P046','P047','P048',
        'P050','P051','P052','P053','P054','P055',      'P057','P058','P059',
        'P060','P061','P062']

### extract subjects with all conditions:fb+trial_type ####
cond_list = ['_norisk_fb_cur_positive',
             '_prerisk_fb_cur_positive',
             '_risk_fb_cur_positive',
             '_postrisk_fb_cur_positive',
             '_norisk_fb_cur_negative',
             '_prerisk_fb_cur_negative',
             '_risk_fb_cur_negative',
             '_postrisk_fb_cur_negative'
             ]

f = os.listdir(out_path)

subj_list = subjects.copy()
for i,subject in enumerate(subjects):
    subject_files = [file for file in f if subject in file] #make list with all subject files 
    for j in cond_list: #check if subject has all conditions
        if not any(j in s for s in subject_files):
            if subject in subj_list:
              subj_list.remove(subject) 


print('subj list with feedback', subj_list)
print('len subject list', len(subj_list))

### extract subjects with all conditions: only trial_type ####
cond_list = ['_norisk',
             '_prerisk',
             '_risk',
             '_postrisk',
             ]

f = os.listdir(out_path)

subj_list = subjects.copy()
for i,subject in enumerate(subjects):
    subject_files = [file for file in f if subject in file] #make list with all subject files 
    for j in cond_list: #check if subject has all conditions
        if not any(j in s for s in subject_files):
            if subject in subj_list:
              subj_list.remove(subject) 
print('subj list no feedback', subj_list)
print('len subject list', len(subj_list))
