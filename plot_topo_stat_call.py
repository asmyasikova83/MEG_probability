import mne
import numpy as np
import os
import statsmodels.stats.multitest as mul
import matplotlib.pyplot as plt
from config import conf
import pathlib
from plot_time_course_in_html_functions import clear_html
from plot_time_course_in_html_functions import to_str_ar
from plot_time_course_in_html_functions import add_str_html
from plot_time_course_in_html_functions import add_pic_topo_html
from plot_time_course_in_html_functions import get_short_legend
from plot_time_course_in_html_functions import delaete_bad_sub
from plot_time_course_in_html_functions import p_val_binary
from plot_time_course_in_html_functions import space_fdr
from compute_p_val import compute_p_val
from tfce import *
from scipy import stats, io
#from compute_p_val_stat_over_runs import compute_p_val_over_runs


def topo_stat(conf):
    print('\trun fdr for topomaps...')
    grand_average = conf.grand_average
    time = conf.time
    times_to_plot = conf.times_to_plot
    p_mul_topo = conf.p_mul_topo
    p_mul_topo_contrast = conf.p_mul_topo_contrast
    p_mul_topo_fdr_contrast = conf.p_mul_topo_fdr_contrast
    baseline = conf.baseline
    legend = conf.legend

    cur_dir = conf.path_fdr
    verbose = conf.verbose

    os.chdir(cur_dir)

    topomaps = [f'{legend[0]}',
                f'{legend[1]}',
                'difference_fdr',
                'difference_deep_fdr']
    options = {
        'page-size':'A3',
        'orientation':'Landscape',
        'zoom':1.0,
        'no-outline':None,
        'quiet':''
    }
    
    os.makedirs(os.path.join(conf.path_fdr, f'{legend[0]}_vs_{legend[1]}'), exist_ok=True)
    if grand_average == True:
        frequency = None
    else:
        frequency = conf.frequency

    #donor data file
    temp = mne.Evoked(f'{conf.path_home}donor-ave.fif', verbose = 'ERROR')
    temp.times = conf.time
    subjects = conf.subjects
    comp1_mean, comp2_mean, contr, temp1, temp2, p_val, binary, subjects1  = compute_p_val(conf, subjects, conf.kind,
               conf.train, frequency, conf.check_num_sens)
    df1 = contr[:, 0, 204:, :] #per channel
    df2 = contr[:, 1, 204:, :]
    if verbose:
        print('df1 shape', df1.shape)
        print('df2 shape', df2.shape)

    #res_tfce = np.zeros((876, 102))
    pos = io.loadmat(f'{conf.path_home}pos_store.mat')['pos']
    chan_labels = to_str_ar(io.loadmat(f'{conf.path_home}channel_labels.mat')['chanlabels'])
    dict_col = { 'risk': 'salmon', 'norisk': 'olivedrab', 'prerisk': 'mediumpurple' , 'postrisk':'darkturquoise'  }
    p_val_fdr = space_fdr(p_val)

    ##### CONDITION1 and Stat  ######
    # average = 0.1 means averaging of the power data over 100 ms
    if verbose:
        print('comp1_mean', comp1_mean.shape)
        print('df1', df1.shape)
        print('time', len(time))
        print('times to plot', len(times_to_plot))
    t_stat_con1, p_val_con1 = stats.ttest_1samp(df1, 0, axis=0)
    if verbose:
        print('p val con1 shape', p_val_con1.shape)
    width, height = p_val_con1.shape
    p_val_con1 = p_val_con1.reshape(width * height)
    _, p_val_con1 = mul.fdrcorrection(p_val_con1)
    p_val_con1 = p_val_con1.reshape((width, height))
    binary = p_val_binary(p_val_con1, treshold = 0.05)


    temp.data = comp1_mean[204:,:]
    fig = temp.plot_topomap(times = times_to_plot, average = 0.1, units = "dB",
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = legend[0] + ' stat fdr against zero', colorbar = True, vmax=p_mul_topo, vmin=-p_mul_topo,
                                extrapolate="local", mask = np.bool_(binary),
                                mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='k',
                                                  linewidth=0, markersize=7, markeredgewidth=2))
    fig.savefig(os.path.join(conf.path_fdr, legend[0] + '_vs_' + legend[1], legend[0] + '.png'), dpi = 300)
    plt.close()

    ##### CONDITION2 and Stat ######
    
    #temp.data = comp2_mean[204:,:]
    t_stat_con2, p_val_con2 = stats.ttest_1samp(df2, 0, axis=0)
    width, height = p_val_con2.shape
    p_val_con2 = p_val_con2.reshape(width * height)
    _, p_val_con2 = mul.fdrcorrection(p_val_con2)
    p_val_con2 = p_val_con2.reshape((width, height))
    binary = p_val_binary(p_val_con2, treshold = 0.05)

    temp.data = comp2_mean[204:,:]
    fig = temp.plot_topomap(times = times_to_plot, average = 0.1, units = 'dB',
                                scalings = dict(eeg=1e6, grad=1, mag=1e15),
                                ch_type='planar1', time_unit='s', show = False, 
                                title = legend[1] + ' stat fdr  against zero', colorbar = True, vmax=p_mul_topo, vmin=-p_mul_topo,
                                extrapolate="local", mask = np.bool_(binary),
                                mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='k',
                                                   linewidth=0, markersize=7, markeredgewidth=2))
    fig.savefig(os.path.join(conf.path_fdr, legend[0] + '_vs_' + legend[1], legend[1] + '.png'), dpi = 300)
    plt.close()
    
    ##### CONDITION2 - CONDITION1 with marks no time  (space FDR) ######
    p_val_fdr = space_fdr(p_val)
    binary_fdr = p_val_binary(p_val_fdr, treshold = 0.05)
    temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]
    fig = temp.plot_topomap(times = times_to_plot, average = 0.1, units = 'dB',
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = '%s - %s  space fdr: marks for each head separately'%(legend[1], legend[0]), colorbar = True,
                                vmax=p_mul_topo_contrast, vmin=-p_mul_topo_contrast, extrapolate="local", mask = np.bool_(binary_fdr[204:,:]),
                                mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='k',
                                                    linewidth=0, markersize=7, markeredgewidth=2))
    fig.savefig(os.path.join(conf.path_fdr, legend[0] + '_vs_' + legend[1],'difference_fdr.png'), dpi = 300)
    plt.close()
 
    #### CONDITION2 - CONDITION1 with marks (WITH FDR) deep FDR with time ####

    t_stat, p_val_deep = stats.ttest_rel(df1, df2, axis=0)
    width, height = p_val_deep.shape
    p_val_resh = p_val_deep.reshape(width * height)
    _, p_val_deep_fdr = mul.fdrcorrection(p_val_resh)
    p_val_deep_fdr = p_val_deep_fdr.reshape((width, height))
    binary_deep_fdr = p_val_binary(p_val_deep_fdr, treshold = 0.05)
    temp.data = comp2_mean[204:,:] - comp1_mean[204:,:]

    fig = temp.plot_topomap(times = times_to_plot, average = 0.1, units = 'dB',
                                scalings = dict(eeg=1e6, grad=1, mag=1e15), 
                                ch_type='planar1', time_unit='s', show = False, 
                                title = '%s - %s deep fdr over all heads'%(legend[1], legend[0]), colorbar = True,
                                vmax=p_mul_topo_fdr_contrast, vmin=-p_mul_topo_fdr_contrast, extrapolate="local", mask = np.bool_(binary_deep_fdr),
                                mask_params = dict(marker='o', markerfacecolor='w', markeredgecolor='k',
                                                   linewidth=0, markersize=7, markeredgewidth=2))
    fig.savefig(os.path.join(conf.path_fdr, legend[0] + '_vs_' + legend[1],'difference_deep_fdr.png'), dpi = 300)
    plt.close()
    html_name = os.path.join(conf.path_fdr, legend[0] + '_vs_' + legend[1] + '.html')
    clear_html(html_name)
    add_str_html(html_name, '<!DOCTYPE html>')
    add_str_html(html_name, '<html>')
    add_str_html(html_name, '<body>')
    if grand_average:
        add_str_html(html_name, '<p style="font-size:20px;"><b> %s, %s, %s, trained, %s, %s, %d subjects </b></p>' % (legend[0] + '_vs_' + legend[1], conf.ERF, conf.stimulus, baseline, conf.zero_point, len(subjects1)))
    else:
        add_str_html(html_name, '<p style="font-size:20px;"><b> %s, %s, %s, trained, %s, %s, %d subjects </b></p>' % (legend[0] + '_vs_' + legend[1], frequency, conf.stimulus, baseline, conf.zero_point, len(subjects1)))

    add_str_html(html_name, '<p style="font-size:20px;"><b> boolean fdr  = 1  marked </b></p>' )
    add_str_html(html_name, '<table>')
    for topo in topomaps:
        add_str_html(html_name, "<tr>")
        add_pic_topo_html(html_name, os.path.join(legend[0] + '_vs_' + legend[1],topo+'.png'))
    add_str_html(html_name, "</tr>")
    add_str_html(html_name, '</body>')
    add_str_html(html_name, '</html>')
    pdf_file = html_name.replace("html", "pdf")
    if verbose:
        print('All done!')
    print('\tfdr for topomaps completed')
