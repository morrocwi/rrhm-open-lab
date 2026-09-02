# R0 — independent reproduction of the published analyses. Status: FIRST RESULT REPRODUCED ✅ (R0-1); remainder in progress

## R0-1 — Figure 1 turnaround~reward model: REPRODUCED WITHIN TOLERANCE (2026-09-02)
Data source: the publisher's Source Data file (41467_2026_70287_MOESM4_ESM.xlsx, Springer
static content) — located AFTER establishing that the Zenodo deposit carries no behavioral
files; the Source Data sheets contain trial-level per-figure data AND the original brms
model summaries, making the comparison self-contained.

| quantity | Original (brms, their sheet, verbatim) | Reproduced (statsmodels MixedLM) |
|---|---|---|
| large_rewardSmall | 0.1115 [0.0905, 0.1326] | **0.1114 [0.0899, 0.1329]** |
| Intercept | −0.0509 | **−0.0509** |
| sd(Intercept) | 0.3841 | 0.3801 |
| subjects | 211 | 211 |
| N obs | 34,298 | 34,609 |

Declared deviations: the MixedLM fit emits a ConvergenceWarning (MLE possibly at the random-slope boundary) — reported for completeness, estimates match regardless; engine ML vs Bayesian (expected near-agreement for Gaussian model —
observed); our extracted sheet holds 34,609 rows vs their stated 34,298 observations
(difference 311, unexplained by us; recorded). Script: code/03_reproduce_fig1_turnaround_reward.py
(self-fetches the Source Data file). Cohort columns confirm the file contains BOTH the
online samples (30,343 rows) and the iEEG cohort (4,266 rows).

## Behavioral-data location — FINAL RESOLUTION
The per-figure Source Data file substantially replaces the missing deposit behavior for
REPRODUCTION purposes (trial-level last_away etc.). LIMIT: it does NOT contain the 20 Hz
game-state streams (positions/velocities), so the M^D reanalysis (R1-v2) still requires
the raw behavioral files — the data inquiry to the authors remains the unblocking step
for R1, while R0 proceeds on Source Data.

## R0 progress log (2026-09-02)
- Archive topology mapped WITHOUT downloading (HTTP range against the zip64 central
  directory, 77.0 GB, ~54 members): the deposit contains ONLY per-subject epoched iEEG
  .fif files (BJH016...SLCH018, LL10...LL19; 0.4–2.0 GB each). No separate behavioral or
  electrode-localization members are present, despite the record description mentioning
  behavioral data — working hypothesis: behavior travels as per-epoch metadata inside the
  MNE .fif epochs. Verification attempt log: (1) first selective extraction of LL19
  (409 MB member) was truncated mid-stream at 142/367 MB by an HTTP error; MNE opened the
  truncated file (240 epochs, 52 ch, 512 Hz) and reported metadata=None — RECORDED AS
  INVALID: a conclusion from a truncated file is not a reading (0 ≠ ⊥). (2) A retrying
  re-download was stopped externally before completion. RESOLVED 2026-09-02 19:0x: the COMPLETE
  LL19 file (369 MB verified download with retry) contains 240 epochs, 51 bipolar sEEG
  channels + 1 STI trigger channel, sfreq 512, tmin/tmax −4/+12 s, metadata = None,
  single event code — NO game-state channels, NO behavioral metadata. Combined with the
  full central-directory enumeration (no behavioral members) and full recursive trees of
  all three public code repos (no per-subject behavioral CSVs; the paths the analysis
  code reads live outside the repos), the finding is now DEFINITIVE:
  **the iEEG-cohort behavioral data required to reproduce the published behavioral and
  brain–behavior analyses is not publicly available, although the Zenodo record
  description states behavioral data are included.** R0 (behavioral and brain-behavior
  arms) is BLOCKED on exactly this; the
  behavioral source is a question FOR the authors, recorded here first.
- Authors' code located and pinned: github.com/bstavel/Staveland_et_al_Pacman_Statistics_and_Behavior
  (R/brms; archived as Zenodo 17727552 'publication-release') and
  github.com/bstavel/Staveland_et_al_Pacman_Neural_Analyses (python; Zenodo 17727554).
  NEITHER repo carries a license -> we run their code by reference, copy nothing.
- Behavioral pilot/clinical CSVs referenced by the stats repo live OUTSIDE the public
  repos (../behavioral_parsing/, munge/) — the iEEG-cohort behavior is the open question
  above.

Nothing in this file may be cited until the runs exist. Planned scope (in order):
1. Behavioral: turnaround/reward behavior from the released behavioral files.
2. Theta synchrony ↔ approach duration (published pipeline, published parameters).
3. Chase vs Strike right-MFG HFA dynamics.

Technical plan (recorded before execution): the Zenodo archive is a single 77 GB zip;
full download is infeasible in the authoring environment. Strategy: HTTP range requests
against the zip central directory to enumerate members and pull ONLY the behavioral and
localization files first (implemented in `code/01_reproduce_staveland.py`); iEEG members
fetched selectively per analysis. The authors' released analysis code is to be located
from the paper's code-availability statement and vendored by reference (URL + commit),
never copied without license check.

Honesty rule: R0 uses ORIGINAL code and parameters — any deviation is listed here with
its reason. R0 contains zero RRHM content. If a published result does not reproduce, that
is reported to the authors privately FIRST, as a possible error on OUR side.
