#%% Rename note suffix from input semitones offset

import os
import re
import shutil
from uvipy.sf import browse
from uvipy.midi import *

def main(root_samples, shift):
    samples = browse(root_samples)

    newdir = os.path.join(root_samples, "TREATED")
    try:
        os.mkdir(newdir)
    except:
        pass

    for note in range(1, 127):
        notesamples = [s for s in samples if midi_to_note_name(note) in s]
        for n in notesamples:
            sname = os.path.split(n)[1]
            newname = sname.replace(midi_to_note_name(note), midi_to_note_name(note + shift))
            print(sname, ">", newname)
            shutil.copy(n, os.path.join(newdir, newname))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print("usage: python <script> <sample folder> <semitones offset>")