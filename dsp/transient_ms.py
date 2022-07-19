#%% Trim sample start from milliseconds input

import os
import numpy as np
from scipy import signal
import uvipy.sf as sf

def main(root_samples, ms):
    samples = sf.browse(root_samples)

    for sample in samples:
        if "._" in sample: continue
        print(os.path.split(sample)[1])
        x, sr = sf.read(sample)
        index = (ms / 1000) * sr
        x = x[int(index):]
    
        loopinfo = sf.get_chunks(sample)
        if loopinfo[0]:
            loopinfo = (loopinfo[0] - index, loopinfo[1] - index)

        sf.write(sample, x, sr, sf.info(sample).subtype, loopinfo)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print("usage: python <script> <root_samples> <offset in ms>")

