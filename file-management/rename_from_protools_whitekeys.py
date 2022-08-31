#%% Rename file from ProTools output with RR option (ex: file_01.wav, file_03.wav, file_05.wav, etc.)
# ONLY WHITE KEYS

import os
import re
from uvipy.sf import browse
from uvipy.midi import *

def natsorted(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def main(root_samples, startnote, rr):
    startnote = note_from_name(startnote)

    c = 0
    rrcount = 0
    samples = browse(root_samples)
    whitekeys = ["C", "D", "E", "F", "G", "A", "B"]

    for sample in natsorted(samples):
        midisuffix = midi_to_note_name(startnote + c)
        while midisuffix[:-1] not in whitekeys:
            c += 1
            midisuffix = midi_to_note_name(startnote + c)

        newpath = f'{sample.split("-")[0]}-{midisuffix}.wav'
        print(newpath)

        rrcount = (rrcount + 1) % rr
        # os.rename(sample, newpath)
        if rrcount == 0:
            c += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:
        print("usage: python <script> <folder> <startnote> <rr (1 if no round robin)>")
