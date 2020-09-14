import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import pdfkit
from config import *

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')
        print('IN: add str html')

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
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC=" ../output/%s" />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+pic))


config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}


contrast = ['Negative_Feedback_versus_Positive']

#planars = ['planar1', 'planar2', 'combine_planar']
planars = ['combine_planar']

output = 'output/'
rewrite = True
os.makedirs(output, exist_ok=True)

if mode == 'server':
    pos = io.loadmat('/home/asmyasnikova83/DATA/pos_store.mat')['pos']
    chan_labels = to_str_ar(io.loadmat('/home/asmyasnikova83/DATA/channel_labels.mat')['chanlabels'])
else:
    pos = io.loadmat('/home/sasha/MEG/GITHUB/MEG_probability/pos_store.mat')['pos']
    chan_labels = to_str_ar(io.loadmat('/home/sasha/MEG/GITHUB/MEG_probability/channel_labels.mat')['chanlabels'])    

subjects = [
    'P000',
    'P002',
    'P003',
    'P004',
    'P005',
    'P006',
    'P007',
    'P008',
    'P009',
    'P010',
    'P011',
    'P012',
    'P014',
    'P015',
    'P016',
    'P017',
    'P018',
    'P019',
    'P020',
    'P021',
    'P022',
    'P023',
    'P024',
    'P025',
    'P026',
    'P028',
    'P029',
    'P030']

path = os.getcwd()
contr = np.zeros((len(subjects), 2, 306, 876))

if mode == 'server':
    out_path = '/home/asmyasnikova83/DATA/evoked_ave/'
else:
    out_path = '/home/sasha/MEG/MIO_cleaning/'

kind = ['positive', 'negative']

for ind, planar in enumerate(planars):
    if mode == 'server':
        html_name = '/home/asmyasnikova83/GITHUB/MEG_probability/output/html_plots/pic_compose_%s_%s_vs_%s_%s.html' % (planar, "Positive", "Negative", "all")
    else:
        html_name = '/home/sasha/MEG/GITHUB/MEG_probability/result/pic_compose_%s_%s_vs_%s_%s.html' % (planar, "Positive", "Negative", "all")
        #html_name = 'output/pos_vs_neg/test.html'     
    clear_html(html_name) 
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    add_str_html(html_name, '<p style="font-size:26px;"><b> %s, feedback averaged Theta ~4-8 Hz <span style="color:green;"> 0.01 < p <= 0.05 </span> <span style="color:Magenta;">p <= 0.01 </span> </b></p>' % (planar))
    title = ["Positive Feedback", "Negative Feedback"]
    add_str_html(html_name, '<p style="font-size:26px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (title[0], title[1]))
    add_str_html(html_name, '<h1 style="font-size:26px;"><b> %s participants </b></h1>' % (contr.shape[0]))
    base = 29
    if ind == 2:
        for ch_num in range(204, len(chan_labels)):
            pic = chan_labels[ch_num] + '.svg'
            print('pic', pic)
            add_pic_html(html_name, pic, "pos_vs_neg", pos[ch_num], [base*4,base*3])
            print('Pic added! (ind == 2)')
    else:
        for ch_num in range(ind, 204, 2):
            pic = chan_labels[ch_num] + '.svg'
            pic = chan_labels[ch_num] + '.svg'
            print('pic', pic)
            add_pic_html(html_name, pic,  "pos_vs_neg", pos[ch_num], [base*4,base*3])
            print('Pic added! (ind == 2)')
    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')

    pdf_file = html_name.split("/")[7].split('.')[0]
    print('pdf_file', pdf_file)
    print('%s' % html_name)
    pdfkit.from_file('%s' % html_name, '/home/sasha/MEG/GITHUB/MEG_probability/output/pos_vs_neg/all_pdf/%s.pdf' % pdf_file, configuration = config, options=options)
print('\tAll printed')
                        
                                                          
