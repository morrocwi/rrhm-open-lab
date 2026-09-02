# PRIMARY — Variant S (short, prediction-first; author-approved direction 2026-09-02)

Subject: A locked prediction about your Pac-Man data

Dear Dr. Staveland,

We reproduced your turnaround-by-reward result from your published Source Data
(0.1114 vs your 0.1115; code public).

We then publicly locked one prediction, with its failure criteria, before we — or
anyone using only public data — could compute it:

    A single task-geometry variable — the time remaining before capture minus the
    time needed to reach the exit — predicts turnaround timing in held-out subjects
    beyond ghost distance, speeds, trial type, reward, your threat CDF, and time.

We cannot test it: the 20 Hz position streams needed to compute it are not in the
public deposit. You can, in an afternoon. The lock (commits 98895aa/bf19562/66ca4eb, sealed by the tagged release
staveland-lock-v2), a fully pinned specification an implementer can run without
asking us anything, and the criteria under which we lose are all here:

https://github.com/morrocwi/rrhm-open-lab/tree/main/targets/staveland_2026

Our own recorded prior is only 0.45 — the point is not our confidence, but that
the prediction is locked and can lose. If it fails, we will record the failure
publicly, as we have done before — and either way, we would be glad to record
the outcome jointly. If we have misread your task geometry, we would value the
correction even more.

Best regards,
Yaoharee Lahtee
Open Civil Science Initiative, Bangkok

---
# DRAFT — GATED. Do not send until all four items exist (protocol step 6 + author ruling 2026-09-02):
# [x] 1. Reproduction table (Original vs Reproduced, with code+commit) — DONE b1d06d8
# [ ] 2. Frozen reanalysis (R1-v2, commit bf19562) — DONE, standing
# [3] transferred BY DESIGN to the data holders for Variant S (gate amendment in PREREG_REANALYSIS.md R1-v3)
# [ ] 4. One-page next experiment — DONE (NEXT_EXPERIMENT.md)
#
# The letter below is the POST-RESULT shape (both variants). The earlier theory-first
# draft is retired: it asked the team to read more than it gave them.

## Variant A — if R1v2.a PASSES
Subject: One preregistered variable adds out-of-sample information in your Pac-Man data

Dear Dr. Staveland,

We first independently reproduced the relevant published analyses from your public Zenodo
data and code (reproduction table and commits in the link below). We then froze, before
computing any outcome, a task-geometry variable — the time remaining before capture minus
the time needed to reach the exit — together with its failure criteria, and tested it with
leave-one-subject-out validation. It adds out-of-sample information about turnaround
timing beyond ghost distance, speeds, trial type, reward, and your threat CDF.

We would value your view on one question: does this reflect remaining effective
recoverability, or a simpler task feature we have missed? Everything (reproduction,
frozen prediction, held-out result, and a one-page task modification that would separate
the two readings prospectively) is in this single folder:
https://github.com/morrocwi/rrhm-open-lab/tree/main/targets/staveland_2026

We explicitly do not map theta or MFG activity onto any model construct, and we state up
front that your current task cannot adjudicate our model's central claim — the proposed
modification exists for that reason. If we have misunderstood the task geometry, we would
especially appreciate the correction.

## Variant B — if R1v2.a FAILS
Subject: A preregistered negative result from a reanalysis of your Pac-Man data

Dear Dr. Staveland,

We independently reproduced the relevant published analyses from your public data and
code, then preregistered and ran a reanalysis testing whether a kinematic
escape-recoverability margin adds out-of-sample information beyond your existing threat
variables. It does not. We record this as a failure of our model's prediction on your
dataset — the frozen criteria and the negative result are archived unedited.

The failure clarified an identifiability issue we think is interesting in itself: in the
current task, remaining actionability and threat proximity are nearly collinear. The
one-page task modification in the link separates them prospectively. If that distinction
seems redundant to you given your interpretation, that judgment is exactly what we are
asking for.
https://github.com/morrocwi/rrhm-open-lab/tree/main/targets/staveland_2026

Best regards,
Yaoharee Lahtee
Open Civil Science Initiative, Bangkok, Thailand

---
# RETIRED first draft (kept for provenance):

Subject: A preregistered follow-up prediction from your 2026 Pac-Man approach–avoidance study

Dear Dr. Staveland,

I have been studying your 2026 Nature Communications paper on cortical–limbic dynamics
during approach–avoidance conflict. The relationship between theta synchrony and approach
duration, together with the Chase–Strike dynamics in right MFG, led us to a narrower
question that I think may be experimentally separable from threat imminence itself.

We are developing a falsifiable model of defensive transition called the Regulatory
Recoverability Horizon Model (RRHM). Its narrow prediction is that transition timing
depends partly on the estimated time remaining before an effective action can no longer
preserve a viable ongoing trajectory.

Rather than asking you to evaluate the theory on narrative grounds, we have taken an
adversarial route. Before running any RRHM-specific analysis of your released data, we
publicly froze the prediction and its failure criteria. We are also independently
reproducing the relevant analyses from your public Zenodo data and code.

Our proposed next step has two parts. First, using the existing Pac-Man data, test whether
a task-geometry-derived escape-recoverability margin explains right-MFG and behavioral
dynamics beyond threat distance, reward and trial type. We explicitly do not treat this as
a direct test of eRRH. Second, we propose a minimal extension of the Pac-Man task that
separates a termination action from an engagement-preserving corrective action while
holding threat and perceived control constant. This would provide a direct test of the
model.

Everything — frozen predictions, reproduction code, null criteria and the proposed task
modification — is available in one reproducible package here:
https://github.com/morrocwi/rrhm-open-lab/tree/main/targets/staveland_2026

I am not asking for endorsement. The question I would most value your judgment on is
simply: do you think the distinction between threat imminence and remaining effective
recoverability is experimentally identifiable in this paradigm, or does your
interpretation already make the distinction redundant? If we have misunderstood any aspect
of the task geometry, I would especially appreciate the correction.

Best regards,
Yaoharee Lahtee
Open Civil Science Initiative
Bangkok, Thailand
