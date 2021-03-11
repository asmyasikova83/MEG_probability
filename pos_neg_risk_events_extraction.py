import mne
import numpy as np
from config import *
                                                                                                                                                                                                                   
fpath = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_events_fb_positive_risk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_fb_positive_risk.txt'
fpath_events_fb_negative_risk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_fb_negative_risk.txt'
fpath_events_fb_positive_norisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_fb_positive_norisk.txt'
fpath_events_fb_negative_norisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_fb_negative_norisk.txt'

for run in runs:
    for subject in subjects:
        print(fpath.format(subject, run, subject))                                                                                                                                                                 
        raw = mne.io.read_raw_fif(fpath.format(subject, run, subject), allow_maxshield=False, preload=True, verbose=None)

        events = mne.find_events(raw, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose=None)

        res = []
        log = []
        fb_positive_risk = []
        fb_negative_risk =  []
        fb_negative_norisk = []
        fb_positive_norisk = []
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
           
            if  trained and events[i][2]== 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                print('first step in pos fb')
                if i + 8 >= len(events):
                    continue
                str_digit1 = str(events[i + 4][2])
                str_digit2 = str(events[i + 5][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                #remove double click
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 4][2] == 42 or events[i + 4][2] == 43  or events[i + 4][2] == 44 or events[i + 4][2] == 45:
                        if trained and events[i + 5][2] == 50 or trained and events[i + 5][2] == 51: #positive reinforcement
                            print('risk:2d step fb positive')
                            if events[i + 8][2] == 40 or events[i + 8][2] == 41  or events[i + 8][2] == 46 or events[i + 8][2] == 47:
                                fb_positive_risk.append(events[i + 4])
                                print('events risk fb pos', events[i + 4])
                                                
            if  trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                print('first step i neg fb!')
                if i + 8 >= len(events):
                    continue
                str_digit2 = str(events[i + 4][2])
                str_digit2 = str(events[i + 5][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                #remove double click
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 4][2] == 42 or events[i + 4][2] == 43  or events[i + 4][2] == 44 or events[i + 4][2] == 45:
                        if trained and events[i + 5][2] == 52 or trained and events[i + 5][2] == 53: #negative reinforcement
                            print('risk:2d step fb negative')
                            if events[i + 8][2] == 40 or events[i + 8][2] == 41  or events[i + 8][2] == 46 or events[i + 8][2] == 47:
                                fb_negative_risk.append(events[i + 4])
                                print('events risk fb neg', events[i + 4])

            if  trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                if i + 8 >= len(events):
                    continue
                str_digit1 = str(events[i + 4][2])
                str_digit2 = str(events[i + 5][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2] 
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 4][2] == 40 or events[i + 4][2] == 41  or events[i + 4][2] == 46 or events[i + 4][2] == 47:
                        if trained and events[i + 5][2] == 50 or trained and events[i + 5][2] == 51:
                            print('norisk: 2d step fb positive')  #positive reinforcement
                            if events[i + 8][2] == 40 or events[i + 8][2] == 41  or events[i + 8][2] == 46 or events[i + 8][2] == 47:
                                fb_positive_norisk.append(events[i + 4])
                                print('events norisk fb pos', events[i + 4])

            if  trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                if i + 8 >= len(events):
                    continue
                str_digit1 = str(events[i + 4][2])
                str_digit2 = str(events[i + 5][2])
                d1 = [int(d) for d in str_digit1]
                d2 = [int(d) for d in str_digit2]
                if d1 == 4 and d2 == 4:
                    continue
                else:
                    if events[i + 4][2] == 40 or events[i + 4][2] == 41  or events[i + 4][2] == 46 or events[i + 4][2] == 47:
                        if trained and events[i + 5][2] == 52 or trained and events[i + 5][2] == 53: #negative reinforcement
                            print('norisk: 2d step fb negative')
                            if events[i + 8][2] == 40 or events[i + 8][2] == 41  or events[i + 8][2] == 46 or events[i + 8][2] == 47:
                                fb_negative_norisk.append(events[i + 4])
                                print('events norisk fb neg', events[i + 4]) 
            
            '''
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
                            if events[i + 4][2] == 50 or events[i + 4][2] == 51:
                                prerisk_fb_positive.append(events[i + 3])
                            if events[i + 4][2] == 52 or events[i + 4][2] == 53:
                                prerisk_fb_negative.append(events[i + 3])
                  

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
                            if events[i + 4][2] == 50 or events[i + 4][2] == 51:
                                postrisk_fb_positive.append(events[i + 3])
                            if events[i + 4][2] == 52 or events[i + 4][2] == 53:
                                postrisk_fb_negative.append(events[i + 3])
        '''
        if len(res) != 0:
            answer_count = correct_counter/len(res)
            print(answer_count)
            if answer_count > 0.66:
                events_fb_positive_risk  = open(fpath_events_fb_positive_risk.format(subject, run), "w")
                events_fb_negative_risk  = open(fpath_events_fb_negative_risk.format(subject, run), "w")
                events_fb_positive_norisk = open(fpath_events_fb_positive_norisk.format(subject, run), "w")
                events_fb_negative_norisk = open(fpath_events_fb_negative_norisk.format(subject, run), "w")
                print('evennts fb positive norisk', fb_positive_norisk)
                print('events fb negative norisk', fb_negative_norisk)
                print('events fb positive risk', fb_positive_risk)
                print('events fb negative risk', fb_negative_risk)
                np.savetxt(events_fb_positive_risk, fb_positive_risk, fmt = "%d")
                np.savetxt(events_fb_negative_risk, fb_negative_risk, fmt = "%d")
                np.savetxt(events_fb_positive_norisk, fb_positive_norisk, fmt = "%d")
                np.savetxt(events_fb_negative_norisk, fb_negative_norisk, fmt = "%d")
                events_fb_positive_norisk.close()
                events_fb_negative_norisk.close()
                events_fb_positive_risk.close()
                events_fb_negative_risk.close()

                print('Saved!')
        else:
            print('Did not find trained!')
         
