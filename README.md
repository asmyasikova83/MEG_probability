# MEG_probability
Analyses of reinforced learning in probability settings

Based on Kozunova, G.L., Voronin, N.A., Venediktov, V.V. et al. Learning with Reinforcement: the Role of Immediate Feedback and the Internal Model of the Situation. Neurosci Behav Physi 49, 1150–1158 (2019). https://doi.org/10.1007/s11055-019-00852-7

we have been preparing and analyzing MEG-data from 30 participants choosing from two alternatives, where one stimulus was rewarded in 70% of cases and the other one in 30%. 

Following the evidence of paradoxical sensitivity to rare stimuli after successful training (we consider the period starting from the forth corrrect response in a row with the share of correct responses over the rest of the run being greater than 66%) we

1) explore the reaction to negative and positive feedback. 

Therefore,in the script main.py we a)identify the events and timing corespondent to successful training; b) in this period we identify events associated with negative and positive feedback. 

After that in the script mio_correction.py we identify muscular contamination and remove contaminated epochs following the criterion of 7*SD AND not more than 1/4th of contaminated epochs.



