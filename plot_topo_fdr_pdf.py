import pdfkit
from config import *

def make_fdr_pdf(conf):
    print('\trun pdf fdr on topomaps...')

    grand_average = conf.grand_average
    verbose = conf.verbose

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    options = {
        'page-size':'A3',
        'orientation':'Landscape',
        'zoom':1.0,
        'no-outline':None,
        'quiet':''
    }

    html_name = conf.path_fdr + f'{legend[0]}_vs_{legend[1]}.html'
    pdf_file = html_name.split("/")[-1].split('.')[0]
    if verbose:
        print('pdf_file', pdf_file)
        print('s' % html_name)
    pdfkit.from_file('%s' % html_name, conf.path_fdr_pdf + '%s.pdf' % pdf_file, configuration = config, options=options)
    if verbose:
        print('\tAll printed')
        print('Done')
    print('\tpdf fdr completed')
