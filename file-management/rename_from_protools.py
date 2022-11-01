#%% Rename file from ProTools output with RR option (ex: file-01.wav, file-03.wav, file-05.wav, etc.)

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
    for sample in natsorted(samples):
        midisuffix = midi_to_note_name(startnote + c)
        rrsuffix = rr != 1 and f'-rr0{rrcount + 1}' or ''
        newpath = f'{samples[:-6]}-{midisuffix}{rrsuffix}.wav'
        print(newpath)

        rrcount = (rrcount + 1) % rr
        os.rename(sample, newpath)
        if rrcount == 0:
            c += 1

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    else:
        print("usage: python <script> <folder> <startnote> <rr (1 if no round robin)>")
