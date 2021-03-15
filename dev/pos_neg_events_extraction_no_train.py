import mne
import numpy as np
from config import *


fpath = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_events_positive = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_positive_no_train.txt'
fpath_events_negative = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_negative_no_train.txt'
fpath_log = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_log_no_train.txt'

for run in runs:
    for subject in subjects:
        print(fpath.format(subject, subject, run))

        raw = mne.io.read_raw_fif(fpath.format(subject, run, subject), allow_maxshield=False, preload=True, verbose=None)

        events = mne.find_events(raw, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose=None)

        reinforcement_pos = []
        reinforcement_neg = []
        reinforcement_positive= []
        reinforcement_negative= []
        log_reinf = []

        for i in range(len(events)):
            if events[i][2] == [50] or events[i][2] == [51]: #positive reinforcement
                reinforcement_pos.append(events[i])
                log_reinf.append('positive reinforcement')

            if events[i][2] == [52] or events[i][2] == [53]: #negative reinforcement
                reinforcement_neg.append(events[i])
                log_reinf.append('negative reinforcement')

        reinforcement_positive.extend(reinforcement_pos)
        reinforcement_negative.extend(reinforcement_neg)
        events_file_positive = open(fpath_events_positive.format(subject, run), "w")
        events_file_negative = open(fpath_events_negative.format(subject, run), "w")
        log_file = open(fpath_log.format(subject, run), "w")

        np.savetxt(events_file_positive, reinforcement_positive, fmt="%d")
        np.savetxt(events_file_negative, reinforcement_negative, fmt="%d")
        log_reinf_str='\n'.join(log_reinf)
        log_file.write(log_reinf_str)

        log_file.close()
        events_file_positive.close()
        events_file_negative.close()
        print('Saved!')

