#!/usr/bin/env python3
"""C29 — formal model comparison M0 (one-scalar latent) vs M1 (two-lane) on rankStab.

Preregistered FROZEN (repo 5c5d810) before any C29 computation. C29.1 acquisition =
QUANTIFICATION-ONLY (contaminated by C28's revealed correlations, no confirmatory weight);
C29.2 extinction = SEMI-BLIND (discrimination never previously computed here).
M0: X_i = lambda_i * F + eps_i (k=8). M1: lane factors F_RAT, F_SCR, corr phi (k=9).
Wishart ML on the sample covariance; BIC decision rule frozen in the prereg.
Requires numpy, scipy, pyreadr; run next to rankstab/ extract.
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pyreadr
from scipy.optimize import minimize

D = "rankstab/rankStab_R1/data/"
PHASES = {"C29.1 (acq, QUANTIFICATION-ONLY/contaminated)": "acq",
          "C29.2 (ext, SEMI-BLIND)": "ext"}

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
    """Wishart log-likelihood of sample cov S under model cov Sigma (up to const)."""
    sign, logdet = np.linalg.slogdet(Sigma)
    if sign <= 0:
        return -1e12
    return -0.5 * n * (logdet + np.trace(np.linalg.solve(Sigma, S)))

def sigma_m0(p):
    lam = p[:4]; psi = p[4:8]
    return np.outer(lam, lam) + np.diag(psi)

def sigma_m1(p):
    lam = p[:4]; psi = p[4:8]; phi = p[8]
    # order: RAT_T0, SCR_T0, RAT_T1, SCR_T1 ; RAT factor loads idx 0,2 ; SCR idx 1,3
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

def compare(X, label, seed):
    n = X.shape[0]
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    S = np.cov(Z, rowvar=False)
    ll0, p0 = fit(S, n, sigma_m0, 8, seed)
    ll1, p1 = fit(S, n, sigma_m1, 9, seed + 1)
    bic0 = -2 * ll0 + 8 * np.log(n)
    bic1 = -2 * ll1 + 9 * np.log(n)
    aic0, aic1 = -2 * ll0 + 16, -2 * ll1 + 18
    d = bic0 - bic1
    band = ("strong M1" if d >= 10 else "weak M1" if d >= 2 else
            "indeterminate" if d > -2 else "M0 preferred (AGAINST typed lanes)")
    print(f"{label}: n={n}")
    print(f"  M0 LL={ll0:.2f} BIC={bic0:.2f} AIC={aic0:.2f}")
    print(f"  M1 LL={ll1:.2f} BIC={bic1:.2f} AIC={aic1:.2f} phi={p1[8]:+.3f}")
    print(f"  dBIC(M0-M1)={d:+.2f} -> {band}")
    return S, n, p0, d

def boot_m0(S, n, p0, seed, sims=500):
    """parametric bootstrap of dBIC under fitted M0 (calibration readout)."""
    rng = np.random.default_rng(seed)
    Sig0 = sigma_m0(p0)
    ds = []
    for i in range(sims):
        Xs = rng.multivariate_normal(np.zeros(4), Sig0, n)
        Ss = np.cov((Xs - Xs.mean(0)) / Xs.std(0, ddof=1), rowvar=False)
        l0, _ = fit(Ss, n, sigma_m0, 8, seed + 7 * i + 1)
        l1, _ = fit(Ss, n, sigma_m1, 9, seed + 7 * i + 2)
        ds.append((-2 * l0 + 8 * np.log(n)) - (-2 * l1 + 9 * np.log(n)))
    ds = np.array(ds)
    print(f"  bootstrap under M0: dBIC median={np.median(ds):+.2f}, "
          f"95th pct={np.percentile(ds, 95):+.2f}, P(dBIC>=10)={np.mean(ds >= 10):.3f}")

def run():
    rat_df = pyreadr.read_r(D + "dataRat_RankStab.RData")["dataRat"]
    scr_df = pyreadr.read_r(D + "dataSCR_RankStab.RData")["dataSCR"]
    for label, phase in PHASES.items():
        rat = disc(rat_df, "rating", phase)
        scr = disc(scr_df, "log.rc.ampl", phase)
        ids = sorted(set(rat.get("T0", {})) & set(rat.get("T1", {}))
                     & set(scr.get("T0", {})) & set(scr.get("T1", {})))
        X = np.array([[rat["T0"][i], scr["T0"][i], rat["T1"][i], scr["T1"][i]]
                      for i in ids])
        S, n, p0, d = compare(X, label, seed=20260902)
        boot_m0(S, n, p0, seed=20260902, sims=500)

if __name__ == "__main__":
    run()
