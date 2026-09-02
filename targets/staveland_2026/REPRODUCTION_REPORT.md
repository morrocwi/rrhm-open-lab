# R0 — independent reproduction of the published analyses. Status: ⏳ IN PROGRESS

## R0 progress log (2026-09-02)
- Archive topology mapped WITHOUT downloading (HTTP range against the zip64 central
  directory, 77.0 GB, ~54 members): the deposit contains ONLY per-subject epoched iEEG
  .fif files (BJH016...SLCH018, LL10...LL19; 0.4–2.0 GB each). No separate behavioral or
  electrode-localization members are present, despite the record description mentioning
  behavioral data — working hypothesis: behavior travels as per-epoch metadata inside the
  MNE .fif epochs (being verified on the smallest subject, LL19). If false, the
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
