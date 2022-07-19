#%% Generate missing samples from velocity/RR sample input

import os
import re
import samplerate
import soundfile as sf
from uvipy.midi import *
import uvipy.sf as sf

def pitch_shift(x, semitones):
    ratio = 2 ** (semitones * -1 / 12)
    return samplerate.resample(x, ratio, "sinc_best")

def main(root_samples, target_range, vel_layers, numrr):
    samples = sf.browse(root_samples)
    basepath = os.path.split(samples[0])[0]
    template_samplename = os.path.split(samples[0])[1].split(get_note_name(samples[0]))[0][:-1]

    for v in range(vel_layers):
        print("--- V"+str(v+1))
        for note in range(target_range[0], target_range[1]+1):
            for rr in range(numrr):
                rrindex = rr + 1
                suffix = f'{midi_to_note_name(note)}-v{v+1}-rr0{rrindex}'
                filename = f'{template_samplename}-{suffix}.wav'
                filepath = os.path.join(basepath, filename)

                if not filepath in samples:
                    found = False
                    direction = 1
                    _rr = 0
                    offset = 1
                    while not found:
                        new_suffix = f'{midi_to_note_name(note + offset * direction)}-v{v+1}-rr0{(rr + _rr) % numrr + 1}'
                        new_filename = f'{template_samplename}-{new_suffix}.wav'
                        new_filepath = os.path.join(basepath, new_filename)
                        if new_filepath not in samples:
                            if _rr < numrr:
                                _rr += 1
                            else:
                                _rr = 0
                                if direction == -1:
                                    direction = 1
                                    offset += 1
                                else:
                                    direction = -1
                        else:
                            print("repitch", new_filename, "to", filename, "with offset", offset * -direction)                            
                            x, sr = sf.read(new_filepath, always_2d=True)
                            x = pitch_shift(x, offset * -direction)
                            sf.write(filepath, x, sr, subtype=sf.info(new_filepath).subtype)
                            found = True

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 6:
        folder = sys.argv[1]
        target_range = (note_from_name(sys.argv[2]), note_from_name(sys.argv[3]))
        vel_layers = int(sys.argv[4])
        numrr = int(sys.argv[5])
        main(folder, target_range, vel_layers, numrr)
    else:
        print("usage: python <script> <sample folder> <low note> <high note> <vel layers> <num rr>")
        print("example: python script folder/ C0 C6 4 3")
