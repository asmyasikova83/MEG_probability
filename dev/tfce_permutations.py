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

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}
planars = ['planar1', 'planar2', 'combine_planar']

def plot_stat_comparison(comp1, comp2, comp1_stderr, comp2_stderr, p_val, res_tfce, time, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2', comp1_color = 'k', comp2_color = 'k'):

    assert(len(comp1) == len(comp2) == len(time))
    res = False
    plt.figure()
    plt.rcParams['axes.facecolor'] = 'none'
    plt.xlim(time[0], time[-1])
    plt.ylim(-p_mul, p_mul)
    plt.plot([0, 0.001], [-3, 3], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([-4, 4], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([2.6, 2.601], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label)
    plt.fill_between(time, comp1-comp1_stderr, comp1+comp1_stderr, alpha=.2, facecolor = comp1_color)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label)
    plt.fill_between(time, comp2-comp2_stderr, comp2+comp2_stderr, alpha=.2, facecolor = comp2_color)

    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = (res_tfce == 1), facecolor = 'crimson', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = ((p_val < 0.05)*(res_tfce==0)), facecolor = 'c', alpha = 0.46, step = 'pre')
    # check statistically significant sensors in a predefined time interval. Here it is [1.0 1.4]
    if sign_sensors:
        for i in range(len(time)): 
           # if 0.195 < time[i] and time[i] < 0.205 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.50 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.60 and p_val[i] < 0.05:
             if np.around(time[i], decimals = 2) == 0.20 and p_val[i] < 0.05 or (np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05) or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05:
                plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'g', alpha = 0.46, step = 'pre')
                res = True
    #arr_ind = np.zeros(102)
    plt.tick_params(labelsize = 14)
    plt.legend(loc='upper right', fontsize = 14)
    plt.title(title, fontsize = 36)
    output = 'output_tfce/'
    path = output + folder + '/'
    os.makedirs(path, exist_ok = True)
    plt.savefig(path+title + '.svg', transparent=True)
    plt.close()
    return res


##############################################################
def tfce (df1,df2, title): #модифицированный пример из гитхаба Платона
    # create random data arrays
    A = df1
    A = A.transpose()
    B = df2
    B = B.transpose()
    subject_count = A.shape[0]
    data_length = A.shape[1]
    # check that python outputs data to binary files with expected byte count
    assert array("B", [0]).itemsize == 1
    assert array("I", [0]).itemsize == 4
    assert array("d", [0]).itemsize == 8

# write input data to file
    data_file = open("data.bin", "wb")
    array("I", [subject_count]).tofile(data_file)
    for s in range(subject_count):
        array("I", [data_length]).tofile(data_file)
        array("d", A[s]).tofile(data_file)
        array("I", [data_length]).tofile(data_file)
        array("d", B[s]).tofile(data_file)
    data_file.close()
    print(f'Channel {title} is being processed')
    print(f'df1 shape is {df1.shape}')
    # call libtfce binary
    subprocess.call([
        "/home/asmyasnikova83/DATA/libtfce",
    #    "--explore",
        "-e", "1",
        "-h", "2",
        "--input-file", "data.bin",
        "--output-file", f"{title}.bin",
        "--permutation-count", "1000",
        "--type", "1d"])

    # read result back
    result_file = open(f"{title}.bin", "rb")
    result_size = array("I", [])
    result_size.fromfile(result_file, 1)
    result = array("B", [])
    result.fromfile(result_file, result_size[0])
    result = result.tolist()
    result_file.close()
#    print(result)
    return (result)
    

os.chdir('/home/asmyasnikova83/GITHUB/MEG_probability') #папка где будут сохраняться картинки
output = 'output_tfce/'
rewrite = True
os.makedirs (output, exist_ok=True)


time = np.arange(-2.000, 1.502, 0.004)
    
num = 0 # это типа номер графика с четырьмя кривыми, самого первого 

i = 0
subjects1 = []
for ind, subj in enumerate(subjects):
    rf1 = out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
    file1 = pathlib.Path(rf1)
    rf2 = out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[1], frequency, train)
    file2 = pathlib.Path(rf2)
    if file1.exists() and file2.exists():
        print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
        subjects1.append(subj)
        i = i + 1
    print('i: ', i)
    #a container for tapers in neg and pos reinforcement, i - ov
cond1 = np.zeros((i, 306, 876))
cond2 = np.zeros((i, 306, 876))

i = 0
rsubjects1 = random.sample(subjects1, k = len(subjects1))
print('rsubjects1', rsubjects1)
for ind, subj in enumerate(rsubjects1):
    rf = out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
    print(rf)
    file = pathlib.Path(rf)
    if file.exists():
        print('exists:', rf)
        print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
        #positive FB
        print('kind[0]', kind[0])
        temp1 = mne.Evoked(out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train))
        temp1 = temp1.pick_types("grad")
        print('data shape', temp1.data.shape)
        #planars
        cond1[i, :204, :] = temp1.data
        #combined planars
        cond1[i, 204:, :] = temp1.data[::2] + temp1.data[1::2]
        #negative FB
        print('kind[1]', kind[1])
        temp2 = mne.Evoked( out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[1], frequency, train))
        temp2 = temp2.pick_types("grad")
        cond2[i, :204, :] = temp2.data
        cond2[i, 204:, :] = temp2.data[::2] + temp2.data[1::2]
        i = i + 1
