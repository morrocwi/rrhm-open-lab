#!/usr/bin/env python3
"""ANNEX C31.2w — within-cohort four-cell computation on ROFL (Zenodo 21472062).

NOT C31.2: same Hamburg cohort as rankStab, so this carries NO external-adjudication
weight (freeze ed48027). Readouts: split-half reliability per lane per occasion,
within-lane persistence, and the C29 4-variable M0-vs-M1 BIC verdict.
Requires numpy, scipy, pyreadr; run next to rofl/ extract.
Self-fetches rofl/data/ (Zenodo 21472062) if missing.
"""
import os, urllib.request, zipfile, io
import warnings
warnings.filterwarnings("ignore")
from collections import defaultdict
import numpy as np
import pyreadr
from scipy.optimize import minimize
from scipy.stats import spearmanr

D = "rofl/data/"

def _ensure_data():
    rat = D + "dataRat.RData"
    scr = D + "dataSCR.RData"
    if os.path.exists(rat) and os.path.exists(scr):
        return
    url = ("https://zenodo.org/api/records/21472062/files/"
           "ROFL_project_Klingelhoefer-Jens_et_al.zip/content")
    buf = io.BytesIO()
    with urllib.request.urlopen(url) as r:
        buf.write(r.read())
    buf.seek(0)
    with zipfile.ZipFile(buf) as zf:
        members = [m for m in zf.namelist()
                   if m.endswith("data/dataRat.RData") or m.endswith("data/dataSCR.RData")]
        os.makedirs(D, exist_ok=True)
        for m in members:
            with zf.open(m) as src, open(D + os.path.basename(m), "wb") as dst:
                dst.write(src.read())

def load(fname, key, val):
    df = pyreadr.read_r(D + fname)[key]
    d = df[(df["phase"].astype(str) == "acq")
           & (df["cs"].astype(str).isin(["CS_P", "CS_M"]))].dropna(subset=[val])
    def norm(s):
        try:
            return str(int(float(s)))
        except ValueError:
            return str(s).strip()
    out = defaultdict(list)
    for _, r in d.iterrows():
        out[(norm(r["id"]), str(r["timepoint"]), str(r["cs"]))].append(float(r[val]))
    return out

def split_half(trials):
    rel = {}
    for occ in ("T0", "T1"):
        d_odd, d_even = {}, {}
        for sid in {k[0] for k in trials if k[1] == occ}:
            p = trials.get((sid, occ, "CS_P"), [])
            m = trials.get((sid, occ, "CS_M"), [])
            if len(p) < 4 or len(m) < 4:
                continue
            d_odd[sid] = np.mean(p[::2]) - np.mean(m[::2])
            d_even[sid] = np.mean(p[1::2]) - np.mean(m[1::2])
        common = sorted(set(d_odd) & set(d_even))
        if len(common) < 10:
            rel[occ] = np.nan
            continue
        r = spearmanr([d_odd[i] for i in common], [d_even[i] for i in common])[0]
        rel[occ] = 2 * r / (1 + r) if r > -1 else np.nan
    return rel

def disc_map(trials):
    out = {}
    for (sid, occ, _), _v in trials.items():
        p = trials.get((sid, occ, "CS_P"), [])
        m = trials.get((sid, occ, "CS_M"), [])
        if p and m:
            out.setdefault(occ, {})[sid] = np.mean(p) - np.mean(m)
    return out

def loglik(S, Sigma, n):
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0:
        return -1e12
    return -0.5 * n * (logdet + np.trace(np.linalg.solve(Sigma, S)))

def sigma_m0(p):
    return np.outer(p[:4], p[:4]) + np.diag(p[4:8])

def sigma_m1(p):
    lam, psi, phi = p[:4], p[4:8], p[8]
    L = np.zeros((4, 2))
    L[0, 0], L[2, 0] = lam[0], lam[2]
    L[1, 1], L[3, 1] = lam[1], lam[3]
    return L @ np.array([[1, phi], [phi, 1]]) @ L.T + np.diag(psi)

def fit(S, n, model, k, seed):
    rng = np.random.default_rng(seed)
    bounds = [(-5, 5)] * 4 + [(0.001, 10)] * 4 + ([(-0.99, 0.99)] if k == 9 else [])
    best = None
    for _ in range(20):
        x0 = np.concatenate([rng.uniform(-1, 1, 4), rng.uniform(0.2, 1.0, 4),
                             rng.uniform(-0.5, 0.5, 1) if k == 9 else []])
        r = minimize(lambda p: -loglik(S, model(p), n), x0,
                     method="L-BFGS-B", bounds=bounds)
        if best is None or r.fun < best.fun:
            best = r
    return -best.fun

def run():
    _ensure_data()
    rat = load("dataRat.RData", "dataRat", "rating")
    scr = load("dataSCR.RData", "dataSCR", "log.rc.ampl")
    rel_rat, rel_scr = split_half(rat), split_half(scr)
    print(f"reliability (SB split-half of D): RAT {rel_rat}  SCR {rel_scr}")
    dr, ds = disc_map(rat), disc_map(scr)
    for lane, dd in (("RAT", dr), ("SCR", ds)):
        c = sorted(set(dd.get("T0", {})) & set(dd.get("T1", {})))
        rho = spearmanr([dd["T0"][i] for i in c], [dd["T1"][i] for i in c])[0]
        print(f"persistence {lane} T0<->T1: rho={rho:+.3f} (n={len(c)})")
    ids = sorted(set(dr.get("T0", {})) & set(dr.get("T1", {}))
                 & set(ds.get("T0", {})) & set(ds.get("T1", {})))
    X = np.array([[dr["T0"][i], ds["T0"][i], dr["T1"][i], ds["T1"][i]] for i in ids])
    n = X.shape[0]
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    S = np.cov(Z, rowvar=False)
    ll0 = fit(S, n, sigma_m0, 8, 20260902)
    ll1 = fit(S, n, sigma_m1, 9, 20260903)
    d = (-2 * ll0 + 8 * np.log(n)) - (-2 * ll1 + 9 * np.log(n))
    band = ("strong M1" if d >= 10 else "weak M1" if d >= 2 else
            "indeterminate" if d > -2 else "M0 preferred")
    print(f"model verdict: n={n} dBIC(M0-M1)={d:+.2f} -> {band}")

if __name__ == "__main__":
    run()
