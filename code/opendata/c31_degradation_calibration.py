#!/usr/bin/env python3
"""C31.1 — degradation calibration on rankStab (freeze 88576db). CALIBRATION, not
independent confirmation: the dataset was already seen (C28/C29).

Question: does degrading rankStab's measurement reliability to IU-Hamburg's level flip
the M0-vs-M1 verdict from M1 to M0 by itself (H_M viable), or not (toward H_A)?
Frozen: split-half (odd/even trials, Spearman-Brown) reliability metric; grid
f ∈ {1.0,0.5,0.25} × noise m ∈ {0,1,2,4}; 100 reps/cell; base seed 20260902;
5 restarts per fit; readouts and interpretation rule in the prereg.
Requires numpy, scipy, pyreadr; run next to rankstab/ extract and the C25 CSVs.
"""
import csv, os
import warnings
warnings.filterwarnings("ignore")
from collections import defaultdict
import numpy as np
import pyreadr
from scipy.optimize import minimize
from scipy.stats import spearmanr

RD = "rankstab/rankStab_R1/data/"

# ---------- trial-level loaders ----------
def load_rankstab(val_file, val):
    df = pyreadr.read_r(RD + val_file[0])[val_file[1]]
    d = df[(df["phase"].astype(str) == "acq")
           & (df["cs"].astype(str).isin(["CS_P", "CS_M"]))].dropna(subset=[val])
    def norm(s):
        try:
            return str(int(float(s)))
        except ValueError:
            return str(s).strip()
    out = defaultdict(list)  # (id, tp, cs) -> [values in trial order]
    for _, r in d.iterrows():
        out[(norm(r["id"]), str(r["timepoint"]), str(r["cs"]))].append(float(r[val]))
    return out

def load_hamburg(fname, ycol):
    out = defaultdict(list)
    for r in csv.DictReader(open(fname)):
        try:
            y = float(r[ycol])
        except ValueError:
            continue
        if r["phase"] in ("ACQ", "EX"):
            out[(r["id"], r["phase"], r["stimulus"])].append(y)
    return out

# ---------- split-half reliability of D ----------
def split_half(trials, occasions, plus_key, minus_key):
    """trials: (id, occ, cs)->list; returns dict occ -> SB reliability."""
    rel = {}
    for occ in occasions:
        d_odd, d_even = {}, {}
        ids = {k[0] for k in trials if k[1] == occ}
        for sid in ids:
            p = trials.get((sid, occ, plus_key), [])
            m = trials.get((sid, occ, minus_key), [])
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

# ---------- M0/M1 machinery (as C29, 5 restarts) ----------
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

def fit(S, n, model, k, rng):
    best = None
    bounds = [(-5, 5)] * 4 + [(0.001, 10)] * 4 + ([(-0.99, 0.99)] if k == 9 else [])
    for _ in range(5):
        x0 = np.concatenate([rng.uniform(-1, 1, 4), rng.uniform(0.2, 1.0, 4),
                             rng.uniform(-0.5, 0.5, 1) if k == 9 else []])
        r = minimize(lambda p: -loglik(S, model(p), n), x0,
                     method="L-BFGS-B", bounds=bounds)
        if best is None or r.fun < best.fun:
            best = r
    return -best.fun

def dbic(X, rng):
    n = X.shape[0]
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    S = np.cov(Z, rowvar=False)
    ll0 = fit(S, n, sigma_m0, 8, rng)
    ll1 = fit(S, n, sigma_m1, 9, rng)
    return (-2 * ll0 + 8 * np.log(n)) - (-2 * ll1 + 9 * np.log(n))

def degrade(trials, f, m, rng):
    out = {}
    for k, v in trials.items():
        v = np.array(v, float)
        if f < 1.0:
            keep = min(len(v), max(1, int(round(len(v) * f))))
            idx = np.sort(rng.choice(len(v), keep, replace=False))
            v = v[idx]
        if m > 0:
            sd = v.std(ddof=1) if len(v) > 1 else 1.0
            v = v + rng.normal(0, m * sd, len(v))
        out[k] = list(v)
    return out

