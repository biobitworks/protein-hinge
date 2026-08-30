# Experiment inventory

Generated from live receipts, not from `EXPERIMENT_MATRIX.md` (that matrix is **stale**: it still lists EXP-004 NOT_STARTED and EXP-006 NOT_STARTED).

Machine copy: `EXPERIMENT_INVENTORY.jsonl`.

## Count by terminal

| Terminal | N | IDs |
| --- | ---: | --- |
| COMPLETE_POSITIVE | 1 | EXP-GAP-ACCOUNTING-001.1 |
| COMPLETE_NEGATIVE | 7 | EXP-GAP-ACCOUNTING-001, EXP-001 (alias), EXP-002, EXP-002-PROV.1, EXP-003, EXP-003-PROV.1, EXP-006 |
| COMPLETE_BOUNDED | 4 | EXP-002-SUCCESSOR-001, EXP-003-SUCCESSOR-001, AUD-FCG-DOCUMENT-LATTICE-001, ANTIGENCE-B4-COMPARATOR |
| UNDERPOWERED | 2 | EXP-004, AUD-FCG-ATOM-SOT-SEMANTIC-003 |
| BLOCKED | 1 | EXP-Q38-COMP-001 (out of team paper) |
| NOT_EXECUTED | 3 | EXP-005, EXP-007, SOT-008-TAFAZZIN-PLUS30 |
| SUPERSEDED | 1 | AUD-FCG-ATOM-SOT-ROUNDTRIP-002 |
| **Total inventoried** | **19** | including alias + imported + out-of-scope |

Do not convert NOT_EXECUTED to failure. Do not convert EXP-006 negative to positive.

## Core lineage the prompt asked to trace

| ID | Terminal (this audit) | Scope |
| --- | --- | --- |
| EXP-GAP-ACCOUNTING-001 | COMPLETE_NEGATIVE | TEAM_CORE |
| EXP-GAP-ACCOUNTING-001.1 | COMPLETE_POSITIVE | TEAM_CORE |
| G1 / EXP-002 | COMPLETE_NEGATIVE (historical) | TEAM_CORE |
| G1 / EXP-002-SUCCESSOR-001 | COMPLETE_BOUNDED (contemporary; this audit frozen replay MATCH) | TEAM_CONTRIBUTED |
| G2 / EXP-003 | COMPLETE_NEGATIVE (historical) | TEAM_CORE |
| G2 / EXP-003-SUCCESSOR-001 | COMPLETE_BOUNDED | TEAM_CONTRIBUTED |
| G3 / EXP-004 | UNDERPOWERED (N=1) | TEAM_CORE |
| EXP-005 | NOT_EXECUTED | TEAM_CORE |
| EXP-006 | COMPLETE_NEGATIVE (cached null retained) | TEAM_CORE |
| EXP-007 | NOT_EXECUTED | FUTURE_DIRECTION / OUT_OF_TEAM_SCOPE |
| AUD-FCG-DOCUMENT-LATTICE-001 | COMPLETE_BOUNDED (136/136 structural; table cells PENDING) | TEAM_IMPORTED_DEPENDENCY |
| AUD-FCG-ATOM-SOT-SEMANTIC-003 | UNDERPOWERED / YELLOW | TEAM_IMPORTED_DEPENDENCY |
| ANTIGENCE-B4-COMPARATOR | COMPLETE_BOUNDED (not a paper Results claim) | TEAM_IMPORTED_DEPENDENCY |

## Stale inventories found (not used as authority)

- `paper/newinml2026/experiments/EXPERIMENT_MATRIX.md`
- `TEAM_HANDOFF_20260829/05_EXPERIMENT_INDEX_ML.jsonl` (EXP-006 as NOT_EXECUTED; successors omitted)
- `paper/newinml2026/thesis/THESIS-001.json` unresolved_blockers still say EXP-002–006 not started
