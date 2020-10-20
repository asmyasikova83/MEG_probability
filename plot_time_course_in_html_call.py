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


i = 0
for ind, subj in enumerate(subjects):
    rf = out_path + "{0}_feedback_{1}_{2}_{3}-ave.fif".format(subj, kind[0], train, frequency)
    file = pathlib.Path(rf)
    if file.exists():
        print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
        i = i + 1
print('i: ', i)
#a container for tapers in neg and pos reinforcement, i - ov
contr = np.zeros((i, 2, 306, 876))


i = 0
for ind, subj in enumerate(subjects):
    rf = out_path + "{0}_feedback_{1}_{2}_{3}-ave.fif".format(subj, kind[0], train, frequency)
    print(rf)
    file = pathlib.Path(rf)
    if file.exists():
        print('exists:', rf)
        print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
        #positive FB
        temp1 = mne.Evoked(out_path + "{0}_feedback_{1}_{2}_{3}-ave.fif".format(subj, kind[0], train, frequency))
        temp1 = temp1.pick_types("grad")
        print('data shape', temp1.data.shape)
        #planars
        contr[i, 0, :204, :] = temp1.data
        #combined planars
        contr[i, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
        #negative FB
        temp2 = mne.Evoked( out_path + "{0}_feedback_{1}_{2}_{3}-ave.fif".format(subj, kind[1], train, frequency))
        temp2 = temp2.pick_types("grad")
        contr[i, 1, :204, :] = temp2.data
        contr[i, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]
        i = i + 1
print('CONTR shape', contr.shape)

comp1 = contr[:, 0, :, :]
comp2 = contr[:, 1, :, :]
#check the number of stat significant sensors in a predefined time interval
t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)

binary = p_val_binary(p_val, treshold = 0.05)

if check_num_sens:
    issue = binary[204:, 600]
    counter = 0
    for i in range(102):
        if issue[i] == 1:
            print('ch idx', i)
            counter = counter + 1
            print('counter', counter)
#average the freq data over subjects
comp1_mean = comp1.mean(axis=0)
comp2_mean = comp2.mean(axis=0)
print('COMP1.mean.shape', comp1_mean.shape)
print('COMP2.mean.shape', comp2_mean.shape)

#a number for plotting time courses - enough for amplitude

if False:
    time = np.arange(-0.5, 0.05*(comp1_mean.shape[1])-0.5, 0.05)
    print(comp1_mean.shape)
else:
    time = temp1.times
    print('time: ', len(time))

if rewrite:
    #for indx in range(comp1_mean.shape[0]):
      #  if indx < 204:
       #     p_mul = 0.3
       # else:
        #    p_mul = 1.6
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
        #print('Here')
        for ch_num in range(204, len(chan_labels)):
            pic = chan_labels[ch_num] + '.svg'
            #print('pic', pic)
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
