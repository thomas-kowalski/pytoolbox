#%% Remove loop

import os
import uvipy.sf as sf

def main(folder):
    for sample in sf.browse(folder):
        print(os.path.split(sample)[1])
        x, sr = sf.read(sample)
        sf.write(sample, x, sr, sf.info(sample).subtype, None)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <folder>")
