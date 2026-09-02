#!/usr/bin/env python3
"""C26 — cross-context lane-dissociation transport (Zenodo 4973029, Giles et al.).

Preregistered FROZEN before the xlsx was opened (repo commit 6923c0a, prereg v2 E0-B append).
Crossover: each subject does TSST (Trier), cold pressor (CP), mental arithmetic (Math), Control.
Frozen precedence resolved on first structure view (recorded): PANAS-NA absent -> mood lane =
POMS TotalMood disturbance; reactivity for every lane = peak of post samples - first (baseline)
sample; stress observations pooled over the three stress tasks (subject x task rows), Control
excluded. C26.1 mood~cortisol, C26.2 mood~HR: PASS iff |r| <= 0.70 AND both discordant
quadrants >= 15%. Compatibility != validation. Requires: numpy, scipy, openpyxl.
"""
import os, subprocess
import numpy as np
from scipy.stats import pearsonr
import openpyxl

URL = "https://zenodo.org/api/records/4973029/files/Giles_PLOS_Data.xlsx/content"
F = "giles.xlsx"

def sheet_dict(ws):
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:] if r[0] is not None]

def react(row, cols):
    vals = [row.get(c) for c in cols]
    if any(v is None for v in vals):
        return None
    base, post = float(vals[0]), [float(v) for v in vals[1:]]
    return max(post) - base

def run():
    if not os.path.exists(F):
        subprocess.run(["curl", "-sL", "-o", F, URL], check=True)
    wb = openpyxl.load_workbook(F, read_only=True)
    poms = {r["Participant"]: r for r in sheet_dict(wb["POMS"])}
    hr = {r["Participant"]: r for r in sheet_dict(wb["HR"])}
    cort = {r["Subject"]: r for r in sheet_dict(wb["Cort"])}

    # column stems per stress task, per sheet (Control excluded per prereg)
    tasks = {
        "TSST": (["TotalMood.Trier.%d" % i for i in (1, 2, 3, 4)],
                 ["Trier.%d.00" % i for i in (1, 2, 3, 4)],
                 ["T%d" % i for i in (1, 2, 3, 4, 5)]),
        "SECPT": (["TotalMood.CP.%d" % i for i in (1, 2, 3, 4)],
                  ["Coldpres.%d.00" % i for i in (1, 2, 3, 4)],
                  ["CP%d" % i for i in (1, 2, 3, 4, 5)]),
        "MAT": (["TotalMood.Math.%d" % i for i in (1, 2, 3, 4)],
                ["Math.%d.00" % i for i in (1, 2, 3, 4)],
                ["M%d" % i for i in (1, 2, 3, 4, 5)]),
    }
    mood_v, cort_v, hr_v = [], [], []
    for task, (mc, cc, hc) in tasks.items():
        for pid in poms:
            m = react(poms[pid], mc)
            c = react(cort.get(pid, {}), cc) if pid in cort else None
            h = react(hr.get(pid, {}), hc) if pid in hr else None
            mood_v.append(m); cort_v.append(c); hr_v.append(h)
    mood_v = np.array([np.nan if v is None else v for v in mood_v], float)
    for other, label, tag in ((cort_v, "cortisol", "C26.1"), (hr_v, "HR", "C26.2")):
        o = np.array([np.nan if v is None else v for v in other], float)
        m = ~(np.isnan(mood_v) | np.isnan(o))
        x, y = mood_v[m], o[m]
        r = pearsonr(x, y)[0]
        mx, my = np.median(x), np.median(y)
        q1 = np.mean((x > mx) & (y <= my)); q2 = np.mean((x <= mx) & (y > my))
        v = "PASS" if (abs(r) <= 0.70 and q1 >= 0.15 and q2 >= 0.15) else "FAIL"
        print(f"{tag} mood~{label}: n(obs)={m.sum()} r={r:+.3f} quadrants={q1:.2f}/{q2:.2f} -> {v}")
    print("note: observations = subject x stress-task (3 per subject, crossover; "
          "non-independence disclosed, pooled per frozen rule)")

if __name__ == "__main__":
    run()
