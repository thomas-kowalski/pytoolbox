#%% Flac files

import os
import sys
import uvipy.sf as sf

def flac(root_samples):
    cmd = "flac -8 \"{}\" --keep-foreign-metadata --channel-map=none"

    for file in sf.browse(root_samples):
        cmdline = cmd.format(file)
        try:
            os.system(cmdline)
        except OSError as e:
            pass
    
    # clean old wav files
    for file in sf.browse(root_samples):
        if file.endswith(".wav"):
            os.remove(file)

    # rename flac > wav
    for file in sf.browse(root_samples):
        if file.endswith(".flac"):
            os.rename(file, file.replace(".flac", ".wav"))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        flac(sys.argv[1])
    else:
    	print("usage: <python> <script> <sample folder>")