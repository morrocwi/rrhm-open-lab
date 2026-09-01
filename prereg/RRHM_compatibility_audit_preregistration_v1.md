# RRHM compatibility audit — preregistration of cases C6–C15

**Status:** written 1 September 2026, **before** the literature for cases C6–C15 was read.
**Anchor document:** *Why We Phobia?* v8 (Adversarial Review Edition, readout-anchored, battery-tested).
**Purpose:** fix what would count as consistent and what would count as inconsistent *in advance*, so that the audit cannot be scored to fit whatever the search returns.

---

## Why this file exists

The manuscript's own rule is `external compatibility ≠ direct validation`. A compatibility audit run *after* looking at the literature is worth very little, because every result can be narrated as compatible with a model flexible enough to accommodate it. The audit is only informative if the prediction, the falsifier, and the source set are named first.

**Cases C1–C5 were scored after looking and are recorded here as post-hoc.** They are kept for completeness but must not be counted as passed tests. Cases C6–C15 below are prospective.

| # | Case | Status |
|---|---|---|
| C1 | access vs assumption (instructed extinction) | post-hoc — do not count |
| C2 | latent, non-verbal updating | post-hoc — do not count |
| C3 | information gain over session count | post-hoc — do not count |
| C4 | safety behaviour classified by function | post-hoc — do not count |
| C5 | horizon readout needs time (slow vs fast threat) | post-hoc — do not count |

---

## Scoring rules, fixed in advance

Each case is scored into exactly one of four labels. No fifth label may be invented during the review.

- **SUPPORT-D** — the observed pattern matches the RRHM prediction *and* at least one named rival predicts the opposite or is silent. Discriminating.
- **SUPPORT-N** — the pattern matches, but a named rival predicts it equally well. Non-discriminating; carries no evidential weight for RRHM over that rival.
- **TENSION** — the pattern is the one named as the falsifier, or points against the prediction without settling it.
- **NO-DATA** — no study in the named source set addresses the prediction. This is the expected label for several cases and is not a failure of the search.

Additional rules:

1. **The prior guess is recorded before searching** and is scored afterwards. A case where the prior guess was wrong is more informative than one where it was right, and must be reported as such.
2. **A case may not be dropped after the search.** All ten are reported whatever they return.
3. **A rival must be named per case, in advance.** A prediction with no named rival cannot earn SUPPORT-D.
4. **Anything the author cannot access in full text is scored NO-DATA**, not inferred from an abstract.
5. Where the prediction is about specific phobia but the only evidence is fear conditioning in healthy volunteers, the case is capped at **SUPPORT-N**.

---

## C6 — Exit constraint should change the defensive *policy*, not the transition time

**Derived from:** Table 4 (four cells of the decisive experiment) and P5. Low `eRRH` with high `dRRH` → escape; low `eRRH` with low `dRRH` → freezing or distressed endurance.

**Prediction.** In phobic contexts where exit is structurally delayed or blocked (MRI bore, dental chair, aircraft cabin), the phenotype at matched fear should shift *away from* escape and *toward* distressed endurance and freezing, without the underlying transition occurring later. Termination rates should be low while distress and freezing indices are high.

**Consistent if:** premature-termination rates in scanner, dental and flight settings are low relative to reported distress, and freezing/endurance measures are correspondingly elevated.

**Inconsistent if:** at matched fear, escape frequency is the same in constrained and unconstrained settings — i.e. exit availability changes nothing about which defensive policy is chosen.

**Named rival:** threat-imminence accounts, which predict policy shifts from proximity, not from exit structure.

**Sources to check:** MRI claustrophobia and scan-termination literature; dental anxiety behavioural studies; flight phobia.

**Prior guess:** SUPPORT-N. Termination rates in scanners are known to be low against high distress, but imminence accounts can also produce this.

---

## C7 — Applied tension should be BII-specific, and specifically so

**Derived from:** P3. Rescue exists iff `v ≥ v* = T/d_max − g₀ − Δg`. Raising `Δg` moves the collapse boundary. In BII the collapse arises because `v(t) → 0` (vasovagal); in animal or height phobia `v` is not collapsing, so raising `Δg` should buy little.

**Prediction.** Applied tension should show a large effect in BII phobia and a small or absent one in animal and height phobia, and the BII benefit should track vasovagal susceptibility rather than fear level.

**Consistent if:** trials of applied tension in non-BII phobia are absent, null, or markedly smaller than in BII, and BII benefit is moderated by syncope history.

**Inconsistent if:** applied tension helps animal or height phobia about as much as BII. That would mean the benefit is generic arousal regulation, not a move on the damping term, and P3's reading of BII would be wrong.

**Named rival:** generic arousal-regulation accounts (any coping skill helps any phobia).

