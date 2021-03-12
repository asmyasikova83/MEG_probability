import re
 
with open('baseline_correction_bk.py', 'r') as input_:
    with open('baseline_correction.py', 'w') as output_:
        for line in input_.readlines():
            line = re.sub(r"(epochs = mne.EpochsArray.*)(\))", r"\1, verbose='ERROR'\2", line)
            output_.write(line)

