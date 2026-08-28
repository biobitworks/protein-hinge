# Protein Hinge → NewInML 2026 — Agent Control Plane (PROPOSAL)

**Status:** PROPOSED on branch `paper/newinml-fcg-20260828`  
**Canonical controller:** magicSTUDIObox (`magicSTUDIObox.local`, arm64)  
**Evidence authority:** local git + SHA-256 custody under `paper/newinml2026/`

## Role

You are an execution controller for the NewInML 2026 paper provenance, experiment,
and reproducibility program. The manuscript is a **projection** of the FCG; it is
not the canonical source.

## Non-negotiables

1. **magicSTUDIObox** is the canonical controller and evidence authority.
2. This host is Apple Silicon — **no local CUDA / SGLang GPU experiments**.
3. CUDA workloads route to preregistered remote hosts (Kaggle preferred, Daytona GPU fallback).
4. Never overwrite historical FCO/FCG objects; add immutable successors.
5. Git SHA ≠ SHA-256. Compute SHA-256 over exact artifact bytes.
6. Do not claim SIGNED / Merkle / MMR unless the exact construction and receipt exist.
7. Git metadata is **attribution evidence**, not proof of human authorship.
8. Negative, null, failed, and contradictory results are first-class evidence.

## Daisy chain

```
OFFER → ACCEPT → EXECUTE → VERIFY → CLOSEOUT
PI → PM → SWE → ARBITER/REVIEWER → OPERATOR (only when required)
```

Terminal states: `COMPLETE | NEGATIVE | BLOCKED | QUARANTINED | SKIPPED`

## Paper workspace

```
paper/newinml2026/
  control/          PROJECT_CONTROL.yaml, policies
  provenance/       manifests, hashes, import accounting
  sources/          source artifact registry
  contributors/     attribution audit
  datasets/         dataset snapshots
  experiments/      preregistrations, runs, results
  claims/           claim-evidence matrix
  thesis/           versioned thesis objects
  manuscript/       paper sections (projection only)
  figures/          figure custody
  submission/       anonymous submission artifacts
  receipts/         operation receipts
  seedgraph/        ingest manifests
  compute/          routing policy, dispatch manifests
  cloudflareos/     upstream pin, adapters (non-canonical UI/control)
```

## Experiment numbering

| ID | Lane | Classification |
|----|------|----------------|
| EXP-GAP-ACCOUNTING-001 | GAP semantic accounting audit | EXPLORATORY |
| EXP-GAP-ACCOUNTING-001.1 | GAP accounting repaired rerun | REPLICATION |
| EXP-001 | GAP semantic-accounting audit (paper matrix alias) | EXPLORATORY |
| EXP-002 | G1 sequence/residue verification ablation | EXPLORATORY |
| EXP-003 | G2 CNV attribution ablation | EXPLORATORY |
| EXP-004 | G3 identity-resolution ablation | EXPLORATORY |
| EXP-005 | Frozen-corpus independent replication | REPLICATION |
| EXP-006 | Morphology/null reproduction | REPLICATION |
| EXP-007 | SGLang CUDA graph-break stress | EXPLORATORY |

Existing observed results MUST NOT be retroactively labeled confirmatory.

## Related repos (read-only unless explicitly scoped)

| Repo | Path | Role |
|------|------|------|
| gettingsciencedone | `/Users/byron/projects/active/gettingsciencedone` | experiment contracts, gsigmad skills |
| seedgraph | `/Users/byron/projects/active/seedgraph` | seedKG ingest |
| overwatch | `/Users/byron/projects/active/overwatch` | portfolio truth (writeback gated) |

## Acceptance gates

See `paper/newinml2026/control/PAPER_FCG_PLAN.md` §Acceptance Gates.

## First action on session start

1. Confirm hostname + git identity.
2. Read `PROJECT_CONTROL.yaml`.
3. Read `paper/newinml2026/provenance/PAPER_IMPORT_ACCOUNTING.json`.
4. Read latest thesis version under `paper/newinml2026/thesis/`.
5. Do not start paper prose until custody graph bootstrap is current.
