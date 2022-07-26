#%% Extracts tuning from UVIP presets to a table in a LUA file 

import os
from uvipy.midi import *
import xml.etree.ElementTree as ET

def get_nearest(note, mapping):
    diff = 127; index = 0
    for n in range(len(mapping)):
        result = abs(mapping[n] - note)
        if result < diff:
            index = n
            diff = result
    return mapping[index]

def uvip_browse(folder):
    matches = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".uvip") or "._" in f: continue
            matches.append(os.path.join(root, f))
    return matches

def extract_tuning(folder):
    f = open(os.path.join(os.path.split(folder)[0], "LayerTunings.lua"), 'w')
    f.write("LayerTunings = {}\n\n")

    for preset in uvip_browse(folder):
        if "._" in preset:
            continue
        print(os.path.splitext(os.path.split(preset)[1])[0])
        f.write("LayerTunings[\""+os.path.splitext(os.path.split(preset)[1])[0]+"\"] = { ")
        tree = ET.parse(preset)
        root = tree.getroot()

        tuninginfos = {}
        for keygroup in root.findall(".//Keygroup"):
            splayer = keygroup.find(".//SamplePlayer")
            basenote = int(splayer.attrib["BaseNote"])
            print(midi_to_note_name(basenote))
            tunevalue = int(splayer.attrib["CoarseTune"]) + float(splayer.attrib["FineTune"]) / 100.
            tuninginfos[basenote] = tunevalue
        
        tuningtable = ""
        for i in range(1, 127 + 1):
            value = 0
            if i not in tuninginfos.keys():
                value = tuninginfos[get_nearest(i, list(tuninginfos.keys()))]
            else:
                value = tuninginfos[i]
            tuningtable += str(value)+", "
        f.write(tuningtable[:-2]+" }\n")

    f.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        extract_tuning(sys.argv[1])
    else:
        print("usage: python <script> <preset folder>")


