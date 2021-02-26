import os
import shutil
import subprocess

from config import *

rm_events = True
create_events = True
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