**Sources to check:** Öst & Sterner 1987 and the applied-tension trial literature; Ayala 2009 review; any applied-tension trial outside BII.

**Prior guess:** SUPPORT-D, with low confidence. I expect applied tension to be BII-specific in practice, but I do not know whether the specificity has been tested rather than assumed.

---

## C8 — Interoceptive load should shift transition earlier at matched fear

**Derived from:** ADM. Raising the drive `T` shortens `eRRH_C` (Eq. 6). Interoceptive load is a rise in `T` (or a fall in `v`) that is not a rise in objective external threat.

**Prediction.** CO₂ inhalation, voluntary hyperventilation, or physical exertion applied during exposure should move defensive transition earlier and reduce approach, *after adjusting for subjective fear and objective threat*. The effect should survive covarying fear ratings.

**Consistent if:** interoceptive manipulations shift behavioural approach or termination beyond their effect on fear ratings.

**Inconsistent if:** interoceptive load raises fear ratings but leaves approach and termination unchanged once fear is covaried. That is the falsifier: it would mean the horizon adds nothing to fear intensity in exactly the manipulation the model says should move it.

**Named rival:** allostatic self-efficacy and anxiety-sensitivity accounts, which also predict interoceptive load matters — but through confidence, not through a temporal margin.

**Sources to check:** CO₂-challenge literature; interoceptive exposure trials; behavioural approach tests under physiological load.

**Prior guess:** NO-DATA. I doubt any study covaries fear and reports the residual effect on termination timing.

---

## C9 — Remitters should retain residual, cue-specific miscalibration

**Derived from:** Eq. 1, `ε_tot > 0 ∀t`. A nonzero calibration error is the healthy default, so recovery cannot be the elimination of error. Remission is recalibration toward, not to, the causal horizon.

**Prediction.** Fully remitted phobic patients should remain distinguishable from never-phobic controls on a cue-specific measure even at symptomatic remission, and the size of that residual should predict relapse.

**Consistent if:** follow-up studies show residual cue-specific abnormality in remitters, and residual measures add to relapse prediction beyond symptom scores.

**Inconsistent if:** remitters are indistinguishable from controls on every cue-specific measure and relapse is unpredicted by any residual index. That would remove the model's distinctive claim about what remission is.

**Named rival:** inhibitory-learning accounts, which also predict retained but inhibited associations — note this may cap the case at SUPPORT-N.

**Sources to check:** Böhnlein 2020 systematic review; de Vos 2025; long-term follow-up and return-of-fear studies in specific phobia.

**Prior guess:** SUPPORT-N. The retained-association prediction is shared, so RRHM will probably not win here even if the pattern holds.

---

## C10 — Forced non-avoidant sampling should recalibrate without therapy

**Derived from:** §14.2. Cue-locking is inherited from the specificity of avoidance: the record channel is closed for one cue only. Anything that forces boundary sampling should recalibrate whether or not it is called treatment.

**Prediction.** Populations whose occupation or circumstance forces repeated non-avoidant contact with a cue should show lower prevalence and severity of that phobia; naturalistic remission should track incidental boundary contact rather than formal treatment.

**Consistent if:** occupational or circumstantial forced contact is associated with lower phobia rates, and naturalistic remitters report incidental contact.

**Inconsistent if:** rates are equal despite documented forced contact, or naturalistic remission is unrelated to contact. That would sever the maintenance mechanism from the phenotype.

**Named rival:** conditioning and extinction accounts, which predict the same thing for a different reason. Likely cap at SUPPORT-N.

**Sources to check:** Trumpf 2009 remission study; occupational epidemiology of specific phobia; natural-course studies.

**Prior guess:** SUPPORT-N, with a real risk of TENSION from healthy-worker selection, which would confound the comparison in the direction that makes the prediction look right for the wrong reason.

---

## C11 — Action *count* should be inert; deadline *geometry* should not

**Derived from:** the decisive experiment's matching rules (§12), which hold action number and efficacy constant and vary only `D`.

**Prediction.** Increasing the number of equally effective available actions, at a fixed deadline, should not change defensive-transition timing. Changing the deadline with a single action should.

**Consistent if:** studies varying number of response options at matched efficacy find no defensive-behaviour effect.

**Inconsistent if:** option count alone reliably changes defensive behaviour at matched efficacy and deadline. That would show the relevant variable is choice availability, not temporal geometry, and would collapse the model into a control account.

**Named rival:** perceived-control and learned-controllability accounts, which predict that option availability matters in itself.

**Sources to check:** controllability literature (Maier & Seligman 2016; Hartley 2014; Wood 2015); choice-availability manipulations in anxiety.

**Prior guess:** TENSION. My expectation is that the control literature has found availability effects independent of efficacy, which would count against the prediction as stated. Recording this because it is the case most likely to go against the model.

