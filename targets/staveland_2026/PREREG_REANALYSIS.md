# PREREG — escape-recoverability-margin reanalysis (R1). FROZEN before any target data file was opened.

Holdings at freeze: Crossref record of the paper; Zenodo record 17726565 METADATA ONLY
(title, creator, license, single-archive structure). No behavioral, localization, or iEEG
file has been opened; the archive has not been downloaded.

## The quantity
Per timepoint t within approach epochs, from TASK GEOMETRY ONLY:
  M^D_t = T_catch,t − T_exit,t
where T_catch,t = time until the ghost reaches Pac-Man under current positions/velocities,
and T_exit,t = time for Pac-Man to reach the nearest viable exit under current position/
speed. Inputs permitted: Pac-Man position/velocity, ghost position/velocity, exit
distance(s), maze geometry. Inputs FORBIDDEN in constructing M^D: any neural signal,
eventual escape outcome, approach duration, or any quantity we predict.
Sign reading: M^D > 0 → an exit remains reachable before capture on current kinematics;
M^D < 0 → current trajectory can no longer out-run capture.
**BOXED: M^D ≠ eRRH.** M^D is defensive/escape recoverability in the existing task. It is
NOT the engagement-preserving recoverability (êRRH_C) that is RRHM's central claim; the
central claim is testable only with the modified task (NEXT_EXPERIMENT.md).

## Two-stage mapping rule (C27/C28 discipline)
Exact column mapping to the released behavioral files will be appended as
PREREG-MAPPING from structure/codebook inspection ONLY, as a separate commit, before any
outcome value is computed. If the released sampling of positions/velocities makes T_catch
or T_exit non-derivable, that is recorded as ⊥ for the affected component — never proxied
silently.

## Frozen tests
- R1.a (behavioral): in a mixed model with random subject intercepts, M^D_t (or its
  per-trial minimum / time-below-zero, mapping-stage choice recorded before outcomes)
  predicts turnaround (approach→avoid transition) timing AFTER the covariate set
  {ghost distance, threat probability/trial type, reward on offer, time in trial}.
  PASS = coefficient in the predicted direction (smaller margin → earlier transition)
  AND model comparison ΔBIC ≥ 2 versus the covariate-only model. FAIL otherwise.
- R1.b (neural, only if R0 step 3 reproduces first): same structure with right-MFG HFA as
  outcome within Chase vs Strike epochs; PASS = ΔBIC ≥ 2 for adding M^D. FAIL otherwise.
- Falsifier honesty: a FAIL here means the threat-imminence covariates already carry the
  signal — recorded as a FAIL of the M^D reanalysis, with NO post-hoc margin redefinition.

## Prior guesses (recorded)
R1.a PASS p = 0.55. R1.b PASS p = 0.40. (Deliberately cautious after the C29/C30 forecast
lessons.)

## Order gate
R1 computation may not begin before R0 (steps 1–2 minimum) succeeds; contact with the
authors happens after R0, with R1 frozen — per the target protocol in ../README.md.

