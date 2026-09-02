# RRHM × Staveland et al. 2026 — one-page landing

**Target paper (verified via Crossref):** Staveland B., Oberschulte J., Berger B., Minarik T.,
Kim-McManus O., Willie J.T., et al. *Cortical-limbic circuit dynamics of approach-avoidance
conflict in humans.* Nature Communications, 2026. doi:10.1038/s41467-026-70287-5
(preprint doi:10.1101/2024.12.31.630927).
**Target data (verified via Zenodo API):** record 17726565 — "minimally processed data"
(cleaned/filtered/bipolar-referenced/epoched iEEG + electrode localization + behavior),
open, CC BY 4.0, single 77 GB archive, creator Staveland, Brooke.

## Two-minute version
- **What the paper found:** theta synchrony across a cortical–limbic circuit tracks
  approach–avoidance behavior and relates to approach duration; right-MFG high-frequency
  activity shows different dynamics between Chase (escape still possible) and Strike
  (escape designed to fail).
- **The gap we think is experimentally separable:** threat imminence versus the
  *remaining actionability of the current trajectory* — how much time is left in which an
  effective action still preserves a viable course. In the existing task these are
  partially confounded.
- **What we predict (frozen before analysis):** see `PREDICTION_LOCK.md` and
  `PREREG_REANALYSIS.md`. Core reanalysis question: does a task-geometry-derived
  escape-recoverability margin M^D explain right-MFG/behavioral dynamics beyond ghost
  distance, threat probability, trial type, reward, and time?
- **What would falsify us here:** M^D adds nothing beyond the threat-imminence covariate
  set → recorded FAIL, no reinterpretation (our repo's ledger already carries such FAILs,
  e.g. case C30).
- **What the existing dataset CANNOT test** (we say this before anyone else does): the
  central RRHM quantity is *engagement-preserving* recoverability, and the current task
  has approach→turn/escape but no "fix the situation and stay" action. `NEXT_EXPERIMENT.md`
  proposes the minimal task modification that adds one.

**Boxed honesty rule:** **M^D ≠ eRRH.** M^D is defensive/escape recoverability inside the
existing task; eRRH (engagement-preserving) needs the modified task.

## Contents
`PREDICTION_LOCK.md` · `REPRODUCTION_REPORT.md` (R0) · `PREREG_REANALYSIS.md` (frozen) ·
`code/01_reproduce_staveland.py` · `code/02_recoverability_margin.py` ·
`NEXT_EXPERIMENT.md` · `DRAFT_EMAIL.md`.
Optional deep dive: the full RRHM manuscript (v21 PDF) lives at `../../paper/`.
