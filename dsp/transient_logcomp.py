#%% Trim sample start with onset detection (energy log compression derivative)
# https://www.audiolabs-erlangen.de/content/05-fau/professor/00-mueller/01-students/2011_DriedgerJonathan_TSM_MasterThesis.pdf
# https://www.audiolabs-erlangen.de/resources/MIR/FMP/C3/C3S1_LogCompression.html

import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from copy import deepcopy
import uvipy.sf as sf

plot = False

def binarize(data, threshold):
    bin, index = [], []
    data = np.where(data < threshold, 0, 1)
    for i in range(1, len(data)):
        value = 0
        if (data[i-1] == 0 and data[i] == 1) or (i-1 == 0 and data[i-1] == 1):
            value = 1
            index.append(i-1)
        bin.append(value)
    return bin, index

def spectral_logcomp(x, sr, threshold):
    # index needs to be converted to sample. may affect precision
    # stft config
    nperseg = 512
    window = signal.windows.nuttall(nperseg, sym=False)
    noverlap = int(nperseg * 3/4)

    zxx = signal.stft(x, fs=sr, window=window, noverlap=noverlap, nperseg=nperseg, boundary="constant")[2]

    C = 100
    log = []
    spectral_diff = []
    for i in range(1, len(zxx[0])):
        spectral_diff.append(sum((abs(zxx[:,i]) - abs(zxx[:,i-1]))**2))
        log.append(sum(abs(np.log10(1 + C * zxx[:,i])) - abs(np.log10(1 + C * zxx[:,i-1]))))

    log /= np.amax(np.abs(log))

    diff = np.diff(log)
    diff = np.maximum(diff, 0)
    diff /= np.amax(diff)

    bin, index = binarize(log, threshold)

    if plot:
        plt.figure(); plt.grid()
        plt.plot(diff, c="blue")
        plt.plot(bin, c="red")

# def butter_highpass(cutoff, fs, order=5):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
#     return b, a

# def butter_highpass_filter(data, cutoff, fs, order=5):
#     b, a = butter_highpass(cutoff, fs, order=order)
#     y = signal.filtfilt(b, a, data)
#     return y

def energy_logcomp(x, threshold):
    x /= np.amax(x)

    N = 256
    w = signal.windows.hann(N)
    w /= np.sum(w)

    energy = signal.convolve(x**2, w, mode="same")
    energy /= np.amax(energy)

    C = 100
    log = np.log(1 + C * energy)

    diff = np.diff(log)
    diff = np.maximum(diff, 0)
    diff /= np.amax(diff)
    bin, index = binarize(diff, threshold)

    if plot:
        plt.figure(); plt.grid()
        plt.plot(diff[:44100 // 2], c="blue")
        plt.plot(x[:44100 // 2])
        plt.plot(bin[:44100 // 2], c="red")

    return index[0]

def main(root_samples):
    for sample in sf.browse(root_samples):
        print(os.path.split(sample)[1])
        x, sr = sf.read(sample)
        loopinfo = sf.get_chunks(sample)

        xcopy = deepcopy(x[:,0])
        index = energy_logcomp(xcopy, 0.9)

        finished = False
        if index > sr // 2:
            for threshold in [0.6, 0.5, 0.4, 0.2]:
                index = energy_logcomp(xcopy, threshold)
                if index < sr // 2:
                    finished = True
                    break
        
            if not finished:
                print(">>>>> Needs manual check")
                continue

        if loopinfo[0]:
            loopinfo = (loopinfo[0] - index, loopinfo[1] - index)

        sf.write(sample, x, sr, sf.info(sample).subtype, loopinfo)
        
        print("trim at index:", index, "\n")
        sf.write(sample, x[index:], sr, sf.info(sample).subtype, loopinfo)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <sample folder>")

