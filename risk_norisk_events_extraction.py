import mne
import numpy as np
from config import conf

def correct_response(event):
    return event[2] == 40 or event[2] == 41 or event[2] == 46 or event[2] == 47

def incorrect_response(event):
    return event[2] == 42 or event[2] == 43 or event[2] == 44 or event[2] == 45

def risk_norisk_events(conf):
    print('\trun risk_norisk_events...')

    path_events = conf.path_events
    fpath = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
    fpath_events_risk = path_events + '{}_run{}_events_risk.txt'
    fpath_events_norisk = path_events + '{}_run{}_events_norisk.txt'
    fpath_events_prerisk = path_events + '{}_run{}_events_prerisk.txt'
    fpath_events_postrisk = path_events + '{}_run{}_events_postrisk.txt'
    verbose = conf.verbose

    for run in conf.runs:
        for subject in conf.subjects:
            print('\t\t', run, subject)

            raw = mne.io.read_raw_fif(fpath.format(subject, run, subject), allow_maxshield=False, preload=True, verbose='ERROR')

            events = mne.find_events(raw, stim_channel='STI101', output='onset',
                    consecutive='increasing', min_duration=0, shortest_event=1,
                    mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose='ERROR')

            res = []
            risk = []
            norisk = []
            prerisk = []
            postrisk = []
            correct_count = 0
            correct_counter = 0
            trained = False
            answer_count = 0

            for i in range(len(events)):
                if not trained:
                    if correct_response(events[i]):
                        correct_count = correct_count + 1
                    elif incorrect_response(events[i]):
                        correct_count = 0
                else:
                    if correct_response(events[i]):
                        res.append(events[i])
                        correct_counter = correct_counter + 1
                    if incorrect_response(events[i]):
                        res.append(events[i])

                if correct_count > 3 and not trained:
                    trained = True
                    res.append(events[i])

                if trained and correct_response(events[i - 1]):
                    if i + 7 >= len(events):
                        continue
                    str_digit1 = str(events[i + 3][2])
                    str_digit2 = str(events[i + 4][2])
                    d1 = [int(d) for d in str_digit1]
                    d2 = [int(d) for d in str_digit2]
                    if d1 == 4 and d2 == 4:
                        continue
                    else:
                        if incorrect_response(events[i + 3]) and correct_response(events[i + 7]):
                            risk.append(events[i + 3])
              
                        if correct_response(events[i + 3]):
                            if correct_response(events[i + 7]):
                                norisk.append(events[i + 3])
                            if incorrect_response(events[i + 7]):
                                prerisk.append(events[i + 3])

                if trained and incorrect_response(events[i - 1]):
                    if i + 7 >= len(events):
                        continue
                    str_digit1 = str(events[i + 3][2])
                    str_digit2 = str(events[i + 4][2])
                    d1 = [int(d) for d in str_digit1]
                    d2 = [int(d) for d in str_digit2]
                    if d1 == 4 and d2 == 4:
                        continue
                    else:
                        if correct_response(events[i + 3]) and correct_response(events[i + 7]):
                            postrisk.append(events[i + 3])
 
            if len(res) != 0:
                answer_count = correct_counter/len(res)
                if verbose:
                    print(answer_count)
                if answer_count > 0.66:
                    events_norisk  = open(fpath_events_norisk.format(subject, run), "w")
                    events_risk = open(fpath_events_risk.format(subject, run), "w")
                    events_prerisk = open(fpath_events_prerisk.format(subject, run), "w")
                    events_postrisk = open(fpath_events_postrisk.format(subject, run), "w")

                    if verbose:
                        print('events norisk', norisk)
                        print('events risk', risk)
                        print('events prerisk', prerisk)
                        print('events postrisk', postrisk)
                    np.savetxt(events_risk, risk, fmt = "%d")
                    np.savetxt(events_norisk, norisk, fmt = "%d")
                    np.savetxt(events_prerisk, prerisk, fmt = "%d")
                    np.savetxt(events_postrisk, postrisk, fmt = "%d")

                    events_norisk.close()
                    events_risk.close()
                    events_prerisk.close()
                    events_postrisk.close()
                    if verbose:
                        print('Saved!')
            else:
                if verbose:
                    print('Did not find trained!')
    print('\trisk_norisk_events completed')

