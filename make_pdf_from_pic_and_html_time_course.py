import os, io
import mne
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import pdfkit
from config import *


def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

options = {
    'page-size':'A1',
    'orientation':'Landscape',
    'zoom':0.4,
    'no-outline':None,
    'quiet':''
}

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

path = os.getcwd()

html_name = '/home/sasha/MEG/GITHUB/MEG_probability/output/pic_compose_combine_planar_Norisk_vs_Risk_all.html'
pdf_file = html_name.split("/")[7].split('.')[0]
print('pdf_file', pdf_file)
print('%s' % html_name)
pdfkit.from_file('%s' % html_name, '/home/sasha/MEG/GITHUB/MEG_probability/output/Norisk_vs_Risk/all_pdf/%s.pdf' % pdf_file, configuration = config, options=options)
print('\tAll printed')
                        
                                                          
