Scripts in R for linear mixed effects modeling and visualization for averaged beta band power activity in subjects

subj_list.csv - list of subjects
subject_demographics.R - age and sex of subjects
example_LMEM.R - a simple LMEM from Vera Tretyakova

Legacy: Ksenia Sayfulina

LMM_p_values_for_heads_factor_significance.R - script for producing LMEM p-values for factors (trial type, feedback sign and their interaction)
**LMM_p_values_for_heads.R - early version of LMM, we do not use it currently

extract_events_from_table.R - derives events from the table events_classification_clean_final.csv

MEG_lmem_statistics_and_visualization.R - basic script which derives significant sensors (info about sensors in sensors.csv) from p_vals_factor_significance_MEG.csv, makes dataframe with infoo from those sensors, averages the data in the predefined time interval in those sensors, develops LMEM model and conducts Tukey HSD (correction for multiple comparisons). Averaged data across the conditions over the time intervals in the sensors are plotted with Tukey p-values

Beta_trial_correct.R - LMEM model for factor trial_type and associated plot #TODO check for outliers in decision and anterior clusters

Beta_feedback_no_outliers.R -  LMEM model for factor feedback_sign and associated plot

LMM_p_values_for_heads_factor_significance_emg_oculo.R
Beta_trial_emg.R - LMEM for one channel (oculo- or mioographic)
Beta_feedback_emg.R

Beta_fix_cross_trial.R - LMEM for the intertrial interval where we expect carryover effects
Beta_fix_cross_feedback.R

Beta__by_subjects.R - LMEM, but plotting for subjects separately
Beta__by_subjects_in_one.R
