# Missed experiments

## Missed core experiments

**0.**

No additional TEAM_CORE result was found that (a) actually ran, (b) produced durable artifacts, (c) materially supports a **canonical** manuscript claim, and (d) is omitted from this inventory.

G1 successor accounting was already in `EXP-002-SUCCESSOR-001`. This audit **replayed** it from frozen bytes (DUPLICATE_RERUN, confirmatory).

## Supporting / out of scope / duplicate / superseded

| ID | Classification | Why it is not missed core |
| --- | --- | --- |
| EXP-Q38-COMP-001 | OUT_OF_SCOPE_EXPERIMENT | Compute canary; not in manuscript Results |
| PROTOCOL-NML-OVERNIGHT-001 waves | SUPPORTING_MINOR_EXPERIMENT | Process/FCG bookkeeping |
| AUD-FCG-ATOM-SOT-ROUNDTRIP-002 | SUPERSEDED_RERUN | Predecessor of SEMANTIC-003 |
| PROTEIN_HINGE_SUCCESSOR_RECOMPUTE_RECEIPT | DUPLICATE_RERUN | Studio 2026-08-29 artifact recompute; `live_refetch_performed=false` |
| AUD-20260830-G1-FROZEN-RECOMPUTE | DUPLICATE_RERUN | This audit; MATCH to successor receipt |
| Elvis Ablation/PerGene/Decline tables | OUT_OF_SCOPE for canonical package | Generated in fork; not merged into NewInML `main.tex` |
| HydraDG / L0-L5 / AntiCube / Delta-G | OUT_OF_SCOPE_EXPERIMENT | Solo research program |

## Local-only Studio evidence

- Clean `protein-hinge` at `a2550d5`; **no unpushed commits**; **no notebooks**.
- Detached worktree `/Users/byron/projects/active/protein-hinge-pr1-review-20260828` @ `6e47dbe` holds PR #1 admitted bytes (hashes MATCH manifests).
- `data/healthomics` and `data/fasta` are **not** on `biobitworks/protein-hinge` `main`. Reproduction from main checkout alone cannot see those files without the fork, the worktree, or a hash import.
- Partner ranking CSV for EXP-006 **is** tracked on main (`data/partner/`).
