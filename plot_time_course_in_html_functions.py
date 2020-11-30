import numpy as np
import matplotlib.pyplot as plt
import copy
from config import *
import pathlib
import statsmodels.stats.multitest as mul

# functions for visualization

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')

def contr_num(filename):
    for ind, c in enumerate(contrast):
        if c in filename:
            return ind+1
    return None

def to_str_ar(ch_l):
    temp = []
    for i in ch_l:
        temp.append(i[0][0])
    return temp

def get_short_legend(contrast):
    temp = contrast.split('_')
    return (temp[0], temp[2], temp[3], temp[4])

def get_full_legend(contrast):
    temp = contrast.split('_')
    return (diction[temp[0]], diction[temp[2]], diction[temp[3]], temp[4])

def delaete_bad_sub(contrast, del_list):
    for sub in del_list:
        if sub in contrast[1]:
            ind = contrast[1].index(sub)
            contrast[1].pop(ind)
            contrast[0] = np.delete(contrast[0], ind, axis=0)
    return contrast


def add_pic_time_course_html(filename, pic, pic_folder, pos_n, size):
    x = size[0]
    y = size[1]
    add_str_html(filename, '<IMG STYLE="position:absolute; TOP: %spx; LEFT: %spx; WIDTH: %spx; HEIGHT: %spx" SRC=" %s" />'%(round(y*(1-pos_n[1])*15,3), round(pos_n[0]*x*15,3), x, y, pic_folder+'/'+pic))

def add_pic_topo_html(filename, pic):
    add_str_html(filename, '<IMG SRC="%s" style="width:%spx;height:%spx;"/>'%(pic,1900,162))

def space_fdr(p_val_n):
    temp = copy.deepcopy(p_val_n)
    for i in range(temp.shape[1]):
        _, temp[:, i] = mul.fdrcorrection(p_val_n[:, i])
    return temp



def plot_stat_comparison_tfce(comp1, comp2, comp1_stderr, comp2_stderr, p_val, res_tfce, time, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2', comp1_color = 'k', comp2_color = 'k'):

    assert(len(comp1) == len(comp2) == len(time))
    res = False
    plt.figure()
    plt.rcParams['axes.facecolor'] = 'none'
    plt.xlim(time[0], time[-1])
    plt.ylim(-p_mul, p_mul)
    plt.plot([0, 0.001], [-3, 3], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([-4, 4], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([2.6, 2.601], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label)
    plt.fill_between(time, comp1-comp1_stderr, comp1+comp1_stderr, alpha=.2, facecolor = comp1_color)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label)
    plt.fill_between(time, comp2-comp2_stderr, comp2+comp2_stderr, alpha=.2, facecolor = comp2_color)

    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = (res_tfce == 1), facecolor = 'crimson', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = ((p_val < 0.05)*(res_tfce==0)), facecolor = 'c', alpha = 0.46, step = 'pre')
    # check statistically significant sensors in a predefined time interval. Here it is [1.0 1.4]
    if sign_sensors:
        for i in range(len(time)):                                                                                                                                                                                            # if 0.195 < time[i] and time[i] < 0.205 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.50 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.60 and p_val[i] < 0.05:
             if np.around(time[i], decimals = 2) == 0.20 and p_val[i] < 0.05 or (np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05) or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05:
                plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'g', alpha = 0.46, step = 'pre')
                res = True
    #arr_ind = np.zeros(102)
    plt.tick_params(labelsize = 14)
    plt.legend(loc='upper right', fontsize = 14)
    plt.title(title, fontsize = 36)
    output = 'output_tfce/'
    path = output + folder + '/'
    os.makedirs(path, exist_ok = True)
    plt.savefig(path+title + '.svg', transparent=True)
    plt.close()
    return res

def plot_stat_comparison(comp1, comp2, p_val, p_mul, time, title='demo_title', folder='comparison',
                         comp1_label='comp1', comp2_label='comp2'):
    assert(len(comp1) == len(comp2) == len(time))
    res = False
    plt.figure()
    plt.rcParams['axes.facecolor'] = 'none'
    plt.xlim(time[0], time[-1])
    plt.ylim(-p_mul, p_mul)
    plt.plot([0, 0.001], [-3, 3], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([-4, 4], [0, 0.001], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot([2.6, 2.601], [-5, 5], color='k', linewidth=3, linestyle='--', zorder=1)
    plt.plot(time, comp1, color='b', linewidth=3, label=comp1_label)
    plt.plot(time, comp2, color='r', linewidth=3, label=comp2_label)
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = (p_val < 0.01), facecolor = 'm', alpha = 0.46, step = 'pre')
    plt.fill_between(time, y1 = p_mul, y2 = -p_mul, where = ((p_val >= 0.01) * (p_val < 0.05)), facecolor = 'g', alpha = 0.46, step = 'pre')
    # check statistically significant sensors in a predefined time interval. Here it is [1.0 1.4]
    if sign_sensors:
        for i in range(len(time)): 
           # if 0.195 < time[i] and time[i] < 0.205 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.50 and p_val[i] < 0.05 or np.around(time[i], decimals = 2) == 0.60 and p_val[i] < 0.05:
             if np.around(time[i], decimals = 2) == 0.20 and p_val[i] < 0.05 or (np.around(time[i], decimals = 2) == 0.30 and p_val[i] < 0.05) or np.around(time[i], decimals = 2) == 0.40 and p_val[i] < 0.05:
                plt.fill_between(time, y1 = p_mul, y2 = -p_mul, facecolor = 'g', alpha = 0.46, step = 'pre')
                res = True
    arr_ind = np.zeros(102)
    plt.tick_params(labelsize = 14)
    plt.legend(loc='upper right', fontsize = 14)
    plt.title(title, fontsize = 36)
    output = 'output/'
    path = output + folder + '/'
    os.makedirs(path, exist_ok = True)
    plt.savefig(path+title + '.svg', transparent=True)
    plt.close()
    return res

def p_val_binary(p_val_n, treshold):
    p_val =  copy.deepcopy(p_val_n)
    for raw in range(p_val.shape[0]):
        for collumn in range(p_val.shape[1]):
            if p_val[raw, collumn] < treshold:
                p_val[raw, collumn] = 1
            else:
                p_val[raw, collumn] = 0
    return p_val