def make_X(rat, scr):
    ids = sorted({k[0] for k in rat} & {k[0] for k in scr})
    rows = []
    for sid in ids:
        vals = []
        for tp in ("T0", "T1"):
            for tr, lane in ((rat, "r"), (scr, "s")):
                p = tr.get((sid, tp, "CS_P"), [])
                mn = tr.get((sid, tp, "CS_M"), [])
                vals.append(np.mean(p) - np.mean(mn) if p and mn else None)
        if all(v is not None for v in vals):
            # order RAT_T0, SCR_T0, RAT_T1, SCR_T1
            rows.append([vals[0], vals[1], vals[2], vals[3]])
    return np.array(rows, float)

def run():
    rat = load_rankstab(("dataRat_RankStab.RData", "dataRat"), "rating")
    scr = load_rankstab(("dataSCR_RankStab.RData", "dataSCR"), "log.rc.ampl")
    h_rat = load_hamburg("data_RAT_long_iu_hamburg_reading.csv", "rat")
    h_scr = load_hamburg("data_SCR_long_iu_hamburg_reading.csv", "scr")

    rel_rs_rat = split_half(rat, ["T0", "T1"], "CS_P", "CS_M")
    rel_rs_scr = split_half(scr, ["T0", "T1"], "CS_P", "CS_M")
    rel_h_rat = split_half(h_rat, ["ACQ", "EX"], "1", "2")
    rel_h_scr = split_half(h_scr, ["ACQ", "EX"], "1", "2")
    print("split-half (Spearman-Brown) reliabilities of D:")
    print(f"  rankStab   RAT {rel_rs_rat}  SCR {rel_rs_scr}")
    print(f"  IU-Hamburg RAT {rel_h_rat}  SCR {rel_h_scr}")
    target_scr = np.nanmean(list(rel_h_scr.values()))
    print(f"  matching target (IU-Hamburg SCR mean): {target_scr:.3f}")

    base_rng = np.random.default_rng(20260902)
    X0 = make_X(rat, scr)
    d0 = dbic(X0, base_rng)
    print(f"intact rankStab dBIC (5-restart pipeline): {d0:+.2f} (n={X0.shape[0]})")

    print("cell: f, m | mean SCR-lane reliability | mean dBIC | P(dBIC<=-2) [100 reps]")
    results = {}
    for f in (1.0, 0.5, 0.25):
        for m in (0, 1, 2, 4):
            if f == 1.0 and m == 0:
                continue
            ds, rels = [], []
            for rep in range(100):
                rng = np.random.default_rng(20260902 + 1000 * rep + int(f * 100) + m)
                scr_d = degrade(scr, f, m, rng)
                rat_d = degrade(rat, f, m, rng)
                rel = split_half(scr_d, ["T0", "T1"], "CS_P", "CS_M")
                rels.append(np.nanmean(list(rel.values())))
                X = make_X(rat_d, scr_d)
                if X.shape[0] >= 30:
                    ds.append(dbic(X, rng))
            ds = np.array(ds)
            key = (f, m)
            results[key] = (np.nanmean(rels), ds.mean(), np.mean(ds <= -2))
            print(f"  f={f} m={m} | rel={results[key][0]:.3f} | "
                  f"dBIC={results[key][1]:+.2f} | P(<=-2)={results[key][2]:.2f}")
    # frozen readout: cells at or below the IU-Hamburg SCR reliability target
    matched = {k: v for k, v in results.items() if v[0] <= target_scr}
    if matched:
        best = min(matched.items(), key=lambda kv: abs(kv[1][0] - target_scr))
        (f, m), (rel, md, p) = best
        verdict = ("H_M viable" if p >= 0.5 else
                   "toward H_A" if p <= 0.1 else "indeterminate")
        print(f"FROZEN READOUT: matched cell f={f} m={m} rel={rel:.3f} "
              f"mean dBIC={md:+.2f} P(dBIC<=-2)={p:.2f} -> {verdict}")
    else:
        print("FROZEN READOUT: no grid cell reached the IU-Hamburg SCR reliability "
              "target -> recorded as grid-insufficient (not scored)")

if __name__ == "__main__":
    run()
