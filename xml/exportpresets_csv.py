#%% List all presets as CSV file > doesn't support subfolders (not needed)
# Example:
# Sound Designer/01.05.22/Preset 1.uvip
# Sound Designer/01.05.22/Preset 2.uvip
# Sound Designer/01.05.22/Preset 3.uvip

import os
import re
import csv

def natsorted(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def main(root_presets):
    basepath, foldername = os.path.split(root_presets)
    csvpath = os.path.join(basepath, f'{foldername}.csv')

    data = {}
    for root, _, files in os.walk(root_presets):
        for f in files:
            if not f.endswith(".uvip") or "._" in f: continue
            key = os.path.split(root)[1]
            filename = os.path.splitext(f)[0] 
            if not key in data.keys():
                data[key] = [filename]
            else:
                data[key].append(filename)

    header = ["Delivery Date", "Preset Name"]
    with open(csvpath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for key in natsorted(data.keys()):
            for preset in natsorted(data[key]):
                writer.writerow([key, preset])

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <presets folder>")