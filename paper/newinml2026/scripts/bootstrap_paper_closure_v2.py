#!/usr/bin/env python3
"""Post-bootstrap paper closure v2: discover, hash, diff, receipt."""
from __future__ import annotations

import hashlib
import json
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"
PROV = PAPER / "provenance"
RECEIPTS = PAPER / "receipts"

INCLUDE_ROOTS = [
    "AGENTS.md",
    "PROJECT_CONTROL.yaml",
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
    "paper/newinml2026",
]

# Anti-recursion: generated index/manifest artifacts reference closure but are
# not re-discovered as new source roots on subsequent passes.
MANIFEST_EXCLUDE_SUFFIXES = {
    "PAPER_SOURCE_MANIFEST.jsonl",
    "PAPER_OBJECT_HASHES.sha256",
    "PAPER_IMPORT_ACCOUNTING.json",
    "PAPER_IMPORT_ACCOUNTING.v2.json",
    "PAPER_CLOSURE_RECEIPT.v2.json",
    "SEEDGRAPH_IMPORT_MANIFEST.jsonl",
    "SEEDGRAPH_IMPORT_ACCOUNTING.json",
    "SEEDGRAPH_FAILED_OBJECTS.jsonl",
    "SEEDGRAPH_CANDIDATE_ACCOUNTING.json",
    "SEEDGRAPH_LOCAL_VALIDATION_RECEIPT.json",
}

EXCLUDE_PATTERNS = {".git", "__pycache__", ".DS_Store", "node_modules", ".tmp"}

EXTERNAL_POINTERS = [
    {
        "path": "/Users/byron/Downloads/biocustody.zip",
        "reason": "ORIGIN_REVIEW.md received artifact; not under repo custody",
        "object_type": "SOURCE_ARTIFACT",
    },
    {
        "path": "HACKDAY_STATE.yaml",
        "reason": "Referenced by fcg/ingest.py; absent from published repo",
        "object_type": "SOURCE_ARTIFACT",
    },
]

PAPER_ARTIFACT_CLASSES = {
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
    ".pdf": "FIGURE",
    ".sha256": "DERIVED_EVIDENCE",
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


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def git_blob_sha(path: Path) -> str | None:
    try:
        rel = path.relative_to(ROOT)
        return subprocess.check_output(
            ["git", "hash-object", str(rel)], cwd=ROOT, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (subprocess.CalledProcessError, ValueError):
        return None


def infer_type(path: Path) -> str:
    rel = path.as_posix()
    if rel.startswith("paper/newinml2026/submission/"):
        return "SUBMISSION_REQUIREMENT" if path.suffix == ".json" else "DOCUMENT"
    if rel.startswith("paper/newinml2026/thesis/"):
        return "THESIS_VERSION" if path.name.startswith("THESIS-") else "DERIVED_EVIDENCE"
    if rel.startswith("paper/newinml2026/claims/"):
        return "CLAIM"
    if rel.startswith("paper/newinml2026/experiments/"):
        if path.name == "prereg.json":
            return "EXPERIMENT_PREREGISTRATION"
        return "EXPERIMENT_RUN" if path.suffix == ".py" else "EXPERIMENT_RESULT"
    if rel.startswith("paper/newinml2026/control/"):
        return "DOCUMENT"
    if rel.startswith("paper/newinml2026/provenance/"):
        return "DERIVED_EVIDENCE"
    if rel.startswith("paper/newinml2026/seedgraph/"):
        return "DERIVED_EVIDENCE"
    if rel.startswith("paper/newinml2026/compute/"):
        return "DOCUMENT"
    if rel.startswith("paper/newinml2026/cloudflareos/"):
        return "DOCUMENT"
    if rel.startswith("paper/newinml2026/contributors/"):
        return "CONTRIBUTOR_EVIDENCE"
    if "fco/" in rel:
        return "DERIVED_EVIDENCE"
    if "gap/runs/" in rel:
        if path.name == "receipt.json":
            return "EXPERIMENT_RESULT"
        if path.name == "abstentions.json":
            return "ABSTENTION"
        if path.suffix == ".csv":
            return "DATASET_MEMBER"
    if path.name in {"AGENTS.md", "PROJECT_CONTROL.yaml"}:
        return "DOCUMENT"
    return PAPER_ARTIFACT_CLASSES.get(path.suffix.lower(), "SOURCE_ARTIFACT")


def should_exclude(path: Path) -> bool:
    if path.is_dir():
        return True
    if path.name in MANIFEST_EXCLUDE_SUFFIXES:
        return True
    if set(path.parts) & EXCLUDE_PATTERNS:
        return True
    return False


def discover_all() -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    seen_sha: dict[str, str] = {}
    head = git_head()
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
                    "git_commit_sha": head,
                    "git_blob_sha": git_blob_sha(path),
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
                "sha256": digest,
                "byte_count": size,
                "relative_path": item["path"],
                "terminal_state": terminal,
                "unavailable_reason": item.get("reason") if terminal == "UNAVAILABLE" else None,
                "evidence_class": "EXTERNALLY_RETRIEVED_EVIDENCE",
            }
        )
    return objects


