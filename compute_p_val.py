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

def compute_p_val(subjects, kind, train, frequency, check_num_sens):
    #coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
    tfr_path = data_path
    subject_counter = 0 
    folder = 'GA/'
    i = 0
    subjects1 = []
    for ind, subj in enumerate(subjects):
        if grand_average == False:
            rf1 = out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
        else:
            assert(grand_average == True)
            rf1 = out_path + folder + "{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
        print(rf1)
        file1 = pathlib.Path(rf1)
        if grand_average == False:
            rf2 = out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[1], frequency, train)
        else:
            assert(grand_average == True)
            rf2 = out_path + folder + "{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subj, spec, stimulus, kind[1], frequency, train)
        file2 = pathlib.Path(rf2)
        if file1.exists() and file2.exists():
            print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
            subjects1.append(subj)
            i = i + 1
    print('i: ', i)
    subject_counter = i
    #a container for tapers in neg and pos reinforcement
    contr = np.zeros((i, 2, 306, int(time.shape[0])))

    print('time.shape[0]', time.shape[0])
    if random_comp:
       #not for grand_average
       length = len(subjects1)
       random_class_one = np.zeros(length)
       random_class_two = np.zeros(length)
       for l in range(length):
           random_class_one[l] = np.around(random.uniform(0, 1))
           random_class_two[l] = np.around(random.uniform(0, 1))
    i = 0
    if random_comp:
        rsubjects1 = random.sample(subjects1, k = len(subjects1))
        subjects1 = rsubjects1
        #print('rsubjects1', rsubjects1)
    for ind, subj in enumerate(subjects1):
        if grand_average == False:
            rf = out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
        else:
            assert(grand_average == True)
            rf = out_path + folder + "{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
        print(rf)
        file = pathlib.Path(rf)
        if file.exists():
            print('exists:', rf)
            print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
            #first 'condition'
            print('kind[0]', kind[0])
            if grand_average == False:
                temp1 = mne.Evoked(out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train))
                temp1 = temp1.pick_types("grad")
                print('data shape', temp1.data.shape)
            else:
                assert(grand_average == True)
                temp1 = mne.Evoked(out_path + folder + "{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subj, spec, stimulus, kind[0], frequency, train))
            #planars
            if random_comp:
                #check that tje classes based on the 'conditions' are real
                contr[i, int(random_class_one[i]), :204, :] = temp1.data
                contr[i, int(random_class_one[i]), 204:, :] = temp1.data[::2] + temp1.data[1::2]
            else:
                contr[i, 0, :204, :] = temp1.data
                #combined plana:us
                if grand_average == False:
                    contr[i, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
                else:
                    assert(grand_average == True)
                    #combined planars for grand average
                    contr[i, 0, 204:, :] = np.power(np.power(temp1.data[::2], 2) + np.power(temp1.data[1::2],2),0.5)
                    #remove trend
                    KIND = kind[0] 
                    #compute baseline to remove trend
                    SUBJ_BASE1 = baseline_GA(subj, subjects1, KIND)
                    SUBJ_BASE_comb1 = np.power(np.power(SUBJ_BASE1[::2], 2) + np.power(SUBJ_BASE1[1::2],2),0.5)
                    contr[i, 0, 204:, :]  = contr[i, 0, 204:, :] - SUBJ_BASE_comb1
            #second 'condition'
            print('kind[1]', kind[1])
            if grand_average == False:
                    temp2 = mne.Evoked( out_path + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[1], frequency, train))
                    temp2 = temp2.pick_types("grad")
                    print('data 2 shape', temp2.data.shape)
            else:
                assert(grand_average == True)
                temp2 = mne.Evoked( out_path + folder + "{0}_{1}{2}{3}_{4}{5}-grand_ave.fif".format(subj, spec, stimulus, kind[1], frequency, train))
            if random_comp:
                #not for ERP todo for stat_over_runs
                contr[i, int(random_class_two[i]), :204, :] = temp2.data
                contr[i, int(random_class_two[i]), 204:, :] = temp2.data[::2] + temp1.data[1::2]
            else:
                if grand_average == False:
                    contr[i, 1, :204, :] = temp2.data
                    contr[i, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]
                else:
                    assert(grand_average == True)
                    #combined planars for grand average
                    contr[i, 1, 204:, :] = np.power(np.power(temp2.data[::2], 2) + np.power(temp2.data[1::2],2),0.5)
                    #remove trend
                    KIND = kind[1]
                    #compute baseline to remove trend
                    SUBJ_BASE2 = baseline_GA(subj, subjects1, KIND)
                    SUBJ_BASE_comb2 = np.power(np.power(SUBJ_BASE2[::2], 2) + np.power(SUBJ_BASE2[1::2],2),0.5)
                    contr[i, 1, 204:, :] = contr[i, 1, 204:, :] - SUBJ_BASE_comb2
            i = i + 1
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
