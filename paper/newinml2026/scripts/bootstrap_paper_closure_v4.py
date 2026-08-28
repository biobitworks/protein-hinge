#!/usr/bin/env python3
"""Post-Wave-3 paper closure v4 — snapshot of WAVE3_SHA."""
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
from bootstrap_paper_closure_v3 import (  # noqa: E402
    METADATA_KEYS,
    bump,
    classify_transition,
    discover_at_commit,
    git_run,
    load_manifest,
    sha256_file,
    utc_now,
    PROV,
    RECEIPTS,
)

# Updated after Wave-3 freeze commit.
WAVE3_SHA = "2453a9bdb400f00c17de36d9e4831fb60f312e83"

V4_SELF_EXCLUDE = {
    "PAPER_SOURCE_MANIFEST.v4.jsonl",
    "PAPER_IMPORT_ACCOUNTING.v4.json",
    "PAPER_OBJECT_HASHES.v4.sha256",
    "PAPER_CLOSURE_RECEIPT.v4.json",
    "bootstrap_paper_closure_v4.py",
}


def should_exclude_v4(name: str) -> bool:
    from bootstrap_paper_closure_v3 import should_exclude_name

    return should_exclude_name(name) or name in V4_SELF_EXCLUDE


def discover_at_commit_v4(commit_sha: str) -> list[dict[str, Any]]:
    from bootstrap_paper_closure_v2 import EXTERNAL_POINTERS, INCLUDE_ROOTS, EXCLUDE_PATTERNS, infer_type, sha256_file

    objects: list[dict[str, Any]] = []
    seen_sha: dict[str, str] = {}
    tree_paths: set[str] = set()
    for include in INCLUDE_ROOTS:
        base = include.rstrip("/")
        try:
            listed = git_run(["ls-tree", "-r", "--name-only", commit_sha, "--", base]).splitlines()
        except subprocess.CalledProcessError:
            continue
        for rel in listed:
            if not rel or should_exclude_v4(Path(rel).name):
                continue
            tree_paths.add(rel)
    for rel in sorted(tree_paths):
        path = ROOT / rel
        try:
            blob_sha = git_run(["rev-parse", f"{commit_sha}:{rel}"])
            raw = subprocess.check_output(["git", "show", f"{commit_sha}:{rel}"], cwd=ROOT)
        except subprocess.CalledProcessError:
            continue
        digest = hashlib.sha256(raw).hexdigest()
        obj_id = f"FCO-{digest[:16]}"
        terminal = "IMPORTED"
        duplicate_of = None
        if digest in seen_sha:
            terminal = "DUPLICATE"
            duplicate_of = seen_sha[digest]
        else:
            seen_sha[digest] = obj_id
        objects.append(
            {
                "object_id": obj_id,
                "type": infer_type(path),
                "source_uri": f"repo://protein-hinge/{rel}",
                "git_commit_sha": commit_sha,
                "git_blob_sha": blob_sha,
                "content_sha256": digest,
                "sha256": digest,
                "byte_count": len(raw),
                "relative_path": rel,
                "terminal_state": terminal,
                "duplicate_of": duplicate_of,
                "closure_subject_sha": commit_sha,
            }
        )
    for item in EXTERNAL_POINTERS:
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
                "relative_path": item["path"],
                "terminal_state": terminal,
                "closure_subject_sha": commit_sha,
            }
        )
    return objects


