#!/usr/bin/env python3
"""C30-A — external transport of the M0-vs-M1 comparison to IU-Hamburg (Zenodo 5648055).

Preregistered FROZEN (repo 4d4b013) before any C30 computation; partial contamination
declared cell-by-cell in the prereg. X = (RAT_ACQ, SCR_ACQ, FPS_ACQ, RAT_EX, SCR_EX,
FPS_EX) discrimination scores; M0 one factor (k=12) vs M1 three lane factors (k=15);
frozen BIC bands as in C29; falsifier dBIC <= -2 = M0 wins externally (binding).
C30-B parameter transport: ruled NOT IDENTIFIABLE in the prereg (occasion semantics
differ); declared bottom, not attempted. Requires numpy, scipy; run next to the C25 CSVs.
"""
import csv, os, subprocess
import warnings
warnings.filterwarnings("ignore")
from collections import defaultdict
import numpy as np
from scipy.optimize import minimize

FILES = {
    "RAT": ("data_RAT_long_iu_hamburg_reading.csv", "rat", "time"),
    "SCR": ("data_SCR_long_iu_hamburg_reading.csv", "scr", "trial"),
    "FPS": ("data_FPS_long_iu_hamburg_reading.csv", "fps", "trial"),
}
BASE = "https://zenodo.org/api/records/5648055/files/{}/content"
LANES = ["RAT", "SCR", "FPS"]
PHASES = ["ACQ", "EX"]

def load(lane):
    fname, ycol, _ = FILES[lane]
    if not os.path.exists(fname):
        subprocess.run(["curl", "-sL", "-o", fname, BASE.format(fname)], check=True)
    rows = defaultdict(list)
    for r in csv.DictReader(open(fname)):
        try:
            y = float(r[ycol])
        except ValueError:
            continue
        rows[(r["id"], r["phase"], r["stimulus"])].append(y)
    return rows

def disc(rows, sid, phase):
    out = []
    for stim in ("1", "2"):
        v = rows.get((sid, phase, stim), [])
        if not v:
            return None
        out.append(np.mean(v))
    return out[0] - out[1]

def loglik(S, Sigma, n):
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0:
        return -1e12
    return -0.5 * n * (logdet + np.trace(np.linalg.solve(Sigma, S)))

def sigma_m0(p):
    return np.outer(p[:6], p[:6]) + np.diag(p[6:12])

def sigma_m1(p):
    # variable order: RAT_ACQ, SCR_ACQ, FPS_ACQ, RAT_EX, SCR_EX, FPS_EX
    lam, psi = p[:6], p[6:12]
    r12, r13, r23 = p[12], p[13], p[14]
    L = np.zeros((6, 3))
    for i, lane_idx in enumerate([0, 1, 2, 0, 1, 2]):
        L[i, lane_idx] = lam[i]
    Phi = np.array([[1, r12, r13], [r12, 1, r23], [r13, r23, 1]])
    return L @ Phi @ L.T + np.diag(psi)

def fit(S, n, model, k, seed):
    rng = np.random.default_rng(seed)
    npar = 12 if k == 12 else 15
    bounds = ([(-5, 5)] * 6 + [(0.001, 10)] * 6
              + ([(-0.99, 0.99)] * 3 if k == 15 else []))
    best = None
    for _ in range(20):
        x0 = np.concatenate([rng.uniform(-1, 1, 6), rng.uniform(0.2, 1.0, 6),
                             rng.uniform(-0.5, 0.5, 3) if k == 15 else []])
        r = minimize(lambda p: -loglik(S, model(p), n), x0,
                     method="L-BFGS-B", bounds=bounds)
        if best is None or r.fun < best.fun:
            best = r
    return -best.fun, best.x

def canonical(p):
    lam = p[:6].copy()
    phis = {"RAT-SCR": p[12], "RAT-FPS": p[13], "SCR-FPS": p[14]}
    flips = []
    for lane_idx, acq_pos in enumerate([0, 1, 2]):
        f = -1.0 if lam[acq_pos] < 0 else 1.0
        flips.append(f)
        lam[acq_pos] *= f
        lam[acq_pos + 3] *= f
    phis["RAT-SCR"] *= flips[0] * flips[1]
    phis["RAT-FPS"] *= flips[0] * flips[2]
    phis["SCR-FPS"] *= flips[1] * flips[2]
    return lam, phis

def run():
    data = {lane: load(lane) for lane in LANES}
    ids = sorted({k[0] for lane in data.values() for k in lane})
    X, kept = [], []
    for sid in ids:
        row = []
        for ph in PHASES:
            for lane in LANES:
                d = disc(data[lane], sid, ph)
                row.append(d)
        if all(v is not None for v in row):
            # reorder to RAT_ACQ,SCR_ACQ,FPS_ACQ,RAT_EX,SCR_EX,FPS_EX (already is)
            X.append(row); kept.append(sid)
    X = np.array(X, float)
    n = X.shape[0]
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    S = np.cov(Z, rowvar=False)
    ll0, p0 = fit(S, n, sigma_m0, 12, 20260902)
    ll1, p1 = fit(S, n, sigma_m1, 15, 20260903)
    bic0 = -2 * ll0 + 12 * np.log(n)
    bic1 = -2 * ll1 + 15 * np.log(n)
    d = bic0 - bic1
    band = ("strong M1" if d >= 10 else "weak M1" if d >= 2 else
            "indeterminate" if d > -2 else
            "M0 WINS EXTERNALLY (FAIL for typed-lane transport)")
    lam, phis = canonical(p1)
    print(f"C30-A: n={n} (complete cases, six cells)")
    print(f"  M0 LL={ll0:.2f} BIC={bic0:.2f}")
    print(f"  M1 LL={ll1:.2f} BIC={bic1:.2f}")
    print(f"  dBIC(M0-M1)={d:+.2f} -> {band}")
    print("  canonical loadings ACQ/EX per lane: "
          + "; ".join(f"{lane}=({lam[i]:+.3f},{lam[i+3]:+.3f})"
                      for i, lane in enumerate(LANES)))
    print("  canonical inter-lane phis: "
          + "; ".join(f"{k}={v:+.3f}" for k, v in phis.items()))

if __name__ == "__main__":
    run()
