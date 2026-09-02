(* ===================================================================== *)
(* recalibration.v — RRHM recalibration law, machine-checked over Q.     *)
(*                                                                       *)
(* Reference implementation:                                             *)
(*   code/calculators/recalibration.py                                   *)
(*     p_hat    = (nC + a) / (nC + nH + a + b)                           *)
(*     p_lesion = (nC + a) / (nC + nH + nE + a + b)                      *)
(*     n*       = max(0, floor(rho*b/(1-rho) - a) + 1)                   *)
(*     k_min nC = max(0, (rho*b/(1-rho) - (nC + a)) / a_anchor)          *)
(*                                                                       *)
(* Coq 8.20.1. No Admitted, no Axiom; all section variables are          *)
(* discharged into universally quantified statements on section close.   *)
(* ===================================================================== *)

Require Import QArith.
Require Import Qround.
Require Import Qminmax.
Require Import ZArith.
Require Import Lia.
Require Import Lqa.

(* ------------------------------------------------------------------ *)
(* Division helpers over Q                                            *)
(* ------------------------------------------------------------------ *)

Lemma Qdiv_mult_cancel : forall y z : Q, 0 < z -> y / z * z == y.
Proof.
  intros y z Hz.
  assert (Hz0 : ~ z == 0) by (intro E; lra).
  unfold Qdiv. rewrite <- Qmult_assoc.
  rewrite (Qmult_comm (/ z) z). rewrite Qmult_inv_r by exact Hz0.
  ring.
Qed.

(* x < y/z  <->  x*z < y   (z > 0) *)
Lemma Qlt_div_iff : forall x y z : Q, 0 < z -> (x < y / z <-> x * z < y).
Proof.
  intros x y z Hz. split; intro H.
  - apply (proj2 (Qmult_lt_r x (y / z) z Hz)) in H.
    rewrite Qdiv_mult_cancel in H by exact Hz. exact H.
  - apply Qlt_shift_div_l; assumption.
Qed.

(* y/z < x  <->  y < x*z   (z > 0) *)
Lemma Qdiv_lt_iff : forall x y z : Q, 0 < z -> (y / z < x <-> y < x * z).
Proof.
  intros x y z Hz. split; intro H.
  - apply (proj2 (Qmult_lt_r (y / z) x z Hz)) in H.
    rewrite Qdiv_mult_cancel in H by exact Hz. exact H.
  - apply Qlt_shift_div_r; assumption.
Qed.

(* Same numerator, larger denominator, smaller (or equal) quotient. *)
Lemma Qdiv_le_denom : forall x y z : Q,
  0 <= x -> 0 < y -> y <= z -> x / z <= x / y.
Proof.
  intros x y z Hx Hy Hyz.
  assert (Hz : 0 < z) by lra.
  apply Qle_shift_div_r; [exact Hz|].
  assert (E : x / y * z == x * z / y) by (unfold Qdiv; ring).
  rewrite E.
  apply Qle_shift_div_l; [exact Hy|].
  nra.
Qed.

(* Strictly positive numerator: quotient determines the denominator. *)
Lemma Qdiv_eq_denom_inj : forall x y z : Q,
  0 < x -> 0 < y -> 0 < z -> x / y == x / z -> y == z.
Proof.
  intros x y z Hx Hy Hz H.
  assert (Hy0 : ~ y == 0) by (intro E; lra).
  assert (Hz0 : ~ z == 0) by (intro E; lra).
  assert (Hx0 : ~ x == 0) by (intro E; lra).
  assert (Hm : x / y * (y * z) == x / z * (y * z)) by (rewrite H; reflexivity).
  assert (E1 : x / y * (y * z) == x * z * (y * / y)) by (unfold Qdiv; ring).
  assert (E2 : x / z * (y * z) == x * y * (z * / z)) by (unfold Qdiv; ring).
  rewrite E1, E2 in Hm.
  rewrite (Qmult_inv_r y Hy0) in Hm.
  rewrite (Qmult_inv_r z Hz0) in Hm.
  rewrite !Qmult_1_r in Hm.
  (* Hm : x * z == x * y  =>  z == y *)
  apply (proj1 (Qmult_inj_l z y x Hx0)) in Hm.
  symmetry; exact Hm.
