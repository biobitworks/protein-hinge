#!/usr/bin/env python3
"""Post-Wave-5 paper closure v6 — includes biocustody external admission pointers."""
from __future__ import annotations

import hashlib
import json
import socket
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "paper" / "newinml2026" / "scripts"))
import bootstrap_paper_closure_v2 as v2  # noqa: E402
from bootstrap_paper_closure_v3 import (
    bump,
    classify_transition,
    git_run,
    load_manifest,
    sha256_file,
    utc_now,
    PROV,
    RECEIPTS,
)

V6_SELF_EXCLUDE = {
    "PAPER_SOURCE_MANIFEST.v6.jsonl",
    "PAPER_IMPORT_ACCOUNTING.v6.json",
    "PAPER_OBJECT_HASHES.v6.sha256",
    "PAPER_CLOSURE_RECEIPT.v6.json",
    "bootstrap_paper_closure_v6.py",
}

BIOCUSTODY_ZIP = Path("/Users/byron/projects/inbox/biocustody-stateshift-aws-bootstrap-v0.2.0.zip")


def should_exclude_v6(name: str) -> bool:
    from bootstrap_paper_closure_v3 import should_exclude_name

    return should_exclude_name(name) or name in V6_SELF_EXCLUDE


def external_pointers_v6() -> list[dict]:
    base = list(v2.EXTERNAL_POINTERS)
    base.append(
        {
            "path": str(BIOCUSTODY_ZIP),
            "reason": "Wave 5 operator handoff; hashed external SOURCE_ARTIFACT",
            "object_type": "SOURCE_ARTIFACT",
        }
    )
    return base


def discover_current_tree() -> list[dict[str, Any]]:
    commit_sha = git_run(["rev-parse", "HEAD"])
    objects: list[dict[str, Any]] = []
    seen_sha: dict[str, str] = {}
    tree_paths: set[str] = set()
    for include in v2.INCLUDE_ROOTS:
        base = include.rstrip("/")
        try:
            listed = git_run(["ls-tree", "-r", "--name-only", "HEAD", "--", base]).splitlines()
        except subprocess.CalledProcessError:
            continue
        for rel in listed:
            if not rel or should_exclude_v6(Path(rel).name):
                continue
            tree_paths.add(rel)
    for rel in sorted(tree_paths):
        path = ROOT / rel
        if not path.is_file():
            continue
        digest, size = sha256_file(path)
        obj_id = f"FCO-{digest[:16]}"
        terminal = "IMPORTED"
        duplicate_of = None
        if digest in seen_sha:
            terminal = "DUPLICATE"
            duplicate_of = seen_sha[digest]
        else:
            seen_sha[digest] = obj_id
        try:
            blob_sha = git_run(["rev-parse", f"HEAD:{rel}"])
        except subprocess.CalledProcessError:
            blob_sha = None
        objects.append(
            {
                "object_id": obj_id,
                "type": v2.infer_type(path),
                "source_uri": f"repo://protein-hinge/{rel}",
                "git_commit_sha": commit_sha,
                "git_blob_sha": blob_sha,
                "content_sha256": digest,
                "sha256": digest,
                "byte_count": size,
                "relative_path": rel,
                "terminal_state": terminal,
                "duplicate_of": duplicate_of,
                "closure_subject_sha": commit_sha,
            }
        )
    for item in external_pointers_v6():
        p = Path(item["path"])
        if p.is_absolute() and p.exists():
            digest, size = sha256_file(p)
            terminal = "IMPORTED"
        else:
            digest, size = None, None
            terminal = "UNAVAILABLE"
        objects.append(
            {
                "object_id": f"FCO-EXT-{hashlib.sha256(item['path'].encode()).hexdigest()[:16]}",
                "type": item["object_type"],
                "source_uri": item["path"],
                "content_sha256": digest,
                "sha256": digest,
                "byte_count": size,
                "relative_path": item["path"],
                "terminal_state": terminal,
                "closure_subject_sha": commit_sha,
                "note": item.get("reason"),
            }
        )
    return objects


def main() -> int:
    closure_subject = git_run(["rev-parse", "HEAD"])
    objects = discover_current_tree()
    v5 = load_manifest(PROV / "PAPER_SOURCE_MANIFEST.v5.jsonl")
    v6_by_path = {o.get("relative_path") or o.get("source_uri"): o for o in objects}
    all_paths = sorted(set(v5) | set(v6_by_path))
    content_counts = {k: 0 for k in ["ADDED", "UNCHANGED", "CHANGED", "REMOVED"]}
    metadata_counts = dict(content_counts)
    for path in all_paths:
        cs, ms = classify_transition(v5.get(path), v6_by_path.get(path))
        bump(content_counts, cs)
        bump(metadata_counts, ms)
        if path in v6_by_path:
            v6_by_path[path]["content_state_since_v5"] = cs
            v6_by_path[path]["metadata_state_since_v5"] = ms
    terminal_counts = {k: 0 for k in ["IMPORTED", "EXCLUDED", "DUPLICATE", "UNAVAILABLE", "FAILED", "QUARANTINED"]}
    for obj in objects:
        terminal_counts[obj["terminal_state"]] += 1
    discovered = len(objects)
    invariant_ok = discovered == sum(terminal_counts.values())
    manifest_v6 = PROV / "PAPER_SOURCE_MANIFEST.v6.jsonl"
    with manifest_v6.open("w") as fh:
        for obj in objects:
            fh.write(json.dumps(obj, sort_keys=True) + "\n")
    accounting_v6 = {
        "schema": "protein_hinge.paper.import_accounting.v6",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "branch": git_run(["branch", "--show-current"]),
        "closure_subject_sha": closure_subject,
        "closure_semantics": "CURRENT_TREE_PLUS_EXTERNAL_POINTERS",
        "receipt_commit_sha": closure_subject,
        "N_discovered": discovered,
        "N_imported": terminal_counts["IMPORTED"],
        "N_duplicate": terminal_counts["DUPLICATE"],
        "N_unavailable": terminal_counts["UNAVAILABLE"],
        "invariant_ok": invariant_ok,
        "biocustody_zip_admitted": BIOCUSTODY_ZIP.exists(),
        "supersedes": "PAPER_IMPORT_ACCOUNTING.v5.json",
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.v6.json").write_text(json.dumps(accounting_v6, indent=2, sort_keys=True) + "\n")
    receipt = {
        "receipt_id": "PAPER-CLOSURE-RECEIPT-v6",
        "generated_at_utc": utc_now(),
        "closure_subject_sha": closure_subject,
        "accounting": accounting_v6,
        "manifest_sha256": sha256_file(manifest_v6)[0],
        "supersedes": "PAPER_CLOSURE_RECEIPT.v5.json",
    }
    (RECEIPTS / "PAPER_CLOSURE_RECEIPT.v6.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    hash_lines = [
        f"{o['sha256']}  {o.get('relative_path')}"
        for o in sorted(objects, key=lambda x: x.get("relative_path", ""))
        if o.get("sha256")
    ]
    (PROV / "PAPER_OBJECT_HASHES.v6.sha256").write_text("\n".join(hash_lines) + "\n")
    print(json.dumps(accounting_v6, indent=2))
    return 0 if invariant_ok else 1


if __name__ == "__main__":
    sys.exit(main())
