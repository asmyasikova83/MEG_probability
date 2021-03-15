import mne
import numpy as np
from config import *


fpath = '/home/asmyasnikova83/DATA/links/{}/{}_run{}_raw_tsss_mc.fif'
fpath_events_positive = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_positive.txt'
fpath_events_negative = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_negative.txt'
fpath_log = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_log.txt'

events_trained = []
log_trained_events = []
reinforcement_trained_positive= []
reinforcement_trained_negative= []
log_reinf_trained = []

for run in runs:
    for subject in subjects:
        print(fpath.format(subject, subject, run))

        raw = mne.io.read_raw_fif(fpath.format(subject, subject, run), allow_maxshield=False, preload=True, verbose=None)

        events = mne.find_events(raw, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose=None)

        res = []
        log = []
        reinforcement_pos = []
        reinforcement_neg = []
        log_reinf = []
        correct_count = 0
        correct_counter = 0
        trained = False
        answer_count = 0

        for i in range(len(events)):
            if events[i][2] == 40 or events[i][2] == 41 or events[i][2] == 46 or events[i][2] == 47: #correct responses
                if trained:
                    res.append(events[i])
                    log.append('correct')
                    correct_counter = correct_counter + 1
                else:
                    correct_count = correct_count + 1

                if trained and events[i][2] == [50] or trained and events[i][2] == [51]: #positive reinforcement
                    reinforcement_pos.append(events[i])
                    log_reinf.append('positive reinforcement')

                if trained and events[i][2] == [52] or trained and events[i][2] == [53]: #negative reinforcement
                    reinforcement_neg.append(events[i])
                    log_reinf.append('negative reinforcement')

            if events[i][2] == 42 or events[i][2] == 43 or events[i][2] == 44 or events[i][2] == 45: #incorrect responses
                if trained:
                    res.append(events[i])
                    log.append('wrong')
                else:
                    correct_count = 0

            if correct_count > 3 and trained == False:
                trained = True
                res.append(events[i])
                log.append('correct')

            if trained and events[i][2] == [50] or trained and events[i][2] == [51]: #positive reinforcement
                reinforcement_pos.append(events[i])
                log_reinf.append('positive reinforcement')

            if trained and events[i][2] == [52] or trained and events[i][2] == [53]: #negative reinforcement
                reinforcement_neg.append(events[i])
                log_reinf.append('negative reinforcement')           
         
        if len(res) != 0:
            answer_count = correct_counter/len(res)
            print(answer_count)
            if answer_count > 0.66:
                reinforcement_trained_positive.extend(reinforcement_pos)
                reinforcement_trained_negative.extend(reinforcement_neg)
                events_file_positive = open(fpath_events_positive.format(subject, run), "w")
                events_file_negative = open(fpath_events_negative.format(subject, run), "w")
                log_file = open(fpath_log.format(subject, run), "w")

                np.savetxt(events_file_positive, reinforcement_trained_positive, fmt="%d")
                np.savetxt(events_file_negative, reinforcement_trained_negative, fmt="%d")
                log_reinf_str='\n'.join(log_reinf)
                log_file.write(log_reinf_str)

                log_file.close()
                events_file_positive.close()
                events_file_negative.close()
                print('Saved!')
        else:
            print('Did not find trained')

