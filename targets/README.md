# targets/ — conversation packages with published research

Each subfolder is a single-door package built FOR one published study, so its authors can
evaluate our engagement in minutes without reading the whole manuscript. The protocol
(binding, in order — no step may borrow credit from a later one):

1. **VERIFY** — paper DOI, authors, dataset accession confirmed field-by-field before
   anything is written (no relayed citations).
2. **PREDICTION LOCK** — falsifiable predictions + failure criteria frozen by public
   commit BEFORE any target data is opened.
3. **R0 REPRODUCE** — original data + original code → original result, independently,
   before any of our own analysis. No RRHM content in this step.
4. **FREEZE REANALYSIS** — our new analysis preregistered (criteria, covariates, FAIL
   conditions) before outcomes are computed.
5. **RUN** — binary scoring against the freeze; FAILs recorded, never reinterpreted.
6. **CONTACT** — one link to the target folder, not the repo root; the ask is a specific
   scientific judgment, never endorsement.
7. **PROPOSE** — the experiment the existing dataset cannot answer, specified to be
   runnable by the target lab.

Status legend: ✅ done · 🔒 frozen · ⏳ pending · ⊥ blocked/unresolved.

| target | paper | status |
|---|---|---|
| staveland_2026 | 10.1038/s41467-026-70287-5 (Nat Commun) | R0-1 reproduced ✅ · prediction locked 🔒 (release staveland-lock-v3) · R1 awaits the data holders |
