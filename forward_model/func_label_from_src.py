import numpy as np
import matplotlib.pyplot as plt
import os
import mne
from mne.minimum_norm import read_inverse_operator, apply_inverse
from mne.datasets import sample
import pandas as pd

data_path = sample.data_path()
subjects_dir = data_path + '/subjects'
fname_inv = data_path + '/MEG/sample/sample_audvis-meg-oct-6-meg-inv.fif'
fname_evoked = data_path + '/MEG/sample/sample_audvis-ave.fif'
subjects_dir = data_path + '/subjects'
subject = 'sample'

snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)

# Compute a label/ROI based on the peak power between 80 and 120 ms.
# The label bankssts-lh is used for the comparison.
aparc_label_name = 'bankssts-lh'
tmin, tmax = 0.080, 0.120

# Load data
evoked = mne.read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
inverse_operator = read_inverse_operator(fname_inv)
src = inverse_operator['src']  # get the source space

# Compute inverse solution
stc = apply_inverse(evoked, inverse_operator, lambda2, method,
                            pick_ori='normal')

# Make an STC in the time interval of interest and take the mean
stc_mean = stc.copy().crop(tmin, tmax).mean()

# use the stc_mean to generate a functional label
# region growing is halted at 60% of the peak value within the
# anatomical label / ROI specified by aparc_label_name
label = mne.read_labels_from_annot(subject, parc='aparc',
                                subjects_dir=subjects_dir,
                                regexp=aparc_label_name)[0]
print(label)

stc_mean_label = stc_mean.in_label(label)
data = np.abs(stc_mean_label.data)
stc_mean_label.data[data < 0.6 * np.max(data)] = 0.

func_labels, _ = mne.stc_to_label(stc_mean_label, src=src, smooth=True,
                                          subjects_dir=subjects_dir, connected=True)

# take first as func_labels are ordered based on maximum values in stc
func_label = func_labels[0]

print(func_label)



# load the anatomical ROI for comparison
anat_label = mne.read_labels_from_annot(subject, parc='aparc',
                                        subjects_dir=subjects_dir,
                                        regexp=aparc_label_name)[0]
print(anat_label)

# extract the anatomical time course for each label
stc_anat_label = stc.in_label(anat_label)

print(stc_anat_label)


pca_anat = stc.extract_label_time_course(anat_label, src, mode='pca_flip')[0]

stc_func_label = stc.in_label(func_label)
pca_func = stc.extract_label_time_course(func_label, src, mode='pca_flip')[0]

# flip the pca so that the max power between tmin and tmax is positive
pca_anat *= np.sign(pca_anat[np.argmax(np.abs(pca_anat))])
pca_func *= np.sign(pca_func[np.argmax(np.abs(pca_anat))])


plt.figure()
plt.plot(1e3 * stc_anat_label.times, pca_anat, 'k',
                 label='Anatomical %s' % aparc_label_name)
plt.plot(1e3 * stc_func_label.times, pca_func, 'b',
                 label='Functional %s' % aparc_label_name)
plt.legend()
#plt.show()



brain = stc_mean.plot(hemi='lh', subjects_dir=subjects_dir)
#brain.show_view('lateral')

# show both labels
brain.add_label(anat_label, borders=True, color='k')
brain.add_label(func_label, borders=True, color='b')
pic = brain.screenshot()
pic.save('/home/asmyasnikova83/MEG_probability/forward_model/ex_brain_obj.png')
