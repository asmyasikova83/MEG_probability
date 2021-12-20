### For more details see plot_timecourses Jupyter Notebook  ######

import mne
import os.path as op
from matplotlib import pyplot as plt
import numpy as np
import copy
import pandas as pd
from scipy import stats
from function import combine_planar_Evoked, plot_topo_vs_zero


subjects = []
for i in range(0,63):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]
        
# следующие испытуемы удаляются из выборки по причине возраста (>40 лет), либо нерискующие
#subjects.remove('P000')
#subjects.remove('P020')
#subjects.remove('P036')
#subjects.remove('P049')
#subjects.remove('P056')

# donor
donor = mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/beta_16_30_trf_early_log/beta_16_30_trf_early_log_ave_into_subj/P001_norisk_evoked_beta_16_30_trf_early_log_resp.fif')
time_len = len(donor.times) # количество временных отчетов
print(time_len)
subjects = ['P001', 'P002', 'P004','P006', 'P007', 'P008', 'P011', 'P014', 'P015', 'P016', 'P017', 'P019',
'P021', 'P022', 'P023', 'P024', 'P025',  'P028', 'P029', 'P030', 'P031', 'P032',
'P033', 'P034', 'P035', 'P039', 'P040', 'P042', 'P043', 'P044',  'P045', 'P047',
'P048', 'P052', 'P053', 'P055', 'P057', 'P059', 'P060', 'P062']

freq_range = 'beta_16_30_trf_early_log'
trial_type = ['postrisk', 'postrisk']
fb = True

contr = np.zeros((len(subjects), 2, 1, time_len))
for ind, subj in enumerate(subjects):
    if fb:
        evoked1= mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_ave_into_subj_separ_fb/{1}_{2}_{0}_resp_fb_cur_negative.fif'.format(freq_range, subj, trial_type[0]))
    else:
        evoked1= mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, trial_type[0]))
    print(evoked1)
    if fb:
        evoked2= mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_ave_into_subj_separ_fb/{1}_{2}_{0}_resp_fb_cur_positive.fif'.format(freq_range, subj, trial_type[1]))
    else:
        evoked2= mne.Evoked('/net/server/data/Archive/prob_learn/asmyasnikova83/mio/contrasts/{0}/{0}_ave_into_subj/{1}_{2}_evoked_{0}_resp.fif'.format(freq_range, subj, trial_type[1]))
    contr[ind, 0, :, :] = evoked1.data
    contr[ind, 1, :, :] = evoked2.data
comp1 = contr[:, 0, :, :]
comp2 = contr[:, 1, :, :]
t_stat, p_val = stats.ttest_rel(comp2, comp1, axis=0)
comp1_mean = comp1.mean(axis=0).mean(axis=0)
comp2_mean = comp2.mean(axis=0).mean(axis=0)
print(comp1_mean.shape)

##################### timecourse ###############################
rej,p_fdr = mne.stats.fdr_correction(p_val, alpha=0.05, method='indep')
p_fdr = p_fdr.mean(axis=0)
p_val = p_val.mean(axis=0)
time = donor.times
print(time.shape)
print(time[0])
print(p_fdr.shape)
if fb: 
    cond1 = trial_type[0] + '_neg'
    cond2 = trial_type[1] + '_pos'
    p_mul_min = -2.0
    p_mul_max = 2.0
else:
    cond1 = trial_type[0]
    cond2 = trial_type[1]
    p_mul_min = -1.0
    p_mul_max = 1.0
title = f'EMG064 in {cond1} vs {cond2}'
plt.figure()
plt.rcParams['axes.facecolor'] = 'none'
plt.xlim(time[0], time[-1])
plt.xticks(np.arange(-1.0,2.0,0.5))
plt.ylim(p_mul_min, p_mul_max)
plt.plot([0, 0.001], [-50, 50], color='k', linewidth=3, linestyle='--', zorder=1)
plt.plot([-50, 50], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
#FB axis
plt.plot([1, 1.001], [-50, 50], color='k', linewidth=3, linestyle='--', zorder=1)
plt.plot(time, comp1_mean, color='r', linewidth=3, label=cond1)
plt.plot(time, comp2_mean, color='b', linewidth=3, label=cond2)
plt.fill_between(time, y1 = p_mul_min, y2 = p_mul_max, where = (p_fdr < 0.05), facecolor = 'm', alpha = 0.46, step = 'pre')
plt.fill_between(time, y1 = p_mul_min, y2 = p_mul_max, where = (p_val < 0.05), facecolor = 'g', alpha = 0.46, step = 'pre')
plt.tick_params(labelsize = 20)
plt.legend(loc='upper right', fontsize = 14)
plt.title(title, fontsize = 20)
plt.savefig(f'/net/server/data/Archive/prob_learn/asmyasnikova83/emg/{cond1}_vs_{cond2}')
plt.close()





