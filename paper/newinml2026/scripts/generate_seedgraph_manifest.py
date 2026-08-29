#!/usr/bin/env python3
"""Generate SeedGraph import manifest from paper source manifest."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROV = ROOT / "paper" / "newinml2026" / "provenance"
SG = ROOT / "paper" / "newinml2026" / "seedgraph"


def main() -> None:
    SG.mkdir(parents=True, exist_ok=True)
    src = PROV / "PAPER_SOURCE_MANIFEST.v2.jsonl"
    if not src.exists():
        src = PROV / "PAPER_SOURCE_MANIFEST.jsonl"
    rows = [json.loads(line) for line in src.read_text().splitlines() if line.strip()]
    out = []
    for obj in rows:
        if obj["terminal_state"] not in {"IMPORTED", "DUPLICATE"}:
            continue
        out.append(
            {
                "object_id": obj["object_id"],
                "sha256": obj.get("sha256"),
                "seed_type": "evidence",
                "source_uri": obj["source_uri"],
                "relative_path": obj.get("relative_path"),
                "git_commit_sha": obj.get("git_commit_sha"),
                "object_type": obj["type"],
                "terminal_ingest_status": "PENDING",
                "duplicate_of": obj.get("duplicate_of"),
            }
        )
    manifest = SG / "SEEDGRAPH_IMPORT_MANIFEST.jsonl"
    with manifest.open("w") as fh:
        for row in out:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    accounting = {
        "N_manifest_rows": len(out),
        "N_pending": len(out),
        "N_ingested": 0,
        "N_failed": 0,
        "N_quarantined": 0,
        "live_writeback_executed": False,
        "note": "Local manifest only; live Neo4j import not executed",
    }
    (SG / "SEEDGRAPH_IMPORT_ACCOUNTING.json").write_text(json.dumps(accounting, indent=2) + "\n")
    (SG / "SEEDGRAPH_FAILED_OBJECTS.jsonl").write_text("")
    print(json.dumps(accounting, indent=2))


if __name__ == "__main__":
    main()
