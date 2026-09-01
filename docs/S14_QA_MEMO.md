# S14 — SOMA-READ v1.0 bundle: QA memo (independent pre-freeze QA, 2026-09-02)

Reviewed: Protocol DOCX (2,606 words, rendered clean per authoring session; manipulation
checks, ethics x8, consent x4, emergency-stop x6 all present) · Preregistration YAML ·
Data Dictionary CSV · Locked Analysis Plan MD.

## Consistency with the RRHM/Readout corpus — PASS
- Anti-circularity (K1): R(t) measured continuously and prospectively; policy_onset is a
  separate event stream; nothing computed from the outcome it predicts. ✓
- The 2x2 (endpoint observability × somatic agency) operationalizes exactly the
  unobservable-D one-cell extension introduced with PRHC-U (v12 §prhcu) plus the
  agency clamp — the decisive experiment's own family. ✓ No contradiction with any
  frozen prereg case; H2 is the laboratory form of C19; kill list mirrors our gate
  discipline (each hypothesis can die separately). ✓
- Claim ceiling stated ("one bounded human causal readout domain") — matches the
  standing compatibility ≠ validation rule. ✓
- Safety forbidden-list matches the paper's §Safety verbatim in spirit (incl. no
  prolonged maximal mouth opening). ✓
- 0–12 s pure-informational window is a genuine improvement over the paper's design
  (identical stimulation + no action available → early R(t) differences cannot be
  attributed to differential stimulation or action use). ✓

## Findings for the protocol authors to consider BEFORE final freeze
(FROZEN_DRAFT_PENDING_PILOT — these are pilot-phase items, not post-hoc edits)
1. **2-D joystick couples the two reported lanes.** R on X and E on Y of one stick
   risks motor cross-talk (artifactual correlation or decorrelation between the very
   lanes H4 tests). Pilot must include a lane-report validity check (e.g., one-lane
   blocks or separated controls) and an a-priori rule for what cross-talk level voids H4.
2. **H6's fixed 5% log-loss threshold at sealed N=40 has no SE guard.** Our K9 run
   showed fixed ELPD-type thresholds leak/starve with N; recommend preregistering the
   5% jointly with an uncertainty rule (e.g., improvement ≥5% AND ≥2×SE of the
   holdout-loss difference) before the seal.
3. Minor: R(t) probe wording differs slightly between narrative and YAML — freeze one
   canonical sentence (both Thai and English versions) in the final protocol.

## Provenance note on E1 Audits A/B (peer session)
The ~25 intervention/longitudinal PMIDs coded in Audits A/B were located and read at
abstract level by the protocol authors, not re-verified here. Before any publication
that cites them, run this session's standard esummary/abstract verification sweep
(the v7 procedure). The architectural corrections they forced (typed→dynamically
coupled→S→R→(E,B,P)→A→O with feedback; Theory v0.2 FROZEN) are recorded as the
current frozen state.

## Next real-world steps (unchanged from authoring session)
1. Find collaborating lab (psychophysiology + programmable haptics)
2. Pilot N=20 → freeze hardware/noise thresholds + resolve QA items 1–3
3. Ethics submission → confirmatory N=120 (80 train / 40 sealed)
