import mne
import numpy as np
from scipy import stats
import os
import copy
import matplotlib.pyplot as plt
import statsmodels.stats.multitest as mul
import pdfkit
from config import *
import pathlib

def clear_html(filename):
    with open(filename, 'w') as f:
        f.write('')

def add_str_html(filename, text):
    with open(filename, 'a') as f:
        f.write(text + '\n')
        

def add_pic_html(filename, pic):
    add_str_html(filename, '<IMG SRC="%s" style="width:%spx;height:%spx;"/>'%(pic,2800,390))


def get_short_legend(contrast):
    temp = contrast.split('_')
    return (temp[0], temp[2], temp[3], temp[4])

def delaete_bad_sub(contrast, del_list):
    for sub in del_list:
        if sub in contrast[1]:
            ind = contrast[1].index(sub)
            contrast[1].pop(ind)
            contrast[0] = np.delete(contrast[0], ind, axis=0)
    return contrast

def p_val_binary(p_val_n, treshold):
    p_val =  copy.deepcopy(p_val_n)
    for raw in range(p_val.shape[0]):
        for collumn in range(p_val.shape[1]):
            if p_val[raw, collumn] < treshold:
                p_val[raw, collumn] = 1
            else:
                p_val[raw, collumn] = 0
    return p_val



def space_fdr(p_val_n):
    print(p_val_n.shape)
    temp = copy.deepcopy(p_val_n)
    for i in range(temp.shape[1]):
        _, temp[:,i] = mul.fdrcorrection(p_val_n[:,i])
    return temp

path = os.getcwd()
list_files = os.listdir(path)

output = 'output_topo/'


topomaps = ["Positive",
            "Negative",
            
            "difference",
            "difference_with_fdr",

            ]

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

options = {
    'page-size':'A3',
    'orientation':'Landscape',
    'zoom':1.0,
    'no-outline':None,
    'quiet':''
}

subjects = [
    'P000',
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


os.makedirs(os.path.join(output, "Positive_vs_Negative"), exist_ok=True)        


if mode == 'server':
    #donor data file
    #temp = mne.Evoked('/home/asmyasnikova83/DATA/P006_run6_evoked-ave.fif')
    temp = mne.Evoked("/home/asmyasnikova83/DATA/donor-ave.fif")
    out_path = '/home/asmyasnikova83/DATA/evoked_ave/'
else:
    temp = mne.Evoked('/home/sasha/MEG/MIO_cleaning/P006_run6_evoked-ave.fif')
    temp = mne.Evoked("/home/sasha/MEG/MIO_cleaning/donor-ave.fif")
    out_path = '/home/sasha/MEG/Evoked/'

temp.nave = 98

temp.first = -2000
temp.last = 1500

temp.times = np.arange(-2.000, 1.502, 0.004)

p_mul = 0.3

times_to_plot = np.arange(-2.0, 1.5, 0.2)
print('times to plot size', times_to_plot.size)
legend = ["Positive", "Negative"]
kind = ['positive', 'negative']

rewrite = True
'''
if rewrite:
#data container for 2 conditions, 305 ch, times
    contr = np.zeros((len(subjects), 2, 306, 876))
    for ind, subj in enumerate(subjects):
        rf = out_path + "{0}_feedback_{1}_theta-ave.fif".format(subj, kind[0])
        file = pathlib.Path(rf)
        if file.exists():
            print('This subject is being processed: ', subj)
            #positive FB
            print(kind[0])
            temp1 = mne.Evoked(out_path + "{0}_feedback_{1}_theta-ave.fif".format(subj, kind[0]))
            temp1 = temp1.pick_types("grad")
            #planars
            contr[ind, 0, :204, :] = temp1.data
            #combined planars
            contr[ind, 0, 204:, :] = temp1.data[::2] + temp1.data[1::2]
            #negative FB
            print(kind[1])
            temp2 = mne.Evoked(out_path + "{0}_feedback_{1}_theta-ave.fif".format(subj, kind[1]))
            temp2 = temp2.pick_types("grad")

            contr[ind, 1, :204, :] = temp2.data
            contr[ind, 1, 204:, :] = temp2.data[::2] + temp2.data[1::2]

    comp1 = contr[:, 0, :, :]
    comp2 = contr[:, 1, :, :]
    
    #axis=0 over conditions
    t_stat, p_val = stats.ttest_rel(comp1, comp2, axis=0)
    p_val_fdr = space_fdr(p_val)

    comp1_mean = comp1.mean(axis=0)
    comp2_mean = comp2.mean(axis=0)
    
       
    
    ##### CONDITION1 ######
    
    temp.data = comp1_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = legend[0], colorbar = True, vmax=p_mul, vmin=-p_mul)

    fig.savefig(os.path.join(output, legend[0] + ".png"), dpi = 300)
    

    plt.close()

    ##### CONDITION2 ######
    
    temp.data = comp2_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = legend[1], colorbar = True, vmax=p_mul, vmin=-p_mul)
    fig.savefig(os.path.join(output, legend[1] + ".png"), dpi = 300)
    plt.close()
    
    
    ##### CONDITION2 - CONDITION1 with marks (WITH FDR) ######
    
    binary = p_val_binary(p_val_fdr, treshold = 0.05)
    temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "%s - %s with_fdr"%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul, vmin=-p_mul, extrapolate="local", mask = np.bool_(binary[204:,:]),
                            mask_params = dict(marker='o', markerfacecolor='yellow', markeredgecolor='k',
                                               linewidth=0, markersize=10, markeredgewidth=2))
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"difference_with_fdr.png"), dpi = 300)
    plt.close()
    
    ##### CONDITION2 - CONDITION1 cutted by thershold (WITH FDR) ######
    
    binary = p_val_binary(p_val_fdr, treshold = 0.05)
    # ask Nikita about the following formula
    temp.data = (comp2_mean[204:,:] - comp1_mean[204:,:])*binary[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.05,
                            scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                            ch_type='planar1', time_unit='s', show = False, 
                            title = "%s - %s (cut) with fdr"%(legend[1], legend[0]), colorbar = True, 
                            vmax=p_mul, vmin=-p_mul, extrapolate="local")
    fig.savefig(os.path.join(output, legend[0] + "_vs_" + legend[1],"p_value_cut_with_fdr.png"), dpi = 300)
    plt.close()
   
'''


html_name = os.path.join(output, legend[0] + "_vs_" + legend[1] + ".html")
clear_html(html_name)
add_str_html(html_name, '<!DOCTYPE html>')
add_str_html(html_name, '<html>')
add_str_html(html_name, '<body>')
add_str_html(html_name, '<p style="font-size:40px;"><b> %s, average Theta 4-8 Hz after feedback presentation in 28 participants after training </b></p>' % (legend[0] + "_vs_" + legend[1]))
add_str_html(html_name, '<p style="font-size:40px;"><b> P_val < 0.05 marked (or saved from cutting) </b></p>' )
add_str_html(html_name, '<table>')
for topo in topomaps:
    add_str_html(html_name, "<tr>")
    add_pic_html(html_name, os.path.join(legend[0] + "_vs_" + legend[1],topo+".png"))
add_str_html(html_name, "</tr>")
add_str_html(html_name, '</body>')
add_str_html(html_name, '</html>')
pdf_file = html_name.replace("html", "pdf")
pdfkit.from_file(html_name, pdf_file, configuration = config, options=options)
