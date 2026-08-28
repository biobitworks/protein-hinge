# SeedGraph Import Plan — NewInML 2026

**SeedGraph repo:** `/Users/byron/projects/active/seedgraph`  
**Live container:** `seedgraph-neo4j` (OrbStack, running at bootstrap)  
**Writeback status:** DEFERRED — local manifests authoritative until verified import

## Pipeline

```
DISCOVER → HASH → CLASSIFY → FCO → VALIDATE → SEEDGRAPH IMPORT → VERIFY IMPORT → RECEIPT
```

Bootstrap completed DISCOVER/HASH/CLASSIFY for 186 paper-scoped objects
(see `provenance/PAPER_IMPORT_ACCOUNTING.json`).

## Import scope

Import **paper-scoped closure** only:

- 173 IMPORTED unique-byte objects
- 11 DUPLICATE (pointer edges to canonical object_id)
- 2 UNAVAILABLE (external pointers recorded, not dropped)

Do not import `.git/` internals or unrelated portfolio repos.

## SeedGraph read-first sources

- `/Users/byron/projects/active/seedgraph/AGENTS.md`
- SeedGraph CLI / ingest docs (inspect at execution time; do not infer)

## Planned artifacts

| File | Status |
|------|--------|
| `seedgraph/SEEDGRAPH_IMPORT_MANIFEST.jsonl` | GENERATED (pending rows) |
| `seedgraph/SEEDGRAPH_IMPORT_ACCOUNTING.json` | GENERATED |
| `seedgraph/SEEDGRAPH_IMPORT_RECEIPT.json` | NOT_EXECUTED |
| `seedgraph/SEEDGRAPH_FAILED_OBJECTS.jsonl` | empty |

## Object mapping

Each manifest row:

- `object_id` (FCO-*)
- `sha256`
- `seed_type` (evidence vs requirement — paper artifacts are evidence)
- `provenance_chain` → git commit + relative path
- `terminal_ingest_status` (PENDING | INGESTED | FAILED | QUARANTINED)

## Validation gates before live writeback

1. Pydantic validate against `PAPER_OBJECT_SCHEMA.json`
2. SHA-256 re-verify on magicSTUDIObox
3. No orphan edges (every edge target resolves)
4. Operator approval for live Neo4j promotion

## Live writeback

Use SeedGraph project's existing promotion path when authorized.
 protein-hinge README explicitly defers KG writeback (`deferred_writeback_candidates.jsonl`).

**Bootstrap:** local JSONL manifest only; live import **NOT EXECUTED** this session.

## Verify import

Post-import:

- Count imported nodes vs manifest
- Spot-check 5 objects: graph node SHA-256 pointer == local file SHA-256
- Write `SEEDGRAPH_IMPORT_RECEIPT.json` with pass/fail

## Blockers

- SeedGraph ingest CLI invocation not run (needs project-specific command from seedgraph repo)
- Writeback operator approval not recorded
- THESIS-000 unresolved blockers include SeedGraph import