def main() -> int:
    closure_subject = WAVE3_SHA
    if closure_subject == "REPLACE_AT_FREEZE":
        closure_subject = git_run(["rev-parse", "HEAD"])
    objects = discover_at_commit_v4(closure_subject)
    v3 = load_manifest(PROV / "PAPER_SOURCE_MANIFEST.v3.jsonl")
    v4_by_path = {o.get("relative_path") or o.get("source_uri"): o for o in objects}
    all_paths = sorted(set(v3) | set(v4_by_path))
    content_counts = {k: 0 for k in ["ADDED", "UNCHANGED", "CHANGED", "REMOVED"]}
    metadata_counts = dict(content_counts)
    for path in all_paths:
        cs, ms = classify_transition(v3.get(path), v4_by_path.get(path))
        bump(content_counts, cs)
        bump(metadata_counts, ms)
        if path in v4_by_path:
            v4_by_path[path]["content_state_since_v3"] = cs
            v4_by_path[path]["metadata_state_since_v3"] = ms
    terminal_counts = {k: 0 for k in ["IMPORTED", "EXCLUDED", "DUPLICATE", "UNAVAILABLE", "FAILED", "QUARANTINED"]}
    for obj in objects:
        terminal_counts[obj["terminal_state"]] += 1
    discovered = len(objects)
    invariant_ok = discovered == sum(terminal_counts.values())
    manifest_v4 = PROV / "PAPER_SOURCE_MANIFEST.v4.jsonl"
    with manifest_v4.open("w") as fh:
        for obj in objects:
            fh.write(json.dumps(obj, sort_keys=True) + "\n")
    v3_acct = json.loads((PROV / "PAPER_IMPORT_ACCOUNTING.v3.json").read_text())
    accounting_v4 = {
        "schema": "protein_hinge.paper.import_accounting.v4",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "branch": git_run(["branch", "--show-current"]),
        "closure_subject_sha": closure_subject,
        "closure_semantics": "SNAPSHOT_OF_PRIOR_COMMIT",
        "receipt_commit_sha": None,
        "WAVE3_SHA": closure_subject,
        "previous_closure_subject_sha": v3_acct.get("closure_subject_sha"),
        "previous_N_discovered": v3_acct.get("N_discovered"),
        "N_discovered": discovered,
        "N_imported": terminal_counts["IMPORTED"],
        "N_duplicate": terminal_counts["DUPLICATE"],
        "N_excluded": terminal_counts["EXCLUDED"],
        "N_unavailable": terminal_counts["UNAVAILABLE"],
        "N_failed": terminal_counts["FAILED"],
        "N_quarantined": terminal_counts["QUARANTINED"],
        "content_added": content_counts["ADDED"],
        "content_changed": content_counts["CHANGED"],
        "content_unchanged": content_counts["UNCHANGED"],
        "content_removed": content_counts["REMOVED"],
        "metadata_added": metadata_counts["ADDED"],
        "metadata_changed": metadata_counts["CHANGED"],
        "metadata_unchanged": metadata_counts["UNCHANGED"],
        "metadata_removed": metadata_counts["REMOVED"],
        "invariant_ok": invariant_ok,
        "supersedes": "PAPER_IMPORT_ACCOUNTING.v3.json",
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.v4.json").write_text(json.dumps(accounting_v4, indent=2, sort_keys=True) + "\n")
    receipt = {
        "receipt_id": "PAPER-CLOSURE-RECEIPT-v4",
        "generated_at_utc": utc_now(),
        "closure_subject_sha": closure_subject,
        "closure_semantics": "SNAPSHOT_OF_PRIOR_COMMIT",
        "receipt_commit_sha": None,
        "WAVE3_SHA": closure_subject,
        "accounting": accounting_v4,
        "manifest_path": str(manifest_v4.relative_to(ROOT)),
        "manifest_sha256": sha256_file(manifest_v4)[0],
        "supersedes": "PAPER_CLOSURE_RECEIPT.v3.json",
    }
    (RECEIPTS / "PAPER_CLOSURE_RECEIPT.v4.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    hash_lines = [f"{o['sha256']}  {o.get('relative_path')}" for o in sorted(objects, key=lambda x: x.get('relative_path', '')) if o.get("sha256")]
    (PROV / "PAPER_OBJECT_HASHES.v4.sha256").write_text("\n".join(hash_lines) + "\n")
    print(json.dumps(accounting_v4, indent=2))
    return 0 if invariant_ok else 1


if __name__ == "__main__":
    sys.exit(main())
