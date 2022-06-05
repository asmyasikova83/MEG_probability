#Head Model: BEM (boundary element model) surface - создается отдельно для каждого испытуемого

import os.path as op
import os
import mne
from config import *

# This code sets an environment variable called SUBJECTS_DIR
#os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'


for subj in subjects:
    fig = mne.viz.plot_bem(subj, subjects_dir, brain_surfaces='white', orientation='coronal', show = False);
    fig.savefig('/net/server/data/Archive/prob_learn/asmyasnikova83/Sources/segmentation_check/{0}.jpeg'.format(subj), dpi = 300)
