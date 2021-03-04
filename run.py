import os
import shutil
import argparse

from config import *
from risk_norisk_events_extraction import risk_norisk_events
from mio_correction import mio_correction

from grand_average import grand_average_process
from tfr import tfr_process
from make_evoked_freq_data_container import container_process

from tfce_time_course_in_html_call import tfce_process
from make_pdf_from_pic_and_html_time_course import make_pdf

from plot_topo_stat_call import topo_stat
from plot_topo_fdr_pdf import make_fdr_pdf

def env(path, prev_path=None):
    if prev_path:
        assert os.path.exists(prev_path) and os.path.isdir(prev_path), f"{prev_path} does not exist"
    if os.path.exists(path) and os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok = True)

run_events_extraction = False
run_mio_correction = False

run_grand_average = False
run_tfr = False
run_container = False

run_tfce = False
convert_pdf = False

run_fdr = False
convert_fdr_pdf = False

parser = argparse.ArgumentParser()
parser.add_argument('mode', choices=['ga', 'tfr'], help='available modes: ga(aka grand_average), tfr')
parser.add_argument('-s', '--stage', \
        choices=['events', 'mio', 'ERF', 'tfr', 'container_tfr', 'time_course_stat', 'make_tfce_pdf', 'topo_stat', 'make_fdr_pdf'], \
        help='stage of processing')
args = parser.parse_args()
mode = args.mode
stage = args.stage

print(mode)
if mode == 'ga':
    conf = conf(mode = 'grand_average', kind = ['norisk', 'risk'])
elif mode == 'tfr':
    conf = conf(mode = 'tfr', kind = ['norisk', 'risk'], frequency = 'theta')

print(stage)

if not stage:
    print('All stages!')
    run_events_extraction = True
    run_mio_correction = True

    if mode == 'ga':
        run_grand_average = True
    elif mode == 'tfr':
        run_tfr = True
        run_container = True

    run_tfce = True
    convert_pdf = True

    run_fdr = True
    convert_fdr_pdf = True

elif stage == 'events':
    run_events_extraction = True
elif stage == 'mio':
    run_mio_correction = True

elif stage == 'ERF':
    assert mode == 'ga'
    run_grand_average = True
elif stage == 'tfr':
    assert mode == 'tfr'
    run_tfr = True
elif stage == 'container_tfr':
    assert mode == 'tfr'
    run_container = True

elif stage == 'time_course_stat':
    run_tfce = True
elif stage == 'make_tfce_pdf':
    convert_pdf = True

elif stage == 'topo_stat':
    run_fdr = True
elif stage == 'make_fdr_pdf':
    convert_fdr_pdf = True


path_events = conf.prefix_out + events_dir
if run_events_extraction:
    env(path_events)
    #subprocess.call("python risk_norisk_events_extraction.py", shell=True)
    risk_norisk_events(conf)

path_mio = conf.prefix_out + mio_dir
if run_mio_correction:
    env(path_mio, path_events)
    mio_correction(conf)

prefix_out = conf.prefix_out
if mode == 'ga':
    GA_dir = conf.GA_dir
    path_GA = prefix_out + GA_dir
    if run_grand_average:
        env(path_GA, path_mio)
        grand_average_process(conf)
    path_pdf = prefix_out + pdf_dir + GA_dir
    path_fdr = prefix_out + fdr_dir + GA_dir
    path_fdr_pdf = prefix_out + fdr_pdf_dir + GA_dir
else:
    tfr_dir = conf.tfr_dir
    path_TFR = prefix_out + tfr_dir
    if run_tfr:
        env(path_TFR, path_mio)
        tfr_process(conf)
    path_container = prefix_out + conf.container_dir
    if run_container:
        env(path_container, path_TFR)
        container_process(conf)
    path_pdf = prefix_out + pdf_dir + fdr_dir
    path_fdr = prefix_out + fdr_dir + tfr_dir
    path_fdr_pdf = prefix_out + fdr_pdf_dir + tfr_dir


if run_tfce:
    env(conf.path_tfce, path_GA if mode == 'ga' else path_container)
    tfce_process(conf)

if convert_pdf:
    env(path_pdf, path_tfce)
    make_pdf(conf)


if run_fdr:
    env(path_fdr, path_GA)
    topo_stat(conf)

if convert_fdr_pdf:
    env(path_fdr_pdf, path_fdr)
    make_fdr_pdf(conf)