---

## C12 — Onset should follow *failed correction*, not merely high fear

**Derived from:** §14.1, where the onset hypothesis is cue locking plus PRHC plus premature termination plus avoidance plus restricted sampling.

**Prediction.** Retrospective and prospective onset studies should show that a first encounter in which an attempted coping action failed — or in which none was available — predicts phobia onset beyond the fear intensity of that encounter.

**Consistent if:** the presence or failure of a coping action at the index encounter adds predictive value over fear or event intensity.

**Inconsistent if:** onset is predicted by fear or aversive-event intensity alone, with no added contribution from whether a corrective action existed or worked.

**Named rival:** conditioning accounts, which predict onset from US intensity and contingency, and the verbal-information pathway, which predicts onset with no encounter at all.

**Sources to check:** pathways-to-fear literature; Trumpf 2010 incidence study; retrospective onset-event studies.

**Prior guess:** NO-DATA. Onset studies rarely code whether a coping action was available at the index event.

---

## C13 — In acrophobia, timing should track the correction window, not sway size

**Derived from:** Table 3, where the acrophobia row commits RRHM to winning on transition timing rather than on postural physiology.

**Prediction.** Avoidance and withdrawal timing at height should track the *estimated balance-correction window* — and should remain predictable after objectively measured sway magnitude is included.

**Consistent if:** sway magnitude does not fully account for avoidance, and a temporal or corrective-window measure adds to it.

**Inconsistent if:** measured sway or visual–vestibular mismatch fully accounts for avoidance behaviour. That is the row's own stated kill condition.

**Named rival:** visual–vestibular mismatch accounts.

**Sources to check:** Huppert, Wuehr & Brandt 2020; postural sway studies in visual height intolerance.

**Prior guess:** NO-DATA or TENSION. Sway studies exist; studies separating sway from a corrective-window estimate probably do not.

---

## C14 — Dental and choking paradigms should show *periodic* corrective windows

**Derived from:** A1 (§4.3), where nested recoverability is stated to fail in exactly these subtypes and the window-set form replaces the scalar horizon.

**Prediction.** Stop-signal requests during dental and swallowing procedures should cluster at phase-locked points — between swallows, at breath boundaries — rather than being uniformly distributed in time, and patients should show "wait for the next window" behaviour that a scalar horizon cannot express.

**Consistent if:** stop requests or distress peaks are phase-locked to swallowing or respiratory cycle.

**Inconsistent if:** stop requests are uniformly distributed with respect to those cycles. That would remove the empirical motivation for the window-set form and simplify the model back to A1.

**Named rival:** none named — this is a prediction RRHM makes largely alone, which is why it can earn SUPPORT-D if it holds.

**Sources to check:** dental anxiety behavioural literature; gag-reflex and swallow-phase studies; procedural distress timing.

**Prior guess:** NO-DATA. Phase-locking of stop requests is unlikely to have been measured.

---

## C15 — Panic should show the construct *without* the cue lock

**Derived from:** Gate K10 and §5.3, which places the model near Klein's suffocation false alarm and says the two part on cue locking.

**Prediction.** Panic disorder should show a horizon bias that is *generic* — present across cues and body states — while specific phobia shows the same bias confined to one cue. The disorders should differ in the shape of the bias, not in its presence.

**Consistent if:** CO₂ and interoceptive sensitivity in panic is broad and context-general, while in specific phobia the corresponding abnormality is cue-bound.

**Inconsistent if:** either (a) panic shows no comparable bias, which would make the construct narrower than claimed, or (b) panic shows the same cue-locked structure, which kills the specificity claim K10 is built on.

**Named rival:** Klein's suffocation false alarm, which predicts the panic half without needing a horizon at all.

**Sources to check:** Klein 1993; CO₂-sensitivity comparisons between panic and specific phobia; transdiagnostic comorbidity structure.

**Prior guess:** TENSION on the specificity side. High comorbidity between specific phobia and panic makes clean separation unlikely in existing samples.

---

## What this audit cannot do

None of these cases can validate RRHM. Every one of them uses data collected for other purposes, and none of the named source sets contains a study that programmes a deadline for engagement-preserving action while holding threat, exit, control, and action efficacy constant. The best possible outcome of the audit is that RRHM survives contact with what is already known and earns SUPPORT-D on one or two cases where the named rival is silent. The most useful outcome is a TENSION, because that is the only result that would change the manuscript.

**Prior guesses in summary, recorded before searching:** SUPPORT-D on C7 and possibly C14; SUPPORT-N on C6, C9, C10; TENSION on C11 and C15; NO-DATA on C8, C12, C13. Scored afterwards, this distribution is itself a check on whether the model's author can predict where his own theory will meet resistance.
