# S9 — coupling-extension simulations (v10, 2026-09-02, planning tier)

ADM + external calm-anchor coupling: d' = T − (v+g0+k)d (anchor d_a≈0).
Independent implementation continuing S8's machinery; seeds fixed (12000+c, 13000+c).

## Sim 0 — closed-form checks (deterministic, Eq.6 with v→v+k)
- P7: v=0, no anchor → eRRH_C = 0 (collapse) · v=0, k=0.3 ≥ v*=0.2 → eRRH_C = 1.386 (rescue)
- P6: v=0.3, k:0→0.3 → eRRH_C 1.386 → 2.012 (horizon lengthens)
- P8: v=0.1, k:0.4→0 → eRRH_C 1.720 → 0 (shared-term removal collapses)

## Sim A — Gate K12 (capacity vs matched felt-safety; covaried contrast, t≥2 rule)
Generators: coupling (k on D_eff=D(1+k)) vs felt-safety-only (b_s=0.6 on hazard).
- N=60, 24 trials, k=0.5: fires pos 0.107 / neg 0.960 — TWO-SIDED. contrast +0.319 s / +0.004 s
- N=40, k=0.5: 0.247/0.980 · N=60, k=0.35: 0.413/0.960 (underpowered)
→ preregister with effect floor k≥0.5 or larger N. First untuned run (N=40, 12 trials,
k=0.35): 0.72/0.965 — recorded as the failure that set the floor.

## Sim B — double-dissociation classifier (uniform-shift vs target-only-shift SSE)
4 situations × N=40 × 32 trials, 200 cohorts/arm, pathology-sized effects (k=0.5, δ=3):
- accuracy: coupling_removal 1.00 · cue_locked 0.99
- small-effect runs (k=0.4, δ=1.5, ≤16 trials): accuracy 0.52–0.68 — effect-size floor
  is real and stated in the manuscript.

All numbers are properties of a toy design; nothing here is evidence about agoraphobia.
