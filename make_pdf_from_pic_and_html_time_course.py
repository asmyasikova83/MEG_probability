import os, io
import mne
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import pdfkit
from config import *


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

html_name = prefix_out + tfce_dir + f'output_tfce/pic_compose_combine_planar_{legend[0]}_vs_{legend[1]}_all.html'
pdf_file = html_name.split("/")[-1].split('.')[0]
print('pdf_file', pdf_file)
print('%s' % html_name)
pdfkit.from_file('%s' % html_name, prefix_out + pdf_dir + '%s.pdf' % pdf_file, configuration = config, options=options)
print('\tAll printed')
                        
                                                          
