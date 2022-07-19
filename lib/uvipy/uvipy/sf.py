# --------------------------------
# SoundFile with loop support
# --------------------------------
import os
import soundfile as sf

__all__ = [
    "browse",
    "read",
    "get_chunks"
    "write",
]

def browse(folder):
    matches = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".wav") or "._" in f: continue
            matches.append(os.path.join(root, f))
    return matches

def read(filepath):
    return sf.read(filepath, always_2d=True)
    
def get_chunks(filepath):
    loopstart, loopend = 0, 0
    with sf.SoundFileEx(filepath, 'r') as snd:
        try:
            chunk = snd.get_instrument_chunk()
            loopstart = chunk.loops[0][0]
            loopend = chunk.loops[0][1]
        except:
            pass
    return (loopstart, loopend)

def _write_with_chunks(filepath, x, sr, channels, subtype, loopinfo=(0, 0)):
        with sf.SoundFileEx(
            filepath,
            'w',
            samplerate = sr,
            channels = channels,
            subtype = subtype
        ) as snd:
            snd.set_instrument_chunk(loops=[loopinfo])
            snd.write(x)

def info(filepath):
    return sf.info(filepath)

def write(filepath, x, sr, subtype, loopinfo=None):
    channels = 1
    try:
        channels = x.shape[1]
    except:
        pass

    if loopinfo != None:
        _write_with_chunks(filepath, x, sr, channels, subtype, loopinfo)
    else:
        sf.write(filepath, x, sr, subtype=subtype)