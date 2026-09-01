#!/usr/bin/env python3
"""S9 coupling-extension simulations (v10): closed-form checks P6-P8, gate K12,
and the double-dissociation classifier. Seeds fixed; planning tier."""
import numpy as np
from scipy.special import expit
DT, TMAX = 0.1, 15.0
def errhc(T, v, g0, dg, k, dmax=1.0, d0=0.0, tmax=10.0):
    vg = v + g0 + k
    dstar0, dstarc = T/vg, T/(vg+dg)
    if dstarc > dmax: return 0.0
    if dstar0 <= dmax: return tmax
    return (1.0/vg)*np.log((dstar0-d0)/(dstar0-dmax))
def sim_lat(rng, D, n, b0, b1, k=0.0, delta=0.0, tau=0.5, b_s=0.0, safety=0.0):
    ts = np.arange(0.0, TMAX, DT); Deff = D*(1.0+k)
    noise = rng.normal(0, 0.3, n)
    er = np.maximum((Deff - ts[None,:]) - delta + noise[:,None], 0.0)
    h = expit(b0 - b1*(er - tau) - b_s*safety)*DT
    fired = rng.random((n, len(ts))) < h
    anyf = fired.any(1)
    return np.where(anyf, ts[np.clip(fired.argmax(1),0,None)], TMAX)
def run_k12(n_cohorts=150, N=60, trials=24, k=0.5):
    fires={'pos':0,'neg':0}
    for c in range(n_cohorts):
        rng=np.random.default_rng(12000+c)
        for arm in ('pos','neg'):
            d_lat=[]; d_saf=[]
            for i in range(N):
                b0=-4.4+rng.normal(0,0.3); b1=max(0.35+rng.normal(0,0.05),0.01)
                s1=2.0+rng.normal(0,0.5); s2=2.0+rng.normal(0,0.5)
                if arm=='pos':
                    lc=sim_lat(rng,5.0,trials,b0,b1,k=k); li=sim_lat(rng,5.0,trials,b0,b1)
                else:
                    lc=sim_lat(rng,5.0,trials,b0,b1,b_s=0.6,safety=s1)
                    li=sim_lat(rng,5.0,trials,b0,b1,b_s=0.6,safety=s2)
                d_lat.append(lc.mean()-li.mean()); d_saf.append(s1-s2)
            d_lat=np.array(d_lat); d_saf=np.array(d_saf)
            X=np.column_stack([np.ones(N), d_saf])
            beta,*_=np.linalg.lstsq(X,d_lat,rcond=None)
            t=beta[0]/((d_lat-X@beta).std(ddof=2)/np.sqrt(N)+1e-9)
            if t<2.0: fires[arm]+=1
    return {a:fires[a]/n_cohorts for a in fires}
def run_dissociation(n_cohorts=200, N=40, n_sit=4, trials=32, k=0.5, delta=3.0):
    acc={'coupling_removal':0,'cue_locked':0}
    for c in range(n_cohorts):
        rng=np.random.default_rng(13000+c)
        for kind in acc:
            per=np.zeros((N,n_sit))
            for i in range(N):
                b0=-4.4+rng.normal(0,0.3); b1=max(0.5+rng.normal(0,0.05),0.01)
                for s in range(n_sit):
                    pre=sim_lat(rng,5.0,trials,b0,b1,k=k)
                    post=(sim_lat(rng,5.0,trials,b0,b1) if kind=='coupling_removal'
                          else sim_lat(rng,5.0,trials,b0,b1,k=k,delta=(delta if s==0 else 0.0)))
                    per[i,s]=pre.mean()-post.mean()
            m=per.mean(0); a=m.mean()
            sse_g=((m-a)**2).sum(); sse_c=(m[1:]**2).sum()
            acc[kind]+= (('coupling_removal' if sse_g<sse_c else 'cue_locked')==kind)
    return {k2:v/n_cohorts for k2,v in acc.items()}
if __name__ == '__main__':
    print('P7 v=0 no anchor:', errhc(1.0,0.0,0.2,0.6,0.0), '| with k=0.3:', round(errhc(1.0,0.0,0.2,0.6,0.3),3))
    print('P6 horizon lengthens:', round(errhc(1.0,0.3,0.2,0.6,0.0),3), '->', round(errhc(1.0,0.3,0.2,0.6,0.3),3))
    print('P8 removal collapses:', round(errhc(1.0,0.1,0.2,0.6,0.4),3), '->', errhc(1.0,0.1,0.2,0.6,0.0))
    print('K12 fires (pos should be low, neg high):', run_k12())
    print('double-dissociation classifier accuracy:', run_dissociation())
