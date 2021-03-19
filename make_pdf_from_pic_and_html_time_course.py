import pdfkit
from config import conf

def make_pdf(conf):
    print('\trun pdf tfce on time courses...')
    legend = conf.legend
    verbose = conf.verbose
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

    html_name = conf.path_tfce + f'output_tfce/pic_compose_combine_planar_{legend[0]}_vs_{legend[1]}_all.html'
    pdf_file = html_name.split("/")[-1].split('.')[0]
    if verbose:
        print('pdf_file', pdf_file)
        print('%s' % html_name)
    pdfkit.from_file('%s' % html_name, conf.path_pdf  + '%s.pdf' % pdf_file, configuration = config, options=options)
    if verbose:
        print('\tAll printed')
    print('\tpdf tfce completed')
