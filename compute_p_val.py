import mne
import numpy as np
from scipy import stats, io
import matplotlib.pyplot as plt
import os
import copy
from config import *
import pathlib
from plot_time_course_in_html_functions import p_val_binary

def compute_p_val(subjects, kind, train, frequency, check_num_sens):
    #coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION

    i = 0
    subjects1 = []
    for ind, subj in enumerate(subjects):
        rf1 = out_path + "{0}_feedback_{1}_{2}{3}-ave.fif".format(subj, kind[0], train, frequency)
        file1 = pathlib.Path(rf1)
        rf2 = out_path + "{0}_feedback_{1}_{2}{3}-ave.fif".format(subj, kind[1], train, frequency)
        file2 = pathlib.Path(rf2)
        if file1.exists() and file2.exists():
            print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
            subjects1.append(subj)
            i = i + 1
    print('i: ', i)
    #a container for tapers in neg and pos reinforcement, i - ov
    contr = np.zeros((i, 2, 306, 876))

    i = 0
    for ind, subj in enumerate(subjects1):
        rf = out_path + "{0}_feedback_{1}_{2}{3}-ave.fif".format(subj, kind[0], train, frequency)
        print(rf)
        file = pathlib.Path(rf)
        if file.exists():
            print('exists:', rf)
            print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
            #positive FB
            print('kind[0]', kind[0])
            temp1 = mne.Evoked(out_path + "{0}_feedback_{1}_{2}{3}-ave.fif".format(subj, kind[0], train, frequency))
            temp1 = temp1.pick_types("grad")
            print('data shape', temp1.data.shape)
            #planars
            contr[i, 0, :204, :] = temp1.data
            #combined planars
            contr[i, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
            #negative FB
            print('kind[1]', kind[1])
            temp2 = mne.Evoked( out_path + "{0}_feedback_{1}_{2}{3}-ave.fif".format(subj, kind[1], train, frequency))
            temp2 = temp2.pick_types("grad")
            contr[i, 1, :204, :] = temp2.data
            contr[i, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]
            i = i + 1
    print('CONTR shape', contr.shape)

    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]
    #check the number of stat significant sensors in a predefined time interval
    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)
    save_t_stat = True
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
