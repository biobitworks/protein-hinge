# Experiment inventory

Generated from live receipts, not from `EXPERIMENT_MATRIX.md` (that matrix is **stale**: it still lists EXP-004 NOT_STARTED and EXP-006 NOT_STARTED).

Machine copy: `EXPERIMENT_INVENTORY.jsonl`.

## Count by control-plane terminal

`terminal_state` uses the daisy-chain vocabulary (`COMPLETE | NEGATIVE | BLOCKED | QUARANTINED | SKIPPED`). Outcome qualifiers are separate fields on each row.

| terminal_state | N | outcome_qualifier breakdown | IDs |
| --- | ---: | --- | --- |
| COMPLETE | 7 | POSITIVE 1; BOUNDED 4; UNDERPOWERED 2 | EXP-GAP-ACCOUNTING-001.1; EXP-002-SUCCESSOR-001, EXP-003-SUCCESSOR-001, AUD-FCG-DOCUMENT-LATTICE-001, ANTIGENCE-B4-COMPARATOR; EXP-004, AUD-FCG-ATOM-SOT-SEMANTIC-003 |
| NEGATIVE | 6 | — | EXP-GAP-ACCOUNTING-001, EXP-002, EXP-002-PROV.1, EXP-003, EXP-003-PROV.1, EXP-006 |
| BLOCKED | 1 | — | EXP-Q38-COMP-001 (out of team paper) |
| SKIPPED | 4 | NOT_EXECUTED 3; SUPERSEDED 1 | EXP-005, EXP-007, SOT-008-TAFAZZIN-PLUS30; AUD-FCG-ATOM-SOT-ROUNDTRIP-002 |
| **Total independent** | **18** | aliases excluded | see jsonl |
| Alias (cross-ref only) | 1 | EXP-001 → EXP-GAP-ACCOUNTING-001 | not counted in totals |

Do not convert SKIPPED/NOT_EXECUTED to failure. Do not convert EXP-006 negative to positive.

## Core lineage the prompt asked to trace

| ID | terminal_state (outcome_qualifier) | Scope |
| --- | --- | --- |
| EXP-GAP-ACCOUNTING-001 | NEGATIVE | TEAM_CORE |
| EXP-GAP-ACCOUNTING-001.1 | COMPLETE (POSITIVE) | TEAM_CORE |
| G1 / EXP-002 | NEGATIVE (historical) | TEAM_CORE |
| G1 / EXP-002-SUCCESSOR-001 | COMPLETE (BOUNDED; this audit frozen replay MATCH) | TEAM_CONTRIBUTED |
| G2 / EXP-003 | NEGATIVE (historical) | TEAM_CORE |
| G2 / EXP-003-SUCCESSOR-001 | COMPLETE (BOUNDED) | TEAM_CONTRIBUTED |
| G3 / EXP-004 | COMPLETE (UNDERPOWERED; N=1) | TEAM_CORE |
| EXP-005 | SKIPPED (NOT_EXECUTED) | TEAM_CORE |
| EXP-006 | NEGATIVE (cached null retained) | TEAM_CORE |
| EXP-007 | SKIPPED (NOT_EXECUTED) | FUTURE_DIRECTION / OUT_OF_TEAM_SCOPE |
| AUD-FCG-DOCUMENT-LATTICE-001 | COMPLETE (BOUNDED; 136/136 structural; table cells PENDING) | TEAM_IMPORTED_DEPENDENCY |
| AUD-FCG-ATOM-SOT-SEMANTIC-003 | COMPLETE (UNDERPOWERED / YELLOW) | TEAM_IMPORTED_DEPENDENCY |
| ANTIGENCE-B4-COMPARATOR | COMPLETE (BOUNDED; not a paper Results claim) | TEAM_IMPORTED_DEPENDENCY |

## Stale inventories found (not used as authority)

- `paper/newinml2026/experiments/EXPERIMENT_MATRIX.md`
- `TEAM_HANDOFF_20260829/05_EXPERIMENT_INDEX_ML.jsonl` (EXP-006 as NOT_EXECUTED; successors omitted)
- `paper/newinml2026/thesis/THESIS-001.json` unresolved_blockers still say EXP-002–006 not started
