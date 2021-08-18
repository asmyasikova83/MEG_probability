import mne
import os.path as op
import os
from scipy import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import copy
import statsmodels.stats.multitest as mul
from function import space_fdr, full_fdr, p_val_binary, compute_p_val, plot_stat_comparison, to_str_ar, clear_html, add_str_html,  add_pic_time_course_html
from config import *

options = {
    'page-size':'A2',
    'orientation':'Landscape',
    'zoom':0.57,
    'no-outline':None,
    'quiet':''
}


# загружаем комбайн планары, усредненные внутри каждого испытуемого
data_path = '/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/{1}_ave_comb_planar'.format(feedb, fr)
print(data_path)
  
###################### при построении topomaps берем только тех испытуемых, у которых есть все категории условий ####################
### extract subjects with all conditions:fb+trial_type ####
#out_path='/net/server/data/Archive/prob_learn/asmyasnikova83/{0}/{1}_epo/'.format(feedb, fr) #path to epochs
out_path = f'/net/server/data/Archive/prob_learn/asmyasnikova83/low_{fr}_CORR/{fr}_epo/' #TODO
f = os.listdir(out_path) # Делает список всех файлов, которые храняться в папке


# задаем время и донора
temp = mne.Evoked("/net/server/data/Archive/prob_learn/vtretyakova/Nikita_mio_cleaned/beta_16_30_ave_into_subjects_comb_planar/P001_norisk_evoked_beta_16_30_resp_comb_planar.fif")

time = temp.times# количество временных отчетов для combaened planars - temp.data.shape = (102 x n), где 102 - количество планаров, а n - число временных отчетов

########################### norisk vs risk ##############################


#coordinates and channel names from matlab files - the files are here https://github.com/niherus/MNE_TFR_ToolBox/tree/master/VISUALISATION
pos = io.loadmat('/net/server/data/Archive/prob_learn/asmyasnikova83/pos_store.mat')['pos']
chan_labels = to_str_ar(io.loadmat(f'/net/server/data/Archive/prob_learn/asmyasnikova83/channel_labels.mat')['chanlabels'])
os.makedirs(path + 'output/', exist_ok=True)

for p in planars:
    #extract data and ttest
    comp1_mean, comp2_mean, p_val = compute_p_val(subjects, cond1, cond2, time)
    #scaling
    if comp1_mean.max()>comp2_mean.max():
        p_mul_max=comp1_mean.max()+ abs(comp1_mean.max()/10)
    else:
        p_mul_max=comp2_mean.max()+ abs(comp2_mean.max()/10)

    if comp1_mean.min()<comp2_mean.min():
        p_mul_min=comp1_mean.min() - abs(comp1_mean.min()/10)
    else:
        p_mul_min=comp2_mean.min() - abs(comp2_mean.min()/10)

    comp1_label = cond1
    comp2_label = cond2
    cond1_name = cond1
    cond2_name = cond2

    for indx in range(102):
        rej,p_fdr = mne.stats.fdr_correction(p_val[indx,:], alpha=0.05, method='indep')
        print('comp_mean', comp1_mean.shape)
        plot_stat_comparison(path, feedb, fr, comp1_mean[indx], comp2_mean[indx], p_mul_min, p_mul_max, p_val[indx], p_fdr, time, title = chan_labels[indx+204],
                             folder = "%s_vs_%s" % (cond1_name, cond2_name), comp1_label = cond1_name, comp2_label = cond2_name)

    for ind, planar in enumerate(planars):
        #place the channel time courses in html file
        html_name = path + 'output/' + 'pic_compose_%s_%s_vs_%s_%s.html' % (planar, f'{cond1}', f'{cond2}', 'all')
        clear_html(html_name)
        add_str_html(html_name, '<!DOCTYPE html>')
        add_str_html(html_name, '<html>')
        add_str_html(html_name, '<body>')
        add_str_html(html_name, '<p style="font-size:32px;"><b> %s, averaged %s, %d subjects <span style="color:green;"> p_val < 0.05 </span> <span style="color:Magenta;">p_fdr < 0.05 </span> </b></p>' % (planar, fr, len(subjects)))
        add_str_html(html_name, '<p style="font-size:32px;"><b> <span style="color: blue;"> %s </span> vs <span style="color: red;"> %s </span> </b></p>' % (cond1, cond2))
        #placing the channel time courses and save the html
        if ind == 2:
            for ch_num in range(204, len(chan_labels)):
                pic = chan_labels[ch_num] + '.png'
                add_pic_time_course_html(html_name, pic, f'{cond1_name}_vs_{cond2_name}', pos[ch_num], [200,150])
        else:
            for ch_num in range(ind, 204, 2):
                pic = chan_labels[ch_num] + '.png'
                add_pic_time_course_html(html_name, pic, f'{cond1_name}_vs_{cond2_name}', pos[ch_num], [200,150])

        add_str_html(html_name, '</body>')
        add_str_html(html_name, '</html>')
        pdf_file = html_name.split("/")[1].split('.')[0]
        print(html_name)
        pdf_path = path + 'output/' + f'all_pdf/'
        os.makedirs(pdf_path, exist_ok = True)
    print('\tAll printed')