df1 = cond1[:, 204:, :] #per channel
df2 = cond2[:, 204:, :]
df1 = df1.transpose(2, 0, 1)
df2 = df2.transpose(2, 0, 1)
print('df1 shape', df1.shape)
print('df2 shape', df2.shape)
    
df1_mean = df1.mean(axis = 1)
df2_mean = df2.mean(axis = 1)
   # df3_mean = df3.mean(axis = 1)
   # df4_mean = df4.mean(axis = 1)
    
    ### тут начинаем готовить общую фигуру### 
    
 
fig = plt.figure(figsize=(8, 5)) # создаем общую фигуру
gs = gridspec.GridSpec(nrows=2, ncols=4)
fig.suptitle('%s' %(i), fontsize=25, fontweight='bold')
plt.gcf().text(0.12, 0.4, '%s subjects' %(df1.shape[1]), fontsize=15, fontweight='bold')
plt.gcf().text(0.12, 0.35, 'tfce_significant_intervals', fontsize=15, bbox=dict(facecolor='crimson', alpha=0.2))
plt.gcf().text(0.12, 0.3, 'p<0.05_intervals', fontsize=15, bbox=dict(facecolor='g', alpha=0.2))
plt.gcf().text(0.12, 0.25, 'soft treshold: >=2 trials for subj', fontsize=15)

df1_stderr = np.zeros((876, 102))
df2_stderr = np.zeros((876, 102))
t_stat = np.zeros((876, 102))
p_val =  np.zeros((876, 102))
res_tfce = np.zeros((876, 102))

pos = io.loadmat(f'{prefix}pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'{prefix}channel_labels.mat')['chanlabels'])
dict_col = { 'risk': 'salmon', 'norisk': 'olivedrab', 'prerisk': 'mediumpurple' , 'postrisk':'darkturquoise'  }

#df2_mean = df2.mean(axis = 1)
for i in range(102):       
    df1_stderr[:, i] = scipy.stats.sem(df1[:, :, i], axis=1)
    df2_stderr[:, i] = scipy.stats.sem(df2[:, :, i], axis=1)
    #p_fdr = mul.fdrcorrection(p_val)[1]
    #ip_fdr = mul.fdrcorrection(p_val)[1]
    t_stat[:, i], p_val[:, i] = stats.ttest_rel(df1[:, :, i], df2[:, :, i], axis=1)
    res_tfce[:, i] = np.array(tfce(df1[:, :, i],df2[:, :, i], title = chan_labels[i+204]))
    res = plot_stat_comparison(df1_mean[:,i], df2_mean[:, i], df1_stderr[:, i], df2_stderr[:, i], p_val[:, i], res_tfce[:, i], time, title = chan_labels[i+204],
                             folder = f'{legend[0]}_vs_{legend[1]}', 
                             comp1_label = kind[0], comp2_label = kind[1], 
                             comp1_color=dict_col[f'{kind[0]}'], comp2_color = dict_col[f'{kind[1]}'])
    n = 1
    if res:
        print(n, " chn num: ", indx, "chn name: ", chan_labels[indx+204])
        n = n + 1
print('\tPictures generated')    

for ind, planar in enumerate(planars):
    #place the channel time courses in html file
    html_name = '/home/asmyasnikova83/GITHUB/MEG_probability/output_tfce/pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{legend[0]}', f'{legend[1]}', 'all')
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:32px;"><b> %s, averaged %s, %s, trained, TFCE corrected, %d subjects <span style="color:cyan;"> (p_val < 0.05)*(res_tfce==0)) </span> <span style="color:crimson;"> res_tfce == 1 </span> </b></p>' % (planar, frequency, stimulus, len(subjects1)))
    #title = ["Positive Feedback", "Negative Feedback"]
    add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (legend[0], legend[1]))
    #add_str_html(html_name, '<h1 style="font-size:32px;"><b> %s participants </b></h1>' % (contr.shape[0]))
    add_str_html(html_name, '<h1 style="font-size:48px;"><b> (%s) </b></h1>' % 3)
    #placing the channel time courses and save the html
    if ind == 2:
        for ch_num in range(204, len(chan_labels)):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_time_course_html(html_name, pic, f'{legend[0]}_vs_{legend[1]}', pos[ch_num], [200,150])
    else:
        for ch_num in range(ind, 204, 2):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_time_course_html(html_name, pic, f'{legend[0]}_vs_{legend[1]}', pos[ch_num], [200,150])

    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdf_file = html_name.split("/")[1].split('.')[0]
    print(os.getcwd() + '/%s' % html_name)
    path = os.getcwd() + f'/output_tfce/{legend[0]}_vs_{legend[1]}/all_pdf/'
    os.makedirs(path, exist_ok = True)
print('\tAll printed')
