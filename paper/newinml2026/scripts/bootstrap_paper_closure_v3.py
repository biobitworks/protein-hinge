#!/usr/bin/env python3
"""Post-Wave-2 paper closure v3 — snapshot of WAVE2_SHA with content/metadata semantics."""
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
from bootstrap_paper_closure_v2 import (  # noqa: E402
    EXTERNAL_POINTERS,
    INCLUDE_ROOTS,
    MANIFEST_EXCLUDE_SUFFIXES,
    EXCLUDE_PATTERNS,
    PROV,
    RECEIPTS,
    infer_type,
    sha256_file,
    utc_now,
)

WAVE2_SHA = "66979d6e20692bfb0b7b9cd8c2feb692a2efed39"

# v3 closure artifacts are excluded from the WAVE2 snapshot (anti-recursion).
V3_SELF_EXCLUDE = {
    "PAPER_SOURCE_MANIFEST.v3.jsonl",
    "PAPER_IMPORT_ACCOUNTING.v3.json",
    "PAPER_OBJECT_HASHES.v3.sha256",
    "PAPER_CLOSURE_RECEIPT.v3.json",
    "bootstrap_paper_closure_v3.py",
}

METADATA_KEYS = (
    "git_commit_sha",
    "git_blob_sha",
    "source_uri",
    "source_repository",
    "attribution_class",
    "evidence_class",
    "seedgraph_status",
)


def git_run(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def should_exclude_name(name: str) -> bool:
    if name in MANIFEST_EXCLUDE_SUFFIXES or name in V3_SELF_EXCLUDE:
        return True
    parts = set(Path(name).parts)
    return bool(parts & EXCLUDE_PATTERNS)


def discover_at_commit(commit_sha: str) -> list[dict[str, Any]]:
    """Discover custody objects exactly as committed at closure_subject_sha."""
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
            if not rel or should_exclude_name(Path(rel).name):
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
        size = len(raw)
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
                "source_repository": "https://github.com/biobitworks/protein-hinge.git",
                "git_commit_sha": commit_sha,
                "git_blob_sha": blob_sha,
                "content_sha256": digest,
                "sha256": digest,
                "byte_count": size,
                "relative_path": rel,
                "evidence_class": "DETERMINISTIC_COMPUTATION",
                "attribution_class": "GIT_COMMITTER_METADATA",
                "claim_ceiling": "REPURPOSING_HYPOTHESIS",
                "source_status": "LOCAL_CUSTODY",
                "seedgraph_status": "PENDING",
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
                "byte_count": size,
                "relative_path": item["path"],
                "terminal_state": terminal,
                "unavailable_reason": item.get("reason") if terminal == "UNAVAILABLE" else None,
                "evidence_class": "EXTERNALLY_RETRIEVED_EVIDENCE",
                "closure_subject_sha": commit_sha,
            }
        )
    return objects


