import shutil
import os
import re

input_dir = '/home/asmyasnikova83/TEST/test5_events_all__2021_03_15__16_36_41/events/'
output_dir = '/home/asmyasnikova83/MEG_probability/ref/test5_events_all/events'

for file in os.listdir(input_dir):
    if not re.match(r'.*log.*', file):
        shutil.copy(input_dir+file, output_dir)
