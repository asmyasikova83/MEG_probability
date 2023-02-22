
import mne
import numpy as np
import pandas as pd
import os


os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

fsaverage = mne.setup_source_space(subject = "fsaverage", spacing="ico5", add_dist=False)

subjects = ['P001','P004','P019','P021','P022','P034','P035','P039', 'P040','P044','P047','P048',
            'P053','P055','P058', 'P059','P060','P061', 'P063','P064','P065','P067','P301','P304','P307',
            'P312','P313','P314','P316', 'P321','P322','P323','P324','P325','P326', 'P327','P328',
            'P329','P333','P334','P335','P341','P342']

rounds = [1, 2, 3, 4, 5, 6]
freq_range = "gamma_30_50"
trial_type = ['norisk', 'risk']
feedback = ['positive', 'negative']


#parc that we used https://balsa.wustl.edu/WN56
labels =  mne.read_labels_from_annot("fsaverage", "aparc_sub", hemi = "both")
#label_names = [label.name for label in labels] 

print('labels before', len(labels))
labels.pop(448)###### delete unknown labels !!!!
print(len(labels))
label_names = [label.name for label in labels] 

data_path = "/net/server/data/Archive/prob_learn/asmyasnikova83/gamma_30_50/stc/stc_epo_fsaverage"

for subj in subjects:
    print(subj)
    df = pd.DataFrame()
    
    for r in rounds:
        for cond in trial_type:
            for fb in feedback:
                    
                try:
                    print(data_path)
                    epochs_num = os.listdir(os.path.join(data_path, '{0}_run{1}_{2}_fb_cur_{3}_fsaverage'.format(subj, r, cond, fb)))
                    print('epochs_num', epochs_num)
                    epo_n = (int(len(epochs_num) / 2))
                    print('epo n', epo_n)
                    for ep in range(epo_n):
                        df_epo= pd.DataFrame()

                        stc = mne.read_source_estimate(os.path.join(data_path, '{0}_run{1}_{2}_fb_cur_{3}_fsaverage/{4}'.format(subj, r, cond, fb, ep)))
                        stc2 = stc.copy()
                        stc2=stc2.crop(tmin=1.500, tmax=1.900, include_tmax=True) ### crop the time what you want to analyse

                        label_ts = mne.extract_label_time_course(stc2,labels, src=fsaverage, mode='mean')
                        label_ts_avg=label_ts.mean(axis=1)
                      
                        epo = [ep for i in range(449)]
                        
                        subject = [subj for i in range(449)]
                        run = [r for i in range(449)]
                        trial = [cond for i in range(449)]
                        fb_cur=[fb for i in range(449)]
                        
                        df_epo['beta_power'] = label_ts_avg
                        df_epo['label'] = label_names
                        df_epo['epo'] = epo
                        df_epo['subject'] = subject
                        df_epo['round'] = run
                        df_epo['trial_type'] = trial
                        df_epo['feedback_cur'] = fb_cur
                            
                        df = df.append(df_epo)    
                         
                                       
                except (OSError, FileNotFoundError):
                    print('This file not exist')
    df.to_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/gamma_30_50/label_stc/df_1500_1900_khan/{0}.csv'.format(subj))
                            
                            
