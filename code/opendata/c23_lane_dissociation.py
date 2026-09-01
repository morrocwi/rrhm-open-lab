#!/usr/bin/env python3
"""C23 Test A — lane dissociation on the VR-spider open dataset (Zenodo 20796399).

Preregistered (frozen before data access, see prereg/RRHM_compatibility_audit_
preregistration_v2.md case C23): (1) |r|(mean SUDS, physiological reactivity) <= 0.70;
(2) both discordant quadrants >= 15% by median split.
Downloads only summary.csv (~33 KB) from the 468 MB archive.
Compatibility != validation. Requires: numpy, requests (or curl fallback).
"""
import csv, io, os, subprocess, sys
import numpy as np

URL = "https://zenodo.org/api/records/20796399/files/vr_spider_dataset.zip/content"
CACHE = "vr_spider_summary.csv"

def get_summary():
    if os.path.exists(CACHE):
        return open(CACHE).read()
    # stream the zip and extract summary.csv only (it sits at the end of the archive)
    zpath = "vr_spider_dataset.zip"
    if not os.path.exists(zpath):
        print("downloading dataset zip (468 MB) from Zenodo...", file=sys.stderr)
        subprocess.run(["curl", "-sL", "-o", zpath, URL], check=True)
    import zipfile
    with zipfile.ZipFile(zpath) as z:
        data = z.read("summary.csv").decode()
    open(CACHE, "w").write(data)
    return data

def f(x):
    try:
        return float(x)
    except Exception:
        return np.nan

def run():
    rows = list(csv.DictReader(io.StringIO(get_summary())))
    subj, cortR, hrR = [], [], []
    for r in rows:
        suds = [f(r.get(f"suds_{i}", "")) for i in range(1, 12)]
        subj.append(np.nanmean(suds) if not all(np.isnan(suds)) else np.nan)
        cortR.append(f(r.get("cort_3", "")) - f(r.get("cort_2", "")))
        hrR.append(f(r.get("PPG_HR_delta", "")) if r.get("PPG_HR_delta") else np.nan)
    subj, cortR, hrR = map(np.array, (subj, cortR, hrR))
    for b, label in ((cortR, "cortisol reactivity (cort3-cort2)"), (hrR, "PPG HR delta")):
        m = ~(np.isnan(subj) | np.isnan(b))
        r = np.corrcoef(subj[m], b[m])[0, 1]
        qa, qb = np.median(subj[m]), np.median(b[m])
        q1 = np.mean((subj[m] > qa) & (b[m] <= qb))
        q2 = np.mean((subj[m] <= qa) & (b[m] > qb))
        crit = "PASS" if (abs(r) <= 0.70 and q1 >= 0.15 and q2 >= 0.15) else "FAIL"
        print(f"SUDS vs {label}: n={m.sum()} r={r:.3f} quadrants={q1:.2f}/{q2:.2f} -> {crit}")

if __name__ == "__main__":
    run()
