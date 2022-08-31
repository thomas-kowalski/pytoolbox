#%% Trim end from milliseconds input

import os
import uvipy.sf as sf

def main(folder, ms):
    for sample in sf.browse(folder):
        print(os.path.split(sample)[1])
        x, sr = sf.read(sample, always_2d=True)
        loopinfo = sf.get_chunks(sample)

        cutsample = int(sr * ms / 1000)
        x = x[:-cutsample]
        sf.write(sample, x, sr, sf.info(sample).subtype, loopinfo)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <folder>")