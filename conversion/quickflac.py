#%% Flac files

import os
import sys
from sympy import root
import uvipy.sf as sf

def flac(root_samples):
    cmd = "flac -8 \"{}\" --keep-foreign-metadata --channel-map=none"

    for file in sf.browse(root_samples):
        cmdline = cmd.format(file)
        try:
            os.system(cmdline)
        except OSError as e:
            pass
    
    for file in sf.browse(root_samples):
        if file.endswith(".wav"):
            os.remove(file)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        flac(sys.argv[1])
    else:
    	print("usage: <python> <script> <sample folder>")