import os
import numpy as np
import uvipytest.snd as sf
file = r'/Users/thomaskowalski/Desktop/Big Slow Holy-A-1.wav'

x, sr = sf.read(file)
y = np.zeros(len(x))

loopinfo = sf.get_chunks(file)
print("loop info:", loopinfo)


writepath = r'/Users/thomaskowalski/Desktop'
sf.write(os.path.join(writepath, "test.wav"), y, sr, sf.info(file).subtype, loopinfo=loopinfo)

