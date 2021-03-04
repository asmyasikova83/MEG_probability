import os
import shutil
import subprocess
import argparse

from config import *
from mio_correction import mio_correction
from grand_average import grand_average_process
from tfce_time_course_in_html_call import tfce_process
from make_pdf_from_pic_and_html_time_course import make_pdf
from plot_topo_stat_call import topo_stat
from plot_topo_fdr_pdf import make_fdr_pdf

def env(path):
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok = True)

run_events_extraction = False
run_mio_correction = False
run_grand_average = False

run_tfce = False
convert_pdf = False

run_fdr = False
convert_fdr_pdf = False

parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=['ga', 'tfr'], help='available modes: ga(aka grand_average), tfr')
parser.add_argument('-s', '--stage', \
        choices=['events', 'mio', 'ERF', 'time_course_stat', 'make_tfce_pdf', 'topo_stat', 'make_fdr_pdf'], \
        help='stage of processing')
args = parser.parse_args()
mode = args.mode
stage = args.stage
print(stage)

if not stage:
    print('All stages!')
    run_events_extraction = True
    run_mio_correction = True
    run_grand_average = True

    run_tfce = True
    convert_pdf = True

    run_fdr = True
    convert_fdr_pdf = True

elif stage == 'events':
    run_events_extraction = True
elif stage == 'mio':
    run_mio_correction = True
elif stage == 'ERF':
    run_grand_average = True

elif stage == 'time_course_stat':
    run_tfce = True
elif stage == 'make_tfce_pdf':
    convert_pdf = True

elif stage == 'topo_stat':
    run_fdr = True
elif stage == 'make_fdr_pdf':
    convert_fdr_pdf = True

conf = conf(mode = 'grand_average', kind = ['norisk', 'risk'])

if run_events_extraction:
    path_events = prefix_out + events_dir
    env(path_events)
    subprocess.call("python risk_norisk_events_extraction.py", shell=True)

if run_mio_correction:
    path_mio = prefix_out + mio_dir
    env(path_mio)
    mio_correction(conf)

if run_grand_average:
    path_GA = prefix_out + GA_dir
    env(path_GA)
    grand_average_process(conf)


if run_tfce:
    path_tfce = prefix_out + tfce_dir + GA_dir
    env(path_tfce)
    tfce_process(conf)

if convert_pdf:
    path_pdf = prefix_out + pdf_dir + GA_dir
    env(path_pdf)
    make_pdf(conf)


if run_fdr:
    path_fdr = prefix_out + fdr_dir + GA_dir
    env(path_fdr)
    topo_stat(conf)

if convert_fdr_pdf:
    path_fdr_pdf = prefix_out + fdr_pdf_dir + GA_dir
    env(path_fdr_pdf)
    make_fdr_pdf(conf)

