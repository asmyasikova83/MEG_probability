import mne
import numpy as np
from scipy import stats
import os
import copy
import matplotlib.pyplot as plt
import statsmodels.stats.multitest as mul
import pdfkit
from config import *
import pathlib

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

def add_pic_html(filename, pic):
    add_str_html(filename, '<IMG SRC="%s" style="width:%spx;height:%spx;"/>'%(pic,2800,390))
    

topomaps = ["Positive",
            "Negative",
            
            "difference",
            "difference_with_fdr",

            ]

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':1.0,
    'no-outline':None,
    'quiet':''
}

html_name = prefix_out + fdr_dir + f'{legend[0]}_vs_{legend[1]}.html'
pdf_file = html_name.split("/")[-1].split('.')[0]
print('pdf_file', pdf_file)
print('%s' % html_name)
pdfkit.from_file('%s' % html_name, prefix_out + fdr_pdf_dir + '%s.pdf' % pdf_file, configuration = config, options=options)
print('\tAll printed')
print('Done')
