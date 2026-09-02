(* =========================================================================
   adm_discrete.v — DISCRETE anchor-drive model step over Q  (Coq 8.20.1)

   Model (all quantities exact rationals, exact Qeq equality — no reals,
   no limits, no continuum injected; the step size h is a finite tick):

     step size    h : Q,  h > 0
     drive        T : Q,  T >= 0
     dissipation  r : Q,  r > 0        (r stands for v + g)
     update map   F(d) := d + h * (T - r * d)
     fixed point  dstar := T / r       (division needs r <> 0, carried
                                        as the hypothesis r > 0)

   All lemmas are closed under the global context (no Admitted, no Axiom,
   no Parameter) — see adm_assumptions.v for the Print Assumptions audit.
   ========================================================================= *)

Require Import QArith.
Require Import Qfield.
Require Import Lqa.

Section ADM.

Variables h T r : Q.

Hypothesis Hh : 0 < h.        (* finite positive tick *)
Hypothesis HT : 0 <= T.       (* nonnegative drive *)
Hypothesis Hr : 0 < r.        (* positive dissipation, r = v + g *)

(* The one-step update map. *)
Definition F (d : Q) : Q := d + h * (T - r * d).

(* The anchor equilibrium. *)
Definition dstar : Q := T / r.

(* r <> 0, needed for every use of division. *)
Lemma r_nonzero : ~ r == 0.
Proof. lra. Qed.

(* -------------------------------------------------------------------------
   1. dstar is a fixed point of F (exact Qeq).
   ------------------------------------------------------------------------- *)
Lemma fixed_point : F dstar == dstar.
Proof.
  unfold F, dstar. field. apply r_nonzero.
Qed.

(* -------------------------------------------------------------------------
   2. Exact contraction identity — pure field algebra over Q, for ALL d:
        F d - dstar == (1 - h*r) * (d - dstar).
   ------------------------------------------------------------------------- *)
Lemma contraction_identity :
  forall d : Q, F d - dstar == (1 - h * r) * (d - dstar).
Proof.
  intro d. unfold F, dstar. field. apply r_nonzero.
Qed.

(* -------------------------------------------------------------------------
   3. Monotone approach in the stable regime 0 < h*r < 1:
      below the anchor the state strictly rises but never overshoots;
      above the anchor it strictly falls but never undershoots.
   ------------------------------------------------------------------------- *)
Lemma monotone_below :
  forall d : Q,
    0 < h * r -> h * r < 1 -> d < dstar ->
    d < F d /\ F d < dstar.
Proof.
  intros d Hlo Hhi Hd.
  pose proof (contraction_identity d) as Hc.
  set (k := h * r) in *.
  split; nra.
Qed.

Lemma monotone_above :
  forall d : Q,
    0 < h * r -> h * r < 1 -> dstar < d ->
    F d < d /\ dstar < F d.
Proof.
  intros d Hlo Hhi Hd.
  pose proof (contraction_identity d) as Hc.
  set (k := h * r) in *.
  split; nra.
Qed.

(* -------------------------------------------------------------------------
   4. Collapse / engagement-feasibility boundary:
      the anchor sits strictly below the capacity ceiling dmax
      iff the drive is strictly below r * dmax.
      (The manuscript's  v* = T/dmax - g  boundary, read over Q:
       dstar < dmax  <->  T < (v+g) * dmax.)
   ------------------------------------------------------------------------- *)
Lemma collapse_boundary :
  forall dmax : Q, 0 < dmax -> (dstar < dmax <-> T < r * dmax).
Proof.
  intros dmax Hdm.
  assert (Hrd : r * dstar == T)
    by (unfold dstar; field; apply r_nonzero).
  split; intro Hlt; nra.
Qed.

End ADM.
