#!/usr/bin/env python3
"""Post-review artifact controls for C23 Test B (ordered by independent review,
2026-09-02). Result on execution: (i) with the window extended to 6 s the median
differential peak moved to 5.99 s (16/20 beyond 3.5 s) -- the peak follows the
window edge, so the original 'peak at 3.48 s vs 3.5 s deadline' was a window-edge
argmax artifact and criterion B2 is WITHDRAWN; (ii) label-permutation nulls also
pile at the edge (mean 0.24); (iii) 7/20 differentials are monotone/edge-pinned.
Requires the HRA1 data fetched by c23_hra1_timing.py."""
import numpy as np, scipy.io as sio
SOA = 3.5
def load(i):
    s = f"{i:02d}"
    sp = sio.loadmat(f"hra1/Data/HRA_1_spike_{s}.mat", squeeze_me=True, struct_as_record=False)
    cg = sio.loadmat(f"hra1/Data/HRA_1_cogent_{s}.mat", squeeze_me=True, struct_as_record=False)
    ch = np.atleast_1d(sp["data"])
    return ch[0].data, ch[1].data, float(ch[1].header.sr), cg["data"][:, 1]
def epochs(markers, scr, sr, cs, t_end):
    Ep, Em = [], []
    for k in range(min(len(markers), len(cs))):
        i0, i1 = int((markers[k] - 1.0) * sr), int((markers[k] + t_end) * sr)
        if i0 < 0 or i1 >= len(scr):
            continue
        seg = scr[i0:i1].astype(float)
        e = seg[int(1.0 * sr):] - seg[: int(1.0 * sr)].mean()
        (Ep if cs[k] == 2 else Em).append(e)
    L = min(min(map(len, Ep)), min(map(len, Em)))
    return np.array([x[:L] for x in Ep]), np.array([x[:L] for x in Em])
def run():
    rng = np.random.default_rng(2026)
    peaks_ext, mono, perm_pile = [], [], []
    for i in range(1, 21):
        m, scr, sr, cs = load(i)
        Ep, Em = epochs(m, scr, sr, cs, 6.0)
        d = Ep.mean(0) - Em.mean(0)
        lo = int(0.5 * sr)
        peaks_ext.append(lo / sr + np.argmax(d[lo:]) / sr)
        Ep2, Em2 = epochs(m, scr, sr, cs, SOA)
        d2 = (Ep2.mean(0) - Em2.mean(0))[int(0.5 * sr):]
        ker = np.ones(int(0.3 * sr)) / int(0.3 * sr)
        ds = np.convolve(d2, ker, mode="valid")
        mono.append(bool(np.all(np.diff(ds) > -1e-4)) or np.argmax(d2) == len(d2) - 1)
        labs = cs.copy(); piles = 0; NP = 20
        for _ in range(NP):
            rng.shuffle(labs)
            Epp, Emp = epochs(m, scr, sr, labs, SOA)
            dp = (Epp.mean(0) - Emp.mean(0))[int(0.5 * sr):]
            piles += abs(0.5 + np.argmax(dp) / sr - SOA) <= 0.06
        perm_pile.append(piles / NP)
    peaks_ext = np.array(peaks_ext)
    print(f"(i) extended-window peaks: median={np.median(peaks_ext):.2f}s; beyond 3.5s: {(peaks_ext>3.56).sum()}/20")
    print(f"(iii) monotone/edge-pinned: {sum(mono)}/20")
    print(f"(ii) permutation edge-pileup: {np.mean(perm_pile):.2f}")
if __name__ == "__main__":
    run()
