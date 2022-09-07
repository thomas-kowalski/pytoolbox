#%% Generate missing samples from velocity/no velocity sample input

import os
import re
import samplerate
from uvipy.midi import *
import uvipy.sf as sf

def get_note_name(filename):
    pattern = "(^|[-_\\s])([a-gA-G][#b]?-?[0-9])($|[-_\\s\.])"
    m = re.search(pattern, filename)
    if m:
        groups = m.groups()
        return groups[1]
    else:
        return None

def note_from_name(name):
    pattern = "([a-gA-G])([#b]?)(-?[0-9]?)"
    note, alt, octave = re.match(pattern, name).groups()
    note = ([9, 11, 0, 2, 4, 5, 7])[(ord(note.upper())-ord('A'))]
    
    if alt == '#': note += 1
    elif alt == 'b': note -= 1
    note += 12 * (2 + int(octave))
    return note

def midi_to_note_name(midi):
    midi = int(midi)
    note = (["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])[midi % 12]
    oct = (midi // 12) - 2
    return note + str(oct)

def pitch_shift(x, semitones):
    ratio = 2 ** (semitones * -1 / 12)
    return samplerate.resample(x, ratio, "sinc_best")

# target_range = (43, 72)
# vel_layers = 3

def main(folder, target_range, vel_layers):
    samples = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".wav"): continue
            samples.append(os.path.join(root, f))

    def get_nearest(note, vel):
        diff = 127; index = 0
        for i in range(len(samples)):
            if not vel: 
                pass
            else:
                if not "v"+str(vel) in samples[i]: continue        

            result = abs(note_from_name(get_note_name(samples[i])) - note)
            if result < diff:
                index = i
                diff = result
        return samples[index]

    for v in range(vel_layers):
        print("--- V"+str(v+1))
        for note in range(target_range[0], target_range[1]+1):
            vel = vel_layers > 1 and v + 1 or None
            nearest = get_nearest(note, vel)
            nearest_note = note_from_name(get_note_name(nearest))
            diff = note-nearest_note

            print(midi_to_note_name(note), ">>", os.path.split(nearest)[1], ">>", diff)
            if diff != 0:
                x, sr = sf.read(nearest)
                x = pitch_shift(x, diff)
                new_fpath = nearest.replace(get_note_name(nearest), midi_to_note_name(note))
                sf.write(new_fpath, x, sr, sf.info(nearest).subtype)  

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 5:
        folder = sys.argv[1]
        target_range = (note_from_name(sys.argv[2]), note_from_name(sys.argv[3]))
        vel_layers = int(sys.argv[4])
        main(folder, target_range, vel_layers)
    else:
        print("usage: python <script> <sample folder> <low note> <high note> <vel layers>")
        print("example: python script folder/ C0 C6 4")
