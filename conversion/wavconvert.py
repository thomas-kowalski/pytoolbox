#%% flac to wav conversion. all files needs to have .flac extension
# use auto_rename flag to rename wav > flac automatically
# NOT ROBUST for mixed wav/flac folders. using soundfile incapability of reading flac files for format detection.

import os
import subprocess
import uvipy.sf as sf

def flac_browse(folder):
    matches = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".flac") or "._" in f: continue
            matches.append(os.path.join(root, f))
    return matches

def main(root_samples, auto_rename=True, remove=True):
    if auto_rename:
        for root, _, files in os.walk(root_samples):
            for f in files:
                if not f.endswith(".wav") or "._" in f: continue
                path = os.path.join(root, f)
                os.rename(path, path.replace(".wav", ".flac"))

    for sample in flac_browse(root_samples):
        iswav = False
        try:
            _, _ = sf.read(sample)
            print(os.path.split(sample)[1], "is WAV format")
            iswav = True
        except:
            pass

        fixed_path = ""
        for i in range(len(sample)):
            char = sample[i]
            if char in [" ", "(", ")"]:
                fixed_path += "\\"
            fixed_path += char

        if iswav:
            os.rename(sample, sample.replace(".flac", ".wav"))
        else:
            try:
                subprocess.check_output(f'flac -d --keep-foreign-metadata {fixed_path}', shell=True)
            except:
                subprocess.check_output(f'flac -d {fixed_path}', shell=True) 

            if remove:
                os.remove(sample)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <samples folder>")