Qed.

(* ================================================================== *)
(* Part 1 — Ledger vs lesion read (L1, L1b)                           *)
(* ================================================================== *)

Section Lesion.

Variables nC nH nE a b : Q.
Hypothesis HnE   : 0 <= nE.
Hypothesis Hnum  : 0 <= nC + a.                (* numerator nonnegative *)
Hypothesis Hden  : 0 < nC + nH + a + b.       (* clean denominator positive *)

Definition p_hat    : Q := (nC + a) / (nC + nH + a + b).
Definition p_lesion : Q := (nC + a) / (nC + nH + nE + a + b).

(* L1: censoring extra trials into the denominator can only lower the read. *)
Lemma L1_lesion_le_hat : p_lesion <= p_hat.
Proof.
  unfold p_lesion, p_hat.
  assert (E : nC + nH + nE + a + b == (nC + nH + a + b) + nE) by ring.
  rewrite E.
  apply Qdiv_le_denom; [exact Hnum | exact Hden | lra].
Qed.

(* L1b: with strictly positive numerator, equality holds iff nE = 0. *)
Lemma L1b_eq_iff : 0 < nC + a -> (p_lesion == p_hat <-> nE == 0).
Proof.
  intro Hpos. unfold p_lesion, p_hat. split; intro H.
  - (* equality of reads forces nE == 0 *)
    assert (E : nC + nH + nE + a + b == (nC + nH + a + b) + nE) by ring.
    rewrite E in H.
    assert (Hd2 : 0 < (nC + nH + a + b) + nE) by lra.
    assert (Hdeq : (nC + nH + a + b) + nE == nC + nH + a + b).
    { apply (Qdiv_eq_denom_inj (nC + a)); [exact Hpos | exact Hd2 | exact Hden | exact H]. }
    lra.
  - (* nE == 0 makes the two denominators equal *)
    rewrite H.
    assert (E : nC + nH + 0 + a + b == nC + nH + a + b) by ring.
    rewrite E. reflexivity.
Qed.

End Lesion.

(* ================================================================== *)
(* Part 2 — Dose minimality (nH = 0 case) and fading (L2..L5)         *)
(* ================================================================== *)

Section Dose.

Variable  rho : Q.
Variables a b : Z.
Hypothesis Hrho0 : 0 <= rho.
Hypothesis Hrho1 : rho < 1.
Hypothesis Ha    : (0 <= a)%Z.
Hypothesis Hb    : (0 < b)%Z.

(* threshold = rho*b/(1-rho) - a  — the real-valued admission cutoff *)
Definition threshold : Q := rho * inject_Z b / (1 - rho) - inject_Z a.

(* admission condition for n consecutive clean trials (nH = 0):
   (n+a)/(n+a+b) > rho *)
Definition admissible (n : Z) : Prop :=
  rho < inject_Z (n + a) / inject_Z (n + a + b).

Definition nstar : Z := Z.max 0 (Qfloor threshold + 1).

Lemma one_minus_rho_pos : 0 < 1 - rho.
Proof. lra. Qed.

(* Admission condition, cleared of divisions:
   for n >= 0, (n+a)/(n+a+b) > rho  <->  inject_Z n > threshold. *)
Lemma admissible_iff : forall n : Z,
  (0 <= n)%Z -> (admissible n <-> threshold < inject_Z n).
