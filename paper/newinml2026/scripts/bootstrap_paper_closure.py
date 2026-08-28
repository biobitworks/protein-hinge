#!/usr/bin/env python3
"""Discover, hash, and classify paper-scoped objects for NewInML 2026 FCG bootstrap."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"
PROV = PAPER / "provenance"

# Paper-scoped include roots (relative to repo root)
INCLUDE_ROOTS = [
    "fcg",
    "fto",
    "gap",
    "fco",
    "figures",
    "docs",
    "data",
    "model_trace",
    "scripts",
    "db",
    "site",
    "output/playwright",
    "README.md",
    "ORIGIN_REVIEW.md",
    "requirements.txt",
    "package.json",
    "package-lock.json",
]

# Explicit excludes within repo
EXCLUDE_PATTERNS = {
    ".git",
    "__pycache__",
    ".DS_Store",
    "node_modules",
    "paper/newinml2026/provenance/.tmp",
}

# External / out-of-repo pointers (UNAVAILABLE unless locally present)
EXTERNAL_POINTERS = [
    {
        "path": "/Users/byron/Downloads/biocustody.zip",
        "reason": "ORIGIN_REVIEW.md received artifact; not under repo custody",
        "object_type": "SOURCE_ARTIFACT",
    },
    {
        "path": "HACKDAY_STATE.yaml",
        "reason": "Referenced by fcg/ingest.py; absent from published repo per ORIGIN_REVIEW.md",
        "object_type": "SOURCE_ARTIFACT",
    },
]

OBJECT_TYPE_MAP = {
    ".py": "CODE_SNAPSHOT",
    ".js": "CODE_SNAPSHOT",
    ".json": "SOURCE_ARTIFACT",
    ".csv": "DATASET_MEMBER",
    ".svg": "FIGURE",
    ".png": "FIGURE",
    ".md": "DOCUMENT",
    ".html": "DOCUMENT",
    ".jsonl": "SOURCE_ARTIFACT",
    ".yaml": "SOURCE_ARTIFACT",
    ".yml": "SOURCE_ARTIFACT",
    ".txt": "DOCUMENT",
    ".db": "DATASET_SNAPSHOT",
    ".cyjs": "FIGURE",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def git_blob_sha(path: Path) -> str | None:
    try:
        rel = path.relative_to(ROOT)
        out = subprocess.check_output(
            ["git", "hash-object", str(rel)],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out
    except (subprocess.CalledProcessError, ValueError):
        return None


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def infer_type(path: Path) -> str:
    if "fco/" in path.as_posix():
        return "DERIVED_EVIDENCE"
    if "gap/runs/" in path.as_posix():
        if path.name == "receipt.json":
            return "EXPERIMENT_RESULT"
        if path.name == "abstentions.json":
            return "ABSTENTION"
        if path.suffix == ".csv":
            return "DATASET_MEMBER"
    if "fto/" in path.as_posix():
        return "SOURCE_ARTIFACT"
    if path.name in {"README.md", "ORIGIN_REVIEW.md"}:
        return "DOCUMENT"
    return OBJECT_TYPE_MAP.get(path.suffix.lower(), "SOURCE_ARTIFACT")


def should_exclude(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_PATTERNS:
        return True
    if path.is_dir():
        return True
    return False


def discover_repo_objects() -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    seen_sha: dict[str, str] = {}

    for include in INCLUDE_ROOTS:
        base = ROOT / include
        if not base.exists():
            continue
        files = [base] if base.is_file() else sorted(base.rglob("*"))
        for path in files:
            if should_exclude(path) or not path.is_file():
                continue
            rel = path.relative_to(ROOT).as_posix()
            digest, size = sha256_file(path)
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
                    "git_commit_sha": git_head(),
                    "git_blob_sha": git_blob_sha(path),
                    "sha256": digest,
                    "byte_count": size,
                    "media_type": "application/octet-stream",
                    "relative_path": rel,
                    "creation_timestamp": None,
                    "evidence_class": "DETERMINISTIC_COMPUTATION",
                    "attribution_class": "GIT_COMMITTER_METADATA",
                    "claim_ceiling": "REPURPOSING_HYPOTHESIS",
                    "license_rights_state": "repo_default",
                    "source_status": "LOCAL_CUSTODY",
                    "seedgraph_status": "PENDING",
                    "terminal_state": terminal,
                    "duplicate_of": duplicate_of,
                }
            )
    return objects


def discover_external() -> list[dict[str, Any]]:
    out = []
    for item in EXTERNAL_POINTERS:
        p = Path(item["path"])
        if p.is_absolute() and p.exists():
            digest, size = sha256_file(p)
            terminal = "IMPORTED"
        else:
            digest, size = None, None
            terminal = "UNAVAILABLE"
        out.append(
            {
                "object_id": f"FCO-EXT-{hashlib.sha256(item['path'].encode()).hexdigest()[:16]}",
                "type": item["object_type"],
                "source_uri": item["path"],
                "source_repository": None,
                "git_commit_sha": None,
                "git_blob_sha": None,
                "sha256": digest,
                "byte_count": size,
                "media_type": "application/octet-stream",
                "relative_path": item["path"],
                "creation_timestamp": None,
                "evidence_class": "EXTERNALLY_RETRIEVED_EVIDENCE",
                "attribution_class": "DOCUMENT_ATTRIBUTION",
                "claim_ceiling": "REPURPOSING_HYPOTHESIS",
                "license_rights_state": "unknown",
                "source_status": terminal,
                "seedgraph_status": "PENDING",
                "terminal_state": terminal,
                "unavailable_reason": item["reason"] if terminal == "UNAVAILABLE" else None,
            }
        )
    return out


def build_contributors() -> list[dict[str, Any]]:
    log = subprocess.check_output(
        ["git", "log", "--format=%H|%an|%ae|%cn|%ce|%s"],
        cwd=ROOT,
        text=True,
    ).strip().splitlines()
    rows = []
    for i, line in enumerate(log, 1):
        parts = line.split("|", 5)
        if len(parts) != 6:
            continue
        sha, an, ae, cn, ce, subj = parts
        rows.append(
            {
                "contribution_id": f"CE-GIT-{sha[:12]}",
                "commit_sha": sha,
                "author_name": an,
                "author_email": ae,
                "committer_name": cn,
                "committer_email": ce,
                "subject": subj,
                "attribution_class_author": "GIT_AUTHOR_METADATA",
                "attribution_class_committer": "GIT_COMMITTER_METADATA",
                "human_authorship_evidence": "UNKNOWN",
                "affected_objects": "repository-wide",
                "notes": "Git metadata is attribution evidence, not proof of human authorship.",
            }
        )
    return rows


def main() -> int:
    PROV.mkdir(parents=True, exist_ok=True)
    repo_objects = discover_repo_objects()
    external = discover_external()
    all_objects = repo_objects + external

    counts = {
        "IMPORTED": 0,
        "EXCLUDED": 0,
        "DUPLICATE": 0,
        "UNAVAILABLE": 0,
        "FAILED": 0,
        "QUARANTINED": 0,
    }
    for obj in all_objects:
        counts[obj["terminal_state"]] += 1

    discovered = len(all_objects)
    accounted = sum(counts.values())
    assert discovered == accounted, f"accounting mismatch: {discovered} != {accounted}"

    manifest_path = PROV / "PAPER_SOURCE_MANIFEST.jsonl"
    with manifest_path.open("w") as fh:
        for obj in all_objects:
            fh.write(json.dumps(obj, sort_keys=True) + "\n")

    accounting = {
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "git_head": git_head(),
        "branch": subprocess.check_output(
            ["git", "branch", "--show-current"], cwd=ROOT, text=True
        ).strip(),
        "N_discovered": discovered,
        "N_imported": counts["IMPORTED"],
        "N_excluded": counts["EXCLUDED"],
        "N_duplicate": counts["DUPLICATE"],
        "N_unavailable": counts["UNAVAILABLE"],
        "N_failed": counts["FAILED"],
        "N_quarantined": counts["QUARANTINED"],
        "invariant_ok": discovered == accounted,
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.json").write_text(
        json.dumps(accounting, indent=2, sort_keys=True) + "\n"
    )

    hash_lines = []
    for obj in sorted(all_objects, key=lambda x: x.get("relative_path", "")):
        if obj.get("sha256"):
            hash_lines.append(f"{obj['sha256']}  {obj.get('relative_path')}")
    (PROV / "PAPER_OBJECT_HASHES.sha256").write_text("\n".join(hash_lines) + "\n")

    contributors = build_contributors()
    csv_path = PAPER / "contributors" / "CONTRIBUTION_PROVENANCE.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(contributors[0].keys()))
        w.writeheader()
        w.writerows(contributors)
    (PAPER / "contributors" / "CONTRIBUTION_PROVENANCE.json").write_text(
        json.dumps(contributors, indent=2) + "\n"
    )

    print(json.dumps(accounting, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
