#!/usr/bin/env python3
"""Recalibration-law calculators (RRHM v13+, exact rationals).

Ledger:   p_hat = (nC + a) / (nC + nH + a + b)          [clean typing]
Lesion:   p_bad = (nC + a) / (nC + nH + nE + a + b)     [censored tallied as outcomes]
Dose:     n*    = floor( (rho*b)/(1-rho) - a ) + 1 (clamped >= 0), rho = tau_corr / D_bar_C
Fading:   k_min(nC) = max(0, ((rho*b)/(1-rho) - (nC + a)) / a_anchor)

Status: Dr-tier bridge to any clinical reading; algebra is toy-exact.
Run:  python3 recalibration.py            (worked example from the manuscript)
      python3 recalibration.py nC nE nH a b tau D_bar [a_anchor]
"""
import sys
from fractions import Fraction as F
from math import ceil

def p_hat(nC, nH, a, b):
    return F(nC + a, nC + nH + a + b)

def p_lesion(nC, nH, nE, a, b):
    return F(nC + a, nC + nH + nE + a + b)

def n_star(rho, a, b):
    # strict margin p_hat > rho  =>  n > (rho*b)/(1-rho) - a ; at integer boundary
    # the strict inequality requires the NEXT integer (review fix, 2026-09-02)
    from math import floor
    x = (rho * b) / (1 - rho) - a
    return max(0, floor(x) + 1)

def k_min(nC, rho, a, b, a_anchor):
    x = ((rho * b) / (1 - rho) - (nC + a)) / a_anchor
    return max(F(0), x)

def demo():
    a = b = 1
    nC, nE, nH = 2, 20, 0
    print("Worked ledger example (manuscript v13):")
    print("  lesion read p' =", p_lesion(nC, nH, nE, a, b), "=", float(p_lesion(nC, nH, nE, a, b)))
    print("  clean  read p  =", p_hat(nC, nH, a, b), "=", float(p_hat(nC, nH, a, b)))
    rho, a2, b2, anch = F(1, 6), 1, 30, 6
    print("Dose n* (rho=1/6, a=1, b=30):", n_star(rho, a2, b2))
    print("Fading schedule k_min(nC):")
    for n in range(0, n_star(rho, a2, b2) + 1):
        print(f"  nC={n}: k_min = {k_min(n, rho, a2, b2, anch)}")

if __name__ == "__main__":
    if len(sys.argv) >= 8:
        nC, nE, nH, a, b = map(int, sys.argv[1:6])
        tau, dbar = map(F, sys.argv[6:8])
        rho = tau / dbar
        print("p_lesion =", p_lesion(nC, nH, nE, a, b))
        print("p_clean  =", p_hat(nC, nH, a, b))
        print("n*       =", n_star(rho, a, b))
        if len(sys.argv) > 8:
            anch = F(sys.argv[8])
            for n in range(0, n_star(rho, a, b) + 1):
                print(f"k_min({n}) = {k_min(n, rho, a, b, anch)}")
    else:
        demo()
