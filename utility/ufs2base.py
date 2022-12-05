#%% Convert UFS UVIP presets to base format (relative path) > may need path customization

import os
import numpy as np
import xml.etree.ElementTree as ET

def ufs2base(presets_folder, ufs_path, contains_ir=False):
    presets = []
    for root, _, files in os.walk(presets_folder):
        for f in files:
            if not f.endswith(".uvip"): continue
            presets.append(os.path.join(root, f))
    
    ufs_name = os.path.splitext(os.path.split(ufs_path)[1])[0]
    for preset in presets:
        if "._" in preset: continue
        print("-"*20)
        print(os.path.splitext(os.path.split(preset)[1])[0])
        print("-"*20)
        tree = ET.parse(preset)
        root = tree.getroot()

        # fix script path
        print("... writing script path ...")
        properties = root.find(".//ScriptProcessor").find(".//Properties")
        try:
            properties.attrib.pop("OriginalProgramPath", None)
        except:
            pass
        stubpath = properties.attrib["ScriptPath"]
        base_stubpath = os.path.join("./../../Scripts/", stubpath.split("Scripts/")[1])
        properties.attrib["ScriptPath"] = base_stubpath
        properties.attrib["PresetPath"] = base_stubpath

        # fix all sample path
        print("... writing sample path ...")
        base_samplepath = "./../../Samples/"
        for splayer in root.findall(".//SamplePlayer"):
            splayer.attrib["SamplePath"] = splayer.attrib["SamplePath"].replace("${0}.ufs/Samples/".format(ufs_name), base_samplepath)
            splayer.attrib["SamplePath"] = splayer.attrib["SamplePath"].replace("${0}.ufs/Scripts/../Samples/".format(ufs_name), base_samplepath)
            splayer.attrib["SamplePath"] = splayer.attrib["SamplePath"].replace("${0}.ufs/Scripts/./../Samples/".format(ufs_name), base_samplepath)
        
        if contains_ir:
            # fix IRs path
            print("... fixing IR path ...")
            base_irpath = "./../../IR/"

            for reverb in (root.findall(".//SampledReverb") + root.findall(".//Convolver")):
                reverb.attrib["SamplePath"] = reverb.attrib["SamplePath"].replace("${0}.ufs/IR/".format(ufs_name), base_irpath)
                reverb.attrib["SamplePath"] = reverb.attrib["SamplePath"].replace("${0}.ufs/Scripts/../IR/".format(ufs_name), base_irpath)
                reverb.attrib["SamplePath"] = reverb.attrib["SamplePath"].replace("${0}.ufs/Scripts/./../IR/".format(ufs_name), base_irpath)
        

        try:
            # remove NeededFS node
            print("... removing NeededFS node ...")
            neededFS = root.find(".//NeededFS")
            root.remove(neededFS)
        except:
            pass

        # write preset
        print("... writing preset ...")
        tree.write(preset)
        print("\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        presets_folder = sys.argv[1]
        ufs_path = sys.argv[2]
        ufs2base(presets_folder, ufs_path)
    else:
        print("usage: python <script> <presets folder> <ufs path>")
