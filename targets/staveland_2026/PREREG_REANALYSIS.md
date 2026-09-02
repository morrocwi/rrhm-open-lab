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
