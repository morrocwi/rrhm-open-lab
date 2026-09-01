#!/usr/bin/env python3
"""C27 — predictability and the clamp (Zenodo 18713991, GUNT freezing/action-prep).

Preregistered FROZEN (repo 6923c0a conceptual criteria; b203bbd structure-only mapping)
before any outcome value was computed. Cue `blink`: black.PNG = predictable threat,
blue.PNG = unpredictable threat, yellow.PNG = safety. Window = 1-s bins 1..8 (bin 0
baseline-adjacent, bin 9 avatar-adjacent; no window edge touches the tested feature).
C27.1a tonic freezing unpredictable > predictable; C27.1b gradient steeper under
predictable; C27.2 lane dissociation of the per-subject U-effect (cardiac vs SCL).
Compatibility != validation. Requires: numpy, scipy, pyreadr; run next to the
extracted FreezingActionPrep_RevII/data/ directory.
"""
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import pyreadr
from scipy.stats import pearsonr, binomtest

D = "FreezingActionPrep_RevII/data/"
PRED, UNPRED = "black.PNG", "blue.PNG"
BINS = list(range(1, 9))

def bin_means(df, val, bincol):
    """subject -> condition -> {bin: mean of trial-level values}"""
    out = {}
    g = df.groupby(["ID", "blink", bincol])[val].mean()
    for (sid, cond, b), v in g.items():
        out.setdefault(sid, {}).setdefault(cond, {})[int(b)] = v
    return out

def tonic_and_slope(bm):
    ton, slp = {}, {}
    for sid, conds in bm.items():
        t, s = {}, {}
        for cond in (PRED, UNPRED):
            xs = [b for b in BINS if b in conds.get(cond, {})]
            if len(xs) < 6:
                break
            ys = [conds[cond][b] for b in xs]
            t[cond] = float(np.mean(ys))
            s[cond] = float(np.polyfit(xs, ys, 1)[0])
        else:
            ton[sid], slp[sid] = t, s
    return ton, slp

def report_direction(name, per_sub, better):
    """better(u, p) -> True if subject ordered per RRHM prediction."""
    flags = [better(v[UNPRED], v[PRED]) for v in per_sub.values()]
    n, k = len(flags), sum(flags)
    gm_u = np.mean([v[UNPRED] for v in per_sub.values()])
    gm_p = np.mean([v[PRED] for v in per_sub.values()])
    rev = binomtest(n - k, n, 0.5, alternative="greater").pvalue < 0.05
    print(f"  {name}: n={n} group means U={gm_u:+.4f} P={gm_p:+.4f} "
          f"majority={k}/{n} ({k/n:.0%}) reversed_sig={rev}")
    return gm_u, gm_p, k / n > 0.5, rev

