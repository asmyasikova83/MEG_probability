import os
import numpy as np
from config import conf
import pathlib

#conf.kinds = ['prerisk_fb_negative','prerisk_fb_positive', 'postrisk_fb_negative', 'postrisk_fb_positive']
conf.subjects = ['P000','P001','P002','P003','P004','P005','P006','P007','P008','P009',
        'P010','P011','P012', 'P014','P015']
conf.kinds = ['prerisk']
#onf.subjects =['P014']
conf.runs = ['1', '2', '3', '4', '5', '6']
conf.train = ''
list_mio_events = []
list_mio_subj = []

#define path mio
path_mio = '/home/asmyasnikova83/WORK/run/MIO/'
mio_fname = f'{path_mio}' + 'mio_out_{}/{}_run{}_mio_corrected_{}{}.txt'
#define path events
path_trained_events = '/home/asmyasnikova83/WORK/run/events/'
trained_fevents = f'{path_trained_events}/' + '{}_run{}_events_{}_save_trained{}.txt'

for i,kind in enumerate(conf.kinds):
    global_proportion = 0
    ctr = 0
    for subject in conf.subjects:
        mio_counter = 0
        event_counter = 0
        proportion = 0
        exists = False
        for run in conf.runs: 
            fpath_mio = mio_fname.format(conf.kinds[i],subject, run, conf.kinds[i], conf.train)
            trained_events = trained_fevents.format(subject, run, conf.kinds[i], conf.train)
            if pathlib.Path(fpath_mio).exists() and os.stat(fpath_mio).st_size != 0:
                exists = True
                mio_events = np.loadtxt(fpath_mio, dtype=int)
                trained_events = np.loadtxt(trained_events, dtype=int)
                print('mio events', mio_events)
                print('trained_events', trained_events)
                if trained_events.shape == (3,):
                    trained_events = trained_events[np.newaxis, :]
                if mio_events.shape == (3,):
                    mio_events = mio_events[np.newaxis, :]
                mio_counter = mio_counter + len(mio_events)
                event_counter = event_counter + len(trained_events)
                print('mio counter', mio_counter)
                print('event counter', event_counter)
            if run == conf.runs[-1]:
                subject_title = subject + ' trained events, mio corr events, % lost events:'
                print('Collected for ', subject)
                if mio_counter != 0:
                    proportion = round((1 - mio_counter/event_counter)*100, 2)
                else:
                    proportion = '100% events are lost'
                if event_counter != 0:
                    list_mio_events.append(kind)
                    list_mio_events.append(subject_title)
                    list_mio_events.append(event_counter)        
                    list_mio_events.append(mio_counter)
                    list_mio_events.append(proportion)
                    list_mio_subj.append(subject)
        if exists:
            global_proportion = global_proportion + proportion
            ctr = ctr + 1
    list_mio_events.append(round(global_proportion/ctr, 2))
#len_list = len(list_mio_subj)
#print('sum subj for this kind', len_list)                   
print('list_mio_events', list_mio_events)                
#print('list_subj', list_mio_subj)
fname = path_mio + 'mio_list.txt'
with open(fname, 'w') as filehandle:
    for listitem in list_mio_events:
        filehandle.write('%s\n' % listitem)
