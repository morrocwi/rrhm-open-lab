"""RRHM gate battery -- the four remaining simulable gates: K3, K6, K8, K9.

Independent re-implementation (S8) of the ADM/hazard machinery specified in
'Why We Phobia?' v8 (Eq. 4 hazard, additive PRHC, probes at 0.3/1.0 s,
dt = 0.1 s, censoring at 15 s). The original S1 engine (rrhm_engine.py) was
not available in this environment; every construct below follows the
manuscript's stated spec, and simplifications are declared per gate.
Planning tier: numbers are properties of a design against a toy generative
model, never evidence about phobia. Python 3 + NumPy/SciPy, seeds fixed.
"""
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit

rng_global = np.random.default_rng(20260901)
DT, TMAX = 0.1, 15.0
PROBE_TIMES = (0.3, 1.0)

# ---------------------------------------------------------------- simulator
def sim_trials(rng, D, n_trials, b0, b1, delta=0.0, clock=1.0, tau_corr=0.5,
               report_sd=0.4):
    """Simulate one subject's trials at deadline D.
    Additive horizon bias `delta` (PRHC: eRRH_hat = D - t - delta) or clock
    gain `clock` (eRRH_hat = D - clock*t). Returns transition times (censored
    at TMAX -> np.nan) and probe reports at PROBE_TIMES (only from trials
    still running, as in the manuscript's survivorship discussion)."""
    ts = np.arange(0.0, TMAX, DT)                       # (S,)
    noise = rng.normal(0, 0.3, n_trials)                # per-trial estimate noise
    errh_hat = np.maximum((D - clock * ts)[None, :] - delta + noise[:, None], 0.0)
    M = errh_hat - tau_corr
    h = expit(b0 - b1 * M) * DT                         # per-step hazard (T,S)
    fired = rng.random((n_trials, len(ts))) < h
    any_f = fired.any(axis=1)
    first = np.where(any_f, fired.argmax(axis=1), -1)
    lat = np.where(any_f, ts[np.clip(first, 0, None)], np.nan)
    probes = []  # (probe_time, report) from trials still running at probe time
    for pt in PROBE_TIMES:
        alive = ~any_f | (lat > pt)
        rep = (np.maximum((D - clock * pt) - delta + noise[alive], 0.0)
               + rng.normal(0, report_sd, alive.sum()))
        probes.extend((pt, r) for r in rep)
    return lat, np.array(probes) if probes else np.zeros((0, 2))

def probe_slope(probes):
    if len(probes) < 4 or len(set(probes[:, 0])) < 2:
        return np.nan
    x, y = probes[:, 0], probes[:, 1]
    return np.polyfit(x, y, 1)[0]

def gauss_elpd(y_tr, X_tr, y_te, X_te):
    """Held-out gaussian log predictive density of OLS fit."""
    beta, *_ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    resid = y_tr - X_tr @ beta
    s2 = max(resid.var(), 1e-6)
    pred = X_te @ beta
    return float(np.sum(-0.5 * np.log(2 * np.pi * s2)
                        - 0.5 * (y_te - pred) ** 2 / s2))

def subject_cv_elpd(y, X, groups, build):
    """Leave-one-subject-out ELPD; `build` selects design columns."""
    total = 0.0
    for g in np.unique(groups):
        te = groups == g
        total += gauss_elpd(y[~te], build(X[~te]), y[te], build(X[te]))
    return total

# ------------------------------------------------------------------- gate K3
def run_k3(n_cohorts=200, N=40, r_bound=0.85):
    """Discriminant validity. Subject-level measured eRRH bias vs perceived-
    control rating. Fires when the collapse is DEMONSTRATED: lower 90% CI
    bound of |r| >= 0.85 (Fisher z; the TOST-style one-sided criterion).
    pos: independent control channel (shared arousal factor only, r~0.3).
    neg: single-channel data -- the rating is a noisy relabel of the same
    latent (r~0.93)."""
    fires = {"pos": 0, "neg": 0}
    rs = {"pos": [], "neg": []}
    for c in range(n_cohorts):
        rng = np.random.default_rng(3000 + c)
        latent_bias = rng.normal(1.5, 0.6, N)          # true per-subject delta
        arousal = rng.normal(0, 1, N)
        meas_bias = latent_bias + 0.25 * arousal + rng.normal(0, 0.35, N)
        for arm in ("pos", "neg"):
            if arm == "pos":
                control = -0.4 * arousal + rng.normal(0, 1, N)   # independent trait
            else:
                control = -(latent_bias + rng.normal(0, 0.22, N))  # relabel
            r = abs(np.corrcoef(meas_bias, control)[0, 1])
            rs[arm].append(r)
            z = np.arctanh(min(r, 0.999)); se = 1 / np.sqrt(N - 3)
            lo = np.tanh(z - 1.645 * se)
            if lo >= r_bound:
                fires[arm] += 1
    return {a: fires[a] / n_cohorts for a in fires}, {a: float(np.mean(rs[a])) for a in rs}

