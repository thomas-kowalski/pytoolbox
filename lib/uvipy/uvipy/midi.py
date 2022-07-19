# --------------------------------
# MIDI Utils
# --------------------------------
import re
from math import log

__all__ = [
    "get_note_name",
    "note_from_name",
    "midi_to_note_name",
    "midi2hz",
    "hz2midi",
]

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

def midi2hz(m): 
    return 440.0 * 2**((m - 69) / 12.0)

def hz2midi(f):
    return 69.0 + 12.0 * log(f / 440.0) / log(2)
