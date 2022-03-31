Plotting scripts

config.py - settings including donor, response, cond names

function.py - functions including compute_p_val.py (output - evoked data averaged over subjects, p_val from ttests

plot_stat_comparison (draws timecourses with stat)

make_pdf.py - html into pdf

plot_sum_topomaps.py - topomapas averaged over a time interval 

plot_timecourse_aver_all_ch.py - timecourses averaged over a set of channels (cluster)

plot_topomaps_LMEM_factors.py - topomaps with statistics from LMEM (factors)

plot_topomaps_line_LMEM.py  - topomaps with p_vals from LMEM 

plot_topomaps_aver_pair.py topomaps averaged over time intervals
#resample_before_stat added, yuilding less time points which stops overfitting

topo_ch_MEG_template.py - MEG template with a set of channels

topo_ch_template.py -  template with green significant channels

p_val_gradient.py - plots topomaps with ttest/LMEM for signed p-vals in contrasts

p_val_gradient_pairs.py - plots averaged topomaps with LMEM for signed p-vas in contrasts

#TODO do donor for less time points



