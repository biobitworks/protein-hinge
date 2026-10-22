# Minimal manuscript delta (recommendation only)

**This audit did not modify `main.tex`.**

Status: **MINIMAL_RECOMMENDED** — optional hygiene, not required to make a generator work.

## Do not do

- Do not merge PR #1.
- Do not reintroduce 24.6%, 14.0%, 51.2%, “silent error rate”, or structure-prediction-tool claims into the NewInML Results.
- Do not average historical 742/642 with contemporary 746/364.
- Do not describe EXP-006 as a positive morphology result.
- Do not describe EXP-005 as executed.

## Optional (if a follow-up commit is authorized)

1. One sentence that **all 16 residue mismatches in the successor G1 evaluation were TAFAZZIN** (already implied by not claiming gene-general silent error; would reduce reviewer over-read).
2. One sentence that successor ClinVar/FASTA bytes are **hash-admitted from team PR #1** and are not in the anonymous main tree.
3. Replace “206 MB” with an exact byte count after a zip re-hash, or cite the existing zip receipt hash.
4. Checklist already answers reproducibility **No** for full G1/G2 chains in the anonymous packet — keep that.

## Not recommended

Importing Elvis generated Table 2–4 (ablation / per-gene / decline) into the NewInML page budget without rewriting claim ceilings. Those tables encode silent-error rates the canonical paper correctly refused.
