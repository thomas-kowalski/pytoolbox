#%% Trim sampling file from few parameter input, all keys

import os
import re
import soundfile as sf
import numpy as np
from uvipy.midi import *

whitekeys = ["C", "D", "E", "F", "G", "A", "B"]
def main(sample, notes, startnote):
    newfolder = os.path.join(os.path.split(sample)[0], os.path.splitext(os.path.split(sample)[1])[0])

    try:
        os.mkdir(newfolder)
    except:
        pass

    note = note_from_name(startnote)
    x, sr = sf.read(sample)
    increment = len(x) // notes
    for i in range(1, notes + 1):
        midinote = midi_to_note_name(note)
        subtype = sf.info(sample).subtype
        print(midinote, (i - 1) * increment, i * increment, len(x))
        segment = x[(i - 1) * increment:i * increment]
        filename = os.path.splitext(os.path.split(sample)[1])[0]+"-"+midinote+".wav"
        print(filename)

        # segment /= np.amax(abs(segment))
        note += 1
        sf.write(os.path.join(newfolder, filename), segment, sr, subtype=subtype)
        print("-")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("usage: python <script> <sampling file> <number of notes> <start note>")
        print("ex: python script.py file.wav 61 C0")
