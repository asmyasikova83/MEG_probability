# строит линии пустых голов (без цветовой заливки), на которой показаны сенсоры, на которых значения фактора, является значимым. Занчипость факторов определяется по моделям LMEM (R)
import mne
import numpy as np
import pandas as pd
from function import ttest_pair, ttest_vs_zero, space_fdr, full_fdr, p_val_binary, plot_deff_topo, plot_topo_vs_zero, nocolor_topomaps_line
from config import *
import re

pre_fb = False
fb = True

path = '/net/server/data/Archive/prob_learn/asmyasnikova83/probability/signif_sensors/'
os.makedirs(path, exist_ok = True)
# загружаем таблицу с pvalue, полученными с помощью LMEM в R
#df  = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_factor_significance_MEG_Vera.csv')
df  = pd.read_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/beta/p_vals_Tukey_condition_contrast_MEG.csv')
# задаем время для построения топомапов (используется в функции MNE plot_topomap)
# загружаем донора (любой Evoked с комбинированными планарами или одним планаром - чтобы было 102 сеносора). 
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")
############### 2. trial_type #####################################
################# p_value ########################
#before feedback onset we use model with the only factor of TRIAL_TYPE
#pick significant sensors from the intersect of time intervals and save them. topo_ch_template_auto.py will read and plot them
if pre_fb:
    pval_in_intevals = []
    for i in range(102):
        pval_s = df[df['sensor'] == i]
        pval_norisk_prerisk = pval_s[f'norisk_{cond1}'].tolist()
        pval_in_intevals.append(pval_norisk_prerisk)
    
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)
    sensors = []

    print(cond1)
    for j in range(102):
        if pval_in_intevals[j,0] < 0.00009 and pval_in_intevals[j,1] < 0.00009 and pval_in_intevals[j,2] < 0.00009:
            f_name = path + 'sensors_decision_pre_resp_900_200_tukey_super_sign.txt'
            sensors.append(j)
        '''
        if pval_full_fdr[j,5] < 0.05 and pval_full_fdr[j,6] < 0.05:
            f_name = path + 'sensors_100_500_post_resp.txt'
            #manually remove outliers TODO automatically
            if j == 63 or j == 45 or j == 7:
                pass
            else:
                sensors.append(j)
        
        if pval_in_intevals[j,8] < 0.01:
            print(pval_in_intevals[j,8])
            f_name = path + 'sensors_fb_anticip_600_800.txt'
            sensors.append(j)
        '''
    print(sensors)
    sensors_to_save = np.array(sensors)
    sensors_to_save = sensors_to_save[np.newaxis]
    np.savetxt(f_name, sensors_to_save, fmt="%s")
############### 3. trial_type:feedback_cur #####################################
################# p_value ########################
#after feedback onset we use model with the interaction trial_type:feedback_cur
if fb:
    pval_in_intevals = []
    for i in range(102):
        pval_s = df[df['sensor'] == i]
        pval_norisk_prerisk = pval_s[f'norisk_{cond1}'].tolist()
        pval_in_intevals.append(pval_norisk_prerisk)
    pval_in_intevals = np.array(pval_in_intevals)
    pval_space_fdr = space_fdr(pval_in_intevals)
    pval_full_fdr =  full_fdr(pval_in_intevals)
    sensors = []
    for j in range(102):
        '''
        if pval_full_fdr[j,10] < 0.05 and pval_full_fdr[j,11] < 0.05:
            f_name = path + 'sensors_early_fb_1100_1500.txt'
            sensors.append(j)
        '''
        if pval_in_intevals[j, 12] < 0.05 and pval_in_intevals[j, 13] < 0.05:
        #if pval_in_intevals[j, 13] < 0.045:
            f_name = path + 'sensors_late_fb_1500_1900_tukey_super_sign.txt'
            sensors.append(j)
    print(sensors)        
    sensors_to_save = np.array(sensors)
    sensors_to_save = sensors_to_save[np.newaxis]
    np.savetxt(f_name, sensors_to_save, fmt="%s")
