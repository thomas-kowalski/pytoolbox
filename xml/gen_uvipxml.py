#%% Generate reduced XML files from presets folder input (cf. backward compatibily between PX SunBox, PXP10, PXV8, etc.)
# cf. loadState/saveState in Falcon

import os
from copy import deepcopy
import xml.etree.ElementTree as ET

def main(source, target):
    presets = []
    for root, _, files in os.walk(source):
        for f in files:
            if not f.endswith(".uvip") or "._" in f: continue
            presets.append(os.path.join(root, f))

    for preset in presets:
        print(os.path.split(preset)[1])
        target_dir = os.path.join(target, os.path.split(os.path.dirname(preset))[1])
        try:
            os.mkdir(target_dir)
        except:
            pass
        
        tree = ET.parse(preset)
        root = tree.getroot()

        event_processor = deepcopy(root.find(".//ScriptProcessor"))
        gen_root = ET.Element("UVI4")
        gen_root.append(event_processor)

        gen_fname = os.path.split(preset)[1].replace(".uvip", ".xml")
        gen_fpath = os.path.join(target_dir, gen_fname)

        gen_tree = ET.ElementTree(gen_root)
        gen_tree.write(gen_fpath)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("usage: python <script> <source folder> <target folder>")