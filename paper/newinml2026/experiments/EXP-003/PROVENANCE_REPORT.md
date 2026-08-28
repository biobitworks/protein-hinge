# EXP-003 G2 CNV Provenance Report

**Status:** COMPLETE_NEGATIVE  
**Classification:** PROVENANCE_RECOVERY  
**Host:** magicSTUDIObox.local  
**Git HEAD:** 38c8c15b12ef2773f0614a7995245dd2d19a0f40

## Summary

Systematic search of protein-hinge custody (current tree, full git history, branches,
deleted files, admitted handoff pointers) did **not** locate the historical G2 CNV
attribution batch accounting (`742` fetched, `642` summarized, `100` missing,
`287/642` multi-gene rate) or gene-level transition tables.

Negative provenance is the terminal result for this wave.

## Historical candidates (NOT accepted)

| Metric | Candidate | Disposition |
|--------|-----------|-------------|
| N_fetched | 742 | NOT_FOUND |
| N_summarized | 642 | NOT_FOUND |
| N_missing | 100 | NOT_FOUND |
| multi_gene_cnv | 287/642 | NOT_FOUND |
| PHB2 | 46 → 0 | NOT_FOUND |
| CHCHD3 | 32 → 0 | NOT_FOUND |
| PGS1 | 14 → 0 | NOT_FOUND |
| CRLS1 | 33 → 3 | NOT_FOUND |
| TAFAZZIN | 237 → 100 | NOT_FOUND |
| HADHA | 267 → 251 | NOT_FOUND |

## Partial context (not G2 evidence)

- **Gene symbols** appear in `fto/registry_digests.json` as FTO registry entries.
- **Multi-gene** language appears in `fto/FTO_DESIGN.md` (design prose only).
- **TAFAZZIN** narrative in FCG atoms (biology context, not CNV counts).

## 742 accounting invariant

Target: `N_fetched == N_admitted + N_excluded + N_abstained + N_failed`

**NOT APPLICABLE** — no row-level fetch ledger located.

## Missing 100 records

**UNKNOWN** — cannot attribute to BATCH_NOT_ITERATED, FETCH_FAILURE, or TAFAZZIN
batch without located source code or data.

## EXP-003.1 rerun

**NOT EXECUTED** — no canonical G2 guard code or ClinVar/CNV corpus in repo custody.

## Terminology ceiling

Do not call `287/642` a silent-error rate. No wrongness predicate established.

## Machine-readable

- `provenance_recovery.json`
- `provenance_candidates.jsonl`
