#%% Rename file from ProTools output (ex: file_01.wav, file_03.wav, file_05.wav, etc.)

import os
import re
from uvipy.sf import browse
from uvipy.midi import *

def natsorted(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def main(root_samples, startnote):
    startnote = note_from_name(startnote)

    c = 0
    samples = browse(root_samples)
    for sample in natsorted(samples):
        midisuffix = midi_to_note_name(startnote + c)
        newpath = f'{sample.split("-")[0]}-{midisuffix}.wav'

        print(newpath)
        os.rename(sample, newpath)
        c += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("usage: python <script> <folder> <startnote>")
