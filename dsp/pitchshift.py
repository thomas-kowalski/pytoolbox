#%% Pitch shift audio sample (override loop points)

import os
import samplerate
import uvipy.sf as sf

def pitch_shift(x, semitones):
    ratio = 2 ** (semitones * -1 / 12)
    return samplerate.resample(x, ratio, "sinc_best")

def main(root_samples, semitone_offset):
    for sample in sf.browse(root_samples):
        x, sr = sf.read(sample)
        xshift = pitch_shift(x, semitone_offset)
        sf.write(sample, xshift , sr, subtype=sf.info(sample).subtype)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print("usage: python <script> <samples folder> <semitones offset>")
