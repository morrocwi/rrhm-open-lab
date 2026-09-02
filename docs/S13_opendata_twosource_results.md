> **SUPERSEDED — READ THIS FIRST (2026-09-02, independent adversarial review).**
> This file is the ORIGINAL v18-era record, kept verbatim for provenance. Its headline
> results were re-adjudicated and PARTLY WITHDRAWN: the Source-B timing result ("PASS,
> striking", peak 3.48 s vs 3.5 s) is **WITHDRAWN as a window-edge argmax artifact**; the
> "MARGINAL" label and the "3.5 of 4 frozen criteria met" aggregate are **RETRACTED** as
> post-unblinding inventions; Source A's criteria were adjudicated **unfailable by design**
> (confirmatory in form only). The binding record is `../prereg/SCORES_2026-09-02.md` and
> `../REVIEW_2026-09-02.md`. Do not cite anything below without those files.

# S13 — C23 executed: two-source open-data test (2026-09-02)

Plan FROZEN in prereg v2 (C23) before any outcome file was opened. Raw data downloaded
from Zenodo and analyzed end-to-end by this session's own pipeline. Zero fitted
parameters. Compatibility ≠ validation (standing rule).

## Source A — Zenodo 20796399 (VR spider exposure; SUDS + cortisol + HR/HRV; N=28)
Frozen criteria: (1) |r|(mean SUDS, physiological reactivity) ≤ 0.70;
(2) both discordant quadrants ≥ 15%.
RESULTS:
- r(SUDS, cortisol reactivity cort3−cort2) = **0.119** (n=27); quadrants 26%/26%
- r(SUDS, PPG HR delta) = **0.005** (n=28); quadrants 32%/32%
- SUDS variance real (means 0–8.6)
**VERDICT: PASS, emphatic** — subjective and physiological lanes near-orthogonal;
Law-2 necessary implication holds far beyond the prior guess (0.3–0.6).
Declared weakness stands: measurement error alone can lower r (but r≈0.005 with
full-range SUDS is difficult to attribute to noise alone; not claimed as proof).

## Source B — Zenodo 321641 (PsPM-HRA1; delay conditioning, SOA 3.5s; N=20)
Frozen criteria: (1) CS+ > CS− anticipatory SCR amplitude;
(2) differential timing structured within the CS-US window.
RESULTS (window 0.5–3.5s post-CS, 1s baseline; all 20 subjects, all trials):
- Amplitude: mean ΔSCR = +0.013, t = 1.51 (12/20 positive) → **MARGINAL** (direction
  correct, underpowered under this crude frozen pipeline; trials include habituation/
  early acquisition — stated limitation, no post-hoc reanalysis performed)
- Timing: differential-curve peak latency median **3.48 s ≈ the 3.5 s deadline**;
  13/20 subjects peak within 0.06s of US onset; 15/20 within [1.0, 3.5]s
  → **PASS, striking** — the CS+/CS− differential is shaped like a remaining-time
  signal ramping to its maximum exactly at the programmed deadline.

## Scorecard
- A: PASS/PASS · B: MARGINAL/PASS — 3.5 of 4 frozen criteria met across two unrelated
  paradigms (phobia-VR psychophysiology; Pavlovian conditioning).
- Epistemic class: preregistered necessary-implication compatibility on raw world data.
  NOT validation of RRHM (no deadline was manipulated; no rival was fitted).
- First real-human-data contact of the program. Next rung: the decisive experiment's
  deadline manipulation — no open dataset manipulates causal recoverability (still true).