## PREREG-MAPPING (appended 2026-09-02 from AUTHORS' CODE inspection only — no outcome data opened)
Sources read: bstavel/Staveland_et_al_Pacman_Neural_Analyses raw_data/*/scripts/states2csv_*.ipynb
and bstavel/Staveland_et_al_Pacman_Statistics_and_Behavior R/create_distance_df.R (both pinned
via Zenodo 17727554/17727552).
- Behavioral stream: BCI2000 game states sampled to 50 ms flips (20 Hz): Trial_on_off,
  GhostLocation, UserLocation, Direction, Biscuit1–5, Attack, Chase, Eaten, Score, Lives,
  TrialType → per-subject `*_raw_behave.csv` (produced upstream of the public deposit).
- Task geometry is ONE-DIMENSIONAL: distance_to_ghost = |GhostLocation − UserLocation|
  (authors' own definition) — our 1-D t_catch/t_exit implementation in
  code/02_recoverability_margin.py maps directly.
- OUTCOME for R1.a = the authors' `last_away` in its trial_time version (the final
  towards→away direction flip per trial) — their turnaround operationalization, adopted
  verbatim, not ours.
- COVARIATE OPERATIONALIZATION (frozen): ghost distance = distance_to_ghost;
  threat probability = their cdf_distance (CDF of distance/100 under their declared
  threat_function) or TrialType where that is the paper's usage; reward = Biscuit/reward
  state per TrialType; time = trial_time. Velocities for M^D = first differences of
  GhostLocation/UserLocation over 50 ms flips.
- M^D per flip: T_catch from closing speed on the 1-D track; T_exit from UserLocation's
  distance to the trial exit at current user speed; exit position to be read from task
  code/constants (structure inspection), never fitted.
- DATA-ACCESS STATUS at this mapping commit: the per-subject behavioral CSVs are NOT in
  the public deposit (verified by central-directory enumeration); whether the epoched
  .fif files carry the game-state channels is under verification. If behavior proves
  unavailable publicly, R1 waits for the authors' pointer — it does NOT proceed on
  reconstructed data.

## R1-v2 AMENDMENT (2026-09-02, appended BEFORE any outcome computation; supersedes R1.a/R1.b criteria — original text retained above for provenance)
Motivated by an internal adversarial simulation of the target team's likely review. Their
strongest objections, adopted as design constraints:
(a) "M^D may simply reparameterize distance/speed/trial type/escape probability" — so the
    test must be INCREMENTAL and OUT-OF-SAMPLE, and the reparameterization outcome is a
    first-class named result, not an insult;
(b) no neural-to-construct mapping (theta/MFG is NOT eRRH; we never say it is);
(c) this dataset cannot adjudicate RRHM's central engagement-preserving claim — stated in
    every output.
FROZEN criteria (replace R1.a/R1.b):
- R1v2.a (behavioral, PRIMARY): leave-one-subject-out cross-validation. Baseline model of
  last_away (trial_time): {distance_to_ghost, user speed, ghost speed, TrialType/reward,
  cdf_distance threat, trial time} with random subject intercepts (fit per training fold).
  Test model: baseline + M^D features (frozen at mapping: instantaneous M^D and per-trial
  min-M^D). PASS = held-out log-likelihood (or ELPD) improves for the M^D model in a
  MAJORITY of left-out subjects AND the mean held-out improvement > 0 with a participant
  bootstrap 95% CI excluding zero. FAIL otherwise.
- R1v2.b (neural, SECONDARY, only if R0 neural step reproduces): same held-out structure
  with right-MFG HFA; identical PASS rule. Neural results are interpreted ONLY as "M^D
  carries incremental information", never as localization of eRRH.
- Named alternative outcome (frozen wording): if M^D adds nothing out-of-sample, the
  recorded conclusion is "the preregistered recoverability proxy did not outperform the
  existing threat variables; the present dataset fails to support that RRHM prediction" —
  and the identifiability lesson feeds NEXT_EXPERIMENT.md. This is a publishable outcome
  of equal standing.
Prior guesses (recorded): R1v2.a PASS p=0.45 (down from 0.55 — the covariate set now
includes speeds, which absorb part of M^D by construction); R1v2.b PASS p=0.30.
Email gate (binding, per protocol step 6): no contact before (1) reproduction table
Original-vs-Reproduced exists, (2) this freeze stands, (3) ONE held-out result (positive
or negative) is archived, (4) the one-page next experiment is final.

## R1-v3 CANONICAL SPECIFICATION (2026-09-02, appended BEFORE any outcome computation; supersedes R1-v2's feature/fit details; R1-v2's spirit — held-out, incremental, reparameterization-as-named-outcome — unchanged)
Trigger: an internal adversarial audit (simulating the data-holding postdoc) found ~8
unpinned implementation forks. Every fork is pinned here so the prediction is
operationally frozen: an implementer needs ZERO choices and ZERO emails. Where prose and
example code disagree, THIS SECTION is authoritative.

### Model class (pins the timepoint/aggregation family of ambiguities at the root)
Discrete-time hazard model at the flip level (50 ms person-period format) — no per-trial
aggregation windows exist, so no window can reference the outcome:
  turn(t) ~ baseline(t) [+ M^D features(t)] + (1 | subject),  binomial GLMM (logit)
where turn(t) = 1 at the flip of the trial's LAST towards→away direction flip (the
authors' last_away moment), 0 at every earlier included flip; flips after last_away are
not in the risk set. Trials with no towards→away flip contribute all their included flips
as 0s (right-censored at trial end).

### Data pins
- Flip inclusion: Trial_on_off == 1; ghost-present trials with TrialType <= 16 (authors'
  own cleaning rule); the authors' jump/flip-artifact exclusions adopted verbatim from
  R/clean_behavioral_data.R; risk set = flips from trial start to last_away inclusive.
- Velocities: backward first difference over exactly 1 flip (x_t − x_{t−1}), no smoothing;
  first flip of each trial has velocity 0 by convention.
- Units: raw game-state position units and 50 ms flips throughout (consistency, not the
  absolute scale, is what matters; M^D is in flips).

### M^D pins
- Exit position: the trial's entry point = the first included UserLocation sample of that
  trial. exit_dist(t) = |UserLocation_t − entry point|.
- T_exit(t) = exit_dist(t) / v_flee, where v_flee = the subject-level median of nonzero
  |ΔUserLocation| per flip across all included flips (a capability constant per subject:
  "how fast can this player move when moving") — NOT current velocity, because T_exit is
  the time a flee-now decision would need, not an extrapolation of current motion.
- T_catch(t): gap(t) = |GhostLocation_t − UserLocation_t|; closing(t) = −Δgap over 1 flip
  (positive = ghost gaining). T_catch = gap/closing if closing > 0, else +CAP.
- M^D(t) = T_catch(t) − T_exit(t), then clipped to [−CAP, +CAP] with CAP = 200 flips
  (10 s). No NaN can arise under these pins.
- Frozen M^D feature set (exactly two, both flip-level): clipped M^D(t), and the binary
  indicator [M^D(t) < 0].
(The R1.a-era "time-below-zero" option is hereby recorded as dropped; "instantaneous vs
min" from R1-v2 is dissolved by the flip-level model.)

### Baseline pins (every covariate a named flip-level column)
distance_to_ghost(t); signed user velocity toward ghost; signed ghost velocity toward
user; TrialType (factor) AND large-reward indicator; the authors' cdf_distance(t)
recomputed by their published formula; flip index t within trial; Chase(t) and Attack(t)
as binary covariates in BOTH baseline and test models.

### Fit & scoring pins
- Engine: lme4::glmer (binomial, logit), ML. Declared fallback if R is unavailable to an
  implementer: statsmodels BinomialBayesMixedGLM, reported as a deviation.
- LOSO: refit on N−1 subjects; score the held-out subject with random effect set to 0
  (population-conditional), score = mean per-flip held-out log predictive probability.
- Per-subject improvement = (mean per-flip lppd of M^D model) − (baseline model).
- PASS = improvement > 0 in a strict majority of subjects (tie or exactly half = FAIL)
  AND mean improvement > 0 with percentile bootstrap 95% CI over subjects (10,000
  resamples, seed 20260902) excluding zero. FAIL otherwise. Direction check (reported,
  not gating): the fixed effect of clipped M^D on turn hazard is negative
  (smaller margin → higher hazard).
- Prior guess carried over: PASS p = 0.45.

### Email-gate amendment (recorded ruling, 2026-09-02)
For the no-public-data case (Variant S letter): gate item 3 ("one held-out result")
transfers BY DESIGN to the data holders — we cannot compute M^D from public materials
(verified in REPRODUCTION_REPORT.md). Variant S's send-gates are therefore:
(1) reproduction table ✅, (2) this freeze ✅, (4) next-experiment page ✅. This amendment
is recorded here, in the frozen file the letter links, so no reader can find the original
gate without finding this ruling beside it.
Lock commits for citation: original freeze 98895aa · mapping 663aadf · R1-v2 bf19562 ·
R1-v3 = the commit introducing this section (hash visible in git history and cited in
README/letter after commit).
