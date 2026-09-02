#!/usr/bin/env python3
"""C29 post-scoring audit (ordered by the author, 2026-09-02).

A1. Factor-orientation audit: factor models have sign indeterminacy (F -> -F with
    flipped loadings preserves the likelihood), so phi(acq)=+0.22 vs phi(ext)=-0.31
    is comparable ONLY after canonicalization. Rule (declared): flip each factor so
    its T0 reference loading (RAT_T0 for F_RAT, SCR_T0 for F_SCR) is positive;
    phi transforms by the product of the flips. Report canonical loadings and phi.
A2. Bootstrap exceedance count vs the OBSERVED statistic (same seed/sims as C29):
    conservative tail p_boot = (count(sim dBIC >= observed) + 1) / (sims + 1),
    named a parametric-bootstrap tail probability under fitted M0 — NOT a p-value
    proving M1.
Self-fetches rankStab_R1 RData files from Zenodo into rankstab/ if missing.
"""
import warnings
warnings.filterwarnings("ignore")
import os
import urllib.request
import zipfile
import numpy as np
import pyreadr
from scipy.optimize import minimize

D = "rankstab/rankStab_R1/data/"
OBS = {"acq": 2.50, "ext": 7.83}
ZENODO_URL = "https://zenodo.org/api/records/7323547/files/rankStab_R1.zip/content"
NEEDED = ("rankStab_R1/data/dataRat_RankStab.RData", "rankStab_R1/data/dataSCR_RankStab.RData")

def ensure_data():
    """Self-download+extract rankStab_R1 RData files from Zenodo if missing (fetch/infra only)."""
    if all(os.path.exists(os.path.join("rankstab", n)) for n in NEEDED):
        return
    os.makedirs("rankstab", exist_ok=True)
    zip_path = "rankStab_R1.zip"
    urllib.request.urlretrieve(ZENODO_URL, zip_path)
    with zipfile.ZipFile(zip_path) as zf:
        for member in NEEDED:
            zf.extract(member, "rankstab")

def disc(df, val, phase):
    d = df[(df["phase"].astype(str) == phase)
           & (df["cs"].astype(str).isin(["CS_P", "CS_M"]))].dropna(subset=[val])
    def norm(s):
        try:
            return str(int(float(s)))
        except ValueError:
            return str(s).strip()
    g = d.groupby([d["id"].astype(str).map(norm), d["timepoint"].astype(str),
                   d["cs"].astype(str)])[val].mean().unstack()
    g = g.dropna(subset=["CS_P", "CS_M"])
    out = {}
    for (sid, tp), row in g.iterrows():
        out.setdefault(tp, {})[sid] = row["CS_P"] - row["CS_M"]
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
    Phi = np.array([[1.0, phi], [phi, 1.0]])
    return L @ Phi @ L.T + np.diag(psi)

def fit(S, n, model, k, seed):
    rng = np.random.default_rng(seed)
    best = None
    bounds = [(-5, 5)] * 4 + [(0.001, 10)] * 4 + ([(-0.99, 0.99)] if k == 9 else [])
    for _ in range(20):
        x0 = np.concatenate([rng.uniform(-1, 1, 4), rng.uniform(0.2, 1.0, 4),
                             rng.uniform(-0.5, 0.5, 1) if k == 9 else []])
        r = minimize(lambda p: -loglik(S, model(p), n), x0,
                     method="L-BFGS-B", bounds=bounds)
        if best is None or r.fun < best.fun:
            best = r
    return -best.fun, best.x

def canonical(p1):
    lam = p1[:4].copy(); phi = p1[8]
    if lam[0] < 0:          # flip F_RAT
        lam[0], lam[2], phi = -lam[0], -lam[2], -phi
    if lam[1] < 0:          # flip F_SCR
        lam[1], lam[3], phi = -lam[1], -lam[3], -phi
    return lam, phi

def run():
    ensure_data()
    rat_df = pyreadr.read_r(D + "dataRat_RankStab.RData")["dataRat"]
    scr_df = pyreadr.read_r(D + "dataSCR_RankStab.RData")["dataSCR"]
    for phase in ("acq", "ext"):
        rat = disc(rat_df, "rating", phase)
        scr = disc(scr_df, "log.rc.ampl", phase)
        ids = sorted(set(rat.get("T0", {})) & set(rat.get("T1", {}))
                     & set(scr.get("T0", {})) & set(scr.get("T1", {})))
        X = np.array([[rat["T0"][i], scr["T0"][i], rat["T1"][i], scr["T1"][i]]
                      for i in ids])
        n = X.shape[0]
        Z = (X - X.mean(0)) / X.std(0, ddof=1)
        S = np.cov(Z, rowvar=False)
        ll0, p0 = fit(S, n, sigma_m0, 8, 20260902)
        ll1, p1 = fit(S, n, sigma_m1, 9, 20260903)
        lam, phi = canonical(p1)
        print(f"A1 {phase}: raw phi={p1[8]:+.3f}; canonical loadings "
              f"RAT=({lam[0]:+.3f},{lam[2]:+.3f}) SCR=({lam[1]:+.3f},{lam[3]:+.3f}) "
              f"-> canonical phi={phi:+.3f}")
        rng = np.random.default_rng(20260902)
        Sig0 = sigma_m0(p0)
        exceed = 0; sims = 500
        for i in range(sims):
            Xs = rng.multivariate_normal(np.zeros(4), Sig0, n)
            Ss = np.cov((Xs - Xs.mean(0)) / Xs.std(0, ddof=1), rowvar=False)
            l0, _ = fit(Ss, n, sigma_m0, 8, 20260902 + 7 * i + 1)
            l1, _ = fit(Ss, n, sigma_m1, 9, 20260902 + 7 * i + 2)
            d = (-2 * l0 + 8 * np.log(n)) - (-2 * l1 + 9 * np.log(n))
            if d >= OBS[phase]:
                exceed += 1
        print(f"A2 {phase}: sims >= observed ({OBS[phase]:+.2f}): {exceed}/{sims}; "
              f"p_boot = {(exceed + 1) / (sims + 1):.4f} "
              f"(parametric-bootstrap tail under fitted M0)")

if __name__ == "__main__":
    run()
