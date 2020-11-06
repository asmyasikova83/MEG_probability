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
    
path = os.getcwd()
list_files = os.listdir(path)

output = 'output_topo/'


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
os.makedirs(os.path.join(output, "Positive_vs_Negative"), exist_ok=True)        

legend = ["Positive", "Negative"]
kind = ['positive', 'negative']

html_name = os.path.join(output, legend[0] + "_vs_" + legend[1] + ".html")
clear_html(html_name)
add_str_html(html_name, '<!DOCTYPE html>')
add_str_html(html_name, '<html>')
add_str_html(html_name, '<body>')
add_str_html(html_name, '<p style="font-size:40px;"><b> %s, average Theta 4-8 Hz after feedback presentation in 28 participants after training </b></p>' % (legend[0] + "_vs_" + legend[1]))
add_str_html(html_name, '<p style="font-size:40px;"><b> P_val < 0.05 marked (or saved from cutting) </b></p>' )
add_str_html(html_name, '<table>')
for topo in topomaps:
    add_str_html(html_name, "<tr>")
    add_pic_html(html_name, os.path.join(legend[0] + "_vs_" + legend[1],topo+".png"))
add_str_html(html_name, "</tr>")
add_str_html(html_name, '</body>')
add_str_html(html_name, '</html>')
pdf_file = html_name.replace("html", "pdf")
pdfkit.from_file(html_name, pdf_file, configuration = config, options=options)
print('Done')
