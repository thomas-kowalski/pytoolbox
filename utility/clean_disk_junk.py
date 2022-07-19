#%% Remove "._" bullshit files 

import os
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        for root, _, files in os.walk(sys.argv[1]):
            for f in files:
                if not "._" in f: continue
                os.remove(os.path.join(root, f))
    else:
        print("usage: python <script> <folder>")