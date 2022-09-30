#%% Check unused sample from UVIP presets

import os
import shutil
import xml.etree.ElementTree as ET

def browse(folder, ext):
    matches = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(ext) or "._" in f: continue
            matches.append(os.path.join(root, f))
    return matches

def main(presets_folder, samples_folder):
    presets = browse(presets_folder, ".uvip")
    samples = browse(samples_folder, ".wav")

    used = []
    for p in presets:
        tree = ET.parse(p)
        root = tree.getroot()
        for splayer in root.findall(".//SamplePlayer"):
            file = os.path.split(splayer.attrib["SamplePath"])[1]
            if not file in used:
                used.append(file)

    unused_folder = os.path.join(os.path.split(samples_folder)[0], "_Unused Samples")
    try:
        os.mkdir(unused_folder)
    except:
        pass

    for s in samples:
        filename = os.path.split(s)[1]
        if not filename in used:
            # move to unused folder
            print(f'moving {filename} to unused folder')
            shutil.move(s, os.path.join(unused_folder, filename))

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("usage: python <script> <presets folder> <samples folder>")
