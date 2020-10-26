import mne
import numpy as np
from config import *
                                                                                                                                                                                                                   
fpath = '/net/server/data/Archive/prob_learn/experiment/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
fpath_events_risk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_risk.txt'
fpath_events_norisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_norisk.txt'
fpath_events_prerisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_prerisk.txt'
fpath_events_postrisk = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events_postrisk.txt'
fpath_log = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_log_risk_norisk.txt'

risk_trained = []
norisk_trained = []
prerisk_trained = []
postrisk_trained = []

for run in runs:
    for subject in subjects:
        print(fpath.format(subject, run, subject))                                                                                                                                                                 
        raw = mne.io.read_raw_fif(fpath.format(subject, run, subject), allow_maxshield=False, preload=True, verbose=None)

        events = mne.find_events(raw, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose=None)

        res = []
        log = []
        risk = []
        norisk = []
        prerisk = []
        postrisk = []
        log_risk_norisk = []
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
                
                if trained and events[i-1][2] == 40 or trained and events[i-1][2] == 41 or trained and events[i-1][2] == 46 or trained and events[i-1][2] == 47:
                    if trained and events[i][2] == 42 or trained and events[i][2] == 43 or trained and events[i][2] == 44 or trained and events[i][2] == 45:
                        print('risk')
                        if trained and events[i+1][2] == 40 or trained and events[i+1][2] == 41 or trained and events[i+1][2] == 46 or trained and events[i+1][2] == 47:
                            risk.append(events[i])
                            log_risk_norisk.append('risk')
          
                if trained and events[i-1][2] == 40 or trained and events[i-1][2] == 41 or trained and events[i-1][2] == 46 or trained and events[i-1][2] == 47:
                    if trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                        print('norisk')
                        if trained and events[i+1][2] == 40 or trained and events[i+1][2] == 41 or trained and events[i+1][2] == 46 or trained and events[i+1][2] == 47:
                            norisk.append(events[i])
                            log_risk_norisk.append('norisk')

                if trained and events[i-1][2] == 40 or trained and events[i-1][2] == 41 or trained and events[i-1][2] == 46 or trained and events[i-1][2] == 47:
                    if trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                        if trained and events[i+1][2] == 42 or trained and events[i+1][2] == 43 or trained and events[i+1][2] == 44 or trained and events[i+1][2] == 45:
                            print('prerisk')
                            prerisk.append(events[i])
                            log_risk_norisk.append('prerisk')

                if trained and events[i-1][2] == 42 or trained and events[i-1][2] == 43 or trained and events[i-1][2] == 44 or trained and events[i-1][2] == 45:
                    if trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                        if trained and events[i+1][2] == 40 or trained and events[i+1][2] == 41 or trained and events[i+1][2] == 46 or trained and events[i+1][2] == 47:
                            print('postrisk')
                            postrisk.append(events[i])
                            log_risk_norisk.append('postrisk')
                
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
           
                if trained and events[i-1][2] == 40 or trained and events[i-1][2] == 41 or trained and events[i-1][2] == 46 or trained and events[i-1][2] == 47:
                    if trained and events[i][2] == 42 or trained and events[i][2] == 43 or trained and events[i][2] == 44 or trained and events[i][2] == 45:
                        print('risk')
                        if trained and events[i+1][2] == 40 or trained and events[i+1][2] == 41 or trained and events[i+1][2] == 46 or trained and events[i+1][2] == 47:
                            risk.append(events[i])
                            log_risk_norisk.append('risk') 
              
                if trained and events[i-1][2] == 40 or trained and events[i-1][2] == 41 or trained and events[i-1][2] == 46 or trained and events[i-1][2] == 47:
                    if trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                        print('norisk')
                        if trained and events[i+1][2] == 40 or trained and events[i+1][2] == 41 or trained and events[i+1][2] == 46 or trained and events[i+1][2] == 47:
                            norisk.append(events[i])
                            log_risk_norisk.append('norisk')

                if trained and events[i-1][2] == 40 or trained and events[i-1][2] == 41 or trained and events[i-1][2] == 46 or trained and events[i-1][2] == 47:
                    if trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                        if trained and events[i+1][2] == 42 or trained and events[i+1][2] == 43 or trained and events[i+1][2] == 44 or trained and events[i+1][2] == 45:
                            print('prerisk')
                            prerisk.append(events[i])
                            log_risk_norisk.append('prerisk')

                if trained and events[i-1][2] == 42 or trained and events[i-1][2] == 43 or trained and events[i-1][2] == 44 or trained and events[i-1][2] == 45:
                    if trained and events[i][2] == 40 or trained and events[i][2] == 41 or trained and events[i][2] == 46 or trained and events[i][2] == 47:
                        if trained and events[i+1][2] == 40 or trained and events[i+1][2] == 41 or trained and events[i+1][2] == 46 or trained and events[i+1][2] == 47:
                            print('postrisk')
                            postrisk.append(events[i])
                            log_risk_norisk.append('postrisk')
 
        if len(res) != 0:
            answer_count = correct_counter/len(res)
            print(answer_count)
            if answer_count > 0.66:
                norisk_trained.extend(norisk)
                risk_trained.extend(risk)
                prerisk_trained.extend(prerisk)
                postrisk_trained.extend(postrisk)
                events_norisk  = open(fpath_events_norisk.format(subject, run), "w")
                events_risk = open(fpath_events_risk.format(subject, run), "w")
                events_prerisk = open(fpath_events_prerisk.format(subject, run), "w")
                events_postrisk = open(fpath_events_postrisk.format(subject, run), "w")
                log_file = open(fpath_log.format(subject, run), "w")
  
                np.savetxt(events_norisk, norisk_trained, fmt = "%d")
                np.savetxt(events_risk, risk_trained, fmt = "%d")
                np.savetxt(events_prerisk, prerisk_trained, fmt = "%d")
                np.savetxt(events_postrisk, postrisk_trained, fmt = "%d")
                log_risk_norisk_str='\n'.join(log_risk_norisk)
                log_file.write(log_risk_norisk_str)

                log_file.close()
                events_norisk.close()
                events_risk.close()
                events_prerisk.close()
                events_postrisk.close()
                print('Saved!')
        else:
            print('Did not find trained!')
         
