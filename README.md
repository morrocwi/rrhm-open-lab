# RRHM Open Lab — computational companion to *Why We Phobia?* (RRHM, adversarial editions)

**Author of the theory:** Yaoharee Lahtee (Open Civil Science Initiative).
**This repository:** every number in the manuscript that came from a computation, made
reproducible — the falsification-gate battery, the coupling-extension simulations, the
preregistered open-data tests (first round C23; second round C25–C31), the
recalibration-law calculators, the machine-checked equation layer (Coq), the figures,
and the citation-verification tool — together with the frozen preregistrations they
answer to.

> **Claim ceiling (read first).** Everything here is *hypothesis-grade*. The Regulatory
> Recoverability Horizon Model (RRHM) and the readout architecture behind it carry
> **zero direct empirical validation**; the simulations are properties of toy designs;
> the open-data results are preregistered *necessary-implication compatibility checks*,
> never validation; nothing is clinical guidance. The manuscript's own boxed rule
> applies everywhere: **external compatibility ≠ direct validation.**

## Layout
```
paper/      manuscript LaTeX source (current public version)
prereg/     frozen preregistrations (compatibility audit v1 & v2, C25–C31 second-round
            freezes, SOMA-READ flagship protocol) + SCORES_2026-09-02.md (scored
            outcomes, kept separate from the frozen texts)
code/
  gates/        K3/K6/K8/K9 falsification-gate battery (seeded; ~1 min runtime)
  opendata/     preregistered open-data pipelines C23–C31 (each auto-downloads its
                own data from Zenodo — see Quickstart)
  calculators/  recalibration law: ledger p̂, lesion fraction, dose n*, fading k_min
  figures/      deterministic regeneration of manuscript figures 1–2
  tools/        PubMed field-by-field citation verifier
coq/        machine-checked equation layer (Coq 8.20.1, axiom-free — see below)
results/    archived outputs (JSON) the manuscript cites, with run notes
docs/       companion records: phenomenology fence, intervention framework (RGIF),
            tier-1 consistency sims, open-data results, SOMA-READ QA memo,
            Coq equation ledger (docs/COQ_EQUATION_LEDGER.md)
```

## Quickstart
```bash
pip install numpy scipy pyreadr openpyxl   # matplotlib additionally for code/figures/
python3 code/gates/rrhm_gates_k3_k6_k8_k9.py        # gate battery (seeds fixed)
python3 code/calculators/recalibration.py           # worked ledger example + n* + fading table
python3 code/figures/make_figures.py                # figs 1-2 from the closed-form equations
```

Every open-data script downloads its own data from Zenodo into the current working
directory on first run — no manual data step. Pipelines, with rough runtimes:

| script (`code/opendata/`) | what it tests | runtime / download |
|---|---|---|
| `c23_lane_dissociation.py` | C23-A: VR-spider two-lane (rating vs SCR) dissociation | ~1 min after a 468 MB download |
| `c23_hra1_timing.py` | C23-B: HRA1 heart-rate temporal structure (result later WITHDRAWN — see below) | 33 MB download, fast |
| `c23_hra1_artifact_controls.py` | the three controls that established C23-B as a window-edge artifact | same 33 MB data, fast |
| `c25_lane_mtmm.py` | C25: multitrait-multimethod lane matrix, fear conditioning | fast (~330 KB) |
| `c26_stress_transport.py` | C26: mood~cortisol / mood~HR transport, 3-paradigm stress crossover | fast (~50 KB) |
| `c27_predictability_clamp.py` | C27: threat-unpredictability clamp (tonic freeze, gradient, lane dissociation) | 302 MB download, minutes |
| `c28_rankstab_mtmm.py` | C28: six-month two-occasion MTMM (rankStab) | fast (4 MB) |
| `c28_sensitivity.py` | C28 exploratory sensitivity (complete-case + participant bootstrap) | bootstrap, ~5 min |
| `c29_model_comparison.py` | C29: one-scalar (M0) vs two-lane (M1) factor model comparison | bootstrap, ~20 min |
| `c29_audit_phi_tail.py` | C29 audit: φ canonicalization + bootstrap tail probabilities | ~15 min |
| `c30_external_transport.py` | C30-A: external transport of the lane architecture (IU-Hamburg) | fast |
| `c31_degradation_calibration.py` | C31.1: SCR-reliability degradation grid (M1→M0 flip calibration) | long (~1 h grid) |
| `c31_2w_rofl_fourcell.py` | C31.2w annex: ROFL four-cell run (proved cohort identity with rankStab) | fast (1.8 MB) |

