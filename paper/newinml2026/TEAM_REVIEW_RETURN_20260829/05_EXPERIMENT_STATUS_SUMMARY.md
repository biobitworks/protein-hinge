# Experiment status summary

Source: `final_team_evidence_audit/EXPERIMENT_INVENTORY.md` (live receipts).

## Terminals

| Terminal | Count | Examples |
| --- | ---: | --- |
| COMPLETE_POSITIVE | 1 | EXP-GAP-ACCOUNTING-001.1 |
| COMPLETE_NEGATIVE | 7 | GAP-001, G1/G2 historical, EXP-006 null |
| COMPLETE_BOUNDED | 4 | G1/G2 successors, document lattice |
| UNDERPOWERED | 2 | EXP-004 (N=1), atom-SOT semantic audit |
| NOT_EXECUTED | 3 | EXP-005, EXP-007, SOT-008 +30 study |
| BLOCKED | 1 | EXP-Q38 (out of paper scope) |

## Core NewInML experiments

| ID | Status | In canonical Results? |
| --- | --- | --- |
| GAP repair | COMPLETE_POSITIVE | Yes |
| G3 identity | UNDERPOWERED | Yes (N=1) |
| G1 historical | COMPLETE_NEGATIVE | Audit only |
| G1 successor | COMPLETE_BOUNDED | Yes (364 subset) |
| G2 historical | COMPLETE_NEGATIVE | Audit only |
| G2 successor | COMPLETE_BOUNDED | Yes (746 fetch accounting) |
| EXP-006 morphology null | COMPLETE_NEGATIVE | Yes (negative retained) |
| EXP-005 replication | NOT_EXECUTED | No — locked, corpus incomplete |

## Negative / not-established (retain explicitly)

- Historical G1/G2 corpora **not recovered** from admitted provenance
- EXP-006: shuffle null not beaten — **negative**, not suppressed
- SOT-008 +30: **NOT_ESTABLISHED**, **nonblocking**, not in canonical manuscript
- Stale Elvis numbers (24.6%, 51.2%): **PROHIBITED** in current Results

## Another experiment required?

**No.** Terminals are sufficient for NewInML scope. EXP-005 and +30 remain optional future work, not submission blockers.
