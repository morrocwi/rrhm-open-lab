#!/usr/bin/env python3
"""Deterministic regeneration of manuscript Figures 1-2 from the stated equations.
Fig 1: closed-form horizon eRRH_C(v) (ADM; T=1, g0=0.2, dmax=1, d0=0, tau_max=10).
Fig 2: design-level Fisher-information ranks (3,3,3,4,4,5) as reported."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
NAVY, SLATE, BLUE, RED = '#17263A', '#5A6877', '#315D86', '#B0413E'
T, g0, dmax, d0, tmax = 1.0, 0.2, 1.0, 0.0, 10.0
def errhc(v, dg):
    dstar0, dstarc = T/(v+g0), T/(v+g0+dg)
    if dstarc > dmax: return 0.0
    if dstar0 <= dmax: return tmax
    return (1.0/(v+g0))*np.log((dstar0-d0)/(dstar0-dmax))
vs = np.linspace(0.01, 1.2, 400)
fig, ax = plt.subplots(figsize=(4.6, 3.1))
for dg, c, ls, lab in [(0.6, NAVY, '-', r'$\Delta g=0.6$'), (1.0, BLUE, '--', r'$\Delta g=1.0$')]:
    ax.plot(vs, [errhc(v, dg) for v in vs], color=c, ls=ls, lw=1.8, label=lab)
ax.axvline(0.2, color=RED, lw=0.8, ls=':')
ax.set_xlabel(r'intrinsic damping $v$ (a.u.)'); ax.set_ylabel(r'$\mathrm{eRRH}_C$ (a.u.)')
ax.set_ylim(-0.3, 10.6); ax.legend(frameon=False, fontsize=8)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('fig1_adm_horizon.pdf'); plt.close()
labels = ['2 deadlines','3 deadlines','4 deadlines','Module F','probes','probes +\nModule F']
ranks = [3,3,3,4,4,5]
fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.bar(labels, ranks, color=[RED if r<5 else NAVY for r in ranks], width=0.62)
ax.axhline(5, color=SLATE, lw=0.8, ls='--')
ax.set_ylabel('rank of design Fisher\ninformation (of 5)'); ax.set_ylim(0, 5.8)
ax.tick_params(axis='x', labelsize=7.5); ax.spines[['top','right']].set_visible(False)
plt.tight_layout(); plt.savefig('fig2_rank.pdf'); plt.close()
print('figures written: fig1_adm_horizon.pdf fig2_rank.pdf')
