# CFMO / MMR Derivation Contract — NewInML 2026

**Status:** PARTIAL — MMR located (Merkle Mountain Range); CFMO acronym implementation NOT FOUND  
**Generated:** 2026-08-28 UTC

## Required invariant

CFMO/MMR outputs are **DERIVED EVIDENCE**. They may emit `THESIS_DELTA_PROPOSAL` only.
They must NOT directly mutate current thesis, source evidence, or historical scores.

## MMR (Merkle Mountain Range — custody)

| Field | Value |
|-------|-------|
| Implementation | `antigence/web_app/static/fco/antigence_fcg.json` (object_mmr recipe) |
| Repo | `/Users/byron/projects/active/antigence` |
| Version/commit | not pinned this session |
| Inputs | atom leaves `sha256(0x00 + canonical(atom))` |
| Outputs | `fco_root`, backbone peaks |
| Deterministic | YES (given fixed atoms) |
| Update semantics | New derivation object per atom set / config change |

**Distinct from:** SIGIR 1998 Maximal Marginal Relevance cited in `docs/FCO_FCG_DESIGN_CITATIONS.md` for reranking — **not implemented** in protein-hinge ranking path.

## CFMO (Custody-Verified Classification / Fractal Custody Objects)

| Field | Value |
|-------|-------|
| Canonical acronym implementation | **NOT FOUND** under `CFMO` identifier |
| Related spec | Zenodo `21830287` — Custody-Verified Classification (operator citation in FCO_FCG_DESIGN) |
| Related manuscript | `antigence/handoff/from_ollarma/ANTIGENCE_IMMUNE_MATRIX_MANUSCRIPT_v1_DRAFT.md` |
| Local FCG implementation | `fcg/fcg.py` (protein-hinge) — Merkle RFC6962-style, not labeled CFMO |
| Status | `BLOCKED_CANONICAL_IMPLEMENTATION_NOT_FOUND` for CFMO-named scorer |

## Per-run requirements (when implementations exist)

```
source FCO set hash
scorer version
config hash
output hash
prior thesis ID
derived FCO ID
```

## protein-hinge policy

Do not invoke CFMO/MMR derivations until:

1. CFMO canonical path identified and pinned, OR
2. Explicit operator approval to use antigence MMR recipe as provisional derived-evidence lane with pinned commit

Historical scores in `fcg/store/` remain immutable COMMITTED/RECOMPUTED nodes — never overwritten.
