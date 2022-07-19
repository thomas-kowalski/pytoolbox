#%% Convert UVIP files to ZIP 

import os
import shutil

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        allfiles = []
        for root, _, files in os.walk(sys.argv[1]):
            for f in files:
                if not f.endswith(".uvip") or "._" in f: continue
                allfiles.append(os.path.join(root, f))

        for file in allfiles:
            print("creating zip file - ", os.path.split(file)[1])
            shutil.make_archive(file, "zip", os.path.split(file)[0], os.path.split(file)[1])
            os.remove(file)
            os.rename(f'{file}.zip', f'{file.replace(".zip", "")}')
    else:
        print("usage: python <script> <preset folder>")

