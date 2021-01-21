import mne
import numpy as np
from scipy import stats, io, signal
import matplotlib.pyplot as plt
import os
import copy
from config import *
import pathlib
from plot_time_course_in_html_functions import p_val_binary
import random
from numpy import random
from baseline_GA import baseline_GA

def compute_p_val_over_runs(subjects, kind, train, frequency, check_num_sens):
    #coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
    subject_counter = 0
    tfr_path = data_path
    folder = 'GA/'
    i = 0
    runs1 = []
    subjects1 = []
    for subj in subjects:
        print('subj', subj)
        for run in runs:
            print('run', run)
            rf1 = tfr_path.format(prefix, kind[0], subj, run, spec, frequency, stimulus, kind[0], train)
            rf2 = tfr_path.format(prefix, kind[1], subj, run, spec, frequency, stimulus, kind[1], train)
            print('rf1', rf1)
            print('rf2', rf2)
            file1 = pathlib.Path(rf1)
            file2 = pathlib.Path(rf2)
            if file1.exists() and file2.exists():
                print('the files exist!')
                runs1.append(run)
                subjects1.append(subj)
                i = i + 1
    print('i: ', i)
    #a container for tapers in neg and pos reinforcement
    contr = np.zeros((i + 1, 2, 306, int(time.shape[0])))

    print('time.shape[0]', time.shape[0])
    print('subjects', subjects)
    for ind, subj in enumerate(subjects):
        for run in runs:
            rf1 = tfr_path.format(prefix, kind[0], subj, run, spec, frequency, stimulus, kind[0], train)
            rf2 = tfr_path.format(prefix, kind[1], subj, run, spec, frequency, stimulus, kind[1], train)
            print(rf1)
            print(rf2)
            file1 = pathlib.Path(rf1)
            file2 = pathlib.Path(rf2)
            if file1.exists() and file2.exists():
                  print('exists:', rf1)
                  print('also exists:', rf2)
                  #first 'condition'
                  print('kind[0]', kind[0])
                  print('stat_over_runs', stat_over_runs)
                  temp1 = mne.time_frequency.read_tfrs(rf1)[0]
                  #remove dim = 2
                  temp1.data = np.mean(temp1.data, axis = 1)
                  print('data shape', temp1.data.shape)
                  #planars
                  contr[i, 0, :204, :] = temp1.data
                  #combined planars
                  contr[i, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
                  print('contr', contr[i, 0, 204:, :])
                  #second 'condition'
                  print('kind[1]', kind[1])
                  temp2 = mne.time_frequency.read_tfrs(rf2)[0]
                  temp2.data = np.mean(temp2.data, axis = 1)
                  print('data 2 shape', temp2.data.shape)
                  contr[i, 1, :204, :] = temp2.data
                  contr[i, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]
                  print('contr', contr[i, 1, 204:, :])
                #i = i + 1
    print('CONTR shape', contr.shape)
    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]

    #check the number of stat significant sensors in a predefined time interval
    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)
    #save_t_stat = True
    if save_t_stat:
        t_stat_str = np.array2string(t_stat)
        print(type(t_stat_str))
        t_stat_file = f'{prefix}t_stat_{kind[0]}_vs_{kind[1]}.txt'
        t_stat_file_name = open(t_stat_file, "w")
        t_stat_file_name.write(t_stat_str)
        t_stat_file_name.close()

    binary = p_val_binary(p_val, treshold = 0.05)

    if check_num_sens:
        issue = binary[204:, 600]
        counter = 0
        for i in range(102):
            if issue[i] == 1:
                print('ch idx', i)
                counter = counter + 1
                print('counter', counter)
    #average the freq data over subjects
    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    print('COMP1.mean.shape', comp1_mean.shape)
    print('COMP2.mean.shape', comp2_mean.shape)
    return comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary, subjects1
