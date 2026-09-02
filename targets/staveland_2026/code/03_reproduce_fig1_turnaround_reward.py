#!/usr/bin/env python3
"""R0-1 — reproduce the paper's Figure-1 turnaround~reward mixed model from the
publisher's own Source Data file (found after the deposit lacked behavioral files).

Source Data: 41467_2026_70287_MOESM4_ESM.xlsx (auto-downloaded from Springer static
content; 34 MB; sheets carry per-figure trial-level data AND the original brms model
summaries, so Original-vs-Reproduced comparison is self-contained).
Original model (sheet 'Turn Distance ~ Reward Size', quoted verbatim):
  distance_to_ghost_at_turn ~ large_reward + (1 + large_reward | subject), Gaussian,
  brms, N=34,298, 211 subjects.
DECLARED DEVIATIONS: (1) engine = statsmodels MixedLM (ML) instead of brms (Bayesian,
default priors) — for a Gaussian model the point estimates are expected to agree closely;
(2) our extracted sheet has 34,609 rows vs the model's 34,298 stated observations
(difference 311, unexplained by us; recorded, not hidden).
Requires: numpy, pandas, statsmodels.
"""
import os
import re
import urllib.request
import warnings
import zipfile
from xml.etree import ElementTree as ET

warnings.filterwarnings("ignore")
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

XLSX = "41467_2026_70287_MOESM4_ESM.xlsx"
URL = ("https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-026-70287-5/"
       "MediaObjects/41467_2026_70287_MOESM4_ESM.xlsx")
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

def fetch():
    if not os.path.exists(XLSX):
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=300) as r, open(XLSX, "wb") as f:
            f.write(r.read())

def sheet_rows(z, shared, sheetfile):
    out = []
    with z.open(f"xl/worksheets/{sheetfile}") as f:
        for _, el in ET.iterparse(f):
            if el.tag == NS + "row":
                vals = []
                for c in el.findall(NS + "c"):
                    v = c.find(NS + "v")
                    vals.append("" if v is None
                                else shared[int(v.text)] if c.get("t") == "s"
                                else v.text)
                out.append(vals)
                el.clear()
    return out

def extract(sheet_name):
    z = zipfile.ZipFile(XLSX)
    shared = ["".join(t.text or "" for t in si.iter(NS + "t"))
              for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(NS + "si")]
    wbx = z.read("xl/workbook.xml").decode()
    rels = z.read("xl/_rels/workbook.xml.rels").decode()
    rid2file = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="worksheets/(sheet\d+\.xml)"',
                               rels))
    name2file = {n: rid2file[r] for n, r in
                 re.findall(r'<sheet name="([^"]+)"[^>]*r:id="(rId\d+)"', wbx)}
    return sheet_rows(z, shared, name2file[sheet_name])

def run():
    fetch()
    rows = extract("figure1_turnaround_reward_plot")
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["last_away"] = pd.to_numeric(df["last_away"], errors="coerce")
    df = df.dropna(subset=["last_away", "large_reward", "subject"])
    df["large_rewardSmall"] = (df["large_reward"] == "Small").astype(float)
    print(f"extracted rows: {len(df)} | subjects: {df['subject'].nunique()}")
    m = smf.mixedlm("last_away ~ large_rewardSmall", df, groups=df["subject"],
                    re_formula="~large_rewardSmall").fit(method="lbfgs", maxiter=300)
    ci = m.conf_int().loc["large_rewardSmall"]
    sd_int = np.sqrt(m.cov_re.iloc[0, 0])
    print("ORIGINAL (brms, from the Source Data model sheet, verbatim):")
    print("  large_rewardSmall = 0.1115 [0.0905, 0.1326]; Intercept = -0.0509; "
          "sd(Intercept) = 0.3841; N = 34,298; 211 subjects")
    print("REPRODUCED (statsmodels MixedLM, declared deviation):")
    print(f"  large_rewardSmall = {m.params['large_rewardSmall']:.4f} "
          f"[{ci[0]:.4f}, {ci[1]:.4f}]; Intercept = {m.params['Intercept']:.4f}; "
          f"sd(Intercept) = {sd_int:.4f}; N = {len(df)}; "
          f"{df['subject'].nunique()} subjects")

if __name__ == "__main__":
    run()
