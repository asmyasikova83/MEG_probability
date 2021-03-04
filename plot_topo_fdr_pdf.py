import pdfkit
from config import *

def make_fdr_pdf(conf):
    grand_average = conf.grand_average

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    options = {
        'page-size':'A3',
        'orientation':'Landscape',
        'zoom':1.0,
        'no-outline':None,
        'quiet':''
    }

    if grand_average == True:
        html_name = prefix_out + fdr_dir + GA_dir + f'{legend[0]}_vs_{legend[1]}.html'
    else:
        html_name = prefix_out + fdr_dir + tfr_dir + f'{legend[0]}_vs_{legend[1]}.html'
    pdf_file = html_name.split("/")[-1].split('.')[0]
    print('pdf_file', pdf_file)
    print('%s' % html_name)
    if grand_average == True:
        pdfkit.from_file('%s' % html_name, prefix_out + fdr_pdf_dir + GA_dir + '%s.pdf' % pdf_file, configuration = config, options=options)
    else:
        pdfkit.from_file('%s' % html_name, prefix_out + fdr_pdf_dir + tfr_dir + '%s.pdf' % pdf_file, configuration = config, options=options)
    print('\tAll printed')
    print('Done')
