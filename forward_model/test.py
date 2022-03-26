import mne
import mne
import os.path as op
import os

import mne
Brain = mne.viz.get_brain_class()
os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

#subjects_dir = mne.datasets.sample.data_path() #/ 'subjects'
mne.datasets.fetch_hcp_mmp_parcellation(subjects_dir=subjects_dir,
                                                verbose=True)

mne.datasets.fetch_aparc_sub_parcellation(subjects_dir=subjects_dir,
                                                  verbose=True)

labels = mne.read_labels_from_annot(
            'fsaverage', 'HCPMMP1', 'lh', subjects_dir=subjects_dir)

brain = Brain('fsaverage', 'lh', 'inflated', subjects_dir=subjects_dir,
                      cortex='low_contrast', background='white', size=(800, 600))
brain.add_annotation('HCPMMP1')
aud_label = [label for label in labels if label.name == 'L_A1_ROI-lh'][0]
brain.add_label(aud_label, borders=False)


#brain = Brain('fsaverage', 'lh', 'inflated', subjects_dir=subjects_dir,
#                      cortex='low_contrast', background='white', size=(800, 600))
#brain.add_annotation('HCPMMP1_combined')
