# Team PR #1 Contribution Summary

**PR:** [biobitworks/protein-hinge#1](https://github.com/biobitworks/protein-hinge/pull/1)  
**Fork:** ElvisHan2022/protein-hinge  
**Branch:** `healthomics-lane`  
**Head:** `6e47dbe367d9223c15c80ef27ca2634b50054035`  
**Author (Git metadata):** Elvis Han (`ElvisHan2022`)

> Git author/committer metadata is contribution evidence, not proof of human authorship.

## Scope

52 files differ from `paper/newinml-fcg-20260828` (no merge performed).

## Classification counts

| Class | Count |
|-------|------:|
| DOCUMENTATION | 16 |
| SCIENTIFIC_CODE | 10 |
| GENERATED_DATA | 8 |
| UI | 6 |
| GENERATED_RECEIPT | 5 |
| SCIENTIFIC_SOURCE | 4 |
| IRRELEVANT_TO_PAPER | 2 |
| ENVIRONMENT | 1 |

## Admission decisions (no blind merge)

| Admission | Paths |
|-----------|-------|
| **ADMIT_TO_PAPER** (by exact hash import) | `scripts/build_clinvar_evidence.py`, `scripts/build_fasta_lane.py`, `data/healthomics/clinvar_subset.tsv`, `data/healthomics/clinvar_provenance.json`, `data/fasta/*`, `data/fasta/fasta_provenance.json` |
| **ADMIT_AS_REFERENCE** | `site/assets/clinvar_evidence.json`, `site/assets/fasta_lane.json`, HealthOmics workflow scripts |
| **TEAM_CONTRIBUTION_ONLY** | Team docs (`docs/ELVIS_*`, `docs/PAPER_CONCERNS_*`), UI mockups, `paper/main.pdf` |
| **EXCLUDE_FROM_ANONYMOUS_PACKAGE** | Identity-bearing docs, Playwright screenshots |
| **EXCLUDE_NOT_RELEVANT** | `.gitignore` deltas unrelated to paper claims |

## G2 successor (EXP-003-SUCCESSOR-001)

Verified from frozen team bytes:

- `ids_fetched=746`, `kept=364`, `excluded_large_cnv=382`, `accounted=746`, `balanced=true`
- TAFAZZIN 100-ID batch: ESummary JSON conversion failure (~16.5 MB XML vs 10 MB ceiling); split-and-retry recovery recorded
- **HISTORICAL_EXACT_REPRODUCTION=NO** for 742→642; **HISTORICAL_FAILURE_MECHANISM_RECOVERED=YES**

## G1 successor (EXP-002-SUCCESSOR-001)

- `records_in=364`, `emitted=98`, `abstained=266` (364=98+266)
- Abstentions: frameshift 131, no_protein_notation 118, residue_mismatch 16, position_out_of_range 1
- **NOT** an exact reproduction of historical G1 numbers

## Manifest

Full per-file SHA-256 manifest: `paper/newinml2026/provenance/TEAM_PR1_CONTRIBUTION_MANIFEST.jsonl`
