# Coq equation ledger — manuscript claim ↔ machine-checked lemma

Maps each manuscript equation/claim to its Coq formalization (Coq **8.20.1**, over ℚ),
with the tier it earns. Verification: compile `coq/recalibration.v` and
`coq/adm_discrete.v`, then `coq/recalibration_assumptions.v` and
`coq/adm_assumptions.v`, which run `Print Assumptions` on every lemma — each prints
`Closed under the global context`, i.e. **axiom-free**.

```bash
cd coq
coqc -q recalibration.v
coqc -q adm_discrete.v
coqc -q -Q . "" recalibration_assumptions.v
coqc -q -Q . "" adm_assumptions.v
```

## Governed claims (tier Th_coqc — axiom-free, verified via Print Assumptions)

### Recalibration law (`coq/recalibration.v`)

| manuscript equation / claim | Coq lemma | tier |
|---|---|---|
| Lesion read never exceeds the clean read (p_lesion ≤ p̂) | `recalibration.v#L1_lesion_le_hat` | Th_coqc |
| Equality holds iff the erased count is zero (p_lesion = p̂ ↔ nE = 0) | `recalibration.v#L1b_eq_iff` | Th_coqc |
| Division-cleared admission condition: (n+a)/(n+a+b) > ρ ↔ n > threshold | `recalibration.v#admissible_iff` | Th_coqc |
| The dose n* is admissible, and n* ≥ 0 | `recalibration.v#L2_nstar_admissible`, `recalibration.v#nstar_nonneg` | Th_coqc |
| n* is the LEAST admissible dose (the floor+1 review fix, machine-checked) | `recalibration.v#L3_nstar_least` | Th_coqc |
| Fading requirement k_min is antitone in the counter-count nC | `recalibration.v#L4_k_min_antitone` | Th_coqc |
| At the dose n*, the fading requirement vanishes: k_min(n*) = 0 | `recalibration.v#L5_k_min_nstar_zero` | Th_coqc |

Note (verified 2026-09-02): the discharged lemma statements do **not** carry the
hypothesis 0 ≤ ρ — the section variable `Hrho0 : 0 <= rho` is never used, so the
theorems hold for any ρ < 1. This is *stronger* than the informal manuscript spec,
which assumes ρ ∈ [0, 1).

### Discrete ADM stepper (`coq/adm_discrete.v`)

| manuscript equation / claim | Coq lemma | tier |
|---|---|---|
| Regulation rate is nonzero (division by r is licensed) | `adm_discrete.v#r_nonzero` | Th_coqc |
| d* = T/r is a fixed point of the stepper: F(T/r) = T/r | `adm_discrete.v#fixed_point` | Th_coqc |
| Exact contraction identity: F(d) − d* = (1 − hr)(d − d*) | `adm_discrete.v#contraction_identity` | Th_coqc |
| Monotone approach from below (d < d* ⇒ d ≤ F(d) ≤ d*) | `adm_discrete.v#monotone_below` | Th_coqc |
| Monotone approach from above (d* < d ⇒ d* ≤ F(d) ≤ d) | `adm_discrete.v#monotone_above` | Th_coqc |
| Collapse boundary: d* < dmax ↔ T < r·dmax (the v* boundary reading) | `adm_discrete.v#collapse_boundary` | Th_coqc |

## NOT yet governed (honest list)

| manuscript equation / claim | why not machine-checked | tier |
|---|---|---|
| Continuous-time ADM ODE closed form | needs real analysis; the discrete stepper above is the readout-first primary object per the workspace discipline | — (readout of the governed discrete form) |
| Hazard model h = σ(β0 − β1·M) | empirical statistical model, not a theorem — there is nothing to prove, only to fit | finite_diagnostic |
| PRHC additive bias and PRHC-U | structural hypotheses, not derived results | Dr |
| Coupling extension dynamics (eq:companion) | structural hypothesis; simulated, not proved | Dr |
| REPL laws | stated laws of the readout architecture, not theorems | Dr |
| All open-data results (C23–C31) | empirical outcomes of preregistered tests — not provable, only reproducible (see `prereg/SCORES_2026-09-02.md`) | finite_diagnostic |
