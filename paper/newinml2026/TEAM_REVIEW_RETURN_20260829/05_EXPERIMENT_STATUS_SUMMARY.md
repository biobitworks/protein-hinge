# Experiment status summary

Source: `final_team_evidence_audit/EXPERIMENT_INVENTORY.md` (live receipts).

## Terminals (control-plane vocabulary)

| terminal_state | Count | outcome_qualifier | Examples |
| --- | ---: | --- | --- |
| COMPLETE | 7 | POSITIVE 1; BOUNDED 4; UNDERPOWERED 2 | GAP repair; G1/G2 successors; EXP-004 N=1 |
| NEGATIVE | 6 | — | GAP-001 historical, G1/G2 historical, EXP-006 null |
| SKIPPED | 4 | NOT_EXECUTED 3; SUPERSEDED 1 | EXP-005, EXP-007, SOT-008 +30 study |
| BLOCKED | 1 | — | EXP-Q38 (out of paper scope) |

EXP-001 alias is retained for cross-reference but excluded from totals (18 independent objects).

## Core NewInML experiments

| ID | Status | In canonical Results? |
| --- | --- | --- |
| GAP repair | COMPLETE (POSITIVE) | Yes |
| G3 identity | COMPLETE (UNDERPOWERED) | Yes (N=1) |
| G1 historical | NEGATIVE | Audit only |
| G1 successor | COMPLETE (BOUNDED) | Yes (364 subset) |
| G2 historical | NEGATIVE | Audit only |
| G2 successor | COMPLETE (BOUNDED) | Yes (746 fetch accounting) |
| EXP-006 morphology null | NEGATIVE | Yes (negative retained) |
| EXP-005 replication | SKIPPED (NOT_EXECUTED) | No — locked, corpus incomplete |

## Negative / not-established (retain explicitly)

- Historical G1/G2 corpora **not recovered** from admitted provenance
- EXP-006: shuffle null not beaten — **negative**, not suppressed
- SOT-008 +30: **NOT_ESTABLISHED**, **nonblocking**, not in canonical manuscript
- Stale Elvis numbers (24.6%, 51.2%): **PROHIBITED** in current Results

## Another experiment required?

**No.** Terminals are sufficient for NewInML scope. EXP-005 and +30 remain optional future work, not submission blockers.