def load_manifest(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = row.get("relative_path") or row.get("source_uri")
        out[key] = row
    return out


def metadata_tuple(row: dict) -> tuple:
    return tuple(row.get(k) for k in METADATA_KEYS)


def classify_transition(old: dict | None, new: dict | None) -> tuple[str, str]:
    if old is None and new is not None:
        return "ADDED", "ADDED"
    if old is not None and new is None:
        return "REMOVED", "REMOVED"
    assert old is not None and new is not None
    old_content = old.get("content_sha256") or old.get("sha256")
    new_content = new.get("content_sha256") or new.get("sha256")
    content_state = "UNCHANGED" if old_content == new_content else "CHANGED"
    metadata_state = "UNCHANGED" if metadata_tuple(old) == metadata_tuple(new) else "CHANGED"
    return content_state, metadata_state


def bump(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


def main() -> int:
    closure_subject = WAVE2_SHA
    objects = discover_at_commit(closure_subject)

    # Annotate v2→v3 transitions per occurrence.
    v2 = load_manifest(PROV / "PAPER_SOURCE_MANIFEST.v2.jsonl")
    v3_by_path = {o.get("relative_path") or o.get("source_uri"): o for o in objects}
    all_paths = sorted(set(v2) | set(v3_by_path))

    content_counts = {"ADDED": 0, "UNCHANGED": 0, "CHANGED": 0, "REMOVED": 0}
    metadata_counts = {"ADDED": 0, "UNCHANGED": 0, "CHANGED": 0, "REMOVED": 0}
    content_changed_paths: list[str] = []
    metadata_changed_paths: list[str] = []

    for path in all_paths:
        old, new = v2.get(path), v3_by_path.get(path)
        cs, ms = classify_transition(old, new)
        bump(content_counts, cs)
        bump(metadata_counts, ms)
        if new is not None:
            new["content_state_since_v2"] = cs
            new["metadata_state_since_v2"] = ms
        if cs == "CHANGED":
            content_changed_paths.append(path)
        if ms == "CHANGED" and cs != "CHANGED":
            metadata_changed_paths.append(path)

    terminal_counts = {k: 0 for k in ["IMPORTED", "EXCLUDED", "DUPLICATE", "UNAVAILABLE", "FAILED", "QUARANTINED"]}
    for obj in objects:
        terminal_counts[obj["terminal_state"]] += 1
    discovered = len(objects)
    invariant_ok = discovered == sum(terminal_counts.values())

    manifest_v3 = PROV / "PAPER_SOURCE_MANIFEST.v3.jsonl"
    with manifest_v3.open("w") as fh:
        for obj in objects:
            fh.write(json.dumps(obj, sort_keys=True) + "\n")

    v2_receipt = json.loads((RECEIPTS / "PAPER_CLOSURE_RECEIPT.v2.json").read_text())
    v2_acct = json.loads((PROV / "PAPER_IMPORT_ACCOUNTING.v2.json").read_text())

    accounting_v3 = {
        "schema": "protein_hinge.paper.import_accounting.v3",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "branch": git_run(["branch", "--show-current"]),
        "closure_subject_sha": closure_subject,
        "closure_semantics": "SNAPSHOT_OF_PRIOR_COMMIT",
        "receipt_commit_sha": None,
        "WAVE2_SHA": closure_subject,
        "previous_closure_sha": v2_acct.get("current_head_sha"),
        "previous_manifest_hash": v2_receipt.get("manifest_sha256"),
        "previous_N_discovered": v2_acct.get("N_discovered"),
        "N_discovered": discovered,
        "N_imported": terminal_counts["IMPORTED"],
        "N_duplicate": terminal_counts["DUPLICATE"],
        "N_excluded": terminal_counts["EXCLUDED"],
        "N_unavailable": terminal_counts["UNAVAILABLE"],
        "N_failed": terminal_counts["FAILED"],
        "N_quarantined": terminal_counts["QUARANTINED"],
        "unique_content_objects": terminal_counts["IMPORTED"],
        "reference_objects": terminal_counts["DUPLICATE"],
        "content_added": content_counts["ADDED"],
        "content_changed": content_counts["CHANGED"],
        "content_unchanged": content_counts["UNCHANGED"],
        "content_removed": content_counts["REMOVED"],
        "metadata_added": metadata_counts["ADDED"],
        "metadata_changed": metadata_counts["CHANGED"],
        "metadata_unchanged": metadata_counts["UNCHANGED"],
        "metadata_removed": metadata_counts["REMOVED"],
        "content_changed_paths_sample": content_changed_paths[:25],
        "metadata_only_changed_paths_sample": metadata_changed_paths[:25],
        "invariant_ok": invariant_ok,
        "supersedes": "PAPER_IMPORT_ACCOUNTING.v2.json",
        "note": "content_state uses exact-byte SHA-256; metadata_state tracks git/provenance fields",
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.v3.json").write_text(
        json.dumps(accounting_v3, indent=2, sort_keys=True) + "\n"
    )

    receipt = {
        "receipt_id": "PAPER-CLOSURE-RECEIPT-v3",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "closure_subject_sha": closure_subject,
        "closure_semantics": "SNAPSHOT_OF_PRIOR_COMMIT",
        "receipt_commit_sha": None,
        "WAVE2_SHA": closure_subject,
        "accounting": accounting_v3,
        "manifest_path": str(manifest_v3.relative_to(ROOT)),
        "manifest_sha256": sha256_file(manifest_v3)[0],
        "supersedes": "PAPER_CLOSURE_RECEIPT.v2.json",
    }
    (RECEIPTS / "PAPER_CLOSURE_RECEIPT.v3.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    hash_lines = [
        f"{o['sha256']}  {o.get('relative_path')}"
        for o in sorted(objects, key=lambda x: x.get("relative_path", ""))
        if o.get("sha256")
    ]
    (PROV / "PAPER_OBJECT_HASHES.v3.sha256").write_text("\n".join(hash_lines) + "\n")

    print(json.dumps(accounting_v3, indent=2))
    return 0 if invariant_ok else 1


if __name__ == "__main__":
    sys.exit(main())
