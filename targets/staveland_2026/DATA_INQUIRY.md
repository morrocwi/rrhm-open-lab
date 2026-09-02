# Minimal data-availability inquiry (separate channel from the science letter)

Status: DRAFT — founder's decision to send. This is NOT the gated science email; it is a
short, giving-first note that reports a verified discrepancy and asks one factual question.
Sending it does not consume the post-result letter.

Subject: Behavioral data files for the Pac-Man iEEG deposit (Zenodo 17726565)?

Dear Dr. Staveland,

We are independently reproducing the analyses from your 2026 Nature Communications paper,
working from the public Zenodo deposit (17726565) and your two released code repositories.
Before writing, we verified carefully: the deposit's archive contains the per-subject
epoched iEEG .fif files (we enumerated the archive index and fully checked one subject's
file), but no behavioral files, and the epochs carry no metadata or game-state channels —
while the record description mentions behavioral data, and your analysis code reads
per-subject `*_raw_behave.csv` files produced by the `states2csv` notebooks.

Could you point us to the behavioral files (or let us know if a separate release is
planned)? We would be glad to report anything useful from the reproduction back to you.

Best regards,
Yaoharee Lahtee — Open Civil Science Initiative, Bangkok
(Working notes, verification steps, and our preregistered reanalysis plan are public:
https://github.com/morrocwi/rrhm-open-lab/tree/main/targets/staveland_2026)
