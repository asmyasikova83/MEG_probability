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
from plot_time_course_in_html_functions import add_pic_time_course_html
from plot_time_course_in_html_functions import plot_stat_comparison
from plot_time_course_in_html_functions import p_val_binary
from compute_p_val import compute_p_val

# visualization of time-course of power deviations from baseline + statistically significant intervals and sensors 
options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}

diction = {"Positive": "Positive Feedback",
           "Negative": "Negative Feedback"}

contrast = [f'{legend[0]}_vs_{legend[1]}']

planars = ['planar1', 'planar2', 'combine_planar']
#pathways
output = 'output/'
rewrite = True
os.makedirs(output, exist_ok=True)
path = os.getcwd()
#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat(f'{prefix}pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'{prefix}channel_labels.mat')['chanlabels'])
#P008, P025 removed
#P000,P012,P026 for trained is empty
#do permutations
if random_comp == True:
    N = 100
    COMP1_MEAN = np.zeros((N, 306, 876))
    COMP2_MEAN = np.zeros((N, 306, 876))
    CONTR = np.zeros((N, 41, 2, 306, 876)) #TODO: check len(subjects)
    P_VAL = np.zeros((N, 306, 876))
    BINARY = np.zeros((N, 306, 876))
    for i in range(N):
        COMP1_MEAN[i,:, :], COMP2_MEAN[i, :, :], CONTR[i,:,:,:,:], temp1, temp2, P_VAL[i, : , :], BINARY[i, :, :], subjects1 = compute_p_val(subjects, kind, train, frequency, check_num_sens)
    comp1_mean = COMP1_MEAN.mean(axis=0)
    comp2_mean = COMP2_MEAN.mean(axis=0)
    contr = CONTR.mean(axis=0)
    p_val = P_VAL.mean(axis=0)
    binary = BINARY.mean(axis=0)
else:
#load and compute statistics
    comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary, subjects1 = compute_p_val(subjects, kind, train, frequency, check_num_sens)


if False:
    time = np.arange(-0.5, 0.05*(comp1_mean.shape[1])-0.5, 0.05)
    print(comp1_mean.shape)
else:
    time = temp1.times
    print('time: ', len(time))

if rewrite:
    n = 1
    #settings for combined planars
    #plot the time courses, mark stat significant intervals and channels
    for indx in range(102):
        res = plot_stat_comparison(comp1_mean[indx+204], comp2_mean[indx+204], p_val[indx+204], p_mul, time, title = chan_labels[indx+204],
                             folder = f'{legend[0]}_vs_{legend[1]}', comp1_label = f'{legend[0]}', comp2_label = f'{legend[1]}')
        if res:
            print(n, " chn num: ", indx, "chn name: ", chan_labels[indx+204])
            n = n + 1
    print('\tPictures generated')
else:
    print('\tPictures uploaded')

for ind, planar in enumerate(planars):
    #place the channel time courses in html file
    html_name = '/home/asmyasnikova83/GITHUB/MEG_probability/output/pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{legend[0]}', f'{legend[1]}', 'all')
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:32px;"><b> %s, averaged %s, trained, %d subjects ORIGINAL (random over subjects) <span style="color:green;"> 0.01 < p <= 0.05 </span> <span style="color:Magenta;">p <= 0.01 </span> </b></p>' % (planar, frequency, len(subjects1)))
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
    path = os.getcwd() + f'/output/{legend[0]}_vs_{legend[1]}/all_pdf/'
    os.makedirs(path, exist_ok = True)
print('\tAll printed')
