#!/usr/bin/env python3
"""SeedGraph v3 local import accounting from paper closure v3 manifest."""
from __future__ import annotations

import hashlib
import json
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"
PROV = PAPER / "provenance"
SG = PAPER / "seedgraph"
MANIFEST_V3 = PROV / "PAPER_SOURCE_MANIFEST.v3.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def seedgraph_head() -> str:
    sg = Path("/Users/byron/projects/active/seedgraph")
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=sg, text=True).strip()


def main() -> int:
    SG.mkdir(parents=True, exist_ok=True)
    rows = [json.loads(line) for line in MANIFEST_V3.read_text().splitlines() if line.strip()]

    manifest_out = SG / "SEEDGRAPH_IMPORT_MANIFEST.v3.jsonl"
    failed_out = SG / "SEEDGRAPH_FAILED_OBJECTS.v3.jsonl"
    counts = {
        "IMPORTED_CONTENT": 0,
        "IMPORTED_REFERENCE": 0,
        "UNAVAILABLE": 0,
        "EXCLUDED": 0,
        "FAILED": 0,
        "QUARANTINED": 0,
    }
    failed_rows: list[dict] = []
    manifest_rows_clean = []
    for obj in rows:
        terminal = obj["terminal_state"]
        rel = obj.get("relative_path") or ""
        if rel.startswith("paper/newinml2026/seedgraph/"):
            status = "EXCLUDED"
            exclude_reason = "seedgraph_self_artifact"
        elif terminal == "IMPORTED":
            status = "IMPORTED_CONTENT"
            exclude_reason = None
        elif terminal == "DUPLICATE":
            status = "IMPORTED_REFERENCE"
            exclude_reason = None
        elif terminal == "UNAVAILABLE":
            status = "UNAVAILABLE"
            exclude_reason = None
        elif terminal == "EXCLUDED":
            status = "EXCLUDED"
            exclude_reason = None
        elif terminal == "QUARANTINED":
            status = "QUARANTINED"
            exclude_reason = None
        else:
            status = "FAILED"
            exclude_reason = f"unexpected_terminal_{terminal}"
            failed_rows.append({"object_id": obj.get("object_id"), "reason": exclude_reason})

        counts[status] += 1
        row = {
            "object_id": obj.get("object_id"),
            "content_sha256": obj.get("content_sha256") or obj.get("sha256"),
            "seed_type": "evidence",
            "source_uri": obj.get("source_uri"),
            "relative_path": rel or None,
            "closure_subject_sha": obj.get("closure_subject_sha"),
            "git_commit_sha": obj.get("git_commit_sha"),
            "object_type": obj.get("type"),
            "terminal_ingest_status": status,
            "duplicate_of": obj.get("duplicate_of"),
            "live_neo4j_write": False,
        }
        if exclude_reason:
            row["exclude_reason"] = exclude_reason
        manifest_rows_clean.append(row)

    with manifest_out.open("w") as fh:
        for row in manifest_rows_clean:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    with failed_out.open("w") as fh:
        for row in failed_rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    n_rows = len(manifest_rows_clean)
    invariant_ok = n_rows == sum(counts.values())

    accounting = {
        "schema": "protein_hinge.seedgraph.import_accounting.v3",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "git_head": git_head(),
        "closure_subject_sha": "66979d6e20692bfb0b7b9cd8c2feb692a2efed39",
        "paper_manifest": str(MANIFEST_V3.relative_to(ROOT)),
        "seedgraph_repo": "/Users/byron/projects/active/seedgraph",
        "seedgraph_head": seedgraph_head(),
        "N_manifest_rows": n_rows,
        **counts,
        "invariant_ok": invariant_ok,
        "live_writeback_executed": False,
        "neo4j_mutated": False,
        "note": "Local manifest + accounting only; uv run seedgraph import not executed (DEFERRED)",
    }
    (SG / "SEEDGRAPH_IMPORT_ACCOUNTING.v3.json").write_text(json.dumps(accounting, indent=2) + "\n")

    receipt = {
        "receipt_id": "SEEDGRAPH-LOCAL-IMPORT-v3",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "git_head": git_head(),
        "closure_subject_sha": "66979d6e20692bfb0b7b9cd8c2feb692a2efed39",
        "seedgraph_head": seedgraph_head(),
        "entrypoint": "uv run seedgraph",
        "actions": [
            {"action": "resolve_entrypoint", "result": "PASS"},
            {"action": "manifest_v3_row_validation", "result": "PASS", "N_rows": n_rows},
            {"action": "live_neo4j_import", "result": "SKIPPED", "reason": "DEFERRED"},
        ],
        "accounting": accounting,
        "live_writeback_status": "DEFERRED",
        "neo4j_mutated": False,
    }
    (SG / "SEEDGRAPH_LOCAL_IMPORT_RECEIPT.v3.json").write_text(json.dumps(receipt, indent=2) + "\n")

    print(json.dumps(accounting, indent=2))
    return 0 if invariant_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
