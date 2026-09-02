(* Assumption audit for recalibration.v — every lemma must print
   "Closed under the global context". *)

Require Import recalibration.

(* Helpers *)
Print Assumptions Qdiv_mult_cancel.
Print Assumptions Qlt_div_iff.
Print Assumptions Qdiv_lt_iff.
Print Assumptions Qdiv_le_denom.
Print Assumptions Qdiv_eq_denom_inj.

(* Part 1 — ledger vs lesion *)
Print Assumptions L1_lesion_le_hat.
Print Assumptions L1b_eq_iff.

(* Part 2 — dose minimality and fading *)
Print Assumptions one_minus_rho_pos.
Print Assumptions admissible_iff.
Print Assumptions nstar_nonneg.
Print Assumptions nstar_gt_threshold.
Print Assumptions L2_nstar_admissible.
Print Assumptions L3_nstar_least.
Print Assumptions L4_k_min_antitone.
Print Assumptions L5_k_min_nstar_zero.
