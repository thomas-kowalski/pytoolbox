#%% 44.1 kHz - 16 bits conversion (requires SOX)

import os
import uvipy.sf as sf

def main(root_samples):
    for sample in sf.browse(root_samples):
        print(os.path.split(sample)[1])
        x, sr = sf.read(sample)

        loopinfo = list(sf.get_chunks(sample))    
        for i in range(len(loopinfo)):
            loopinfo[i] //= (sr // 44100)
        loopinfo = tuple(loopinfo)

        newpath = os.path.join(os.path.split(sample)[0], f'_{os.path.split(sample)[1]}')
        cmd = f'sox "{sample}" -b 16 "{newpath}" gain -1 rate 44100 dither -s -f gesemann'

        try:
            os.system(cmd)
        except:
            pass

        os.remove(sample)
        os.rename(newpath, sample)

        x, sr = sf.read(sample)
        sf.write(sample, x, sr, sf.info(sample).subtype, loopinfo)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <samples folder>")

