#%% Detect f0 and apply tuning to XML keygroup "FineTune"/"Coarse" parameters

import os
import re
import numpy as np
from scipy import signal
from uvipy.midi import *
import uvipy.sf as sf
import xml.etree.ElementTree as ET

def uvip_browse(folder):
    uvip = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".uvip") or "._" in f: continue
            uvip.append(os.path.join(root, f))
    return uvip

def get_f0(x, sr,
           minF0=8,
           maxF0=12600,
           threshold=0.1,
           use_lowpass=False,
           use_highpass=True):

    def qint(ym1, y0, yp1):
        p = (yp1 - ym1) / (2 * (2 * y0 - yp1 - ym1))
        y = y0 - 0.25 * (ym1 - yp1) * p
        a = 0.5 * (ym1 - 2 * y0 + yp1)
        return p, y, a

    if use_lowpass:
        fc = maxF0 / float(sr)
        b,a = signal.butter(4, fc, 'low')
        x = signal.lfilter(b, a, x)

    if use_highpass:
        fc = minF0/float(sr)
        b,a = signal.butter(4, fc, 'high')
        x = signal.lfilter(b, a, x)
    
    minPeriod = int(sr / maxF0)
    maxPeriod = int(sr / minF0)
  
    # AMDF
    r = np.zeros(maxPeriod)
    for i in range(0, maxPeriod):
        r[i] = np.sum((x[0:len(x)-maxPeriod] - x[i:len(x)-maxPeriod+i])**2) / (len(x)-maxPeriod)

    C = np.zeros(maxPeriod)
    C[0] = 1
    for i in range(1,maxPeriod):
        C[i] = r[i] * i / np.sum(r[1:i+1])
    r = C
  
    # A find first minimum below threshold
    minimums = np.zeros(maxPeriod)
    below_thres = r[minPeriod:maxPeriod-1] < threshold
    is_minimum = (r[minPeriod:maxPeriod-1] < r[minPeriod-1:maxPeriod-2]) * (r[minPeriod:maxPeriod-1] < r[minPeriod+1:maxPeriod])
    minimums[minPeriod:maxPeriod-1] = below_thres * is_minimum
    I = np.nonzero(minimums)
    
    if(len(I[0]) > 0):
        T = I[0][0]
    else:
        # B if no min, use global minimum
        T = minPeriod + np.argmin(r[minPeriod:maxPeriod])
    
    if (T+1) >= len(r):
        # if still no pitch raise exception
        raise Exception("pitch not found, please increase range")

    p, y, a = qint(r[T-1], r[T], r[T+1])
    T0 = T + p
    f0 = sr / float(T0)
    return f0

def get_pitch(filepath, 
    octave_range=2.0, 
    showCAMDF=True, 
    skip_front=0, 
    use_file_note_name=True,
    fmin=None,
    fmax=None):

    note_name = get_note_name(filepath)
    if note_name is None or not use_file_note_name:
        f_min = 8.0
        f_max = 4000.0
    else:
        note = note_from_name(note_name)
        freq = midi2hz(note)

        # restrict range around theorical pitch to +/- octave_range
        f_min = freq * 2.0**(-octave_range)
        f_max = freq * 2.0**(octave_range)

    f_min = fmin if fmin else f_min
    f_max = fmax if fmax else f_max

    x, sr = sf.read(filepath); x = x[:,0]
    
    if len(x) > sr:
        x = x[:sr]
    else:
        x = x[:len(x)//2]        
    
    f0 = get_f0(x, sr, minF0=f_min, maxF0=f_max)
    midi_pitch = hz2midi(f0)
    note = int(np.floor(midi_pitch + 0.5)) # nearest note
    detune_cents = 100 * (midi_pitch - note)
    note_name = midi_to_note_name(note)
    return note, detune_cents, midi_pitch, f0, note_name

def main(root_presets, root_samples, output_file=True):

    output = ""
    for preset in uvip_browse(root_presets):
        filename = os.path.splitext(os.path.split(preset)[1])[0]
        print(filename)
        output += filename+"\n"

        tree = ET.parse(preset)
        root = tree.getroot()

        for keygroup in root.findall(".//Keygroup"):
            splayer = keygroup.find(".//SamplePlayer")
            samplepath = splayer.attrib["SamplePath"]
            samplepath = os.path.join(root_samples, samplepath.split("Samples/")[1])
            init_midi_note = note_from_name(get_note_name(samplepath))

            fine = 0
            coarse = 0

            try:
                _, detune_cents, _, f0, _ = get_pitch(samplepath)
                measured_note = int(round(hz2midi(f0)))

                fine = detune_cents * -1
                coarse = (init_midi_note % 12) - (measured_note % 12)
                if abs(coarse) == 11:
                    coarse = -1 * np.sign(coarse)
                
                log = f'{os.path.split(samplepath)[1]} > coarse: {coarse}, fine: {fine}'
                print(log)
                output += log+"\n"

            except:
                log = f'!!!!!!!!! {os.path.split(samplepath)[1]} > ERROR, setting coarse and fine to 0 !!!!!!!'
                output += log+"\n"
                print(log)
            
            splayer.attrib["CoarseTune"] = str(coarse)
            splayer.attrib["FineTune"] = str(fine)

        output+="\n"
        print("... writing preset ...")
        tree.write(preset)
        print("\n")

    if output_file:
        with open(os.path.join(os.path.split(root_presets)[0], "TUNING LOG.txt"), "w") as f:
            f.write(output)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("usage: python <script> <preset folder> <sample folder>")