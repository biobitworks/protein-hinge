# Paper FCG Plan — NewInML 2026

**Branch:** `paper/newinml-fcg-20260828`  
**Base SHA:** `94f8949f1bbcb63d8e80baadd0c5f380f01b9f92`  
**Controller:** magicSTUDIObox.local (arm64, non-CUDA)

## Objective

Build a complete, versioned FCO/FCG custody graph for the NewInML 2026 paper
derived from `protein-hinge`, ingest the paper-scoped object closure through
SeedGraph, and maintain reproducible experiment contracts under Getting Science Done
semantics.

The manuscript is a **projection** of the graph, never the canonical source.

## Scope boundary

**In scope (paper-scoped transitive closure):**

- `protein-hinge` repository lanes: `fcg/`, `fto/`, `gap/`, `fco/`
- Demo surfaces: `site/`, `db/`, `figures/`, `output/playwright/`
- Operator docs and model trace artifacts under `docs/`, `model_trace/`
- Regulatory/partner pinned data under `data/`
- Build/ingest scripts under `scripts/`
- Paper control plane under `paper/newinml2026/`
- External citations referenced by committed docs (Zenodo DOIs, RFC 6962, MMR)
- Elvis handoff materials referenced by GAP lane (`gap/elvis_prescripted_demo.json`)

**Explicitly excluded:**

- Unrelated portfolio repos (cellico, xenodisorder, etc.) unless later cited by a
  manuscript claim with operator approval
- `.git/` object database (metadata captured separately)
- Live Convoke/Open Targets responses not yet wired
- CUDA/SGLang execution artifacts (remote-only, preregistered)

**Unavailable (recorded, not dropped):**

- `/Users/byron/Downloads/biocustody.zip` — origin zip per `ORIGIN_REVIEW.md`
- `HACKDAY_STATE.yaml` — required by ingest builders, absent from published repo

## Object classes and edges

See `PAPER_OBJECT_SCHEMA.json` for required fields and edge relation enum.

Every object MUST have exact-byte SHA-256 where bytes exist under custody.
Git blob/commit SHAs are supplementary attribution pointers only.

## Pipeline phases

### Phase 0 — Bootstrap (this branch)

- [x] Confirm host + git identity
- [x] Propose `AGENTS.md` + `PROJECT_CONTROL.yaml`
- [x] Create `paper/newinml2026/` directory lattice
- [x] Discover + hash paper-scoped closure
- [x] Write import manifests and contributor audit
- [x] Define experiment matrix + preregistrations
- [ ] SeedGraph import (local manifest first; live writeback gated)

### Phase 1 — Deterministic validation (local, cheap)

- [ ] EXP-GAP-ACCOUNTING-001 retrospective audit
- [ ] EXP-GAP-ACCOUNTING-001.1 repaired rerun
- [ ] EXP-002..004 ablation recoveries (source/code reconciliation)
- [ ] EXP-005 frozen-corpus preregistration before outcome inspection
- [ ] EXP-006 null morphology reproduction from frozen inputs

### Phase 2 — Remote CUDA lane (preregistered only)

- [ ] EXP-007 SGLang graph-break stress on Kaggle or Daytona
- [ ] Hash verify remote receipts before FCG aggregation

### Phase 3 — Thesis + claim closure

- [ ] THESIS-001 after EXP-001.1 evidence delta
- [ ] Claim-evidence matrix completion
- [ ] CFMO/MMR derived evidence objects (new versions, never overwrite)

### Phase 4 — Manuscript projection

- [ ] Machine-generated tables/figures from artifacts
- [ ] Paper build receipt with PDF SHA-256
- [ ] Anonymous submission artifact custody

## Acceptance gates

| Gate | Criterion | Status |
|------|-----------|--------|
| A. Source accounting | N_discovered == sum(terminal states) | PASS (186) |
| B. Experiment accounting | N_input == admitted+excluded+abstained+failed | PENDING |
| C. Hash custody | Every paper-critical artifact has SHA-256 | IN PROGRESS |
| D. Contributor provenance | Attribution classified; ambiguity preserved | IN PROGRESS |
| E. Reproducibility | Every experiment has snapshot/env/command/receipt | PENDING |
| F. Claim closure | Every claim maps to supporting/contradicting FCOs | PENDING |
| G. Negative evidence | Nulls/failures retained as FCOs | IN PROGRESS |
| H. Remote compute | Remote outputs verify against dispatch hashes | NOT STARTED |
| I. SeedGraph | Intended objects have terminal ingest status | PENDING |
| J. Paper projection | Tables/figures machine-generated or provenance-labeled | NOT STARTED |

## Immutable history rule

August 13 GAP run artifacts under `gap/runs/2026-08-13/` are **historical evidence**.
Repairs produce **successor runs** under new run IDs, linked by `supersedes` edges.
Never rewrite committed hashes or receipt Merkle roots in place.

## CFMO / MMR

CFMO and MMR outputs are `DERIVED_EVIDENCE` objects. Config or scorer changes
create new derivation objects; prior scores remain addressable.

## SeedGraph

Pipeline: DISCOVER → HASH → CLASSIFY → FCO → VALIDATE → SEEDGRAPH IMPORT → VERIFY → RECEIPT

Live Neo4j container `seedgraph-neo4j` is available; promotion follows SeedGraph
project writeback gates. Local JSONL manifests are authoritative until verified import.

## Cloudflare OS

Control/UI surface only. Canonical scientific truth remains on magicSTUDIObox.
See `cloudflareos/INTEGRATION.md`.
