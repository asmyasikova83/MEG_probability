# MEG_probability
Analyses of reinforced learning in probability settings

Based on Kozunova, G.L., Voronin, N.A., Venediktov, V.V. et al. Learning with Reinforcement: the Role of Immediate Feedback and the Internal Model of the Situation. Neurosci Behav Physi 49, 1150–1158 (2019). https://doi.org/10.1007/s11055-019-00852-7

we have been preparing and analyzing MEG-data from 30 participants choosing from two alternatives, where one stimulus was rewarded in 70% of cases and the other one in 30%. 

Exploring the issue of exploration/exploitation after successful training (we consider the period starting from the forth corrrect response in a row with the share of correct responses over the rest of the run being greater than 66%) we

1) investigate  the reaction to negative and positive feedback. 

Therefore, in the script events_extraction.py we

 a) identify the events and timing corespondent to successful training;

 b) in this period we identify events associated with negative and positive feedback. 

After that in the script mio_correction.py we identify muscular contamination and remove contaminated epochs following the criterion of 7*SD AND not more than 1/4th of contaminated epochs.

Next, in the script grand_average.py we

 a) perform baseline correction by substracting averages of the time interval before the appearance of fixation cross from each epoch of interest, correspondigly

 b) compute grand average of the obtained evokeds and save correspondent figure in /home/asmyasnikova83/DATA/evoked_ave

Time frequency analysis

Script baseline_correction.py contains a function for manual computation of power baseline based on time interval as of (-0.350, -0.050) ms before the appearance of fixation cross (0 ms)
and that of manual correction of frequency representation of the epochs of interest (with feedback) by summation of power bands in a freq range, their division by mean power in the (-0.350, -0.050) ms interval preceding the appearance of fixation cross summarized over the freq tapers (see multitaper method)  and log transformation of the result.

Script tfr.py contains further processing and plotting options of tfr data: collecting and averaging of tfr data over 30 participants and 7 runs.
Plot_topomap and plot_topo are available.


