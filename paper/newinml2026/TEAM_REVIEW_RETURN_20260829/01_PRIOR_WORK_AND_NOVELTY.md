# Prior work and novelty

## Which preprints matter?

| Priority | DOI | Role |
| --- | --- | --- |
| **Primary** | [10.5281/zenodo.21210575](https://doi.org/10.5281/zenodo.21210575) | Original public FCO custody concept (2026-07-05) |
| **Secondary** | [10.5281/zenodo.21382831](https://doi.org/10.5281/zenodo.21382831) | FCO/FCG architecture + selective replay (2026-07-15) |
| **Optional** | [10.5281/zenodo.21829929](https://doi.org/10.5281/zenodo.21829929) | FCO v4/v5 PASS/FAIL/ABSTAIN grammar — **omit unless explicitly adopted** |

**Do not add** for NewInML main text: Antigence tier-0 (18109862), Antigence custody matrix (21830287), Shadow Dogma (21830361), XenoDisorder (21830386).

## Classification

- FCO/FCG custody machinery → **SHARED_PREEXISTING_INFRASTRUCTURE** / **PRIOR_METHOD_WORK**
- Biomedical verify-or-abstain audits (GAP, G1/G2/G3, EXP-006) → **TEAM_CORE**
- Successor ClinVar/FASTA from PR #1 → **TEAM_CONTRIBUTED** (hash-admitted, fork not merged)

## Does current wording conflict?

`main.tex` does **not** say “we introduce FCO/FCG” or “novel/first.” Good.

**Gap:** §3 figure and §6 name **FCG** / content-addressed custody without citing prior Zenodo work. **Recommended action:** add Related Work cites (see `03_PROPOSED_MANUSCRIPT_EDITS.md`).

Abstract “We present an evidence-pipeline reliability study” → **KEEP** (team empirical scope).

## Default citation language

> Prior work introduced a content-addressed custody framework for deterministic computational biology and AI-agent provenance. Protein Hinge applies related custody concepts within a bounded verify-or-abstain biomedical evidence workflow.

Full audit: `final_team_evidence_audit/PREPRINT_PRIOR_WORK_SUGGESTIONS.md`
