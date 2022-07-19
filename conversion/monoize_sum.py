#%% Monoize audio files (sum both channels)

import os
import numpy as np
import uvipy.sf as sf

def main(folder):
    for sample in sf.browse(folder):
        x, sr = sf.read(sample)

        y = np.zeros(len(x))
        for k in range(x.shape[1]):
            y = y + x[:,k]
        
        y /= x.shape[1]
        sf.write(sample, y, sr, sf.info(sample).subtype, sf.get_chunks(sample))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <folder>")
