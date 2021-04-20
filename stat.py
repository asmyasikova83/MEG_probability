import numpy as np
import os
import re

#file1 = open(fname,'r+')
#fname_p_val = 'home/asmyasnikova83/COLLECT/COLLECT/TFR_BETA_prerisk_STAT__2021_04_20__13_14_37/TFCE/TFR/p_stat_norisk_fb_positive_vs_prerisk_fb_positive.txt'
#fname_t_stat = '/home/asmyasnikova83/COLLECT/TFR_BETA_prerisk_STAT__2021_04_20__13_14_37/TFCE/TFR/t_stat_norisk_fb_positive_vs_prerisk_fb_positive.txt'
#fname_fdr_pval = '/home/asmyasnikova83/COLLECT/TFR_BETA_prerisk_STAT__2021_04_20__13_14_37/TFCE/TFR/p_val_fdr_norisk_fb_positive_vs_prerisk_fb_positive.txt'
fname_p_val = '/home/asmyasnikova83/COLLECT/TFR_BETA_prerisk_STAT__2021_04_20__13_14_37/TFCE/TFR/p_stat_norisk_fb_positive_vs_prerisk_fb_positive.txt'
fname_t_stat = '/home/asmyasnikova83/COLLECT/TFR_BETA_prerisk_STAT__2021_04_20__13_14_37/TFCE/TFR/t_stat_norisk_fb_positive_vs_prerisk_fb_positive.txt'
fname_fdr_pval = '/home/asmyasnikova83/COLLECT/TFR_BETA_prerisk_STAT__2021_04_20__13_14_37/TFCE/TFR/p_val_fdr_norisk_fb_positive_vs_prerisk_fb_positive.txt'
#tstat = file1.read().split(np.mean)
#res = str(tstat[1:-1])

tstat = np.loadtxt(fname_t_stat)
p_stat = np.loadtxt(fname_p_val)
fdr_p_stat = np.loadtxt(fname_fdr_pval)
print(type(tstat))

tstat_1800 = np.mean(tstat[204:306, 788:812], axis = 1)
p_stat_1800 = np.mean(p_stat[204:306, 788:812], axis = 1)
fdr_p_stat_1800 = np.mean(fdr_p_stat[204:306, 788:812], axis = 1)
sum_counter = 0
p_val = 0
for ch in range(102):
    if p_stat_1800[ch] < 0.05:
        print('pstat ', p_stat_1800[ch])
        p_val = p_val + p_stat_1800[ch]
        sum_counter = sum_counter + 1
p_val_total = p_val/sum_counter
print('p_val total', p_val_total)    
sum_t_counter = 0
t_val = 0
for ch in range(102):
    if p_stat_1800[ch] < 0.05:
        print('pstat ', p_stat_1800[ch])
        print('tstat ', tstat_1800[ch])
        t_val = t_val + tstat_1800[ch]
        sum_t_counter = sum_t_counter + 1
t_val_total = t_val/sum_t_counter
print('t val total', t_val_total)    
sum_fdr_counter = 0
fdr_val = 0
for ch in range(102):
    if fdr_p_stat_1800[ch] < 0.05:
        print('fdr stat ', fdr_p_stat_1800[ch])
        fdr_val = fdr_val + fdr_p_stat_1800[ch]
        sum_fdr_counter = sum_fdr_counter + 1
fdr_val_total = fdr_val/sum_fdr_counter
print('fdr pval total', fdr_val_total)    
'''
fnamenew = 'tstat_new'
np.savetxt(fnamenew, res, fmt = "%d")
tstat = np.loadtxt(fnamenew, dtype=int)
print(type(tstat))
#for ch in range(102):
#    if res[ch, 750] <
'''