# ------------------------------------------------------------------- gate K6
def run_k6(n_cohorts=100, n_class=3, N_per=20, trials=16):
    """Cross-phobia invariance on log transition latency ~ deadline.
    shared model: common D slope + class intercepts. class-specific model:
    D x class slopes. Fires when class-specific wins LOSO ELPD by >= 4.
    pos: shared true slope (classes differ in b0/tau_corr only).
    neg: class-specific true slopes (0.50, 0.25, 0.05)."""
    fires = {"pos": 0, "neg": 0}
    d_elpds = {"pos": [], "neg": []}
    for c in range(n_cohorts):
        rng = np.random.default_rng(6000 + c)
        for arm in ("pos", "neg"):
            rows, ys, groups = [], [], []
            sid = 0
            for k in range(n_class):
                b1k = 0.35 if arm == "pos" else (0.50, 0.25, 0.05)[k]
                b0k = (-4.6, -4.2, -5.0)[k]
                tauk = (0.4, 0.8, 0.6)[k]
                for s in range(N_per):
                    b0i = b0k + rng.normal(0, 0.3)
                    b1i = max(b1k + rng.normal(0, 0.05), 0.01)
                    for D in (3.0, 12.0):
                        lat, _ = sim_trials(rng, D, trials // 2, b0i, b1i,
                                            delta=1.0, tau_corr=tauk)
                        lat = np.where(np.isnan(lat), TMAX, lat)
                        for L in lat:
                            rows.append((D, k)); ys.append(np.log(L + DT)); groups.append(sid)
                    sid += 1
            rows = np.array(rows, float); ys = np.array(ys); groups = np.array(groups)
            def shared(Xr):
                cols = [np.ones(len(Xr)), Xr[:, 0]]
                cols += [(Xr[:, 1] == k).astype(float) for k in range(1, n_class)]
                return np.column_stack(cols)
            def classwise(Xr):
                cols = [np.ones(len(Xr))]
                cols += [(Xr[:, 1] == k).astype(float) for k in range(1, n_class)]
                cols += [Xr[:, 0] * (Xr[:, 1] == k) for k in range(n_class)]
                return np.column_stack(cols)
            d = (subject_cv_elpd(ys, rows, groups, classwise)
                 - subject_cv_elpd(ys, rows, groups, shared))
            d_elpds[arm].append(d)
            if d >= 4:
                fires[arm] += 1
    return ({a: fires[a] / n_cohorts for a in fires},
            {a: (float(np.mean(d_elpds[a])), float(np.std(d_elpds[a]))) for a in d_elpds})

# ------------------------------------------------------------------- gate K8
def logistic_cv_elpd(y, X, groups, cols):
    def nll(b, Xd, yd):
        p = expit(Xd @ b)
        return -np.sum(yd * np.log(p + 1e-9) + (1 - yd) * np.log(1 - p + 1e-9)) + 0.01 * b @ b
    total = 0.0
    for g in np.unique(groups):
        te = groups == g
        Xtr, ytr = X[~te][:, cols], y[~te]
        Xte, yte = X[te][:, cols], y[te]
        res = minimize(nll, np.zeros(len(cols)), args=(Xtr, ytr), method="BFGS")
        p = expit(Xte @ res.x)
        total += float(np.sum(yte * np.log(p + 1e-9) + (1 - yte) * np.log(1 - p + 1e-9)))
    return total

def run_k8(n_cohorts=100, N=80):
    """Remission prediction. Fires when adding d(eRRH_hat) to fear+avoidance
    gains < 4 held-out ELPD (10-fold by subject; subjects are folds).
    pos: remission driven by recalibration (d_errh), fear change corr 0.5.
    neg: fear-only recovery; d_errh correlated 0.5 but carries nothing."""
    fires = {"pos": 0, "neg": 0}
    d_elpds = {"pos": [], "neg": []}
    for c in range(n_cohorts):
        rng = np.random.default_rng(8000 + c)
        for arm in ("pos", "neg"):
            z = rng.normal(0, 1, N)                      # shared factor
            d_errh = z + rng.normal(0, 0.9, N)
            d_fear = 0.5 * z + rng.normal(0, 0.87, N)
            d_avoid = 0.4 * d_fear + rng.normal(0, 0.9, N)
            driver = d_errh if arm == "pos" else d_fear
            logit = 1.4 * (driver - driver.mean()) / driver.std() - 0.2
            y = (rng.random(N) < expit(logit)).astype(float)
            X = np.column_stack([np.ones(N), d_fear, d_avoid, d_errh])
            groups = np.arange(N) % 10
            d = (logistic_cv_elpd(y, X, groups, [0, 1, 2, 3])
                 - logistic_cv_elpd(y, X, groups, [0, 1, 2]))
            d_elpds[arm].append(d)
            if d < 4:
                fires[arm] += 1
    return ({a: fires[a] / n_cohorts for a in fires},
            {a: (float(np.mean(d_elpds[a])), float(np.std(d_elpds[a]))) for a in d_elpds})

