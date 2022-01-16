Scripts for processing miographic channels (EMG64), neck muscles

function_emg.py - contains make_beta_signal_mio which conducts tfr and does baseline correction

main_emg.py - calls make_beta_signal_mio for each subject, run, cond, fb sign and saves the tfr data

create_mem_table_emg.py - calls  make_subjects_df  which makes data frame for EMG64 sensor containing subj, run, fb, mean beta power and saves it

evoked_ave_between_runs_and_fb_var3_emg.py averages fbs in each subj, in each condition yuilding one recording for each subj in each condition

evoked_ave_between_runs_var3_separ_fb_emg.py - averages pos and neg fb separately in each subject, in each condition, yuilding 2 recordings in each subj and condition

plot_timecourses_veog_mio.py - draws timecourses for each fb separately (contrasting fbs in each condition) and irrespective of fb (contrasting conditions)

check_mio_veog.py - tfr for EMG64
