import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy import stats
import scipy
import statsmodels.stats.multitest as mul
from itertools import combinations
import matplotlib.gridspec as gridspec
from array import array
import subprocess
from config import *
import pathlib
import random
from scipy import stats, io
from plot_time_course_in_html_functions import clear_html
from plot_time_course_in_html_functions import add_str_html
from plot_time_course_in_html_functions import contr_num
from plot_time_course_in_html_functions import to_str_ar
from plot_time_course_in_html_functions import get_short_legend
from plot_time_course_in_html_functions import get_full_legend
from plot_time_course_in_html_functions import delaete_bad_sub
from plot_time_course_in_html_functions import add_pic_time_course_html
from plot_time_course_in_html_functions import plot_stat_comparison
from plot_time_course_in_html_functions import p_val_binary
from compute_p_val import compute_p_val
from plot_time_course_in_html_functions import add_pic_topo_html
from tfce import tfce

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':1.0,
    'no-outline':None,
    'quiet':''
}
planars = ['planar1', 'planar2', 'combine_planar']


os.chdir('/home/asmyasnikova83/GITHUB/MEG_probability') #папка где будут сохраняться картинки
output = 'output_topo_tfce/'
rewrite = True
os.makedirs (output, exist_ok=True)
os.makedirs(os.path.join(output, f'{legend[0]}_vs_{legend[1]}'), exist_ok=True)

topomaps = [f'{legend[0]}',
            f'{legend[1]}',
            'difference',
            'difference_with_TFCE']

#time = np.arange(-2.000, 1.502, 0.004)
#donor data file
temp = mne.Evoked(f'{prefix}donor-ave.fif')
temp.times = time
#times_to_plot = np.arange(-1.4, 2.0, 0.2)

print('time shape', time.shape)

comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary, subjects1 = compute_p_val(subjects, kind, train, frequency, check_num_sens)

df1 = contr[:, 0, 204:, :]
df2 = contr[:, 1, 204:, :]
print('df1 shape', df1.shape)
print('df2 shape', df2.shape)

df1 = df1.transpose(2, 0, 1)
df2 = df2.transpose(2, 0, 1)
df1_mean = df1.mean(axis = 1)
df2_mean = df2.mean(axis = 1)

t_stat = np.zeros((df1.shape[0], df1.shape[2]))
p_val =  np.zeros((df1.shape[0], df1.shape[2]))
res_tfce = np.zeros((df1.shape[0], df1.shape[2]))
print(res_tfce.shape)

pos = io.loadmat(f'{prefix}pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'{prefix}channel_labels.mat')['chanlabels'])
dict_col = { 'risk': 'salmon', 'norisk': 'olivedrab', 'prerisk': 'mediumpurple' , 'postrisk':'darkturquoise'  }

for i in range(102):       
    res_tfce[:, i] = np.array(tfce(df1[:, :, i],df2[:, :, i], title = chan_labels[i+204]))
print('\tTFCE done')    

#print('res_tfce shape', res_tfce.shape)


res_tfce = res_tfce.transpose(1,0)
print('res_tfce shape new', res_tfce.shape)
#donor data file

print('BINARY SHAPE', binary.shape)
##### CONDITION1 ######
# average = 0.1 means averaging of the power data over 100 ms

temp.data = comp1_mean[204:,:]
fig = temp.plot_topomap(times = times_to_plot, average = 0.1,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = legend[0], colorbar = True, vmax=p_mul_topo, vmin=-p_mul_topo)

fig.savefig(os.path.join(output, legend[0] + '_vs_' + legend[1], legend[0] + '.png'), dpi = 300)
plt.close()

##### CONDITION2 ######
    
temp.data = comp2_mean[204:,:]
fig = temp.plot_topomap(times = times_to_plot, average = 0.1,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15),
                            ch_type='planar1', time_unit='s', show = False, 
                            title = legend[1], colorbar = True, vmax=p_mul_topo, vmin=-p_mul_topo)
fig.savefig(os.path.join(output, legend[0] + '_vs_' + legend[1], legend[1] + '.png'), dpi = 300)
plt.close()
    
##### CONDITION2 - CONDITION1 with marks (no FDR, TFCE correction) ######

temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]
fig = temp.plot_topomap(times = times_to_plot, average = 0.1,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = '%s - %s'%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul_topo_contrast, vmin=-p_mul_topo_contrast, extrapolate="local", mask = np.bool_(binary[204:,:]),
                            mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='k',
                                               linewidth=0, markersize=7, markeredgewidth=2))
fig.savefig(os.path.join(output, legend[0] + '_vs_' + legend[1],'difference.png'), dpi = 300)
plt.close()

#### CONDITION2 - CONDITION1 with marks (WITH TFCE) ######
temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]

fig = temp.plot_topomap(times = times_to_plot, average = 0.1,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = '%s - %s, with TFCE'%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul_topo_fdr_contrast, vmin=-p_mul_topo_fdr_contrast, extrapolate="local", mask = np.bool_(res_tfce),
                            mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='k',
                                               linewidth=0, markersize=7, markeredgewidth=2))
fig.savefig(os.path.join(output, legend[0] + '_vs_' + legend[1],'difference_with_TFCE.png'), dpi = 300)
plt.close()

html_name = os.path.join(output, legend[0] + '_vs_' + legend[1] + '.html')
clear_html(html_name)
add_str_html(html_name, '<!DOCTYPE html>')
add_str_html(html_name, '<html>')
add_str_html(html_name, '<body>')
if grand_average == True:
    add_str_html(html_name, '<p style="font-size:20px;"><b> %s, %s, %s, trained, %s, %d subjects </b></p>' % (legend[0] + '_vs_' + legend[1], ERF, stimulus, baseline, len(subjects1)))
else:
    assert(grand_average == False)
    if response:
        add_str_html(html_name, '<p style="font-size:20px;"><b> %s, averaged %s, trained, %s, %s, %d subjects </b></p>' % (legend[0] + '_vs_' + legend[1], frequency, baseline, zero_point, len(subjects1)))
    if stim:
        add_str_html(html_name, '<p style="font-size:20px;"><b> %s, averaged %s, trained, %s, zero_point at stimulus %d subjects </b></p>' % (legend[0] + '_vs_' + legend[1], frequency,  baseline, len(subjects1)))
add_str_html(html_name, '<p style="font-size:20px;"><b> P_val < 0.05 marked (or saved from cutting) </b></p>' )
add_str_html(html_name, '<table>')
for topo in topomaps:
    add_str_html(html_name, "<tr>")
    add_pic_topo_html(html_name, os.path.join(legend[0] + '_vs_' + legend[1],topo+'.png'))
add_str_html(html_name, "</tr>")
add_str_html(html_name, '</body>')
add_str_html(html_name, '</html>')
pdf_file = html_name.replace("html", "pdf")
#pdfkit.from_file(html_name, pdf_file, configuration = config, options=options)
print('All done!')
