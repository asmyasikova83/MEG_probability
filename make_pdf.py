import os
import pdfkit
from config import cond1, cond2, planars, path, path_pdf


config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':1.0,
    'no-outline':None,
    'quiet':''
 }

for planar in planars:
    html_name =  path + 'output/' + 'pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{cond1}', f'{cond2}', 'all')
    pdf_file = html_name.split("/")[-1].split('.')[0]
    pdfkit.from_file('%s' % html_name, path_pdf + '%s.pdf' % pdf_file, configuration = config, options=options)
    print('\tAll printed')
    print('Done')
    print('\tpdf completed') 