def run():
    # cardiac: log.ibi baseline-corrected by trial bin-0 mean
    ibi = pyreadr.read_r(D + "df_ibi.Rdata")["df_ibi"]
    ibi = ibi.dropna(subset=["log.ibi", "timebins1s", "blink"])
    ibi["timebins1s"] = ibi["timebins1s"].astype(float)
    ibi["blink"] = ibi["blink"].astype(str)
    ibi["ID"] = ibi["ID"].astype(str).map(lambda s: str(int(float(s))))
    base = ibi[ibi["timebins1s"] == 0].groupby(["ID", "trialnr"])["log.ibi"].mean()
    ibi = ibi.join(base.rename("b0"), on=["ID", "trialnr"])
    ibi = ibi.dropna(subset=["b0"])
    ibi["ibi_bc"] = ibi["log.ibi"] - ibi["b0"]
    # 9-s trials only: trial must reach bin 8
    mx = ibi.groupby(["ID", "trialnr"])["timebins1s"].max()
    ibi = ibi.join(mx.rename("mxb"), on=["ID", "trialnr"])
    ibi = ibi[ibi["mxb"] >= 8]
    bm_hr = bin_means(ibi, "ibi_bc", "timebins1s")
    ton_hr, slp_hr = tonic_and_slope(bm_hr)

    # sway: per-trial per-bin SD of COPYbpbc; bin = floor(current_time - coreTrialStart)
    sw = pyreadr.read_r(D + "df_anticip.Rdata")["df_anticip"]
    sw = sw.dropna(subset=["COPYbpbc", "blink", "coreTrialStart"])
    sw["blink"] = sw["blink"].astype(str)
    # coreTrialStart is the running sample clock; elapsed = clock - trial minimum
    t0 = sw.groupby(["ID", "trialnr"])["coreTrialStart"].min()
    sw = sw.join(t0.rename("t0"), on=["ID", "trialnr"])
    sw["bin"] = np.floor(sw["coreTrialStart"] - sw["t0"])
    sw = sw[(sw["bin"] >= 0) & (sw["bin"] <= 9)]
    mxs = sw.groupby(["ID", "trialnr"])["bin"].max()
    sw = sw.join(mxs.rename("mxb"), on=["ID", "trialnr"])
    sw = sw[sw["mxb"] >= 8]
    tb = sw.groupby(["ID", "blink", "trialnr", "bin"])["COPYbpbc"].std().rename("sdcop")
    tb = tb.reset_index()
    bm_sw = bin_means(tb, "sdcop", "bin")
    ton_sw, slp_sw = tonic_and_slope(bm_sw)

    print("C27.1a tonic freezing (RRHM: unpredictable > predictable):")
    _, _, maj_hr, rev_hr = report_direction(
        "cardiac IBI_bc (freeze = higher)", ton_hr, lambda u, p: u > p)
    _, _, maj_sw, rev_sw = report_direction(
        "sway SD (freeze = lower)      ", ton_sw, lambda u, p: u < p)
    gm_hr_ok = np.mean([v[UNPRED] - v[PRED] for v in ton_hr.values()]) > 0
    gm_sw_ok = np.mean([v[UNPRED] - v[PRED] for v in ton_sw.values()]) < 0
    ok1a = ((gm_hr_ok and maj_hr and not rev_sw) or (gm_sw_ok and maj_sw and not rev_hr))
    print(f"C27.1a -> {'PASS' if ok1a else 'FAIL'}")

    print("C27.1b gradient (RRHM: predictable steeper toward threat):")
    _, _, maj_hs, rev_hs = report_direction(
        "cardiac slope (steeper = more positive under P)", slp_hr,
        lambda u, p: p > u)
    _, _, maj_ss, rev_ss = report_direction(
        "sway slope (steeper = more negative under P)   ", slp_sw,
        lambda u, p: p < u)
    gm_hs_ok = np.mean([v[PRED] - v[UNPRED] for v in slp_hr.values()]) > 0
    gm_ss_ok = np.mean([v[PRED] - v[UNPRED] for v in slp_sw.values()]) < 0
    ok1b = ((gm_hs_ok and maj_hs and not rev_ss) or (gm_ss_ok and maj_ss and not rev_hs))
    print(f"C27.1b -> {'PASS' if ok1b else 'FAIL'}")

    # SCL lane for C27.2
    scl = pyreadr.read_r(D + "df.filtered.Rdata")["df.filtered"]
    scl = scl.dropna(subset=["log.rc.scl", "second", "blink"])
    scl["blink"] = scl["blink"].astype(str)
    scl["ID"] = scl["ID"].astype(str).map(lambda s: str(int(float(s))))
    scl["second"] = scl["second"].astype(float)
    bm_sc = bin_means(scl[(scl["second"] >= 1) & (scl["second"] <= 8)],
                      "log.rc.scl", "second")
    ton_sc, _ = tonic_and_slope(bm_sc)
    u_hr = {s: v[UNPRED] - v[PRED] for s, v in ton_hr.items()}
    u_sc = {s: v[UNPRED] - v[PRED] for s, v in ton_sc.items()}
    common = sorted(set(u_hr) & set(u_sc))
    x = np.array([u_hr[s] for s in common]); y = np.array([u_sc[s] for s in common])
    r = pearsonr(x, y)[0]
    mx_, my_ = np.median(x), np.median(y)
    q1 = np.mean((x > mx_) & (y <= my_)); q2 = np.mean((x <= mx_) & (y > my_))
    ok2 = abs(r) <= 0.70 and q1 >= 0.15 and q2 >= 0.15
    print(f"C27.2 U-effect cardiac~SCL: n={len(common)} r={r:+.3f} "
          f"quadrants={q1:.2f}/{q2:.2f} -> {'PASS' if ok2 else 'FAIL'}")

if __name__ == "__main__":
    run()
