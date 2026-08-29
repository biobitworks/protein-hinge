#!/usr/bin/env python3
"""Explain SeedGraph candidate accounting and duplicate/reference semantics."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROV = ROOT / "paper" / "newinml2026" / "provenance"
SG = ROOT / "paper" / "newinml2026" / "seedgraph"


def main() -> None:
    manifest = PROV / "PAPER_SOURCE_MANIFEST.v2.jsonl"
    if not manifest.exists():
        manifest = PROV / "PAPER_SOURCE_MANIFEST.jsonl"
    rows = [json.loads(line) for line in manifest.read_text().splitlines() if line.strip()]

    by_state = Counter(r["terminal_state"] for r in rows)
    imported = [r for r in rows if r["terminal_state"] == "IMPORTED"]
    duplicates = [r for r in rows if r["terminal_state"] == "DUPLICATE"]
    unavailable = [r for r in rows if r["terminal_state"] == "UNAVAILABLE"]

    unique_sha = {r["sha256"] for r in imported if r.get("sha256")}
    ref_objects = []
    for d in duplicates:
        ref_objects.append(
            {
                "reference_object_id": f"REF-{d['sha256'][:16]}",
                "canonical_object_id": d.get("duplicate_of"),
                "sha256": d.get("sha256"),
                "relative_path": d.get("relative_path"),
                "edge": "exact_copy_of",
                "seedgraph_policy": "REFERENCE_ONLY — no second content object",
            }
        )

    ingest_candidates = []
    for r in imported:
        ingest_candidates.append(
            {
                "object_id": r["object_id"],
                "sha256": r.get("sha256"),
                "relative_path": r.get("relative_path"),
                "seedgraph_action": "IMPORT_CONTENT_OBJECT",
            }
        )
    for d in duplicates:
        ingest_candidates.append(
            {
                "object_id": f"REF-{d['sha256'][:16]}",
                "canonical_object_id": d.get("duplicate_of"),
                "sha256": d.get("sha256"),
                "relative_path": d.get("relative_path"),
                "seedgraph_action": "IMPORT_REFERENCE_EDGE_ONLY",
            }
        )

    accounting = {
        "explanation": (
            "188 pending rows (v1) = N_imported + N_duplicate from source closure, "
            "excluding N_unavailable external pointers. "
            "SeedGraph receives unique_content_objects as evidence seeds plus "
            "reference_objects as exact_copy_of edges — not independent scientific duplicates."
        ),
        "source_objects": len(rows),
        "unique_content_objects": len(unique_sha),
        "duplicate_occurrences": len(duplicates),
        "reference_objects": len(ref_objects),
        "unavailable": len(unavailable),
        "ingest_candidates": len(ingest_candidates),
        "terminal_breakdown": dict(by_state),
        "invariant": (
            "source_objects == unique_content_objects + duplicate_occurrences + unavailable "
            f"→ {len(rows)} == {len(unique_sha)} + {len(duplicates)} + {len(unavailable)} "
            f"→ {len(rows) == len(unique_sha) + len(duplicates) + len(unavailable)}"
        ),
        "duplicate_paths": [{"path": d.get("relative_path"), "canonical": d.get("duplicate_of")} for d in duplicates],
        "reference_policy": "DUPLICATE terminal → REFERENCE/ALIAS object with exact_copy_of edge to canonical FCO",
    }
    (SG / "SEEDGRAPH_CANDIDATE_ACCOUNTING.json").write_text(json.dumps(accounting, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: accounting[k] for k in accounting if k != "duplicate_paths"}, indent=2))


if __name__ == "__main__":
    main()
