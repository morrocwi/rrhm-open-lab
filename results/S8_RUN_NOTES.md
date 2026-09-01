# S8 — K3/K6/K8/K9 battery run notes (v9, 2026-09-01)

Independent re-implementation of ADM + Eq.4 hazard from the v8/v9 manuscript spec
(S1 engine not available in the executing environment). Main script:
`S8_rrhm_gates_k3_k6_k8_k9.py` (seeds fixed). Repaired variants (K3' split-half
disattenuation; K6' 2-SE rule + N=120/32 trials; K9' 2-SE rule) were run inline;
their exact definitions mirror the main script with the changes named in the
manuscript's Table 9. Sample-size sweeps:

- K3' fires pos/neg: N=40: 0.18/0.585 · N=120: 0.093/0.82 · N=220: 0.027/0.893
- K3 as written (observed r, N=40): 0.00/0.00 (mean neg |r| = 0.756)
- K6 as written (N=60, 16 trials): 0.05/0.21 · K6' (N=120, 32 trials, 2-SE): 0.10/0.317
- K8 as written: 0.01/1.00 (dELPD +10.4±3.8 / −0.77±1.1)
- K9 as written (N=60): 0.23/0.89 · K9' (2-SE): N=60: 0.02/0.43 · N=120: 0.167/0.95

Compatibility-audit searches (Section "Compatibility audit of preregistered
cases C6–C15"): PubMed E-utilities, 16 query cells + serial re-verification of
zero cells + PMC full-text retrieval attempts (both elink-returned PMC ids for
the C6/C13 targets resolved to cited-by articles, not the targets — recorded as
inaccessible). Watts & Sharrock 1984 (PMID 6514503) metadata + abstract verified
via esummary/efetch.

Figures fig1_adm_horizon.pdf / fig2_rank.pdf regenerated deterministically from
the manuscript's own closed-form Eq. 6 and the stated Fisher-rank results
(generation script inline in the session log; spot-checked: eRRH_C(0.5)=1.72,
eRRH_C(0.2)=1.28, collapse at v*<0.2 for Δg=0.6 — matches the v8 caption).
