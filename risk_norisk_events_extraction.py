import mne
import numpy as np
from config import conf, correct_response, incorrect_response, response

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

def save_events(norisk, risk, prerisk, postrisk, stimulus_risk, stimulus_norisk, conf, subject, run):
    verbose = conf.verbose 
    path_events = conf.path_events
    train = conf.train
    fpath_events_risk = path_events + '{}_run{}_events_risk{}.txt'
    fpath_events_norisk = path_events + '{}_run{}_events_norisk{}.txt'
    fpath_events_prerisk = path_events + '{}_run{}_events_prerisk{}.txt'
    fpath_events_postrisk = path_events + '{}_run{}_events_postrisk{}.txt'
    fpath_events_stimulus_risk = path_events + '{}_run{}_events_stimulus_risk{}.txt'
    fpath_events_stimulus_norisk = path_events + '{}_run{}_events_stimulus_norisk{}.txt'
    events_norisk  = open(fpath_events_norisk.format(subject, run, train), "w")
    events_risk = open(fpath_events_risk.format(subject, run, train), "w")
    events_prerisk = open(fpath_events_prerisk.format(subject, run, train), "w")
    events_postrisk = open(fpath_events_postrisk.format(subject, run, train), "w")
    events_stimulus_risk = open(fpath_events_stimulus_risk.format(subject, run, train), "w")
    events_stimulus_norisk = open(fpath_events_stimulus_norisk.format(subject, run, train), "w")
    if verbose:
        print('events norisk', norisk)
        print('events risk', risk)
        print('events prerisk', prerisk)
        print('events postrisk', postrisk)
        print('events stimulus risk', stimulus_risk)
        print('events stimulus norisk', stimulus_norisk)
    np.savetxt(events_risk, risk, fmt = "%d")
    np.savetxt(events_norisk, norisk, fmt = "%d")
    np.savetxt(events_prerisk, prerisk, fmt = "%d")
    np.savetxt(events_postrisk, postrisk, fmt = "%d")
    np.savetxt(events_stimulus_risk, stimulus_risk, fmt = "%d")
    np.savetxt(events_stimulus_norisk, stimulus_norisk, fmt = "%d")
    events_norisk.close()
    events_risk.close()
    events_prerisk.close()
    events_postrisk.close()
    events_stimulus_risk.close()
    events_stimulus_norisk.close()
    if verbose:
        print('Saved!')

def risk_norisk_events(conf):
    verbose = conf.verbose
    print('\trun risk_norisk_events...')

    for run in conf.runs:
        for subject in conf.subjects:
            print('\t\t', run, subject)

            raw = mne.io.read_raw_fif(conf.fpath_raw.format(subject, run, subject), allow_maxshield=False, preload=True, verbose='ERROR')

            events = mne.find_events(raw, stim_channel='STI101', output='onset',
                    consecutive='increasing', min_duration=0, shortest_event=1,
                    mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose='ERROR')

            # consider events starting from 4-th correct response in a row (=trained)
            begin = detect_trained(events)
            end = len(events)

            # countera for correct responses and the proportion of correct responses in a block (should be no less than 2/3 for trained)
            correct_counter = sum([1 for i in range(begin, end) if correct_response(events[i])])
            answer_counter = sum([1 for i in range(begin, end) if correct_response(events[i]) or incorrect_response(events[i])])
            if answer_counter == 0 or correct_counter/answer_counter <= 0.66:
                if verbose:
                    if answer_count != 0:
                        print(answer_counter, correct_counter/answer_counter)
                    print('Did not find trained!')
                continue

            risk = []
            norisk = []
            prerisk = []
            postrisk = []
            stimulus_risk = []
            stimulus_norisk = []
            for i in range(begin, end-8):

                if response(events[i + 4]) and response(events[i + 5]):
                    continue

                if correct_response(events[i]) and correct_response(events[i + 8]):
                    if incorrect_response(events[i + 4]):
                        risk.append(events[i + 4])
                        if events[i + 3][2] == 11:
                            stimulus_risk.append(events[i + 3])
                    if correct_response(events[i + 4]):
                        norisk.append(events[i + 4])
                        if events[i + 3][2] == 11:
                            stimulus_norisk.append(events[i + 3])

                if correct_response(events[i + 4]):
                    if correct_response(events[i]) and incorrect_response(events[i + 8]):
                        prerisk.append(events[i + 4])
                    if incorrect_response(events[i]) and correct_response(events[i + 8]):
                        postrisk.append(events[i + 4])
 
            save_events(norisk, risk, prerisk, postrisk, stimulus_risk, stimulus_norisk, conf, subject, run)
    print('\trisk_norisk_events completed')

