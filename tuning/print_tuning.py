#%% Print tuning in audio samples from UVIP preset input

import os
import samplerate
import uvipy.sf as sf
import xml.etree.ElementTree as ET

def pitch_shift(x, semitones):
    ratio = 2 ** (semitones * -1 / 12)
    return samplerate.resample(x, ratio, "sinc_best", verbose=True)

def main(preset, root_samples):
    samples = []
    for root, _, files in os.walk(root_samples):
        for f in files:
            if not f.endswith(".wav"): continue
            samples.append(os.path.join(root, f))

    tree = ET.parse(preset); root = tree.getroot()
    for splayer in root.findall(".//SamplePlayer"):
        finetune = int(splayer.attrib["FineTune"])
        samplepath = os.path.join(os.path.split(preset)[0], splayer.attrib["SamplePath"])
        x, sr = sf.read(samplepath)
        print(os.path.split(samplepath)[1], finetune/100)
        x = pitch_shift(x, finetune / 100)

        sf.write(samplepath, x, sr)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("usage: python <script> <tuning preset> <samples folder>")
