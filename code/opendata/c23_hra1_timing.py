#!/usr/bin/env python3
"""C23 Test B — temporal-readout structure in PsPM-HRA1 (Zenodo 321641).

Preregistered (frozen; prereg v2 case C23): (1) CS+ > CS- anticipatory SCR amplitude;
(2) differential timing structured within the 3.5 s CS-US window.
Frozen pipeline (reported in the manuscript with its habituation-pooling limitation;
no post-hoc reanalysis): window 0.5-3.5 s post-CS, 1 s baseline, all 20 subjects,
all trials pooled. Requires: numpy, scipy. Downloads Data.zip (33 MB).
"""
import os, subprocess
import numpy as np
import scipy.io as sio

URL = "https://zenodo.org/api/records/321641/files/Data.zip/content"
SOA = 3.5

def fetch():
    if not os.path.isdir("hra1"):
        subprocess.run(["curl", "-sL", "-o", "hra1.zip", URL], check=True)
        subprocess.run(["unzip", "-q", "hra1.zip", "-d", "hra1"], check=True)

def run():
    fetch()
    diffs, peaks = [], []
    for i in range(1, 21):
        s = f"{i:02d}"
        sp = sio.loadmat(f"hra1/Data/HRA_1_spike_{s}.mat", squeeze_me=True, struct_as_record=False)
        cg = sio.loadmat(f"hra1/Data/HRA_1_cogent_{s}.mat", squeeze_me=True, struct_as_record=False)
        chans = np.atleast_1d(sp["data"])
        markers, scr, sr = chans[0].data, chans[1].data, float(chans[1].header.sr)
        cs = cg["data"][:, 1]  # 1 CS-, 2 CS+
        def epoch(onset):
            i0, i1 = int((onset - 1.0) * sr), int((onset + SOA) * sr)
            if i0 < 0 or i1 >= len(scr):
                return None
            seg = scr[i0:i1].astype(float)
            return seg[int(1.0 * sr):] - seg[: int(1.0 * sr)].mean()
        Ep, Em = [], []
        for k in range(min(len(markers), len(cs))):
            e = epoch(markers[k])
            if e is not None:
                (Ep if cs[k] == 2 else Em).append(e)
        L = min(min(map(len, Ep)), min(map(len, Em)))
        Ep = np.array([x[:L] for x in Ep]); Em = np.array([x[:L] for x in Em])
        d = Ep.mean(0) - Em.mean(0)
        diffs.append(Ep.mean(0)[int(0.5 * sr):].mean() - Em.mean(0)[int(0.5 * sr):].mean())
        peaks.append(np.argmax(d) / sr)
    diffs, peaks = np.array(diffs), np.array(peaks)
    t = diffs.mean() / (diffs.std(ddof=1) / np.sqrt(len(diffs)))
    print(f"CS+ minus CS- amplitude: mean={diffs.mean():.4f}, t={t:.2f}, positive {int((diffs>0).sum())}/20")
    print(f"differential peak latency: median={np.median(peaks):.2f}s (deadline 3.5s); within 0.06s of deadline: {int((abs(peaks-3.5)<=0.06).sum())}/20")

if __name__ == "__main__":
    run()
