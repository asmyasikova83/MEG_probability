import os
import numpy as np
from config import conf
import pathlib

conf.kinds = ['norisk']
conf.subjects = ['P006','P007', 'P008']
conf.runs = ['2', '3', '4']
conf.train = ''
list_mio_events = []
list_mio_subj = []
conf.path_mio = '/home/asmyasnikova83/COLLECT/theta_norisk_risk__2021_03_30__16_47_04/MIO/'
mio_fname = f'{conf.path_mio}/' + 'mio_out_{}/{}_run{}_mio_corrected_{}{}.txt'
for i,kind in enumerate(conf.kinds):
    for subject in conf.subjects:
        mio_counter = 0
        for run in conf.runs: 
            path_mio = mio_fname.format(conf.kinds[i],subject, run, conf.kinds[i], conf.train)
            if pathlib.Path(path_mio).exists() and os.stat(path_mio).st_size != 0:
                mio_events = np.loadtxt(path_mio, dtype=int)
                print('subject', subject)
                print('run', run)
                print('mio events', mio_events)
                print('mio shape', len(mio_events))
                mio_counter = mio_counter + len(mio_events)
                print('mio_counter', mio_counter)
                mio_events = 0
            if run == conf.runs[-1]:
                print('Collected for ', subject)
                list_mio_events.append(subject)        
                list_mio_events.append(mio_counter)
                list_mio_subj.append(subject)

len_list = len(list_mio_subj)
print('sum subj for this kind', len_list)                   
print('list_mio_events', list_mio_events)                
print('list_subj', list_mio_subj)                
