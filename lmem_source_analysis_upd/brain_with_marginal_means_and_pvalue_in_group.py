import mne
import os.path as op
import os
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import (make_axes_locatable, ImageGrid,
                                     inset_locator)
from matplotlib  import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from mne.stats import  fdr_correction
mne.viz.set_3d_options(antialias=False)


os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'


labels= mne.read_labels_from_annot("fsaverage", parc = "aparc_sub")


labels = [lab for lab in labels if 'unknown' not in lab.name]
label_names = [label.name for label in labels]


df = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/gamma_30_50/stc/lmem_label/tukey_label_1500_1900_ingroup.csv')
src = mne.setup_source_space(subject = "fsaverage", spacing="ico5", add_dist=False)

###### create plot  with p_value with marginal means ######
data =df['norisk-autists-negative - positive']
data = data.drop([448])
data = np.array(data)
data[data>0.05]=1
space_fdr_data = mul.fdrcorrection(data,alpha=0.05)
space_fdr_data=space_fdr_data[1]
space_fdr_data[space_fdr_data>0.05]=1
   

mean_data =df['hp_aut']
mean_data = mean_data.drop([448])
mean_data= np.array(mean_data)
label_number= np.linspace(0, 447, 448)
arr= np.column_stack((data, mean_data, label_number))


arr[arr[:, 0] == 1, 1] = 0
space_arr= np.column_stack((space_fdr_data, mean_data, label_number))
space_arr[space_arr[:, 0] == 1, 1] = 0

nofdr_stc = mne.labels_to_stc(labels,arr[:,1], subject="fsaverage")

nofdr_stc.save ('/net/server/data/Archive/prob_learn/asmyasnikova83/gamma_30_50/stc/lmem_label/group_trial_type_feedback_no_fdr')

nofdr_stc.plot(hemi="both")


fdr_stc = mne.labels_to_stc(labels,space_arr[:,1], tmin = 1.700, tstep = 0.1)
fdr_stc.save ('/net/server/data/Archive/prob_learn/asmyasnikova83/gamma_30_50/stc/lmem_label/group_trial_type_feedback_fdr')

####### create brain picture, don't forget change pos_lims
stc=nofdr_stc
            #for t in time_points:
brain = mne.viz.plot_source_estimates(stc, hemi='split', time_viewer=False, background='white', 
                                                  foreground = 'black', cortex='bone', size = (1200, 800),
                                                        views = ['lat', 'med'], clim = dict(kind = 'value', 
                                                                                          
                                                                                          pos_lims= [0.25,0.30, 1]), 
                                                  initial_time = 1.500, spacing ='ico5')
                                
#brain.add_text(0.0, 0.9, f'no_fdr_LP_losses_vs_wins_beta 30-50Hz, **{scale[ind]}**',
#                   font_size=12, color='black')


#brain.add_text(0.0, 0.8, f'{inter[0]} .... inter[1]s',
#                   font_size=10, color='green')                   
#brain.add_text(0.0, 0.8, f'{v}', font_size=10, color='blue')
#brain.add_label(label_list[4])
#brain.add_annotation('HCPMMP1')
brain.save_image('/net/server/data/Archive/prob_learn/asmyasnikova83/gamma_30_50/stc/lmem_label/hp_AT.jpeg')
brain.close()



