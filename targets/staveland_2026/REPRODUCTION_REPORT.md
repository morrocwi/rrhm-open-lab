# R0 — independent reproduction of the published analyses. Status: ⏳ NOT YET RUN

Nothing in this file may be cited until the runs exist. Planned scope (in order):
1. Behavioral: turnaround/reward behavior from the released behavioral files.
2. Theta synchrony ↔ approach duration (published pipeline, published parameters).
3. Chase vs Strike right-MFG HFA dynamics.

Technical plan (recorded before execution): the Zenodo archive is a single 77 GB zip;
full download is infeasible in the authoring environment. Strategy: HTTP range requests
against the zip central directory to enumerate members and pull ONLY the behavioral and
localization files first (implemented in `code/01_reproduce_staveland.py`); iEEG members
fetched selectively per analysis. The authors' released analysis code is to be located
from the paper's code-availability statement and vendored by reference (URL + commit),
never copied without license check.

Honesty rule: R0 uses ORIGINAL code and parameters — any deviation is listed here with
its reason. R0 contains zero RRHM content. If a published result does not reproduce, that
is reported to the authors privately FIRST, as a possible error on OUR side.
