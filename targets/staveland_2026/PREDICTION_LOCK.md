# Prediction lock — where the lock lives

**The binding, operationally frozen prediction for this target is in
[`PREREG_REANALYSIS.md`](PREREG_REANALYSIS.md)** — freeze commits 98895aa (original) ·
663aadf (mapping) · bf19562 (R1-v2, held-out criteria, prior 0.45) · 66ca4eb (R1-v3,
fully pinned canonical spec) and the cohort pin — sealed by the tagged release
`staveland-lock-v3` (final; v1/v2 are earlier seals superseded by it).

## Historical note
An earlier same-day lock of this prediction exists in a separate working session; it has
not been imported here and nothing in this package depends on it. The binding lock is the
one above, and any future import will be recorded as an addition, never a substitution — and unless and until it is imported with its own hash, it has no standing: the freeze above is the only lock.