## Status of the open-data program (honest narrative)

Exact numbers, frozen criteria, priors, and every concession live in
`prereg/SCORES_2026-09-02.md` — that file is the authority; this is only the shape:

- **C23 (first round):** no informative preregistered pass survives. A1/A2 were weakly
  informative by design, B1 failed the frozen binary rule, and B2 (temporal structure)
  was **WITHDRAWN** as a window-edge argmax artifact, established by the three controls
  in `c23_hra1_artifact_controls.py`. Recorded as a lesson for the later freezes.
- **C25–C28 (second round, preregistered contacts):** see SCORES for the per-criterion
  table. The strongest replicated empirical pattern across all open-data contacts is
  near-zero between-lane coupling with substantial discordant quadrants, across four
  independent paradigms; C28.1 (six-month MTMM) is the strongest lane-typing result in
  the corpus, and C28.3 is a real recorded FAIL with its concession.
- **C29 (model comparison):** two-lane M1 preferred over one-scalar M0 at **weak**
  strength under the frozen ΔBIC bands, with mandatory dual reporting (the frozen
  verdict is weak; the parametric-bootstrap calibration readout shows values this size
  essentially do not arise under M0-true at this n — both statements go together).
  "Single latent factor falsified" remains a claim we do NOT make.
- **C30 (external transport): FAIL — falsifier triggered.** M0 wins externally
  (IU-Hamburg); the frozen consequence stands verbatim: the theory takes a **claim
  boundary** here. The post-hoc measurement-floor reading is labeled diagnostic, not a
  rescue.
- **C31 (boundary adjudication):** H_M (measurement-quality explanation of the C30
  loss) is VIABLE and currently the better-supported rival; H_A (architectural) is
  NOT excluded. C31.2 external remains **unresolved (⊥)** — the sole independent
  qualifying open dataset is embargoed to 2031-08-25; the ROFL annex run proved
  cohort identity with rankStab, so it carries no independent adjudication weight.

The running PASS/FAIL tally is an **internal audit object, never an evidence headline** —
per the author's own rule, stated plainly here so nobody quotes a "score" as support.

## Machine-checked equation layer (`coq/`)

The manuscript's recalibration law and the discrete ADM stepper are formalized over
ℚ in Coq **8.20.1**. Compile and re-verify axiom-freedom:

```bash
cd coq
coqc -q recalibration.v
coqc -q adm_discrete.v
coqc -q -Q . "" recalibration_assumptions.v   # Print Assumptions for every lemma
coqc -q -Q . "" adm_assumptions.v
```

The two `*_assumptions.v` files print `Closed under the global context` for every
lemma — i.e. all results are **axiom-free**. The mapping from manuscript equation to
Coq lemma, with tiers and the honest list of what is *not* yet machine-checked, is in
`docs/COQ_EQUATION_LEDGER.md`.

## Reproducibility contract
- Every stochastic script fixes its seeds; archived outputs in `results/` state the
  exact numbers the manuscript quotes.
- Open-data tests were **preregistered before any outcome file was opened** — frozen
  criteria, locked falsifiers, and the recorded-and-wrong prior guesses are all in
  `prereg/` (v1/v2 for the first round; per-case freeze commits for C25–C31 are cited
  in `prereg/SCORES_2026-09-02.md`). Scored outcomes are kept in that SCORES file,
  separate from the frozen texts.
- The theory itself is **FROZEN** (v0.2: state → readout → internal lanes → action →
  outcome → feedback; typed, dynamically coupled). New anomalies go to a challenge
  ledger, not into the equations.

## Planned analyses (not yet run — help welcome)
- SOMA-READ flagship experiment (prereg/SOMA_READ_*): needs a psychophysiology lab
  with programmable haptics. Pilot N=20 → ethics → confirmatory N=120 (80/40 sealed).
- The formerly-listed rankStab analysis **has run** (as preregistered case C28) —
  see `TODO_planned_analyses.md` for the resolution record.

## Licensing
Code: MIT. Documents and preregistrations: CC BY 4.0.
The manuscript states its own license (CC BY 4.0) and correspondence address.

## Provenance
Built by the ANSE.ASIA research pipeline (human founder + AI sessions) with the
discipline recorded in the manuscript: tiered claims, full-text-or-NO-DATA holdings,
maker–checker review before public release. This repository was assembled after an
independent multi-agent adversarial review pass; the review's confirmed findings and
their dispositions are recorded in `docs/`.
