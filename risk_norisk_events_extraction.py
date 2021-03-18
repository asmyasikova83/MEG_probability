import mne
import numpy as np
from config import conf

def correct_response(event):
    return event[2] == 40 or event[2] == 41 or event[2] == 46 or event[2] == 47

def incorrect_response(event):
    return event[2] == 42 or event[2] == 43 or event[2] == 44 or event[2] == 45

def detect_trained(events):
    end = len(events)
    correct_counter = 0
    for i in range(end):
         if correct_response(events[i]):
             correct_counter += 1
             if correct_counter > 3:
                 return i
         elif incorrect_response(events[i]):
             correct_counter = 0
    return end

def save_events(norisk, risk, prerisk, postrisk, conf, subject, run):
    verbose = conf.verbose 
    path_events = conf.path_events
    fpath_events_risk = path_events + '{}_run{}_events_risk.txt'
    fpath_events_norisk = path_events + '{}_run{}_events_norisk.txt'
    fpath_events_prerisk = path_events + '{}_run{}_events_prerisk.txt'
    fpath_events_postrisk = path_events + '{}_run{}_events_postrisk.txt'
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

def risk_norisk_events(conf):
    verbose = conf.verbose
    print('\trun risk_norisk_events...')

    fpath = '/net/server/data/Archive/prob_learn/vtretyakova/ICA_cleaned/{}/run{}_{}_raw_ica.fif'
    for run in conf.runs:
        for subject in conf.subjects:
            print('\t\t', run, subject)

            raw = mne.io.read_raw_fif(fpath.format(subject, run, subject), allow_maxshield=False, preload=True, verbose='ERROR')

            events = mne.find_events(raw, stim_channel='STI101', output='onset',
                    consecutive='increasing', min_duration=0, shortest_event=1,
                    mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose='ERROR')

            # consider events starting from 4-th correct response in a row (=trained)
            begin = detect_trained(events)
            end = len(events)

            # countera for correct responses and the proportion of correct responses in a block (should be no less than 2/3 for trained)
            correct_counter = sum([1 for i in range(begin+1, end) if correct_response(events[i])]) #FIXME begin+1
            answer_counter = sum([1 for i in range(begin, end) if correct_response(events[i]) or incorrect_response(events[i])])
            if answer_counter == 0 or correct_counter/answer_counter <= 0.66:
                if verbose:
                    print(answer_counter, correct_counter/answer_counter)
                    print('Did not find trained!')
                continue

            res = []
            risk = []
            norisk = []
            prerisk = []
            postrisk = []
            # FIXME begin-1
            for i in range(begin-1, end-8):

                # check double responses starting from '4'
                if str(events[i + 4][2])[0] == '4' and str(events[i + 5][2])[0] == '4':
                    continue

                # TODO
                if correct_response(events[i]) and correct_response(events[i + 8]):
                    if incorrect_response(events[i + 4]):
                        risk.append(events[i + 4])
                    if correct_response(events[i + 4]):
                        norisk.append(events[i + 4])

                if correct_response(events[i + 4]):
                    if correct_response(events[i]) and incorrect_response(events[i + 8]):
                        prerisk.append(events[i + 4])
                    if incorrect_response(events[i]) and correct_response(events[i + 8]):
                        postrisk.append(events[i + 4])
 
            save_events(norisk, risk, prerisk, postrisk, conf, subject, run)
    print('\trisk_norisk_events completed')

