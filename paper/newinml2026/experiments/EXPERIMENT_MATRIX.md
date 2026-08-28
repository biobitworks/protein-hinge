# Experiment Matrix — NewInML 2026

**Controller:** magicSTUDIObox.local  
**Branch:** `paper/newinml-fcg-20260828`

## Classification key

- **EXPLORATORY** — hypothesis-generating or defect investigation; not confirmatory
- **REPLICATION** — frozen plan + inputs before outcome inspection
- **CONFIRMATORY** — requires full prereg (H0/H1/alpha/MESI/power); none retroactive

## Matrix

| ID | Title | Class | Status | Host | Earliest dependency |
|----|-------|-------|--------|------|---------------------|
| EXP-GAP-ACCOUNTING-001 | GAP semantic-accounting retrospective audit | EXPLORATORY | COMPLETE | LOCAL | `gap/ingest_gap.py:119-124` |
| EXP-GAP-ACCOUNTING-001.1 | GAP accounting repaired rerun | REPLICATION | PREREGISTERED | LOCAL | EXP-001 findings |
| EXP-001 | Alias for EXP-GAP-ACCOUNTING-001 | EXPLORATORY | COMPLETE | LOCAL | same |
| EXP-002 | G1 sequence/residue verification — provenance recovery | EXPLORATORY | COMPLETE_NEGATIVE | LOCAL | all historical counts NOT_FOUND; rerun blocked |
| EXP-003 | G2 CNV attribution ablation | EXPLORATORY | COMPLETE_NEGATIVE | LOCAL | provenance recovery; no source corpus located |
| EXP-004 | G3 identity-resolution ablation | EXPLORATORY | NOT_STARTED | LOCAL | raw vs canonical ID join |
| EXP-005 | Frozen-corpus independent replication | REPLICATION | PREREGISTERED_LOCKED | LOCAL | outcome_exposure=NO |
| EXP-006 | Morphology/null reproduction | REPLICATION | NOT_STARTED | LOCAL | frozen CPJUMP1 inputs |
| EXP-007 | SGLang CUDA graph-break stress | EXPLORATORY | PREREGISTERED | KAGGLE/DAYTONA | SGLANG_GRAPH_BREAK_PREREG.md |

## EXP-GAP-ACCOUNTING-001 findings (retrospective)

**Hypothesis (exploratory):** committed GAP abstention summary matches terminal row counts.

**Observed:**

- `gap/runs/2026-08-13/candidates.csv`: 4 data rows
  - 1 × `NOT_A_GAP`
  - 3 × `ABSTAIN` (grade column)
- `gap/runs/2026-08-13/abstentions.json`: all summary counters = 0

**Earliest divergent dependency:**

```119:124:gap/ingest_gap.py
    abstentions = {
        "diseases_with_no_target_above_threshold": 0,
        "targets_whose_names_did_not_reconcile": 0,
        "lookups_that_failed": 0,
        "reasons": [],
    }
```

Summary is **hardcoded**, not derived from graded rows.

**Mandatory invariants (for 001.1):**

```
summary.ABSTAIN == count(row.terminal_state == ABSTAIN)
N_input == N_admitted + N_excluded + N_abstained + N_failed
```

**Historical artifacts:** preserved immutable under `gap/runs/2026-08-13/`.

## Required artifacts per experiment

Each run directory under `experiments/<id>/` must contain:

- `prereg.json` (if CONFIRMATORY or REPLICATION)
- `inputs/` hashed snapshots
- `environment.json`
- `command.txt`
- `results/`
- `accounting.json`
- `receipt.json`
- `rerun.md`

## Promotion rule

No experiment promotes manuscript claims above its `claim_ceiling` or statistical
evidence class. Failures ingest as `FAILURE` / `ABSTENTION` FCOs.
