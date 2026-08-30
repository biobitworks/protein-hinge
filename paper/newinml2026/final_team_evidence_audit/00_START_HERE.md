# Final team-evidence + deterministic provenance audit

**Audit ID:** `AUD-FINAL-TEAM-EVIDENCE-20260829`  
**Recorded:** 2026-08-30T02:20:00Z  
**Cockpit:** `magicPRObox.local` (Cursor session)  
**Evidence host queried:** `magicSTUDIObox.local` (same `HEAD`, clean, no unpushed commits)

This package is an **audit of existing evidence**. It does not add new science campaigns. The only bounded recomputation was a no-network replay of the G1 `apply_variant` guard against hash-admitted FASTA + ClinVar bytes (receipt: `G1_FROZEN_RECOMPUTE_RECEIPT.json`).

## Canonical authority (resolved, not assumed)

| Field | Value |
| --- | --- |
| `REPO_HEAD_SHA` | `a2550d589594ae6e440885bc68a618f3b852764d` |
| `CANONICAL_PAPER_SOURCE_SHA` | `bc4b0d575d130af3f335b712ec1763c164d7d74b` |
| `CI_RUN_ID` | `33264903580` |
| `FINAL_PDF_SHA256` | `ded8f72e299642a7f8ed4fc0f5318b1e961c413b5640acaa6cda6d65880448ab` |
| Anonymous bundle SHA-256 | `c64812be34132242e166e862fe4197091de73abf56d32fc175d7424ad8cb20d8` |

`paper/newinml2026/provenance/CANONICAL_PAPER_SOURCE.yaml` still lists PR #2 merge `2ba0d923…`. Treat that file as **stale**. Live authority is `PROJECT_CONTROL.yaml` `current_state` + CI run `33264903580`.

Manuscript `main.tex` is **byte-identical** between CI source `bc4b0d5` and current `main`. Later commits only touch probox review access docs.

## What the team built (TEAM_CORE)

Protein Hinge is a hash-pinned evidence ledger plus a NewInML 2026 **verify-or-abstain** paper projection. Admitted team science is:

- GAP row/summary invariant repair
- G3 identity-guard ablation (N=1 observed-source)
- G1/G2 **historical provenance negatives** plus **contemporary successor** evaluations on PR #1 hash-admitted ClinVar/FASTA bytes
- EXP-006 cached morphology **null** (negative retained)
- EXP-005 locked and **not executed**
- Explicit claim ceilings; no RWE / efficacy / FTO opinion

PR #1 (ElvisHan2022 `healthomics-lane`) is **OPEN** and **not merged**. Successor numbers are hash-admitted from snapshot `6e47dbe…`. Live fork head is `d0e992be…` (ClinVar TSV unchanged; Elvis `paper/main.tex` diverged).

## Read next

1. `AUDIT_STATE.json` — gates
2. `GIT_AUTHORITY.json` — SHAs, hosts, remotes
3. `EXPERIMENT_INVENTORY.md` — every experiment terminal
4. `NUMERICAL_CLAIM_LEDGER.csv` — every tracked number
5. `CLAIM_EVIDENCE_AUDIT.md` — manuscript statements
6. `GROUP_EFFORT_EVIDENCE_AUDIT.md` — bounded process finding
7. `MINIMAL_MANUSCRIPT_DELTA.md` — recommendation only (manuscript not edited)
8. `PREPRINT_PRIOR_WORK_MATRIX.md` / `.csv` — prior-work classification
9. `PREPRINT_PRIOR_WORK_SUGGESTIONS.md` — citation + novelty audit (review only)
10. `PROPOSED_PRIOR_WORK_MANUSCRIPT_DELTA.md` — human-review diff proposals
11. `SUBMISSION_CONTROL_CLARIFICATION_20260829.json` — SOT-008 +30 nonblocking clarification
12. `FINAL_AUDIT_RECEIPT.json`

Team-facing summary folder: `paper/newinml2026/TEAM_REVIEW_RETURN_20260829/`

## Gates (do not collapse)

| Gate | Status |
| --- | --- |
| GIT_AUTHORITY_GATE | PASS_WITH_BOUNDED_GAPS |
| TEAM_SCOPE_GATE | PASS |
| EXPERIMENT_ACCOUNTING_GATE | PASS_WITH_BOUNDED_GAPS |
| RERUN_LINEAGE_GATE | PASS |
| NUMERICAL_CLAIM_GATE | PASS_WITH_BOUNDED_GAPS |
| TABLE_PROVENANCE_GATE | YELLOW |
| FIGURE_PROVENANCE_GATE | PASS |
| NOTEBOOK_PROVENANCE_GATE | NOT_APPLICABLE |
| CLAIM_EVIDENCE_GATE | PASS_WITH_BOUNDED_GAPS |
| GROUP_EFFORT_AUDIT_GATE | PASS |
| ANONYMITY_GATE | PASS |

No gate is a blanket PASS covering the others.

## Stop conditions

Central manuscript results have terminals. Canonical scientific numbers have terminals (one PARTIAL_TRACE: 206 MB zip not rehashed here). Canonical Table 1 is receipt-matched but not generator-produced. The single figure is CONCEPTUAL. Studio reruns are accounted. Missed **core** experiments: **0**. Team vs imported/solo/future is explicit.

Do not launch further science from this audit.
