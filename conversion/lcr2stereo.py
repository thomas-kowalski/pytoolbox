#%% Convert LCR audio files to stereo

import os
import numpy as np
import uvipy.sf as sf

def main(folder):
    currentfile = os.path.split(folder)[1]
    genpath = os.path.join(os.path.split(folder)[0], "GENERATED "+currentfile)
    try:
        os.mkdir(genpath)
    except:
        pass

    for sample in sf.browse(folder):
        x, sr = sf.read(sample)
        if x.shape[1] < 3:
            print(os.path.split(sample)[1], ">> FILE IS NOT LCR")
            continue
        print(os.path.split(sample)[1])
        
        l = x[:,0]; r = x[:,1]; c = x[:,2]
        lc = l + c * 10**(-3/20)
        rc = r + c * 10**(-3/20)
        y = np.array([lc, rc]).transpose()

        filename = os.path.split(sample)[1]
        sf.write(os.path.join(genpath, filename), y, sr, sf.info(sample).subtype, sf.get_chunks(sample))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: <python> <script> <folder>")