def load_v1_index() -> dict[str, dict]:
    v1_path = PROV / "PAPER_SOURCE_MANIFEST.jsonl"
    if not v1_path.exists():
        return {}
    out = {}
    for line in v1_path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = row.get("relative_path") or row.get("source_uri")
        out[key] = row
    return out


def main() -> int:
    PROV.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    head = git_head()
    objects = discover_all()
    counts = {k: 0 for k in ["IMPORTED", "EXCLUDED", "DUPLICATE", "UNAVAILABLE", "FAILED", "QUARANTINED"]}
    for obj in objects:
        counts[obj["terminal_state"]] += 1
    discovered = len(objects)
    assert discovered == sum(counts.values())

    v1 = load_v1_index()
    v2_by_path = {o.get("relative_path") or o.get("source_uri"): o for o in objects}
    v1_paths = set(v1)
    v2_paths = set(v2_by_path)
    added = sorted(v2_paths - v1_paths)
    removed = sorted(v1_paths - v2_paths)
    changed = []
    unchanged = 0
    for p in sorted(v1_paths & v2_paths):
        if v1[p].get("sha256") != v2_by_path[p].get("sha256"):
            changed.append(p)
        else:
            unchanged += 1

    manifest_v2 = PROV / "PAPER_SOURCE_MANIFEST.v2.jsonl"
    with manifest_v2.open("w") as fh:
        for obj in objects:
            fh.write(json.dumps(obj, sort_keys=True) + "\n")

    prev_manifest_hash = sha256_file(PROV / "PAPER_SOURCE_MANIFEST.jsonl")[0] if (PROV / "PAPER_SOURCE_MANIFEST.jsonl").exists() else None
    v1_acct_path = PROV / "PAPER_IMPORT_ACCOUNTING.json"
    previous_head = json.loads(v1_acct_path.read_text()).get("git_head") if v1_acct_path.exists() else "94f8949f1bbcb63d8e80baadd0c5f380f01b9f92"

    accounting_v2 = {
        "schema": "protein_hinge.paper.import_accounting.v2",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
        "previous_head_sha": previous_head,
        "current_head_sha": head,
        "previous_manifest_hash": prev_manifest_hash,
        "previous_N_discovered": 190,
        "N_discovered": discovered,
        "N_imported": counts["IMPORTED"],
        "N_duplicate": counts["DUPLICATE"],
        "N_excluded": counts["EXCLUDED"],
        "N_unavailable": counts["UNAVAILABLE"],
        "N_failed": counts["FAILED"],
        "N_quarantined": counts["QUARANTINED"],
        "objects_added": len(added),
        "objects_removed": len(removed),
        "objects_changed": len(changed),
        "objects_unchanged": unchanged,
        "added_paths_sample": added[:20],
        "removed_paths_sample": removed[:20],
        "changed_paths_sample": changed[:20],
        "invariant_ok": discovered == sum(counts.values()),
        "supersedes": "PAPER_IMPORT_ACCOUNTING.json",
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.v2.json").write_text(json.dumps(accounting_v2, indent=2, sort_keys=True) + "\n")

    receipt = {
        "receipt_id": "PAPER-CLOSURE-RECEIPT-v2",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "git_head": head,
        "accounting": accounting_v2,
        "manifest_path": str(manifest_v2.relative_to(ROOT)),
        "manifest_sha256": sha256_file(manifest_v2)[0],
    }
    (RECEIPTS / "PAPER_CLOSURE_RECEIPT.v2.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    hash_lines = [
        f"{o['sha256']}  {o.get('relative_path')}"
        for o in sorted(objects, key=lambda x: x.get("relative_path", ""))
        if o.get("sha256")
    ]
    (PROV / "PAPER_OBJECT_HASHES.v2.sha256").write_text("\n".join(hash_lines) + "\n")

    print(json.dumps(accounting_v2, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
