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
from tfce import tfce
from plot_time_course_in_html_functions import plot_stat_comparison_tfce
from compute_p_val import compute_p_val

def tfce_process(conf):
    grand_average = conf.grand_average
    kind = conf.kind
    # perfom statistical check by means of Threshold Free Cluster Enhancement 
    options = {
        'page-size':'A3',
        'orientation':'Landscape',
        'zoom':0.57,
        'no-outline':None,
        'quiet':''
    }
    planars = ['planar1', 'planar2', 'combine_planar']

    if conf.grand_average == True:
        os.chdir(prefix_out + tfce_dir + GA_dir) #папка где будут сохраняться картинки
        cur_dir = prefix_out + tfce_dir + GA_dir
        frequency = None
    else:
        os.chdir(prefix_out + tfce_dir + tfr_dir)
        cur_dir = prefix_out + tfce_dir + tfr_dir
        frequency = conf.frequency
    comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary, subjects1 = compute_p_val(conf, subjects, kind, train, frequency, check_num_sens)
    df1 = contr[:, 0, 204:, :]
    df2 = contr[:, 1, 204:, :]
    print('df1 shape', df1.shape)
    print('df2 shape', df2.shape)
    df1 = df1.transpose(2, 0, 1)
    df2 = df2.transpose(2, 0, 1)
    df1_mean = df1.mean(axis = 1)
    df2_mean = df2.mean(axis = 1)
    df1_stderr = np.zeros((df1.shape[0], df1.shape[2]))
    df2_stderr = np.zeros((df1.shape[0], df1.shape[2]))
    t_stat = np.zeros((df1.shape[0], df1.shape[2]))
    p_val =  np.zeros((df1.shape[0], df1.shape[2]))
    res_tfce = np.zeros((df1.shape[0], df1.shape[2]))
    print(res_tfce.shape)

    pos = io.loadmat(f'{path_home}pos_store.mat')['pos']
    chan_labels = to_str_ar(io.loadmat(f'{path_home}channel_labels.mat')['chanlabels'])
    dict_col = { 'risk': 'salmon', 'norisk': 'olivedrab', 'prerisk': 'mediumpurple' , 'postrisk':'darkturquoise','risk_fb_negative':'crimson','risk_fb_positive':'cyan', 'norisk_fb_negative':'red','norisk_fb_positive':'blue', 'fb_positive_risk':'cyan', 'fb_negative_risk':'red', 'fb_positive_norisk':'salmon',  'fb_negative_norisk':'crimson' }

    #working with combined planars
    for i in range(102):       
        df1_stderr[:, i] = scipy.stats.sem(df1[:, :, i], axis=1)
        df2_stderr[:, i] = scipy.stats.sem(df2[:, :, i], axis=1)
        t_stat[:, i], p_val[:, i] = stats.ttest_rel(df1[:, :, i], df2[:, :, i], axis=1)
        res_tfce[:, i] = np.array(tfce(df1[:, :, i],df2[:, :, i], title = chan_labels[i+204]))
        res = plot_stat_comparison_tfce(conf, df1_mean[:,i], df2_mean[:, i], df1_stderr[:, i], df2_stderr[:, i], p_val[:, i], res_tfce[:, i], conf.time, title = chan_labels[i+204],
                                 folder = f'{legend[0]}_vs_{legend[1]}', 
                                 comp1_label = kind[0], comp2_label = kind[1], 
                                 comp1_color=dict_col[f'{kind[0]}'], comp2_color = dict_col[f'{kind[1]}'])
    print('\tPictures generated')    

    for ind, planar in enumerate(planars):
        #place the channel time courses in html file
        if conf.grand_average == True:
            html_name = prefix_out + tfce_dir + GA_dir + 'output_tfce/pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{legend[0]}', f'{legend[1]}', 'all')
        else:
            html_name = prefix_out + tfce_dir + tfr_dir +  'output_tfce/pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{legend[0]}', f'{legend[1]}', 'all')
        clear_html(html_name)
        add_str_html(html_name, '<!DOCTYPE html>')
        add_str_html(html_name, '<html>')
        add_str_html(html_name, '<body>')
        if grand_average == True:
            add_str_html(html_name, '<p style="font-size:32px;"><b> %s, %s, %s, trained, TFCE corrected, %s,  %d subjects <span style="color:cyan;"> (p_val < 0.05)*(res_tfce==0)) </span> <span style="color:crimson;"> res_tfce == 1 </span> </b></p>' % (planar, ERF, stimulus, baseline, len(subjects1)))
        else:
            assert(grand_average == False)
            if response:
                add_str_html(html_name, '<p style="font-size:32px;"><b> %s, averaged %s, trained, TFCE corrected, %s, %s, %d subjects <span style="color:cyan;"> (p_val < 0.05)*(res_tfce==0)) </span> <span style="color:crimson;"> res_tfce == 1 </span> </b></p>' % (planar, frequency, baseline, zero_point, len(subjects1)))
            if stim:
                add_str_html(html_name, '<p style="font-size:32px;"><b> %s, averaged %s, trained, TFCE corrected, %s, zero point at stimulus, %d subjects <span style="color:cyan;"> (p_val < 0.05)*(res_tfce==0)) </span> <span style="color:crimson;"> res_tfce == 1 </span> </b></p>' % (planar, frequency, baseline, len(subjects1)))
        add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (legend[0], legend[1]))
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
        #print('/%s' % html_name)
        path = f'{cur_dir}/output_tfce/{legend[0]}_vs_{legend[1]}/all_pdf/'
        print(path)
        os.makedirs(path, exist_ok = True)
    print('\tAll printed')
