# SOMA-READ v1.0 — Locked Analysis Plan

## Primary causal model
Fit a hierarchical mixed model to R(t) during 0–12 s:

`R ~ time * endpoint_obs * agency_preserved * trait_fear_z + duration_s + (1 + time + endpoint_obs + agency_preserved | participant)`

Primary target: `endpoint_obs × agency_preserved` and its interaction with time. The predicted lowest R trajectory is non-observable endpoint + reduced agency.

## Policy-transition hazard
Discretize each trial into 1-s bins until first policy-onset event or censoring. Fit hierarchical logistic hazard models.

- M0: condition factors + elapsed time + trait fear + lagged distress + lagged autonomic features.
- M1: M0 + lagged R(t) + prespecified R-by-condition terms.

Primary mechanistic criterion: lagged R adds predictive information and is not eliminated by distress/physiology rivals.

## Sealed predictive holdout
- Fit coefficients using 80 participants.
- Open 40-participant holdout once.
- Primary metric: mean log loss.
- Confirmatory predictive advantage requires >=5% relative improvement for M1 over M0.
- Secondary: Brier score and time-dependent AUC.

## Cross-context transport
Estimate participant-specific Unknown×Agency effects in Context A with partial pooling. Predict Context-B effect direction/magnitude without redefining factors or thresholds.

## Multiplicity
H1–H3 are primary mechanistic hypotheses. H4–H6 are confirmatory-support/transport claims. Report exact effect estimates and intervals; do not promote secondary outcomes if primary tests fail.

## Missingness and censoring
Emergency stop is an action/event, never coded as harm. Hardware/synchronization failures are excluded only by frozen integrity rules. Do not remove unexpected responders.

## Claim ceiling
A positive result supports a bounded causal readout mechanism in this somatic task. It does not prove Readout Genesis universally, establish a psychiatric diagnosis, or validate a treatment.