# ------------------------------------------------------------------- gate K9
def run_k9(n_cohorts=100, n_sub=3, N_per=20, trials=16):
    """One construct, not many. Joint (log latency, probe slope) family.
    shared model: every subtype additive-bias (common probe-slope mean,
    subtype-specific ADM params via intercepts). per-subtype model: subtype 3
    gets its own latent definition (clock-type: own slope mean AND its
    latency depends on scaled deadline). Fires when per-subtype wins >= 4.
    pos: all subtypes generated additive (delta_k in 0.8/1.5/2.2).
    neg: subtype 3 generated by clock gain c=1.3, no additive bias."""
    fires = {"pos": 0, "neg": 0}
    d_elpds = {"pos": [], "neg": []}
    for c in range(n_cohorts):
        rng = np.random.default_rng(9000 + c)
        for arm in ("pos", "neg"):
            ys, slopes, rows, groups = [], [], [], []
            sid = 0
            for k in range(n_sub):
                if arm == "neg" and k == 2:
                    delta_k, clock_k = 0.0, 1.3
                else:
                    delta_k, clock_k = (0.8, 1.5, 2.2)[k], 1.0
                for s in range(N_per):
                    b0i = -4.4 + rng.normal(0, 0.3)
                    b1i = max(0.35 + rng.normal(0, 0.05), 0.01)
                    subj_pr = []
                    for D in (3.0, 12.0):
                        lat, pr = sim_trials(rng, D, trials // 2, b0i, b1i,
                                             delta=delta_k, clock=clock_k)
                        lat = np.where(np.isnan(lat), TMAX, lat)
                        for L in lat:
                            ys.append(np.log(L + DT)); rows.append((D, k)); groups.append(sid)
                        if len(pr):
                            subj_pr.append(pr)
                    sl = probe_slope(np.vstack(subj_pr)) if subj_pr else np.nan
                    slopes.append((sid, k, sl))
                    sid += 1
            ys = np.array(ys); rows = np.array(rows, float); groups = np.array(groups)
            sl = np.array([(s, k, v) for s, k, v in slopes if np.isfinite(v)])
            def timing_elpd(build):
                return subject_cv_elpd(ys, rows, groups, build)
            def shared_t(Xr):
                cols = [np.ones(len(Xr)), Xr[:, 0]]
                cols += [(Xr[:, 1] == k).astype(float) for k in range(1, n_sub)]
                return np.column_stack(cols)
            def persub_t(Xr):
                cols = [np.ones(len(Xr))]
                cols += [(Xr[:, 1] == k).astype(float) for k in range(1, n_sub)]
                cols += [Xr[:, 0] * (Xr[:, 1] == k) for k in range(n_sub)]
                return np.column_stack(cols)
            # probe-slope component: gaussian, shared mean vs subtype-3-own mean
            def slope_elpd(per_subtype):
                tot = 0.0
                for g in np.unique(sl[:, 0]):
                    te = sl[:, 0] == g
                    tr = ~te
                    if per_subtype:
                        k3 = sl[:, 1] == 2
                        mu_a = sl[tr & ~k3, 2].mean(); mu_b = (sl[tr & k3, 2].mean()
                                                               if (tr & k3).any() else mu_a)
                        s2 = max(np.var(np.concatenate([sl[tr & ~k3, 2] - mu_a,
                                                        sl[tr & k3, 2] - mu_b])), 1e-4)
                        mu = np.where(sl[te, 1] == 2, mu_b, mu_a)
                    else:
                        mu = sl[tr, 2].mean()
                        s2 = max(sl[tr, 2].var(), 1e-4)
                    tot += float(np.sum(-0.5 * np.log(2 * np.pi * s2)
                                        - 0.5 * (sl[te, 2] - mu) ** 2 / s2))
                return tot
            d = ((timing_elpd(persub_t) + slope_elpd(True))
                 - (timing_elpd(shared_t) + slope_elpd(False)))
            d_elpds[arm].append(d)
            if d >= 4:
                fires[arm] += 1
    return ({a: fires[a] / n_cohorts for a in fires},
            {a: (float(np.mean(d_elpds[a])), float(np.std(d_elpds[a]))) for a in d_elpds})

if __name__ == "__main__":
    import json, time
    out = {}
    t0 = time.time()
    f, extra = run_k3(); out["K3"] = {"fires": f, "mean_abs_r": extra}
    print("K3", out["K3"], f"{time.time()-t0:.0f}s", flush=True)
    f, extra = run_k6(); out["K6"] = {"fires": f, "dELPD_mean_sd": extra}
    print("K6", out["K6"], f"{time.time()-t0:.0f}s", flush=True)
    f, extra = run_k8(); out["K8"] = {"fires": f, "dELPD_mean_sd": extra}
    print("K8", out["K8"], f"{time.time()-t0:.0f}s", flush=True)
    f, extra = run_k9(); out["K9"] = {"fires": f, "dELPD_mean_sd": extra}
    print("K9", out["K9"], f"{time.time()-t0:.0f}s", flush=True)
    with open("rrhm_gates_k3689_results.json", "w") as fh:
        json.dump(out, fh, indent=1)
    print("DONE", f"{time.time()-t0:.0f}s")
