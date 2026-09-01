# RRHM Open Lab — computational companion to *Why We Phobia?* (RRHM, adversarial editions)

**Author of the theory:** Yaoharee Lahtee (Open Civil Science Initiative).
**This repository:** every number in the manuscript that came from a computation, made
reproducible — the falsification-gate battery, the coupling-extension simulations, the
preregistered open-data tests, the recalibration-law calculators, the figures, and the
citation-verification tool — together with the frozen preregistrations they answer to.

> **Claim ceiling (read first).** Everything here is *hypothesis-grade*. The Regulatory
> Recoverability Horizon Model (RRHM) and the readout architecture behind it carry
> **zero direct empirical validation**; the simulations are properties of toy designs;
> the open-data results are preregistered *necessary-implication compatibility checks*,
> never validation; nothing is clinical guidance. The manuscript's own boxed rule
> applies everywhere: **external compatibility ≠ direct validation.**

## Layout
```
paper/      manuscript LaTeX source (current public version)
prereg/     frozen preregistrations: compatibility audit v1 (FROZEN) & v2 (C16–C24),
            SOMA-READ flagship protocol (FROZEN draft, pending pilot + ethics)
code/
  gates/        K3/K6/K8/K9 falsification-gate battery (seeded; ~1 min runtime)
  opendata/     C23 preregistered two-source tests (auto-download from Zenodo)
  calculators/  recalibration law: ledger p̂, lesion fraction, dose n*, fading k_min
  figures/      deterministic regeneration of manuscript figures 1–2
  tools/        PubMed field-by-field citation verifier
results/    archived outputs (JSON) the manuscript cites, with run notes
docs/       companion records: phenomenology fence, intervention framework (RGIF),
            tier-1 consistency sims, open-data results, SOMA-READ QA memo
```

## Quickstart
```bash
pip install numpy scipy matplotlib
python3 code/gates/rrhm_gates_k3_k6_k8_k9.py        # gate battery (seeds fixed)
python3 code/calculators/recalibration.py           # worked ledger example + n* + fading table
python3 code/figures/make_figures.py                # figs 1-2 from the closed-form equations
python3 code/opendata/c23_lane_dissociation.py      # downloads Zenodo 20796399 summary
python3 code/opendata/c23_hra1_timing.py            # downloads Zenodo 321641 (33 MB)
```

## Reproducibility contract
- Every stochastic script fixes its seeds; archived outputs in `results/` state the
  exact numbers the manuscript quotes.
- Open-data tests were **preregistered before any outcome file was opened**
  (`prereg/…v2.md`, case C23) — the frozen criteria, locked falsifiers, and the
  recorded-and-wrong prior guesses are all in the file.
- The theory itself is **FROZEN** (v0.2: state → readout → internal lanes → action →
  outcome → feedback; typed, dynamically coupled). New anomalies go to a challenge
  ledger, not into the equations.

## Planned analyses (not yet run — help welcome)
- `rankStab` (Zenodo 7323547): lane-trajectory separability across conditioning phases.
  Data ships as `.RData`; now readable via pyreadr (verified 2026-09-02) — analysis still owed. See `TODO_planned_analyses.md`.
- SOMA-READ flagship experiment (prereg/SOMA_READ_*): needs a psychophysiology lab
  with programmable haptics. Pilot N=20 → ethics → confirmatory N=120 (80/40 sealed).

## Licensing
Code: MIT. Documents and preregistrations: CC BY 4.0.
The manuscript states its own license (CC BY 4.0) and correspondence address.

## Provenance
Built by the ANSE.ASIA research pipeline (human founder + AI sessions) with the
discipline recorded in the manuscript: tiered claims, full-text-or-NO-DATA holdings,
maker–checker review before public release. This repository was assembled after an
independent multi-agent adversarial review pass; the review's confirmed findings and
their dispositions are recorded in `docs/`.
