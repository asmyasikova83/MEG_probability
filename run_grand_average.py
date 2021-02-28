import os
import shutil
import subprocess

from config import *

run_events_extraction = True
run_mio_correction = True
run_grand_average = True
run_tfce = True

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
    path_GA = prefix_out + 'GA/'
    if os.path.exists(path_GA) and os.path.isdir(path_GA):
        shutil.rmtree(path_GA)
    os.makedirs(path_GA, exist_ok = True)
    subprocess.call("python grand_average.py", shell=True)

if run_tfce:
    path_tfce = prefix_out + tfce_dir
    if os.path.exists(path_tfce) and os.path.isdir(path_tfce):
        shutil.rmtree(path_tfce)
    os.makedirs(path_tfce, exist_ok = True)
    subprocess.call("python tfce_time_course_in_html_call.py", shell=True)

