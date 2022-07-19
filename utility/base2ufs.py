#%% Convert XML presets from base to UFS format 

import os
import xml.etree.ElementTree as ET

def base2ufs(presets_folder, ufs_path, contains_ir=True):
    presets = []
    for root, _, files in os.walk(presets_folder):
        for f in files:
            if not f.endswith(".uvip"): continue
            presets.append(os.path.join(root, f))
    
    ufs_name = os.path.splitext(os.path.split(ufs_path)[1])[0]
    for preset in presets:
        print("-"*20)
        print(os.path.splitext(os.path.split(preset)[1])[0])
        print("-"*20 )
        tree = ET.parse(preset)
        root = tree.getroot()

        try:
            # fix script path
            properties = root.find(".//ScriptProcessor").find(".//Properties")
            stubpath = properties.attrib["ScriptPath"]
            ufs_stubpath = os.path.join("${0}.ufs/Script/".format(ufs_name), stubpath.split("Script/")[1])
            properties.attrib["PresetPath"] = ufs_stubpath
            properties.attrib["ScriptPath"] = ufs_stubpath
        except:
            continue
        print("... writing script path ...")

        # fix all sample path
        print("... writing sample path ...")
        ufs_samplepath = "${0}.ufs/Samples/".format(ufs_name)
        for splayer in root.findall(".//SamplePlayer"):
            splayer.attrib["SamplePath"] = splayer.attrib["SamplePath"].replace("./../../../../Samples/", ufs_samplepath)
            splayer.attrib["SamplePath"] = splayer.attrib["SamplePath"].replace("./../../../../Script/../Samples/", ufs_samplepath)

        if contains_ir:
            # fix IRs path
            print("... fixing IR path ...")
            ufs_irpath = "${0}.ufs/IR/".format(ufs_name)
            for reverb in root.findall(".//SampledReverb"):
                reverb.attrib["SamplePath"] = reverb.attrib["SamplePath"].replace("./../../../../Script/../IR/", ufs_irpath)
                reverb.attrib["SamplePath"] = reverb.attrib["SamplePath"].replace("./../../../../IR/", ufs_irpath)

        # add NeededFS node
        print("... writing NeededFS node ...")
        neededFS = ET.Element("NeededFS")
        neededFS.attrib["Source"] = ufs_path
        root.append(neededFS)

        # write preset
        print("... writing uvip ...")
        tree.write(preset)
        print("\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        presets_folder = sys.argv[1]
        ufs_path = sys.argv[2]
        base2ufs(presets_folder, ufs_path)
    else:
        print("usage: python <script> <presets folder> <ufs path>")
