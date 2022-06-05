import os
import pdfkit
from config import parameter3, cond1_name, cond2_name, planars, path, path_pdf


config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

options = {
    'page-size':'A1',
    'orientation':'Landscape',
    'zoom':1.0,
    'no-outline':None,
    'quiet':''
 }
planars = ['comb_planar']
if parameter3 == 'negative':
    name = cond1
    cond1 = name + '_negative'
    cond2 = name + '_positive'
    pic_compose_comb_planar_LP_vs_HP_all.html
for planar in planars:
    html_name =  path + 'output/' + 'pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{cond1_name}', f'{cond2_name}', 'all')
    pdf_file = html_name.split("/")[-1].split('.')[0]
    pdfkit.from_file('%s' % html_name, path_pdf + '%s.pdf' % pdf_file, configuration = config, options=options)
    print('\tAll printed')
    print('Done')
    print('\tpdf completed') 
