#%% Samples / Presets counter

import os
if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        samples = 0
        presets = 0
        for root, _, files in os.walk(sys.argv[1]):
            for f in files:
                if "._" in f: continue
                if f.endswith(".wav"):
                    samples += 1
                if f.endswith(".uvip") or f.endswith(".M5p"):
                    presets += 1
        print(f'Samples: {samples}')
        print(f'Presets: {presets}')
    else:
        # print("-")
        print("usage: python <script> <base folder>")
