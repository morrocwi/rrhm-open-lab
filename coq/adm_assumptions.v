(* =========================================================================
   adm_assumptions.v — axiom audit for adm_discrete.v
   Compile:  coqc -q -Q . "" adm_assumptions.v
   Every lemma must print "Closed under the global context".
   ========================================================================= *)

Require Import adm_discrete.

Print Assumptions r_nonzero.
Print Assumptions fixed_point.
Print Assumptions contraction_identity.
Print Assumptions monotone_below.
Print Assumptions monotone_above.
Print Assumptions collapse_boundary.
