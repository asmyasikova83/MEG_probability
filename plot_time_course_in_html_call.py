import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import copy
#import pdfkit
from config import *
import pathlib
from plot_time_course_in_html_functions import clear_html
from plot_time_course_in_html_functions import add_str_html
from plot_time_course_in_html_functions import contr_num
from plot_time_course_in_html_functions import to_str_ar
from plot_time_course_in_html_functions import get_short_legend
from plot_time_course_in_html_functions import get_full_legend
from plot_time_course_in_html_functions import delaete_bad_sub
from plot_time_course_in_html_functions import add_pic_html
from plot_time_course_in_html_functions import plot_stat_comparison
from plot_time_course_in_html_functions import p_val_binary
from compute_p_val import compute_p_val

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}

diction = {"Positive": "Positive Feedback",
           "Negative": "Negative Feedback"}

contrast = ['Negative_Feedback_versus_Positive']

planars = ['planar1', 'planar2', 'combine_planar']
#pathways
output = 'output/'
rewrite = True
os.makedirs(output, exist_ok=True)
path = os.getcwd()
#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/home/asmyasnikova83/DATA/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat('/home/asmyasnikova83/DATA/channel_labels.mat')['chanlabels'])
#P008, P025 removed
#P000,P012,P026 for trained is empty


kind = ['positive', 'negative']

comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary = compute_p_val(subjects, kind, train, frequency, check_num_sens)

#a number for plotting time courses - enough for amplitude

if False:
    time = np.arange(-0.5, 0.05*(comp1_mean.shape[1])-0.5, 0.05)
    print(comp1_mean.shape)
else:
    time = temp1.times
    print('time: ', len(time))

if rewrite:
    n = 1
    #settings for combined planars
    for indx in range(102):
        res = plot_stat_comparison(comp1_mean[indx+204], comp2_mean[indx+204], p_val[indx+204], p_mul, time, title = chan_labels[indx+204],
                             folder = "pos_vs_neg", comp1_label = "positive", comp2_label = "negative")
        if res:
            print(n, " chn num: ", indx, "chn name: ", chan_labels[indx+204])
            n = n + 1

    print('\tPictures generated')
else:
    print('\tPictures uploaded')

for ind, planar in enumerate(planars):
    #place the channel time courses on html file
    html_name = '/home/asmyasnikova83/GITHUB/MEG_probability/output/pic_compose_%s_%s_vs_%s_%s.html' % (planar, "Positive", "Negative", "all")
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    if frequency == 'gamma':
        add_str_html(html_name, '<p style="font-size:32px;"><b> %s, Feedback averaged Gamma ~32-100  Hz, no-trained, 1 run,  in 0.2 - 0.4 s  <span style="color:green;"> 0.01 < p <= 0.05 </span> <span style="color:Magenta;">p <= 0.01 </span> </b></p>' % (planar))
    title = ["Positive Feedback", "Negative Feedback"]
    add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (title[0], title[1]))
    add_str_html(html_name, '<h1 style="font-size:32px;"><b> %s participants </b></h1>' % (contr.shape[0]))
    add_str_html(html_name, '<h1 style="font-size:48px;"><b> (%s) </b></h1>' % 3)
    #placing the channel time courses and save the html
    if ind == 2:
        for ch_num in range(204, len(chan_labels)):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_html(html_name, pic, "pos_vs_neg", pos[ch_num], [200,150])
    else:
        for ch_num in range(ind, 204, 2):
            pic = chan_labels[ch_num] + '.svg'
            add_pic_html(html_name, pic,  "pos_vs_neg", pos[ch_num], [200,150])

    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdf_file = html_name.split("/")[1].split('.')[0]
    print(os.getcwd() + '/%s' % html_name)
    path = os.getcwd() + '/output/pos_vs_neg/all_pdf/'
    os.makedirs(path, exist_ok = True)
    #pdfkit.from_file(os.getcwd() + '/%s' % html_name, 'all_pdf/%s.pdf' % pdf_file, configuration = config, options=options)
print('\tAll printed')
