#%% Trim sample start with onset detection (minimum difference between energy and its derivative)

import os
import uvipy.sf as sf
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def main(folder, threshold, plot=False):
    samples = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".wav"): continue
            samples.append(os.path.join(root, f))

    threshold = 10 ** (threshold / 20)
    for sample in samples:
        if "._" in sample: continue
        print(os.path.split(sample)[1])
        x, sr = sf.read(sample, always_2d=True)

        N = 64
        w = signal.windows.hann(N)
        w /= np.sum(w)

        xseg = x[:len(x)//40,0]
        xenergy = abs(np.convolve(xseg ** 2, w, mode="same"))
        xenergy /= np.amax(xenergy)
        xderiv = abs(np.diff(xenergy))
        xderiv /= np.amax(xderiv)

        xderiv = np.append(xderiv, 0)
        # threshold = 0.002
        index = np.where(xenergy - xderiv >= threshold)[0][0]
        print("threshold:", threshold)
        print("energy/derivative minimum diff index:", index)
        print("-"*20)

        if plot:
            plotmax = 1000
            plt.grid()
            plt.plot(xseg[:plotmax])
            plt.plot(abs(xenergy[:plotmax]), c="red")
            plt.plot(abs(xderiv[:plotmax]), c="black")
            plt.scatter(index, xseg[index], marker="x")
            plt.vlines(index, -1, 1, color="orange")

        x = x[index:]

        loopinfo = sf.get_chunks(sample)
        if loopinfo[0]:
            loopinfo = (loopinfo[0] - index, loopinfo[1] - index)

        sf.write(sample, x, sr, sf.info(sample).subtype, loopinfo)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        main(sys.argv[1], int(sys.argv[2]))
    else:
        print("usage: python <script> <folder> <threshold>")

