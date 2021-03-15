import shutil
import os
import re

input_dir = '/home/asmyasnikova83/COLLECT/TFR__2021_03_15__03_11_27/events/'
output_dir = '/home/asmyasnikova83/MEG_probability/ref/full_TFR/events/'

for file in os.listdir(input_dir):
    if not re.match(r'.*log.*', file):
        shutil.copy(input_dir+file, output_dir)
