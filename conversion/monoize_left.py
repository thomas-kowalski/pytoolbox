#%% Monoize audio files (keep only left channel)

import os
import uvipy.sf as sf

def main(folder):
    for sample in sf.browse(folder):
        x, sr = sf.read(sample)
        sf.write(sample, x[:,0], sr, sf.info(sample).subtype, sf.get_chunks(sample))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <folder>")
