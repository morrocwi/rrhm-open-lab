# Planned analyses (registered intent; not yet run)

## rankStab lane-trajectory separability (blocked on tooling in the authoring environment)
Dataset: Zenodo 7323547 (rankStab_R1.zip) — 120 individuals, longitudinal fear
conditioning; SCR, ratings, fMRI reliability data as .RData.
Status: RESOLVED 2026-09-02 — pyreadr unblocked .RData; run as preregistered case C28
(freeze 84f55a7, mapping 1fa0d4d, results 0d2acd8; see prereg/SCORES_2026-09-02.md).
Intent (freeze before opening outcomes, per the corpus discipline):
test whether the rating lane and SCR lane show distinct cross-phase stability
(typed-but-coupled signature) rather than a single shared stability ordering.
To run: open data/dataRat_RankStab.RData and data/dataSCR_RankStab.RData in R,
compute per-lane cross-phase rank stability, compare orderings across lanes.
If you run this: freeze your criteria first, and report wrong guesses.