Proof.
  intros n Hn. unfold admissible, threshold.
  assert (HD : 0 < inject_Z (n + a + b)).
  { change 0 with (inject_Z 0). rewrite <- Zlt_Qlt. lia. }
  assert (HDsum : inject_Z (n + a + b) == inject_Z (n + a) + inject_Z b).
  { rewrite <- inject_Z_plus. reflexivity. }
  assert (HXsum : inject_Z (n + a) == inject_Z n + inject_Z a).
  { rewrite <- inject_Z_plus. reflexivity. }
  assert (H1r : 0 < 1 - rho) by lra.
  split; intro H.
  - (* forward *)
    apply (proj1 (Qlt_div_iff rho (inject_Z (n + a)) (inject_Z (n + a + b)) HD)) in H.
    rewrite HDsum in H.
    assert (Hcut : rho * inject_Z b / (1 - rho) < inject_Z (n + a)).
    { apply (proj2 (Qdiv_lt_iff (inject_Z (n + a)) (rho * inject_Z b) (1 - rho) H1r)).
      nra. }
    rewrite HXsum in Hcut. lra.
  - (* backward *)
    apply (proj2 (Qlt_div_iff rho (inject_Z (n + a)) (inject_Z (n + a + b)) HD)).
    rewrite HDsum.
    assert (Hcut : rho * inject_Z b / (1 - rho) < inject_Z (n + a))
      by (rewrite HXsum; lra).
    apply (proj1 (Qdiv_lt_iff (inject_Z (n + a)) (rho * inject_Z b) (1 - rho) H1r)) in Hcut.
    nra.
Qed.

Lemma nstar_nonneg : (0 <= nstar)%Z.
Proof. apply Z.le_max_l. Qed.

Lemma nstar_gt_threshold : threshold < inject_Z nstar.
Proof.
  apply Qlt_le_trans with (inject_Z (Qfloor threshold + 1)).
  - apply Qlt_floor.
  - rewrite <- Zle_Qle. apply Z.le_max_r.
Qed.

(* L2: nstar satisfies the admission condition. *)
Lemma L2_nstar_admissible : admissible nstar.
Proof.
  apply (proj2 (admissible_iff nstar nstar_nonneg)).
  apply nstar_gt_threshold.
Qed.

(* L3: no nonnegative integer below nstar is admissible —
   nstar is the LEAST admissible nonnegative integer. *)
Lemma L3_nstar_least : forall n : Z,
  (0 <= n)%Z -> (n < nstar)%Z -> ~ admissible n.
Proof.
  intros n Hn0 Hnlt Hadm.
  apply (proj1 (admissible_iff n Hn0)) in Hadm.
  (* n < nstar and n >= 0 force n < Qfloor threshold + 1, i.e. n <= floor *)
  assert (Hfl : (n <= Qfloor threshold)%Z).
  { unfold nstar in Hnlt. lia. }
  assert (Hle : inject_Z n <= inject_Z (Qfloor threshold)).
  { rewrite <- Zle_Qle. exact Hfl. }
  assert (Hup : inject_Z (Qfloor threshold) <= threshold) by apply Qfloor_le.
  lra.
Qed.

(* ---------------------------------------------------------------- *)
(* Fading schedule k_min                                            *)
(* ---------------------------------------------------------------- *)

Variable a_anchor : Q.
Hypothesis Hanchor : 0 < a_anchor.

Definition k_min (nC : Q) : Q :=
  Qmax 0 ((rho * inject_Z b / (1 - rho) - (nC + inject_Z a)) / a_anchor).

(* L4: k_min is antitone in nC. *)
Lemma L4_k_min_antitone : forall nC1 nC2 : Q,
  nC1 <= nC2 -> k_min nC2 <= k_min nC1.
Proof.
  intros nC1 nC2 H12. unfold k_min.
  apply Q.max_lub.
  - apply Q.le_max_l.
  - apply Qle_trans with
      ((rho * inject_Z b / (1 - rho) - (nC1 + inject_Z a)) / a_anchor);
      [| apply Q.le_max_r].
    unfold Qdiv at 2 4.
    apply Qmult_le_compat_r.
    + lra.
    + apply Qlt_le_weak, Qinv_lt_0_compat, Hanchor.
Qed.

(* L5: at the minimal admissible dose nstar, no anchor boost is needed. *)
Lemma L5_k_min_nstar_zero : k_min (inject_Z nstar) == 0.
Proof.
  unfold k_min. apply Q.max_l.
  apply Qle_shift_div_r; [exact Hanchor|].
  assert (H := nstar_gt_threshold). unfold threshold in H.
  lra.
Qed.

End Dose.
