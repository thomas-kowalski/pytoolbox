#%% Generate layer list as .lua file from sample folder input 

import os
import re

def natsorted(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def main(root_samples):
    folders = []
    for root, dirs, files in os.walk(root_samples):
        if len(dirs) == 0: continue
        for dir in dirs:
            folders.append(os.path.join(root, dir))

    folders = natsorted(folders)
    with open(os.path.join(os.path.split(root_samples)[0], "LayerList.lua"), 'w') as f:
        f.write("layers = {\n")

        for i in range(len(folders)):
            if not os.listdir(folders[i])[0].endswith(".wav"): 
                continue
            
            f.write(f'\t"{folders[i].split("Samples/")[1]}",\n')
        f.write("}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <samples folder>")
