import os.path as op
import os
import mne


# This code sets an environment variable called SUBJECTS_DIR
#os.environ['SUBJECTS_DIR'] = '/net/server/data/Archive/prob_learn/freesurfer'
subjects_dir = '/net/server/data/Archive/prob_learn/freesurfer'

subjects = []
for i in range(20,22):
    if i < 10:
        subjects += ['P00' + str(i)]
    else:
        subjects += ['P0' + str(i)]


# удаляем испытуемых без МРТ        
subjects.remove('P036')
subjects.remove('P062')     

subjects.remove('P052')   # bad segmentation

conductivity = [0.3] # for single layer        
os.makedirs('/net/server/data/Archive/prob_learn/asmyasnikova83/forward_model/bem', exist_ok = True) 
for subj in subjects:

    conductivity = [0.3] # for single layer
    model = mne.make_bem_model(subject=subj, ico=4, conductivity= conductivity, subjects_dir=subjects_dir, verbose=None)

    bem = mne.make_bem_solution(model)
    
    mne.write_bem_solution('/home/asmyasnikova83/forward_model/bem/{0}_bem.h5'.format(subj), bem, overwrite=False, verbose=None)
        

    
