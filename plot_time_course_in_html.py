import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import copy
#import pdfkit
from config import *
import pathlib

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

def contr_num(filename):
    for ind, c in enumerate(contrast):
        if c in filename:
            return ind+1
    return None

def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

def get_short_legend(contrast):
    temp = contrast.split('_')
    return (temp[0], temp[2], temp[3], temp[4])

def get_full_legend(contrast):
    temp = contrast.split('_')
    return (diction[temp[0]], diction[temp[2]], diction[temp[3]], temp[4])

def delaete_bad_sub(contrast, del_list):
    for sub in del_list:
        if sub in contrast[1]:
            ind = contrast[1].index(sub)
            contrast[1].pop(ind)
            contrast[0] = np.delete(contrast[0], ind, axis=0)
    return contrast


def add_pic_html(filename, pic, pic_folder, pos_n, size):
    x = size[0]
    y = size[1]
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC=" %s" />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+pic))

def plot_stat_comparison(comp1, comp2, p_val, p_mul, time, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2'):
    assert(len(comp1) == len(comp2) == len(time))
    res = False
    plt.figure()
    plt.rcParams['axes.facecolor'] = 'none'
    plt.xlim(time[0], time[-1])
    plt.ylim(-p_mul, p_mul)
    plt.plot([0, 0.001], [-3, 3], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([-4, 4], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([2.6, 2.601], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1)
    #plt.axvline(0, color = 'k', linewidth = 3, linestyle = '--', zorder = 1)
    #plt.axhline(0, color = 'k', linewidth = 1.5, zorder = 1)
    #plt.axvline(2.5, color = 'k', linewidth = 3, linestyle = '--', zorder = 1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label)
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = (p_val < 0.01), facecolor = 'm', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = ((p_val >= 0.01) * (p_val < 0.05)), facecolor = 'g', alpha = 0.46, step = 'pre')
    # check statistically significant sensors in a predefined time interval. Here it is [1.0 1.4]
    sign_sensors2 = True
    if sign_sensors2:
        for i in range(len(time)): 
           # if 0.195 < time[i] and time[i] < 0.205 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.50 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.60 and p_val[i] < 0.05:
             if np.around(time[i], decimals = 2) == 0.20 and p_val[i] < 0.05 or (np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05) or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05:
                plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'g', alpha = 0.46, step = 'pre')
                res = True
            #if 0.395 < time[i] and time[i < 0.405 and p_val[i] < 0.05:
             #   plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'g', alpha = 0.46, step = 'pre')
            #if 0.495 < time[i] and time[i < 0.505 and p_val[i] < 0.05:
             #   plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'g', alpha = 0.46, step = 'pre')
            #if 0.595 < time[i] and time[i < 0.605 and p_val[i] < 0.05:
             #   plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'y', alpha = 0.46, step = 'pre')
    arr_ind = np.zeros(102)
    plt.tick_params(labelsize = 14)

    plt.legend(loc='upper right', fontsize = 14)
    plt.title(title, fontsize = 36)
    path = output + folder + '/'
    os.makedirs(path, exist_ok = True)
    plt.savefig(path+title + '.svg', transparent=True)
    plt.close()
    return res

def p_val_binary(p_val_n, treshold):
    p_val =  copy.deepcopy(p_val_n)
    for raw in range(p_val.shape[0]):
        for collumn in range(p_val.shape[1]):
            if p_val[raw, collumn] < treshold:
                p_val[raw, collumn] = 1
            else:
                p_val[raw, collumn] = 0
    return p_val

#config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

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

output = 'output/'
rewrite = True
os.makedirs(output, exist_ok=True)
#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/home/asmyasnikova83/DATA/pos_store.mat')['pos']

chan_labels = to_str_ar(io.loadmat('/home/asmyasnikova83/DATA/channel_labels.mat')['chanlabels'])
#P008, P025 removed
#P000,P012,P026 for trained is empty
#subjects for trained
path = os.getcwd()
# a container for averaged over runs and theta freq tapers data for Negative and Positve FB
contr = np.zeros((len(subjects), 2, 306, 876))

if mode == 'server':
    out_path = '/home/asmyasnikova83/DATA/evoked_ave/'
else:
    out_path = '/home/sasha/MEG/Evoked/'

kind = ['positive', 'negative']


i = 0
for ind, subj in enumerate(subjects):
    rf = out_path + "{0}_feedback_{1}_no_train_gamma-ave.fif".format(subj, kind[0])
    file = pathlib.Path(rf)
    if file.exists():
        print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
        i = i + 1
print('i: ', i)
contr = np.zeros((i, 2, 306, 876))


i = 0

for ind, subj in enumerate(subjects):
    rf = out_path + "{0}_feedback_{1}_no_train_gamma-ave.fif".format(subj, kind[0])
    print(rf)
    file = pathlib.Path(rf)
    if file.exists():
        print('exists:', rf)
        print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
        #positive FB
        temp1 = mne.Evoked(out_path + "{0}_feedback_{1}_no_train_gamma-ave.fif".format(subj, kind[0]))
        temp1 = temp1.pick_types("grad")
        print('data shape', temp1.data.shape)
        #planars
        contr[i, 0, :204, :] = temp1.data
        #combined planars
        contr[i, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
        #negative FB
        temp2 = mne.Evoked( out_path + "{0}_feedback_{1}_no_train_gamma-ave.fif".format(subj, kind[1]))
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
p_mul = 0.4

path = '/home/asmyasnikova83/DATA/evoked_ave/'

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
