import os
import shutil
import subprocess

from config import *

run_events_extraction = False
run_mio_correction = False
run_grand_average = True
run_tfce = True
convert_pdf = True
run_fdr = True
convert_fdr_pdf = True

if not convert_fdr_pdf:
    run_fdr = False

if not convert_pdf:
    run_tfce = False

if not run_tfce:
    run_grand_average = False

if not run_grand_average:
    run_mio_correction = False

if not run_mio_correction:
    run_events_extraction = False

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
    subprocess.call("python mio_correction.py", shell=True)

if run_grand_average:
    path_GA = prefix_out + GA_dir
    if os.path.exists(path_GA) and os.path.isdir(path_GA):
        shutil.rmtree(path_GA)
    os.makedirs(path_GA, exist_ok = True)
    subprocess.call("python grand_average.py", shell=True)

if run_tfce:
    path_tfce = prefix_out + tfce_dir + GA_dir
    if os.path.exists(path_tfce) and os.path.isdir(path_tfce):
        shutil.rmtree(path_tfce)
    os.makedirs(path_tfce, exist_ok = True)
    subprocess.call("python tfce_time_course_in_html_call.py", shell=True)

if convert_pdf:
    path_pdf = prefix_out + pdf_dir + GA_dir
    if os.path.exists(path_pdf) and os.path.isdir(path_pdf):
        shutil.rmtree(path_pdf)
    os.makedirs(path_pdf, exist_ok = True)
    subprocess.call("python make_pdf_from_pic_and_html_time_course.py", shell=True)

if run_fdr:
    path_fdr = prefix_out + fdr_dir + GA_dir
    if os.path.exists(path_fdr) and os.path.isdir(path_fdr):
         shutil.rmtree(path_fdr)
    os.makedirs(path_fdr, exist_ok = True)
    subprocess.call("python plot_topo_stat_call.py", shell=True)

if convert_fdr_pdf:
    path_fdr_pdf = prefix_out + fdr_pdf_dir + GA_dir
    if os.path.exists(path_fdr_pdf) and os.path.isdir(path_fdr_pdf):
         shutil.rmtree(path_fdr_pdf)
    os.makedirs(path_fdr_pdf, exist_ok = True)
    subprocess.call("python plot_topo_fdr_pdf.py", shell=True)
