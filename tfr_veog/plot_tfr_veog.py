
import mne
import os.path as op
import os
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from functions import ttest_pair_veog, plot_deff_tf_veog

freq_range = '2_40_step_2_time_bandwidth_by_default_4_early_log'
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


# у следующих испытуемых риски удалились после коррекции меток (удаления технических артефактов и восставновления недостающих (Лера)). У этих испытуемых "Риски" были повторными, а мы брали, только одиночные
subjects.remove('P005')
subjects.remove('P037')
subjects.remove('P061')

  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
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

out_path='/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_epo/' #path to epochs
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


subj_list = subjects.copy()
for i,subject in enumerate(subjects):
    subject_files = [file for file in f if subject in file] #make list with all subject files 
    for j in cond_list: #check if subject has all conditions
        if not any(j in s for s in subject_files):
            if subject in subj_list:
                subj_list.remove(subject)

subjects = subj_list
print(len(subjects))

# донор (donor creation see make_donor_for_tfr_plot.ipynb)
donor = mne.time_frequency.read_tfrs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/donor_evoked.h5'.format(freq_range), condition=None)[0]

n = donor.data.shape[2] # количество временных точек (берем у донора, если донор из тех же данных.
fr = donor.data.shape[1] # number of frequencies  (берем у донора, если донор из тех же данных.

#s.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/heog/{0}/oculo'.format(freq_range), exist_ok = True)

############# позитивный фидбэк против негативного в рисках #########################################
data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_ave_into_subj_fb_separ'.format(freq_range)

#os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/{0}/oculo/veog/risk_pos_vs_neg'.format(freq_range), exist_ok = True)
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_risk_pos_vs_neg'.format(freq_range), exist_ok = True)
folder_out = '/risk_pos_vs_neg'

cond = 'risk'

p1 = 'fb_cur_positive'
p2 = 'fb_cur_negative'

_, p_val, mean1, mean2 = ttest_pair_veog(data_path, subjects, cond, p1, p2, freq_range, n)

fig = plot_deff_tf_veog(p_val, donor, mean1, mean2, folder_out, title = "VEOG {0} {1} vs {2}".format(cond, p1, p2), treshold = 0.05)
#plt.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/{0}/oculo/veog/risk_pos_vs_neg/risk_pos_vs_neg_stat_no_fdr.jpeg'.format(freq_range), dpi = 300)
plt.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/tfr_plots/veog/{0}_risk_pos_vs_neg/risk_pos_vs_neg_stat_no_fdr_veog.jpeg'.format(freq_range), dpi = 300)

