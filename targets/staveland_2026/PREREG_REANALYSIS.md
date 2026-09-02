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
