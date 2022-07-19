#%% Denoise audio file (noise print is 1 SECOND, taken at the end of each file)
# Optimised for decaying sounds, sustain is not supported

import os
import uvipy.sf as sf
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar
from scipy import signal

def natsorted(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def get_energy(x, win):
    # computes energy
    return np.convolve(x ** 2, win, mode="same")

def dec_exp(coef, size):
    # generates f(x) = e ^ (-a*x) according to size
    return np.exp(1) ** (-coef * np.arange(size))

def norm(x):
    x *= (10 ** (-0.01/20)) / np.amax(abs(x))    
    return x
    
def get_behavior(x):
    #True: decreasing, False: sustained
    segment = x[len(x)//8:len(x)//4]
    verbose = "decreasing"; decreasing = True
    
    win_size = 4096
    win = signal.nuttall(win_size)
    win /= np.sum(win)
    
    energy = get_energy(segment, win)
    energy /= np.amax(energy)

    def get_dist(p):
        if p == 0: p = 1
        exp = dec_exp(p, len(energy))
        return np.sum((energy - exp)**2)
    
    op_coef = minimize_scalar(get_dist).x
    if op_coef < 1e-6:
        verbose = "sustained"; decreasing = False
    print("behavior:", verbose)
    # plt.figure();plt.title("behavior:"+verbose);plt.plot(energy)
    # plt.plot(dec_exp(op_coef, len(energy)))    
    return decreasing
    
def get_psd_peaks(x, sr):
    # computes power spectral density, returns spectral peaks estimation
    x = x[:sr]
    nperseg = 4096 * 2; noverlap = nperseg * 3/4
    psd = signal.welch(x, fs=sr, window=signal.nuttall(nperseg,sym=False), noverlap=noverlap, nperseg=nperseg)[1]
    psd /= np.amax(psd)
    
    peaks = signal.find_peaks(psd, height=0.002)[0]
    return len(peaks)

# not used yet
# if heavy harmonic content + decreasing sound, filter may not be active on attack
def get_energy_decoef(x):
    # decreasing exponential - energy inversed match
    # f(x) = 1 - e ^(-a*x)
    win_size = 1024
    win = signal.nuttall(win_size)
    win /= np.sum(win)

    def get_dist(p):
        if p == 0:p = 1
        exp = dec_exp(p, len(x))
        return np.sum((x - exp)**2) 
    op_coef = minimize_scalar(get_dist).x
    return op_coef

def parametric_dec_exp(coef, size, maximum, minimum):
    curve = (maximum - minimum) * dec_exp(coef, size) + minimum
    return curve 

# stft config
nperseg = 2048
window = signal.nuttall(nperseg, sym=False)
noverlap = int(nperseg * 3/4)

def stft(x, sr):
    return signal.stft(x, fs=sr,window=window,noverlap=noverlap,nperseg=nperseg,boundary="constant")[2]
                       
def istft(zxx, sr):
    return signal.istft(zxx,fs=sr,window=window,noverlap=noverlap,nperseg=nperseg,boundary=True)[1]

def get_padsize(x, sr):
    return len(istft(stft(x, sr), sr))

#####################
sensitivity = 4 # ratio
noise_detection_mode = "welch" #"welch, max"
# db_reduction = 10 ** (-20/20)

# smoothing : 1 - 5 range
horizontal_smoothing = 1
vertical_smoothing = 1
######################
minimum = 2 ** (1 + vertical_smoothing)
maximum = 512

# with exponential curve fit
def dnoise(x, sr,
           xnoise,
           sensitivity, 
           noise_detection_mode, 
           db_reduction, 
           horizontal_smoothing,
           vertical_smoothing):    
    zxx_noise = stft(xnoise, sr) 
    x.resize((get_padsize(x[:,0], sr), x.shape[1]), refcheck=False)
    # get_psd_peaks(x[:,0], sr)
    
    # analyse noise print 
    noise_print = []
    for i in range(len(zxx_noise[:,0])):
        if noise_detection_mode == "welch":
            nw = np.sum(abs(zxx_noise[i]) ** 2) / len(zxx_noise[i])
            rmsn = np.sqrt(nw)
            noise_print.append(rmsn)
        elif noise_detection_mode == "max":
            noise_print.append(np.amax(zxx_noise[i]))
            
    skip = 0
    for ch in range(x.shape[1]):
        zxx = stft(x[:,ch], sr)
        # ---
        # plotfreq = 1520
        # plotbin = plotfreq * ((nperseg / 2) + 1) // (sr // 2)
        # ---
        filt_frames = []
        for i in range(skip, len(zxx[0])):
            filt_response = np.real(np.ones_like(zxx[:,i]))
            for j in range(len(zxx[:,i])):
                if abs(zxx[:,i][j]) / abs(noise_print[j]) < sensitivity: #sensitivity_curve[i]:
                    filt_response[j] = 0
            filt_frames.append(filt_response)
        
        # smooth filter reponse
        filt_win_size = 8
        filt_win = signal.boxcar(filt_win_size)
        
        horizontal_win = signal.hann(2 ** (4 + horizontal_smoothing)) 
        horizontal_win /= np.sum(horizontal_win)
        onepad = np.ones(500)
        
        if vertical_smoothing > 1:
            vertical_smooth_curve = parametric_dec_exp(0.2, len(filt_frames), 1024, 2 ** (1 + vertical_smoothing))
        #    vertical_win = signal.nuttall(2 ** (1 + vertical_smoothing))
        #    vertical_win /= np.sum(vertical_win)
            for i in range(len(filt_frames)):
                vertical_win = signal.nuttall(int(vertical_smooth_curve[i]))
                vertical_win /= np.sum(vertical_win)
                
                filt_frames[i] = np.insert(filt_frames[i], 0, onepad)
                filt_frames[i] = signal.convolve(filt_frames[i], vertical_win, mode="same")
                filt_frames[i] = filt_frames[i][500:]
        
        filt_frames = np.transpose(filt_frames)
        for i in range(len(filt_frames)):
            fftbin = np.minimum(1, signal.convolve(filt_frames[i], filt_win, mode="same"))
            average_size = 10
            for j in range(len(fftbin)//average_size):
                segment = fftbin[j * average_size:(j+1) * average_size]
                if np.sum(segment) / len(segment) < 0.05:
                    fftbin[j * average_size:(j+1) * average_size] = 0
    
            try:
                if np.sum(fftbin) / len(fftbin) > 0.00001:
                    coef = get_energy_decoef(fftbin)
                    index = np.where(fftbin == 0)[0][0]
                    fftbin[index:] = dec_exp(coef, len(fftbin))[index:]
            except:
                pass
            
            fftbin = db_reduction * (fftbin * -1) + db_reduction + fftbin
            filt_frames[i] = fftbin

        # re-iterate stft to apply filter
        filt_frames = np.transpose(filt_frames)

        for i in range(skip, len(zxx[0])):
            zxx[:,i] *= filt_frames[i-skip]
        x[:,ch] = istft(zxx, sr)
    return x

if __name__ == "__main__":
    import sys, re
    if len(sys.argv) == 3:
        finput = sys.argv[1]
        dbreduction = int(sys.argv[2])

        infiles = []
        if not os.path.isdir(finput):
            infiles.append(finput)
        else:
            for root, _, files in os.walk(finput):
                for f in files:
                    if not f.endswith(".wav"): continue
                    infiles.append(os.path.join(root, f))
        
        for fpath in natsorted(infiles):
            f = os.path.split(fpath)[1]
            print("processing....", f)
            x, sr = sf.read(fpath)
            xnoise = x[-(sr//2):,0]

            xdnoise = dnoise(x, sr, xnoise, sensitivity, noise_detection_mode, 10**(dbreduction/20), horizontal_smoothing, vertical_smoothing)
            sf.write(os.path.join(os.path.split(fpath)[0], "_"+f), xdnoise, sr, sf.info(fpath).subtype)
    else:
        print("usage: <python> <script> <file / folder> <db reduction>")