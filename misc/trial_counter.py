import numpy as np
from config import *
from os.path import exists
import pandas as pd

path = '/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/events_by_cond_mio_corrected/'

collect_trials_by_subj_cond = False
collect_trials_by_cond = True

rounds = [1, 2, 3, 4, 5, 6]
#trial_type = ['norisk', 'prerisk', 'risk', 'postrisk']
trial_type = ['norisk', 'postrisk', 'prerisk', 'risk']

feedback = ['positive', 'negative']

df_all = pd.DataFrame()
for cond in trial_type:
    subj_in_cond = []
    for idx, subj in enumerate(subjects):
        counter = 0
        for r in rounds:
            for fb in feedback:
                path_f = path + f'{subj}_run{r}_{cond}_fb_cur_{fb}.txt'
                if  exists(path_f):
                    events = np.loadtxt(path + f'{subj}_run{r}_{cond}_fb_cur_{fb}.txt', dtype = int)
                    if events.shape == (3,):
                        events = events.reshape(1,3)
                    num_ev = len(events)
                    counter = counter + num_ev
                else:
                    pass
        subj_in_cond.append(counter)
        if collect_trials_by_subj_cond:
            data = {'Subject':[subj], 'Cond':[cond], 'Trials':[subj_in_cond[idx]]}
            df = pd.DataFrame(data)
            df_all = df_all.append(df)
    if collect_trials_by_cond:
        data = {'N subjects':[len(subj_in_cond)], 'Cond':[cond], 'Mean':[np.mean(subj_in_cond)], 'SD':[np.std(subj_in_cond)] }
        df = pd.DataFrame(data)
        df_all = df_all.append(df)
print(df_all)
#df_all.to_csv('/net/server/data/Archive/prob_learn/asmyasnikova83/df_trials.csv')
