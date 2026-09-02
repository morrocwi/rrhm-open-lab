#!/usr/bin/env python3
"""C28 — six-month longitudinal MTMM lane typing on rankStab (Zenodo 7323547).

Preregistered FROZEN (repo 84f55a7 criteria / 1fa0d4d mapping) before outcome computation.
Lanes: RAT (fear rating), SCR (log.rc.ampl). D = mean(CS_P) - mean(CS_M), acquisition,
per subject x timepoint (T0, T1 six months apart).
C28.1: mean within-lane T0<->T1 Spearman > mean between-lane same-timepoint Spearman
       (PASS if diff >= +0.01).
C28.2: RAT~SCR Pearson at EACH timepoint: |r| <= 0.70 AND both discordant quadrants >= 15%.
C28.3: rho_RAT(T0,T1) - rho_SCR(T0,T1) >= +0.10.
Compatibility != validation. Requires numpy, scipy, pyreadr; run next to rankstab/ extract
(auto-downloaded from Zenodo record 7323547 on first run if missing).
"""
import os
import urllib.request
import warnings
import zipfile

warnings.filterwarnings("ignore")
import numpy as np
import pyreadr
from scipy.stats import spearmanr, pearsonr

D = "rankstab/rankStab_R1/data/"

ZENODO_URL = "https://zenodo.org/api/records/7323547/files/rankStab_R1.zip/content"
_NEEDED = ("dataRat_RankStab.RData", "dataSCR_RankStab.RData")

def ensure_data():
    """Download + extract the two RData files into rankstab/rankStab_R1/data/ if missing."""
    if all(os.path.exists(D + f) for f in _NEEDED):
        return
    zip_path = "rankStab_R1.zip"
    if not os.path.exists(zip_path):
        urllib.request.urlretrieve(ZENODO_URL, zip_path)
    members = [f"rankStab_R1/data/{f}" for f in _NEEDED]
    with zipfile.ZipFile(zip_path) as zf:
        for m in members:
            zf.extract(m, "rankstab")

def disc(df, val):
    """(id, timepoint) -> D over acq trials."""
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

def sp(d1, d2):
    c = sorted(set(d1) & set(d2))
    return spearmanr([d1[i] for i in c], [d2[i] for i in c])[0], len(c)

def run():
    ensure_data()
    rat = disc(pyreadr.read_r(D + "dataRat_RankStab.RData")["dataRat"], "rating")
    scr = disc(pyreadr.read_r(D + "dataSCR_RankStab.RData")["dataSCR"], "log.rc.ampl")

    w_rat, n1 = sp(rat["T0"], rat["T1"])
    w_scr, n2 = sp(scr["T0"], scr["T1"])
    b_t0, n3 = sp(rat["T0"], scr["T0"])
    b_t1, n4 = sp(rat["T1"], scr["T1"])
    print(f"  within RAT T0<->T1: rho={w_rat:+.3f} (n={n1})")
    print(f"  within SCR T0<->T1: rho={w_scr:+.3f} (n={n2})")
    print(f"  between RAT~SCR T0: rho={b_t0:+.3f} (n={n3})")
    print(f"  between RAT~SCR T1: rho={b_t1:+.3f} (n={n4})")
    w, b = np.mean([w_rat, w_scr]), np.mean([b_t0, b_t1])
    print(f"C28.1 MTMM: within={w:+.3f} between={b:+.3f} diff={w-b:+.3f} -> "
          f"{'PASS' if (w - b) >= 0.01 else 'FAIL'}")

    for tp in ("T0", "T1"):
        c = sorted(set(rat[tp]) & set(scr[tp]))
        x = np.array([rat[tp][i] for i in c]); y = np.array([scr[tp][i] for i in c])
        r = pearsonr(x, y)[0]
        mx, my = np.median(x), np.median(y)
        q1 = np.mean((x > mx) & (y <= my)); q2 = np.mean((x <= mx) & (y > my))
        ok = abs(r) <= 0.70 and q1 >= 0.15 and q2 >= 0.15
        print(f"C28.2 {tp}: n={len(c)} r={r:+.3f} quadrants={q1:.2f}/{q2:.2f} -> "
              f"{'PASS' if ok else 'FAIL'}")

    print(f"C28.3 stability ordering: RAT {w_rat:+.3f} - SCR {w_scr:+.3f} = "
          f"{w_rat - w_scr:+.3f} -> {'PASS' if (w_rat - w_scr) >= 0.10 else 'FAIL'}")

if __name__ == "__main__":
    run()
