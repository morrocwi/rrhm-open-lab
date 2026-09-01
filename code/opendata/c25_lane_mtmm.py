#!/usr/bin/env python3
"""C25 — lane-typing MTMM inequality on IU-Hamburg fear conditioning (Zenodo 5648055).

Preregistered FROZEN before any outcome file was opened (repo commit 6923c0a, prereg v2
E0-B append). Lanes: RAT / SCR / FPS. D = mean(CS+) - mean(CS-) per subject x phase x lane.
C25.1 PRIMARY: mean within-lane ACQ<->EX Spearman  >  mean between-lane same-phase Spearman
              (3 lane pairs x {ACQ, EX}); tie band |diff| < 0.01 = FAIL.
C25.2 SECONDARY: last-4 EX trials, RAT vs SCR D: |r| <= 0.70 AND both discordant
              quadrants >= 15% (median split). Compatibility != validation.
Requires: numpy, scipy. Downloads three long CSVs (~330 KB total).
"""
import csv, os, subprocess, sys
from collections import defaultdict
import numpy as np
from scipy.stats import spearmanr, pearsonr

FILES = {
    "RAT": ("data_RAT_long_iu_hamburg_reading.csv", "rat", "time"),
    "SCR": ("data_SCR_long_iu_hamburg_reading.csv", "scr", "trial"),
    "FPS": ("data_FPS_long_iu_hamburg_reading.csv", "fps", "trial"),
}
BASE = "https://zenodo.org/api/records/5648055/files/{}/content"

def load(lane):
    fname, ycol, tcol = FILES[lane]
    if not os.path.exists(fname):
        subprocess.run(["curl", "-sL", "-o", fname, BASE.format(fname)], check=True)
    rows = defaultdict(list)  # (id, phase, stim) -> [(trial, y)]
    for r in csv.DictReader(open(fname)):
        try:
            y = float(r[ycol])
        except ValueError:
            continue
        rows[(r["id"], r["phase"], r["stimulus"])].append((float(r[tcol]), y))
    return rows

def disc(rows, sid, phase, last_n=None):
    """D = mean(CS+) - mean(CS-); stimulus 1 = CS+, 2 = CS- (readme)."""
    out = []
    for stim in ("1", "2"):
        tv = sorted(rows.get((sid, phase, stim), []))
        if last_n:
            tv = tv[-last_n:]
        if not tv:
            return None
        out.append(np.mean([y for _, y in tv]))
    return out[0] - out[1]

def run():
    data = {lane: load(lane) for lane in FILES}
    ids = sorted({k[0] for lane in data.values() for k in lane})
    lanes, phases = list(FILES), ["ACQ", "EX"]
    D = {}  # (lane, phase) -> {id: D}
    for lane in lanes:
        for ph in phases:
            D[(lane, ph)] = {i: d for i in ids if (d := disc(data[lane], i, ph)) is not None}

    def sp(d1, d2):
        common = sorted(set(d1) & set(d2))
        return spearmanr([d1[i] for i in common], [d2[i] for i in common])[0], len(common)

    within = [sp(D[(l, "ACQ")], D[(l, "EX")]) for l in lanes]
    pairs = [(a, b) for i, a in enumerate(lanes) for b in lanes[i + 1:]]
    between = [sp(D[(a, ph)], D[(b, ph)]) for a, b in pairs for ph in phases]
    w = np.mean([r for r, _ in within]); b = np.mean([r for r, _ in between])
    for l, (r, n) in zip(lanes, within):
        print(f"  within-lane  {l} ACQ<->EX: rho={r:+.3f} (n={n})")
    for (a, bl), _ in zip([(f"{a}-{b}", None) for a, b in pairs for _ in phases], between):
        pass
    k = 0
    for a, bb in pairs:
        for ph in phases:
            r, n = between[k]; k += 1
            print(f"  between-lane {a}~{bb} {ph}: rho={r:+.3f} (n={n})")
    verdict = "PASS" if (w - b) >= 0.01 else "FAIL"
    print(f"C25.1 MTMM: mean within={w:+.3f}  mean between={b:+.3f}  diff={w-b:+.3f} -> {verdict}")

    dr = {i: d for i in ids if (d := disc(data["RAT"], i, "EX", last_n=4)) is not None}
    ds = {i: d for i in ids if (d := disc(data["SCR"], i, "EX", last_n=4)) is not None}
    common = sorted(set(dr) & set(ds))
    x = np.array([dr[i] for i in common]); y = np.array([ds[i] for i in common])
    r = pearsonr(x, y)[0]
    mx, my = np.median(x), np.median(y)
    q1 = np.mean((x > mx) & (y <= my)); q2 = np.mean((x <= mx) & (y > my))
    v2 = "PASS" if (abs(r) <= 0.70 and q1 >= 0.15 and q2 >= 0.15) else "FAIL"
    print(f"C25.2 end-EX RAT vs SCR: n={len(common)} r={r:+.3f} quadrants={q1:.2f}/{q2:.2f} -> {v2}")

if __name__ == "__main__":
    run()
