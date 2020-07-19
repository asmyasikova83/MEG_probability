import mne
import numpy as np

subjects = [ 
    'P000',
    'P001',
    'P002',
    'P003',
    'P004',
    'P005',
    'P006',
    'P007',
    'P008',
    'P009',
    'P010',
    'P011',
    'P012',
    'P014',
    'P015',
    'P016',
    'P017',
    'P018',
    'P019',
    'P020',
    'P021',
    'P022',
    'P023',
    'P024',
    'P025',
    'P026',
    'P028',
    'P029',
    'P030']

runs = ['1','2','3','4','5','6','7']

fpath = '/home/asmyasnikova83/DATA/links/{}/{}_run{}_raw_tsss_mc.fif'
fpath_events = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_events.txt'
fpath_log = '/home/asmyasnikova83/DATA/reinforced/{}_run{}_log.txt'

events_trained = []
log_trained_events = []
reinforcement_trained = []
log_reinf_trained = []

for run in runs:
    for subject in subjects:
        print(fpath.format(subject, subject, run))

        raw = mne.io.read_raw_fif(fpath.format(subject, subject, run), allow_maxshield=False, preload=True, verbose=None)

        events = mne.find_events(raw, stim_channel='STI101', output='onset', consecutive='increasing', min_duration=0, shortest_event=1, mask=None, uint_cast=False, mask_type='and',  initial_event=False, verbose=None)

        res = []
        log = []
        reinforcement = []
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
                    reinforcement.append(events[i])
                    log_reinf.append('positive reinforcement')

                if trained and events[i][2] == [52] or trained and events[i][2] == [53]: #negative reinforcement
                    reinforcement.append(events[i])
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
                reinforcement.append(events[i])
                log_reinf.append('positive reinforcement')

            if trained and events[i][2] == [52] or trained and events[i][2] == [53]: #negative reinforcement
                reinforcement.append(events[i])
                log_reinf.append('negative reinforcement')           
         
        if len(res) != 0:
            answer_count = correct_counter/len(res)
            print(answer_count)
            if answer_count > 0.66:
                events_file = open(fpath_events.format(subject, run), "w")
                log_file = open(fpath_log.format(subject, run), "w")

                np.savetxt(events_file, reinforcement, fmt="%d")
                log_reinf_str='\n'.join(log_reinf)
                log_file.write(log_reinf_str)

                log_file.close()
                events_file.close()
                print('Saved!')
        else:
            print('Did not find trained')

