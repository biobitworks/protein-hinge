# Group-effort evidence audit (bounded)

This is a **systems / process observation** over the Protein Hinge NewInML 2026 corpus. It is not a controlled human-subject study. No causality or population validity is claimed.

Machine copy: `GROUP_EFFORT_EVIDENCE_AUDIT.json`.

## Proposition under test

> A multi-contributor scientific software/paper workflow can preserve explicit provenance, deterministic derivation, abstention, negative results, and contribution boundaries across Git collaboration, experiment repair, manuscript generation, and submission review.

## What the corpus supports

| Metric | Value |
| --- | --- |
| Git contributors on relevant PRs | `biobitworks`, `ElvisHan2022` |
| PRs 1–7 | 5 merged, 1 open (PR #1), 1 closed unmerged (PR #3, superseded by #4) |
| Experiment objects inventoried | 19 |
| COMPLETE_POSITIVE | 1 |
| COMPLETE_NEGATIVE | 7 |
| COMPLETE_BOUNDED | 4 |
| UNDERPOWERED | 2 |
| BLOCKED | 1 (out-of-scope canary) |
| NOT_EXECUTED | 3 |
| SUPERSEDED | 1 |
| Canonical scientific numbers with MANUAL_VALUE | 0 |
| Canonical tables | 1 (receipt-matched, not generator-produced) |
| Canonical figures | 1 CONCEPTUAL |
| Notebooks | 0 |
| Contradictions preserved | Yes (GAP 0 vs 3; historical G1/G2 quarantined; EXP-006 negative retained) |
| Operator-required | Submission seal roster; SOT-008; SOT-020; PR #1 merge decision |

## Bounded finding

On **this** project, Git collaboration plus hash-admitted fork artifacts plus explicit negative and not-executed terminals **did** keep contribution boundaries visible, and canonical Results numbers (except the 206 MB zip size, PARTIAL_TRACE here) have machine paths. The Elvis “nothing typed by hand” generator exists on the fork and was **not** wired into the canonical NewInML `main.tex` table.

That is a descriptive statement about this repository. It is not evidence that arbitrary teams will preserve provenance.
