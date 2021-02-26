import os
import shutil
import subprocess

from config import *

rm_events = True
create_events = True
run_events_extraction = True
run_mio_correction = False
run_grand_average = True

if not run_mio_correction:
    run_events_extraction = False

if not run_events_extraction:
    rm_events = False
    create_events = False

if rm_events:
    path_events = prefix_out + events_dir
    if os.path.exists(path_events) and os.path.isdir(path_events):
        shutil.rmtree(path_events)

if create_events:
    os.makedirs(path_events, exist_ok = True)

if run_events_extraction:
    subprocess.call("python risk_norisk_events_extraction.py", shell=True)

if run_mio_correction:
    subprocess.call("python mio_correction.py", shell=True)

if run_grand_average:
    path_GA = prefix_out + 'GA/'
    os.makedirs(path_GA, exist_ok = True)
    subprocess.call("python grand_average.py", shell=True)

