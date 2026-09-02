#!/usr/bin/env python3
"""C28 sensitivity analyses (labeled EXPLORATORY; the frozen primary result is untouched).

Ordered by the author after C28 scoring (2026-09-02):
S1. Common-sample check: all four correlations recomputed on the complete-case
    subsample (participants with RAT_T0, SCR_T0, RAT_T1, SCR_T1 all present),
    removing sample-composition differences between cells.
S2. Participant bootstrap (10,000 resamples, fixed seed) of
    delta_r = mean(within-lane 6-month rho) - mean(between-lane same-day rho)
    on the complete-case subsample, reported as a percentile 95% CI.
NOTE: the six-month correlations are test-retest stabilities that include true
change; they are NOT pure reliability coefficients and must not be used to
disattenuate the cross-lane correlations.
Requires numpy, scipy, pyreadr; auto-downloads rankstab/ extract from Zenodo if missing.
"""
import os
import urllib.request
import warnings
import zipfile
warnings.filterwarnings("ignore")
import numpy as np
import pyreadr
from scipy.stats import spearmanr

D = "rankstab/rankStab_R1/data/"

ZENODO_URL = "https://zenodo.org/api/records/7323547/files/rankStab_R1.zip/content"
ZENODO_ZIP = "rankStab_R1.zip"
NEEDED_MEMBERS = [
    "rankStab_R1/data/dataRat_RankStab.RData",
    "rankStab_R1/data/dataSCR_RankStab.RData",
]

def _ensure_data():
    """Download and extract the two required RData files into rankstab/ if missing."""
    targets = [os.path.join("rankstab", m) for m in NEEDED_MEMBERS]
    if all(os.path.exists(t) for t in targets):
        return
    os.makedirs("rankstab", exist_ok=True)
    if not os.path.exists(ZENODO_ZIP):
        urllib.request.urlretrieve(ZENODO_URL, ZENODO_ZIP)
    with zipfile.ZipFile(ZENODO_ZIP) as zf:
        for member in NEEDED_MEMBERS:
            zf.extract(member, "rankstab")

def disc(df, val):
    d = df[(df["phase"].astype(str) == "acq")
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

def run():
    _ensure_data()
    rat = disc(pyreadr.read_r(D + "dataRat_RankStab.RData")["dataRat"], "rating")
    scr = disc(pyreadr.read_r(D + "dataSCR_RankStab.RData")["dataSCR"], "log.rc.ampl")
    ids = sorted(set(rat["T0"]) & set(rat["T1"]) & set(scr["T0"]) & set(scr["T1"]))
    n = len(ids)
    M = np.array([[rat["T0"][i], rat["T1"][i], scr["T0"][i], scr["T1"][i]]
                  for i in ids])  # columns: rT0 rT1 sT0 sT1

    def cors(A):
        w1 = spearmanr(A[:, 0], A[:, 1])[0]  # RAT T0-T1
        w2 = spearmanr(A[:, 2], A[:, 3])[0]  # SCR T0-T1
        b1 = spearmanr(A[:, 0], A[:, 2])[0]  # RAT~SCR T0
        b2 = spearmanr(A[:, 1], A[:, 3])[0]  # RAT~SCR T1
        return w1, w2, b1, b2

    w1, w2, b1, b2 = cors(M)
    print(f"S1 complete-case (n={n}):")
    print(f"  within RAT {w1:+.3f}  within SCR {w2:+.3f}  "
          f"between T0 {b1:+.3f}  between T1 {b2:+.3f}")
    d0 = (w1 + w2) / 2 - (b1 + b2) / 2
    print(f"  delta_r = {d0:+.3f}")

    rng = np.random.default_rng(20260902)
    boots = []
    for _ in range(10000):
        A = M[rng.integers(0, n, n)]
        try:
            a, b, c, d = cors(A)
            boots.append((a + b) / 2 - (c + d) / 2)
        except Exception:
            continue
    lo, hi = np.percentile(boots, [2.5, 97.5])
    print(f"S2 bootstrap delta_r 95% CI: [{lo:+.3f}, {hi:+.3f}] "
          f"(10,000 resamples, seed fixed; CI excludes 0: {lo > 0})")

if __name__ == "__main__":
    run()
