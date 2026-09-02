#!/usr/bin/env python3
"""R1 scaffold — escape-recoverability margin M^D per PREREG_REANALYSIS.md (frozen).

Status: SCAFFOLD. Blocked by design behind two gates: (1) R0 must reproduce first;
(2) PREREG-MAPPING (column mapping from structure-only inspection) must be committed
before any outcome value is computed. This file implements only the frozen DEFINITION so
the computation is fixed before the data is seen.

  M^D_t = T_catch,t - T_exit,t     (task geometry only; forbidden inputs: any neural
                                    signal, eventual escape, approach duration)
"""
import numpy as np

def t_catch(pac_pos, pac_vel, ghost_pos, ghost_vel):
    """Time until ghost reaches Pac-Man under current kinematics (1-D track distance).
    Closing speed <= 0 -> np.inf (no capture on current course)."""
    gap = np.abs(np.asarray(ghost_pos) - np.asarray(pac_pos))
    closing = np.asarray(ghost_vel) - np.asarray(pac_vel)
    closing = np.where(np.sign(ghost_pos - pac_pos) > 0, -closing, closing)
    with np.errstate(divide="ignore"):
        t = np.where(closing > 0, gap / closing, np.inf)
    return t

def t_exit(pac_pos, pac_speed, exit_dist):
    """Time for Pac-Man to reach the nearest viable exit at current speed."""
    with np.errstate(divide="ignore"):
        return np.where(np.asarray(pac_speed) > 0,
                        np.asarray(exit_dist) / np.asarray(pac_speed), np.inf)

def margin(pac_pos, pac_vel, pac_speed, ghost_pos, ghost_vel, exit_dist):
    """M^D_t; positive = exit reachable before capture on current kinematics."""
    return (t_catch(pac_pos, pac_vel, ghost_pos, ghost_vel)
            - t_exit(pac_pos, pac_speed, exit_dist))

if __name__ == "__main__":
    print("R1 scaffold: frozen M^D definition only. Gates: R0 reproduction, then "
          "PREREG-MAPPING commit, before any outcome is computed. M^D != eRRH.")
