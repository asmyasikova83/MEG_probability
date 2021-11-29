# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)
import mne
import numpy as np
import pandas as pd
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero, nocolor_topomaps_line
from config import *


# загружаем таблицу с pvalue, полученными с помощью LMEM в R
#TODO
df  = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_factor_significance_MEG.csv')
#df  = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/PREV_FB/p_val_theta_4_8/p_vals_factor_significance_MEG.csv')
#df  = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/CUR_FB/p_val_theta_4_8/analysis/p_vals_factor_significance_MEG.csv')
# задаем время для построения топомапов (используется в функции MNE plot_topomap)
# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
'''
############### 1. feedback_cur #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    pval_norisk_prerisk = pval_s['feedback_cur'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

'''
############### 2. trial_type #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    pval_norisk_prerisk = pval_s['trial_type'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)
print(pval_full_fdr.shape)

for j in range(102):
    if pval_full_fdr[j,8] < 0.05:
        print('found')
        print(pval_full_fdr[j,8])
        print('channel', j)
            

'''
############### 3. trial_type:feedback_cur #####################################
################# p_value ########################
pval_in_intevals = []
# number of heads in line and the number og intervals into which we divided (see amount od tables with p_value in intervals)
for i in range(102):
    
    pval_s = df[df['sensor'] == i]
    if feedb == 'CUR_FB':
        pval_norisk_prerisk = pval_s['trial_type:feedback_cur'].tolist()
    if feedb == 'PREV_FB':
        pval_norisk_prerisk = pval_s['trial_type:feedback_prev'].tolist()
    pval_in_intevals.append(pval_norisk_prerisk)
    
pval_in_intevals = np.array(pval_in_intevals)
pval_space_fdr = space_fdr(pval_in_intevals)
pval_full_fdr =  full_fdr(pval_in_intevals)

'''
