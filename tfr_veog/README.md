Scripts for making TF_plots of oculografic channels (MISC301 - VEOG, MISC302 HEOG)

functions.py - contains make_beta_signal_mio which conducts tfr and does baseline correction

make_h5_for_TF_plots_veog.py - calls make_h5_files function which makes tfr and baseline correction of the data from oculographic channels. The TF dayta are saved in -h5 format

make_donor_veog.py - using make_h5_files donor data file is made for further plotting 

ave_into_subj_fb_separ_h5_veog.py - averaging runs keeping fb separate for further plotting

plot_tfr_veog.py - using plot_deff_tf_veog do TF plot with statistics


