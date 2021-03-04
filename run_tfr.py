import os
import shutil
import subprocess

from config import *
from mio_correction import mio_correction
from tfr import tfr_process

run_events_extraction = False
run_mio_correction = False
run_tfr = True
run_container = False
run_tfce = False
convert_pdf = False
run_fdr = False
convert_fdr_pdf = False

conf = conf(mode = 'tfr', kind = ['norisk', 'risk'], frequency = 'theta')

if run_events_extraction:
    path_events = prefix_out + events_dir
    if os.path.exists(path_events) and os.path.isdir(path_events):
        shutil.rmtree(path_events)
    os.makedirs(path_events, exist_ok = True)
    subprocess.call("python risk_norisk_events_extraction.py", shell=True)

if run_mio_correction:
    path_mio = prefix_out + mio_dir
    if os.path.exists(path_mio) and os.path.isdir(path_mio):
        shutil.rmtree(path_mio)
    os.makedirs(path_mio, exist_ok = True)
    #subprocess.call("python mio_correction.py", shell=True)
    mio_correction(conf)

if run_tfr:
    path_TFR = prefix_out + tfr_dir
    if os.path.exists(path_TFR) and os.path.isdir(path_TFR):
        shutil.rmtree(path_TFR)
    os.makedirs(path_TFR, exist_ok = True)
    #subprocess.call("python tfr.py", shell=True)
    tfr_process(conf)

if run_container:
    path_container = prefix_out + container_dir
    if os.path.exists(path_container) and os.path.isdir(path_container):
        shutil.rmtree(path_container)
    os.makedirs(path_container, exist_ok = True)
    subprocess.call("python make_evoked_freq_data_container.py", shell=True)

if run_tfce:
    path_tfce = prefix_out + tfce_dir + tfr_dir
    if os.path.exists(path_tfce) and os.path.isdir(path_tfce):
        shutil.rmtree(path_tfce)
    os.makedirs(path_tfce, exist_ok = True)
    subprocess.call("python tfce_time_course_in_html_call.py", shell=True)

if convert_pdf:
    path_pdf = prefix_out + pdf_dir + tfr_dir
    if os.path.exists(path_pdf) and os.path.isdir(path_pdf):
        shutil.rmtree(path_pdf)
    os.makedirs(path_pdf, exist_ok = True)
    subprocess.call("python make_pdf_from_pic_and_html_time_course.py", shell=True)

if run_fdr:
    path_fdr = prefix_out + fdr_dir + tfr_dir
    if os.path.exists(path_fdr) and os.path.isdir(path_fdr):
         shutil.rmtree(path_fdr)
    os.makedirs(path_fdr, exist_ok = True)
    subprocess.call("python plot_topo_stat_call.py", shell=True)

if convert_fdr_pdf:
    path_fdr_pdf = prefix_out + fdr_pdf_dir + tfr_dir
    if os.path.exists(path_fdr_pdf) and os.path.isdir(path_fdr_pdf):
         shutil.rmtree(path_fdr_pdf)
    os.makedirs(path_fdr_pdf, exist_ok = True)
    subprocess.call("python plot_topo_fdr_pdf.py", shell=True)
