#%% Remove specified note range in sample folder

import os
from uvipy.sf import browse
from uvipy.midi import *

def main(root_samples, midirange):
    for i in range(2):
        midirange[i] = note_from_name(midirange[i])

    for sample in browse(root_samples):
        note = note_from_name(get_note_name(sample))
        if note >= midirange[0] and note <= midirange[1] and not "._" in sample: 
            print("... removing", os.path.split(sample)[1], "...")
            os.remove(sample)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 4:
        midirange = [sys.argv[2], sys.argv[3]]
        main(sys.argv[1], midirange)
    else:
        print("usage: python <script> <low note> <high note>")

