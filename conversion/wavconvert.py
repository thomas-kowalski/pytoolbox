#%% flac to wav conversion. all files needs to have .flac extension
# NOT ROBUST for mixed wav/flac folders. using soundfile incapability of reading flac file for format detection.

import os
import uvipy.sf as sf

def flac_browse(folder):
    matches = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".flac"): continue
            matches.append(os.path.join(root, f))
    return matches

def cmd_execute(cmd):
    try:
        os.system(cmd)
    except OSError as e:
        pass

def main(root_samples):
    for sample in flac_browse(root_samples):
        iswav = False
        try:
            _, _ = sf.read(sample)
            iswav = True
        except:
            pass

        if iswav:
            os.rename(sample, sample.replace(".flac", ".wav"))
        else:
            space = "\ "
            cmd = f'flac -d --keep-foreign-metadata "{sample.replace(" ", space)}"'
            cmd_execute(cmd)
            os.remove(sample)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <samples folder>")
