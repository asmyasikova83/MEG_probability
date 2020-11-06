# MEG_probability
Analyses of reinforced learning in probability settings

Based on Kozunova, G.L., Voronin, N.A., Venediktov, V.V. et al. Learning with Reinforcement: the Role of Immediate Feedback and the Internal Model of the Situation. Neurosci Behav Physi 49, 1150–1158 (2019). https://doi.org/10.1007/s11055-019-00852-7

we have been preparing and analyzing MEG-data from 30 participants choosing from two alternatives, where one stimulus was rewarded in 70% of cases and the other one in 30%. 

Exploring the issue of exploration/exploitation after successful training (we consider the period starting from the forth corrrect response in a row with the share of correct responses over the rest of the run being greater than 66%) we

1) investigate  the reaction to negative and positive feedback. 

2) explore neuromagnetic correlates of risk, prerisk and postrisk behavior.

Therefore, in the script events_extraction.py (and pos_neg_events_extraction.py for separate positive and negative FB analyses, pos_neg_events_extraction_no_train.py for the analysis without training) - for feedbacks, risk_norisk_events_extraction.py - for risks,  we

 a) identify the events and timing corespondent to successful training;

 b) in this period we identify events associated with negative and positive feedback (or for risks, respectively)

After that in the script mio_correction.py we identify muscular contamination and remove contaminated epochs following the criterion of 7*SD AND not more than 1/4th of contaminated epochs.

Note: All necessary settings are in config.py.
Note: Workflow for feedback: config settings -> events_extraction.py (or pos_neg_events_extraction.py, pos_neg_events_extraction_no_train.py) -> mio_correction.py -> grand_average.py for GA analysis ( in progress) or tfr.py

Workflow for risks: config settings -> risk_norisk_events_extraction.py  -> mio_correction.py -> grand_average.py for GA analysis ( in progress) or tfr.py

if tfr.py for both FB and risks -> make_evoked_freq_data_container.py -> plot_time_course_in_html_call.py or plot_topo_stat_call.py -> make_pdf_from_pic_and_html_time_course.py or plot_topo_stat_call.py 

NOTE: in pdf makers do the settings (in  progress)

Event related response

In the script grand_average.py we

 a) perform baseline correction by substracting averages of the time interval before the appearance of fixation cross from each epoch of interest, correspondigly

 b) compute grand average of the obtained evokeds and save correspondent figure in /home/asmyasnikova83/DATA/evoked_ave

Note: Adjust grand_average.py for risks.

Time frequency analysis

Script baseline_correction.py contains a function for manual computation of power baseline based on time interval as of (-0.350, -0.050) ms before the appearance of fixation cross (0 ms)
and that of manual correction of frequency representation of the epochs of interest (with feedback) by summation of power bands in a freq range, their division by mean power in the (-0.350, -0.050) ms interval preceding the appearance of fixation cross summarized over the freq tapers (see multitaper method)  and log transformation of the result.

Total power, evoked and induced power

We explore total_power 
The information within responses is obtained by evaluating the frequency spectrum of each block in every subject, which is then averaged - first over the blocks (runs), then over the subjects.
Evoked responses imply linear average of many short trials whose responses are phase-locked to the onset of a stimulus. 
Adjamian, Peyman. (2014). The Application of Electro- and Magneto-Encephalography in Tinnitus Research  Methods and Interpretations. Frontiers in neurology. 5. 228. 10.3389/fneur.2014.00228. 

Spectrograms

For statistical comparisons we do the summation of power over tapers  in both power baseline and data. For spectrograms we DO NOT do any summation. This option is introduced via flag plot_spectrogram = True 
before calling correct_baseline_power and is available in plot_spectrogram.py, tfr_for_spec.py
Spectrograms are plotted via plot_spectrogram.py using the plotting build-in function freq_spec_data.plot
More advanced framework for doing spectrograms involves tfr_for_spec.py which launches tfr processing of data (each subject, each run). We set plot_spectrogram = True here to avoid summation of power over tapers in both baseline and data. Script do_spec.py reads the tfr data and average the data over all runs in each particular subject. Consequenctly, for each subject we obtain 2 tfr data - one for negative, one for positive feedback. After that we do the grand averaging and use a built-in function freq_data.plot_topo in order to obtain a channel-wise spectrogram (topomap)

Statistics and Visualization of total power deviations from baseline over time

Plot_time_course_in_html_call.py exploits compute_p_val.py to compute t_statistics and relevant p_vals when comparing 2 states (available - Negative feedback versus Positive feedback, Risk vs Norisk, Prerisk vs Postrisk). Time intervals with stat. significant comparisons are highlighted. The output of plot_time_course_in_html_call.py comprises .svg for each channel  + html for the overall result. Make_pdf_from_pic_and_html_time_course.py converts html into pdf. Note: pdfkit is needed.


For plotting topomaps with marked stat. significant sensors in contrasts use plot_topo_stat_call.py. This script also calls compute_p_val.py for statistics. The resuls is plotted over time using built-in plot_topomap. Note: averaging is performed over 100 ms (+/- 50 ms from the indicated time point). Plot_topo_stat_call.py visualizes states, contrast, contrast with marked sensors, contrast with marked sensors after fdr correction (correction for multiple comparisons). The output is .png for states and contrasts and overall html which is further converted to pdf using plot_topo_fdr_pdf.py

Note: settings for visualization are located in config.py.

TODO
Change paths in tfr_for_spec.py, do_spec.py, settings in pdf makers

