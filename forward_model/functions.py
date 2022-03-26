import mne

def make_fwd_solution(subj, bem, src, trans, epochs_info):
    fwd = mne.make_forward_solution(info = epochs_info, trans = trans, src = src, bem = bem)
    return fwd

