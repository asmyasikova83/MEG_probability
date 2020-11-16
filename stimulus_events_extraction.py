import mne
import numpy as np
from config import *
                                                                                                                                                                                                                   
fpath = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_events_stimulus_risk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_stimulus_risk.txt'
fpath_events_stimulus_norisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_stimulus_norisk.txt'
#fpath_events_prerisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_prerisk.txt'
#fpath_events_postrisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_postrisk.txt'
fpath_log = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_log_risk_norisk.txt'

for run in runs:
    for subject in subjects:
        print(fpath.format(subject, run, subject))                                                                                                                                                                 
        raw = mne.io.read_raw_fif(fpath.format(subject, run, subject), allow_maxshield=False, preload=True, verbose=None)

        events = mne.find_events(raw, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose=None)

        res = []
        log = []
        stimulus_risk = []
        stimulus_norisk = []
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
                #risk
            if events[i][2] == 42 or events[i][2] == 43 or events[i][2] == 44 or events[i][2] == 45: #incorrect response
                if trained:
                    res.append(events[i])
                    log.append('wrong')
                else:
                    correct_count = 0
       
            if correct_count > 3 and trained == False:
                trained = True
                res.append(events[i])
                log.append('correct')
           
            if trained and events[i - 1][2] == 40 or trained and events[i - 1][2] == 41 or trained and events[i - 1][2] == 46 or trained and events[i - 1][2] == 47:
                if i + 7 >= len(events):
                    continue
                str_digit1 = str(events[i + 3][2])
                str_digit2 = str(events[i + 4][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 3][2] == 42 or events[i + 3][2] == 43  or events[i + 3][2] == 43 or events[i + 3][2] == 44 or events[i + 3][2] == 45:
                        print('risk:2d step')
                        if events[i + 7][2] == 40 or events[i + 7][2] == 41  or events[i + 7][2] == 46 or events[i + 7][2] == 47:
                            if events[i + 2][2] == 11:
                                stimulus_risk.append(events[i + 2])
                            #risk.append(events[i + 3])
                                print('risk: 3d step')
              
            if trained and events[i - 1][2] == 40 or trained and events[i - 1][2] == 41 or trained and events[i - 1][2] == 46 or trained and events[i - 1][2] == 47:
                if i + 7 >= len(events):
                    continue
                str_digit1 = str(events[i + 3][2])
                str_digit2 = str(events[i + 4][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 3][2] == 40 or events[i + 3][2] == 41 or events[i + 3][2] == 46 or events[i + 3][2] == 47:
                        print('norisk: 2d step')
                        if events[i + 7][2] == 40 or events[i + 7][2] == 41 or events[i + 1][2] == 46 or events[i + 7][2] == 47:
                            if events[i + 2][2] == 11:
                                stimulus_norisk.append(events[i + 2])
                                print('norisk: 3d step')
                               # norisk.append(events[i + 3])
  
            if trained and events[i - 1][2] == 40 or trained and events[i - 1][2] == 41 or trained and events[i - 1][2] == 46 or trained and events[i - 1][2] == 47:
                if i + 7 >= len(events):
                    continue
                str_digit1 = str(events[i + 3][2])
                str_digit2 = str(events[i + 4][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 3][2] == 40 or events[i + 3][2] == 41 or events[i + 3][2] == 46 or events[i + 3][2] == 47:
                        print('prerisk: 2d step')
                        if events[i + 7][2] == 42 or events[i + 7][2] == 43 or events[i + 7][2] == 44 or events[i + 7][2] == 45:
                            print('prerisk: 3d step')
                            #prerisk.append(events[i + 3])
                            #log_risk_norisk.append('prerisk')

            if trained and events[i - 1][2] == 42 or trained and events[i - 1][2] == 43 or trained and events[i - 1][2] == 44 or trained and events[i - 1][2] == 45:
                if i + 7 >= len(events):
                    print('Ready to continue')
                    continue
                str_digit1 = str(events[i + 3][2])
                str_digit2 = str(events[i + 4][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 3][2] == 40 or events[i + 3][2] == 41 or events[i + 3][2] == 46 or events[i + 3][2] == 47:
                        print('postrisk: 2d step')
                        if events[i + 7][2] == 40 or events[i + 7][2] == 41 or events[i + 7][2] == 46 or events[i+7][2] == 47:
                            print('postrisk: 3d step')
                            #postrisk.append(events[i + 3])
                            #log_risk_norisk.append('postrisk')
 
        if len(res) != 0:
            answer_count = correct_counter/len(res)
            print(answer_count)
            if answer_count > 0.66:
                events_stimulus_risk  = open(fpath_events_stimulus_risk.format(subject, run), "w")
                events_stimulus_norisk  = open(fpath_events_stimulus_norisk.format(subject, run), "w")
                print('events stimulus risk', stimulus_risk)
                np.savetxt(events_stimulus_risk, stimulus_risk, fmt = "%d")
                np.savetxt(events_stimulus_norisk, stimulus_norisk, fmt = "%d")
                events_stimulus_norisk.close()
                events_stimulus_risk.close()
                print('Saved!')
        else:
            print('Did not find trained!')
         
