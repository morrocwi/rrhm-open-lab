# Staveland 2026 × RRHM: Reproduction, preregistered reanalysis, and one prospective dissociation

**Target:** Staveland B. et al., *Cortical-limbic circuit dynamics of approach-avoidance
conflict in humans.* Nat Commun 2026, doi:10.1038/s41467-026-70287-5 · data: Zenodo
17726565 · code: Zenodo 17727552 / 17727554.

**The one question this package asks:**

> Threat proximity ≟ time remaining for effective action.

The paper shows theta synchrony and right-MFG dynamics tracking approach–avoidance. We ask
whether part of what those signals track is not how close the threat is, but how much time
remains in which an effective action still preserves a viable trajectory — and we test it
so that the answer can be **no**.

| | | |
|---|---|---|
| **[Reproduction](REPRODUCTION_REPORT.md)** | **[Prediction lock](PREREG_REANALYSIS.md)** | **[Next experiment](NEXT_EXPERIMENT.md)** |
| original data + original code → original result (status inside; nothing claimed before it runs) | frozen before any outcome: held-out, subject-wise, incremental over distance/speed/trial-type/reward/threat; the "your margin just reparameterizes distance" outcome is a named, publishable result | the one-page task modification that separates threat imminence from engagement-preserving recoverability — the thing the current dataset cannot test, said by us first |

**Three things we state up front**
1. The existing dataset **cannot adjudicate RRHM's central claim** (no engagement-preserving
   corrective action exists in the task). The reanalysis tests a narrower, escape-side margin
   only — boxed everywhere as **M^D ≠ eRRH**.
2. **No neural signal is mapped onto a model construct.** Theta is not eRRH; MFG is not eRRH.
   The neural test (if run) asks only whether a task-geometry margin carries incremental
   information.
3. A negative result is recorded as a failure of the RRHM prediction on this dataset, verbatim,
   in the same file as a positive one would be. Our track record of doing exactly that is in
   the repo root (`prereg/SCORES_2026-09-02.md` — including a triggered falsifier, C30).

*Optional: [full theory manuscript (v21, PDF)](../../paper/) — not required for anything above.*
