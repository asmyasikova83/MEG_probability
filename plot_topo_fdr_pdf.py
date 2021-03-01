import pdfkit
from config import *

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
