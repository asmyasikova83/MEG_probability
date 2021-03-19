import mne
import numpy as np
import sys
from scipy import stats, io, signal
import matplotlib.pyplot as plt
import os
import copy
from config import conf
import pathlib
from plot_time_course_in_html_functions import p_val_binary
import random
from numpy import random
#from baseline_GA import baseline_GA

def compute_p_val(conf, subjects, kind, train, frequency, check_num_sens):
    #coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
    grand_average = conf.grand_average
    subjects = conf.subjects
    stimulus = conf.stimulus
    random_comp = conf.random_comp
    spec = conf.spec
    verbose = conf.verbose

    subject_counter = 0 
    i = 0
    subjects1 = []
    for ind, subj in enumerate(subjects):
        print('\t\t', subj)
        if grand_average == False:
            rf1 = conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
        else:
            rf1 = conf.path_GA + "{0}_{1}{2}{3}_{4}_grand_ave.fif".format(subj, spec, stimulus, kind[0], train)
        if verbose:
            print(rf1)
        file1 = pathlib.Path(rf1)
        if grand_average == False:
            rf2 = conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[1], frequency, train)
        else:
            assert(grand_average == True)
            rf2 = conf.path_GA + "{0}_{1}{2}{3}_{4}_grand_ave.fif".format(subj, spec, stimulus, kind[1], train)
        file2 = pathlib.Path(rf2)
        if file1.exists() and file2.exists():
            if verbose:
                print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
            subjects1.append(subj)
            i = i + 1
    if verbose:
        print('i: ', i)
    subject_counter = i
    #a container for tapers in neg and pos reinforcement
    time = conf.time
    contr = np.zeros((i, 2, 306, int(time.shape[0])))
    if verbose:
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
            rf = conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train)
        else:
            rf = conf.path_GA + "{0}_{1}{2}{3}_{4}_grand_ave.fif".format(subj, spec, stimulus, kind[0], train)
        if verbose:
            print(rf)
        file = pathlib.Path(rf)
        if file.exists():
            if verbose:
                print('exists:', rf)
                print('This subject is being processed: ', subj, ' (', i, ') ( ', ind, ' ) ')
                #first 'condition'
                print('kind[0]', kind[0])
            if grand_average == False:
                temp1 = mne.Evoked(conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[0], frequency, train),
                        verbose = 'ERROR')
                temp1 = temp1.pick_types("grad")
                if verbose:
                    print('data shape', temp1.data.shape)
            else:
                temp1 = mne.Evoked(conf.path_GA + "{0}_{1}{2}{3}_{4}_grand_ave.fif".format(subj, spec, stimulus, kind[0], train), verbose = 'ERROR')

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
                    NEW_BASELINE1 = np.mean(contr[i, 0, 204:, 125:250], axis = 1)
                    NEW_BASELINE1 = NEW_BASELINE1[:, np.newaxis]
                    NEW_BASELINE1 = np.tile(NEW_BASELINE1, time.shape[0])
                    contr[i, 0, 204:, :] = contr[i, 0, 204:, :] - NEW_BASELINE1
                else:
                    assert(grand_average == True)
                    #combined planars for grand average
                    contr[i, 0, 204:, :] = np.power(np.power(temp1.data[::2], 2) + np.power(temp1.data[1::2],2),0.5)
                    #remove trend using baseline
                    KIND = kind[0]
                    NEW_BASELINE1 = np.mean(contr[i, 0, 204:, 125:250], axis = 1)
                    NEW_BASELINE1 = NEW_BASELINE1[:, np.newaxis]
                    NEW_BASELINE1 = np.tile(NEW_BASELINE1, time.shape[0])
                    #compute baseline to remove trend
                    contr[i, 0, 204:, :] = contr[i, 0, 204:, :] - NEW_BASELINE1
            #second 'condition'
            if verbose:
                print('kind[1]', kind[1])
            if grand_average == False:
                temp2 = mne.Evoked(conf.path_container + "{0}_{1}{2}{3}_{4}{5}-ave.fif".format(subj, spec, stimulus, kind[1], frequency, train),
                        verbose = 'ERROR')
                temp2 = temp2.pick_types("grad")
                if verbose:
                    print('data 2 shape', temp2.data.shape)
            else:
                temp2 = mne.Evoked(conf.path_GA + "{0}_{1}{2}{3}_{4}_grand_ave.fif".format(subj, spec, stimulus, kind[1], train), verbose = 'ERROR')
            if random_comp:
                #not for ERP todo for stat_over_runs
                contr[i, int(random_class_two[i]), :204, :] = temp2.data
                contr[i, int(random_class_two[i]), 204:, :] = temp2.data[::2] + temp1.data[1::2]
            else:
                if grand_average == False:
                    contr[i, 1, :204, :] = temp2.data
                    contr[i, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]
                    NEW_BASELINE2= np.mean(contr[i, 1, 204:, 125:250], axis = 1)
                    NEW_BASELINE2 = NEW_BASELINE2[:, np.newaxis]
                    NEW_BASELINE2 = np.tile(NEW_BASELINE2, time.shape[0])
                    contr[i, 1, 204:, :] = contr[i, 1, 204:, :] - NEW_BASELINE2
                else:
                    assert(grand_average == True)
                    #combined planars for grand average
                    contr[i, 1, 204:, :] = np.power(np.power(temp2.data[::2], 2) + np.power(temp2.data[1::2],2),0.5)
                    #remove trend using baseline
                    KIND = kind[1]
                    NEW_BASELINE2= np.mean(contr[i, 1, 204:, 125:250], axis = 1)
                    NEW_BASELINE2 = NEW_BASELINE2[:, np.newaxis]
                    NEW_BASELINE2 = np.tile(NEW_BASELINE2, time.shape[0])
                    contr[i, 1, 204:, :] = contr[i, 1, 204:, :] - NEW_BASELINE2
            i = i + 1
    if verbose:
        print('CONTR shape', contr.shape)
    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]

    #check the number of stat significant sensors in a predefined time interval
    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)
    save_t_stat = True
    if save_t_stat:
        np.set_printoptions(threshold=sys.maxsize)
        t_stat_str = np.array2string(t_stat)
        if verbose:
            print(type(t_stat_str))
        t_stat_file = f'{conf.path_tfce}t_stat_{kind[0]}_vs_{kind[1]}.txt'
        t_stat_file_name = open(t_stat_file, "w")
        t_stat_file_name.write(t_stat_str)
        t_stat_file_name.close()

    binary = p_val_binary(p_val, treshold = 0.05)

    if check_num_sens:
        issue = binary[204:, 600]
        counter = 0
        for i in range(102):
            if issue[i] == 1:
                if verbose:
                    print('ch idx', i)
                counter = counter + 1
                if verbose:
                    print('counter', counter)
    #average the freq data over subjects
    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    if verbose:
        print('COMP1.mean.shape', comp1_mean.shape)
        print('COMP2.mean.shape', comp2_mean.shape)
    return comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary, subjects1
