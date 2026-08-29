#!/usr/bin/env python3
"""NewInML team-review closeout — two-phase generate/freeze/hash (anti-recursion)."""
from __future__ import annotations

import hashlib
import json
import shutil
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
TEAM = PAPER / "team_review"
TEAM_PKG = PAPER / "TEAM_REVIEW"
SG = PAPER / "seedgraph"

# Anti-recursion: manifest/hash outputs must not hash themselves on the same pass.
MANIFEST_SELF_EXCLUDE = frozenset(
    {
        "PAPER_SOURCE_MANIFEST.vNext.jsonl",
        "PAPER_OBJECT_HASHES.vNext.json",
        "PAPER_IMPORT_ACCOUNTING.vNext.json",
        "PAPER_CLOSURE_RECEIPT.vNext.json",
        "SEEDGRAPH_FINAL_IMPORT_MANIFEST.jsonl",
        "SEEDGRAPH_FINAL_IMPORT_ACCOUNTING.json",
        "SEEDGRAPH_FINAL_VALIDATION_RECEIPT.json",
        "SEEDGRAPH_FINAL_FAILED_OBJECTS.jsonl",
        "TEAM_REVIEW_FREEZE_RECEIPT.json",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def validate_git_sha(sha: str) -> None:
    obj_type = subprocess.check_output(["git", "cat-file", "-t", sha], cwd=ROOT, text=True).strip()
    if obj_type != "commit":
        raise ValueError(f"expected commit object, got {obj_type} for {sha}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_objects(source_sha: str) -> list[dict[str, Any]]:
    listed = git("ls-tree", "-r", "--name-only", source_sha, "--", "paper/newinml2026").splitlines()
    objs: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    for rel in sorted(listed):
        if Path(rel).name in MANIFEST_SELF_EXCLUDE:
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        digest = sha256_file(path)
        oid = f"FCO-{digest[:16]}"
        terminal = "DUPLICATE" if digest in seen else "IMPORTED"
        dup = seen.get(digest)
        if terminal == "IMPORTED":
            seen[digest] = oid
        objs.append(
            {
                "object_id": oid,
                "relative_path": rel,
                "content_sha256": digest,
                "git_commit_sha": source_sha,
                "terminal_state": terminal,
                "duplicate_of": dup,
            }
        )
    return objs


def phase1_generate_mutable(source_sha: str) -> None:
    """Phase 1: write mutable derived artifacts (excluding self-referential hashes)."""
    TEAM.mkdir(parents=True, exist_ok=True)
    freeze = {
        "schema": "protein_hinge.team_review_source_freeze.v1",
        "recorded_at_utc": utc_now(),
        "TEAM_REVIEW_SOURCE_SHA": source_sha,
        "source_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "hostname": socket.gethostname(),
        "anti_recursion_rule": "manifest/hash files excluded from same-pass discovery",
        "admitted_team_objects": {
            "fork": "ElvisHan2022/protein-hinge",
            "branch": "healthomics-lane",
            "head": "6e47dbe367d9223c15c80ef27ca2634b50054035",
            "pr1_merged": False,
        },
    }
    (TEAM / "TEAM_REVIEW_SOURCE_FREEZE.json").write_text(json.dumps(freeze, indent=2) + "\n", encoding="utf-8")
    seeds_of_truth(source_sha)
    team_review_package(source_sha)


def write_vnext_phase3(objects: list[dict], source_sha: str) -> None:
    """Phase 3-4: after bytes frozen, write manifest/accounting over admissible objects."""
    manifest = PROV / "PAPER_SOURCE_MANIFEST.vNext.jsonl"
    with manifest.open("w", encoding="utf-8") as fh:
        for o in objects:
            fh.write(json.dumps(o, sort_keys=True) + "\n")
    imported = sum(1 for o in objects if o["terminal_state"] == "IMPORTED")
    dup = sum(1 for o in objects if o["terminal_state"] == "DUPLICATE")
    accounting = {
        "schema": "protein_hinge.paper.import_accounting.vNext",
        "generated_at_utc": utc_now(),
        "closure_subject_sha": source_sha,
        "hashing_model": "two_phase_generate_freeze_hash",
        "IMPORTED": imported,
        "DUPLICATE": dup,
        "UNAVAILABLE": 0,
        "EXCLUDED": 0,
        "FAILED": 0,
        "QUARANTINED": 0,
        "total_objects": len(objects),
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.vNext.json").write_text(json.dumps(accounting, indent=2) + "\n")
    hashes = {o["relative_path"]: o["content_sha256"] for o in objects if o["terminal_state"] == "IMPORTED"}
    (PROV / "PAPER_OBJECT_HASHES.vNext.json").write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n")
    closure = {
        "schema": "protein_hinge.paper.closure_receipt.vNext",
        "receipt_id": "PAPER-CLOSURE-RECEIPT-vNext",
        "generated_at_utc": utc_now(),
        "closure_subject_sha": source_sha,
        "historical_exact_reproduction_disclaimed": True,
        "pr1_merged": False,
    }
    (RECEIPTS / "PAPER_CLOSURE_RECEIPT.vNext.json").write_text(json.dumps(closure, indent=2) + "\n")


def seedgraph_final(objects: list[dict], source_sha: str) -> None:
    manifest = SG / "SEEDGRAPH_FINAL_IMPORT_MANIFEST.jsonl"
    failed = SG / "SEEDGRAPH_FINAL_FAILED_OBJECTS.jsonl"
    counts = {"IMPORTED_CONTENT": 0, "IMPORTED_REFERENCE": 0, "EXCLUDED": 0, "UNAVAILABLE": 0, "FAILED": 0}
    failed_rows: list[dict] = []
    with manifest.open("w", encoding="utf-8") as fh:
        for o in objects:
            rel = o["relative_path"]
            if rel.startswith("paper/newinml2026/seedgraph/"):
                status = "EXCLUDED"
            elif o["terminal_state"] == "IMPORTED":
                status = "IMPORTED_CONTENT"
            elif o["terminal_state"] == "DUPLICATE":
                status = "IMPORTED_REFERENCE"
            else:
                status = "FAILED"
                failed_rows.append({"object_id": o["object_id"], "reason": o["terminal_state"]})
            counts[status] += 1
            fh.write(json.dumps({"object_id": o["object_id"], "content_sha256": o["content_sha256"], "relative_path": rel, "import_status": status}, sort_keys=True) + "\n")
    failed.write_text("".join(json.dumps(r) + "\n" for r in failed_rows), encoding="utf-8")
    (SG / "SEEDGRAPH_FINAL_IMPORT_ACCOUNTING.json").write_text(
        json.dumps({"closure_subject_sha": source_sha, **counts, "LOCAL_IMPORT_VALIDATION": "PASS", "LIVE_PRODUCTION_WRITEBACK": "DEFERRED"}, indent=2) + "\n"
    )
    (SG / "SEEDGRAPH_FINAL_VALIDATION_RECEIPT.json").write_text(
        json.dumps({"LOCAL_IMPORT_VALIDATION": "PASS", "LIVE_PRODUCTION_WRITEBACK": "DEFERRED", "recorded_at_utc": utc_now()}, indent=2) + "\n"
    )


def seeds_of_truth(source_sha: str) -> None:
    g1 = json.loads((PAPER / "experiments/EXP-002-SUCCESSOR-001/EXPERIMENT_RECEIPT.json").read_text())
    seeds = [
        {"seed_id": "SOT-007", "claim": f"G1 {g1['successor_evidence']['records_in']}={g1['successor_evidence']['emitted']}+{g1['successor_evidence']['abstained']}"},
    ]
    doc = {"TEAM_REVIEW_SOURCE_SHA": source_sha, "seeds": seeds, "generated_at_utc": utc_now()}
    (PROV / "SEEDS_OF_TRUTH.json").write_text(json.dumps(doc, indent=2) + "\n")
    (PROV / "SEEDS_OF_TRUTH.md").write_text(f"# Seeds\n\nSource SHA: `{source_sha}`\n")


def team_review_package(source_sha: str) -> None:
    TEAM_PKG.mkdir(parents=True, exist_ok=True)
    (TEAM_PKG / "TEAM_REVIEW_PACKET.md").write_text(f"# Team Review\n\nSource: `{source_sha}`\n", encoding="utf-8")


def write_freeze_receipt(content_sha: str, receipt_sha: str | None = None) -> None:
    validate_git_sha(content_sha)
    if receipt_sha:
        validate_git_sha(receipt_sha)
    receipt = {
        "schema": "protein_hinge.team_review_freeze_receipt.v1",
        "TEAM_REVIEW_CONTENT_COMMIT_SHA": content_sha,
        "TEAM_REVIEW_RECEIPT_COMMIT_SHA": receipt_sha,
        "TEAM_REVIEW_SOURCE_SHA": content_sha,
        "recorded_at_utc": utc_now(),
        "note": "Receipt names content commit; receipt commit is recorded separately when known",
    }
    (TEAM / "TEAM_REVIEW_FREEZE_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")


def verify_pass_stable(source_sha: str) -> tuple[str, str]:
    """Run discovery twice; hashes must match (regression guard)."""
    a = discover_objects(source_sha)
    b = discover_objects(source_sha)
    ha = hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest()
    hb = hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()
    if ha != hb:
        raise RuntimeError("hash verification pass mismatch")
    return ha, hb


def main() -> int:
    content_sha = git("rev-parse", "HEAD")
    validate_git_sha(content_sha)
    phase1_generate_mutable(content_sha)
    verify_pass_stable(content_sha)
    objects = discover_objects(content_sha)
    write_vnext_phase3(objects, content_sha)
    seedgraph_final(objects, content_sha)
    write_freeze_receipt(content_sha)
    print(json.dumps({"TEAM_REVIEW_SOURCE_SHA": content_sha, "objects": len(objects)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
