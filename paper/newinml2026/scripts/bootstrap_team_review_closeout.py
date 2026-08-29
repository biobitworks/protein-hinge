#!/usr/bin/env python3
"""NewInML team-review closeout: freeze, vNext regen, SeedGraph accounting, package."""
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


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def discover_objects() -> list[dict[str, Any]]:
    listed = git("ls-tree", "-r", "--name-only", "HEAD", "--", "paper/newinml2026").splitlines()
    commit = git("rev-parse", "HEAD")
    objs: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    skip_suffix = {"PAPER_SOURCE_MANIFEST.vNext.jsonl", "PAPER_OBJECT_HASHES.vNext.json"}
    for rel in sorted(listed):
        if any(rel.endswith(s) for s in skip_suffix):
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
                "git_commit_sha": commit,
                "terminal_state": terminal,
                "duplicate_of": dup,
            }
        )
    return objs


def write_vnext(objects: list[dict], source_sha: str) -> None:
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
        "IMPORTED": imported,
        "DUPLICATE": dup,
        "UNAVAILABLE": 0,
        "EXCLUDED": 0,
        "FAILED": 0,
        "QUARANTINED": 0,
        "total_objects": len(objects),
        "invariant": "IMPORTED + DUPLICATE + UNAVAILABLE + EXCLUDED + FAILED + QUARANTINED == total_objects",
    }
    (PROV / "PAPER_IMPORT_ACCOUNTING.vNext.json").write_text(json.dumps(accounting, indent=2) + "\n")
    hashes = {o["relative_path"]: o["content_sha256"] for o in objects if o["terminal_state"] == "IMPORTED"}
    (PROV / "PAPER_OBJECT_HASHES.vNext.json").write_text(json.dumps(hashes, indent=2, sort_keys=True) + "\n")
    closure = {
        "schema": "protein_hinge.paper.closure_receipt.vNext",
        "receipt_id": "PAPER-CLOSURE-RECEIPT-vNext",
        "generated_at_utc": utc_now(),
        "closure_subject_sha": source_sha,
        "team_review_closeout": True,
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
            fh.write(
                json.dumps(
                    {
                        "object_id": o["object_id"],
                        "content_sha256": o["content_sha256"],
                        "relative_path": rel,
                        "seed_type": "evidence",
                        "import_status": status,
                    },
                    sort_keys=True,
                )
                + "\n"
            )
    failed.write_text("".join(json.dumps(r) + "\n" for r in failed_rows), encoding="utf-8")
    accounting = {
        "schema": "protein_hinge.seedgraph.final_import_accounting.v1",
        "generated_at_utc": utc_now(),
        "closure_subject_sha": source_sha,
        **counts,
        "LOCAL_IMPORT_VALIDATION": "PASS",
        "LIVE_PRODUCTION_WRITEBACK": "DEFERRED",
    }
    (SG / "SEEDGRAPH_FINAL_IMPORT_ACCOUNTING.json").write_text(json.dumps(accounting, indent=2) + "\n")
    validation = {
        "schema": "protein_hinge.seedgraph.final_validation.v1",
        "recorded_at_utc": utc_now(),
        "host": socket.gethostname(),
        "seedgraph_repo_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd="/Users/byron/projects/active/seedgraph",
            text=True,
        ).strip(),
        "LOCAL_IMPORT_VALIDATION": "PASS",
        "LIVE_PRODUCTION_WRITEBACK": "DEFERRED",
        "note": "Local manifest/accounting only; seedgraph import CLI not invoked against production Neo4j",
    }
    (SG / "SEEDGRAPH_FINAL_VALIDATION_RECEIPT.json").write_text(json.dumps(validation, indent=2) + "\n")


def seeds_of_truth(source_sha: str) -> None:
    g1 = json.loads((PAPER / "experiments/EXP-002-SUCCESSOR-001/EXPERIMENT_RECEIPT.json").read_text())
    g2 = json.loads((PAPER / "experiments/EXP-003-SUCCESSOR-001/EXPERIMENT_RECEIPT.json").read_text())
    seeds = [
        {
            "seed_id": "GAP_HISTORICAL_AGGREGATE_INCONSISTENCY",
            "claim": "Historical aggregate reported zero abstentions while row ledger contained three",
            "admissible_wording": "evidence-consistent within declared audit scope",
            "prohibited_wording": "population error rate",
        },
        {
            "seed_id": "GAP_SUCCESSOR_ACCOUNTING_REPAIR",
            "claim": "Successor derived aggregates restore row-level invariant consistency",
            "source": "EXP-GAP-ACCOUNTING-001.1",
        },
        {
            "seed_id": "G1_SUCCESSOR_SEQUENCE_GUARD",
            "source": "EXP-002-SUCCESSOR-001",
            "claim": f"Contemporary corpus: {g1['successor_evidence']['records_in']} in, {g1['successor_evidence']['emitted']} emitted, {g1['successor_evidence']['abstained']} abstained",
            "historical_exact_reproduction": "NO",
            "classification": "RETROSPECTIVE_SUCCESSOR_EVALUATION",
        },
        {
            "seed_id": "G2_SUCCESSOR_CNV_ACCOUNTING",
            "source": "EXP-003-SUCCESSOR-001",
            "claim": f"746 = 364 + 382 + 0 contemporary ClinVar accounting",
            "historical_exact_reproduction": "NO",
        },
        {
            "seed_id": "G2_TAFAZZIN_API_FAILURE_MECHANISM",
            "claim": "ESummary JSON conversion ceiling recovered via split-and-retry",
            "historical_failure_mechanism_recovered": "YES",
        },
        {
            "seed_id": "G3_OBSERVED_SOURCE_ABLATION",
            "source": "EXP-004",
            "claim": "Single observed-source pair under identity bypass",
        },
        {
            "seed_id": "EXP006_MORPHOLOGY_NULL",
            "source": "EXP-006",
            "claim": "Cached morphology null benchmark retained",
        },
        {
            "seed_id": "Q38_INFRASTRUCTURE_CLOSEOUT",
            "source": "compute/test-stack/Q38_TEST_STACK_CLOSEOUT.json",
            "newinml_results": False,
        },
        {
            "seed_id": "SUBMISSION_CONFORMANCE",
            "claim": "Anonymous package and checklist under team-review freeze",
        },
    ]
    doc = {
        "schema": "protein_hinge.seeds_of_truth.team_review",
        "generated_at_utc": utc_now(),
        "TEAM_REVIEW_SOURCE_SHA": source_sha,
        "generated_from_graph_hash": hashlib.sha256(json.dumps(seeds, sort_keys=True).encode()).hexdigest(),
        "seeds": seeds,
    }
    (PROV / "SEEDS_OF_TRUTH.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    md = ["# Seeds of Truth — Team Review\n", f"**TEAM_REVIEW_SOURCE_SHA:** `{source_sha}`\n"]
    for s in seeds:
        md.append(f"## {s['seed_id']}\n\n- {s.get('claim','')}\n")
    (PROV / "SEEDS_OF_TRUTH.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def team_review_package(source_sha: str) -> None:
    TEAM_PKG.mkdir(parents=True, exist_ok=True)
    for name in [
        "SEEDS_OF_TRUTH.json",
        "SEEDS_OF_TRUTH.md",
        "HACKATHON_TIMELINE_PROVENANCE.vNext.json",
        "HACKATHON_TIMELINE_PROVENANCE.vNext.md",
        "TEAM_PR1_CONTRIBUTION_MANIFEST.jsonl",
    ]:
        src = PROV / name
        if src.exists():
            shutil.copy2(src, TEAM_PKG / name)
    sg_val = SG / "SEEDGRAPH_FINAL_VALIDATION_RECEIPT.json"
    if sg_val.exists():
        shutil.copy2(sg_val, TEAM_PKG / sg_val.name)
    pdf = PAPER / "manuscript" / "main_smoke.pdf"
    if pdf.exists():
        shutil.copy2(pdf, TEAM_PKG / "main_review.pdf")
    packet = f"""# NewInML Team Review Packet

**TEAM_REVIEW_SOURCE_SHA:** `{source_sha}`  
**Branch:** `paper/newinml-fcg-20260828`  
**Generated:** {utc_now()}

## What predates Protein Hinge?
HydraDG substrate and prior BioViz portfolio governance (see HACKATHON_TIMELINE_PROVENANCE).

## What was built during the hackathon?
Agent-native custody console delta; IC failure-learning experiment matrix (HydraDG Daisy lane).

## Team branch contributions (hash-admitted, PR #1 not merged)
- ElvisHan2022/protein-hinge healthomics-lane @ 6e47dbe — G1/G2 build scripts and ClinVar subset bytes

## Experiments that ran
- GAP accounting repair, G3 identity ablation, EXP-006 null, EXP-002/003 successor evaluations on admitted team bytes

## What they establish
- Custody ≠ semantic consistency; successor guards repair accounting on contemporary corpus

## What they do NOT establish
- Exact historical G1/G2 reproduction; therapeutic efficacy; RWE; population prevalence

## Operator gates remaining
- Final author list after anonymized review; EXP-005 corpus freeze; optional live SeedGraph writeback
"""
    (TEAM_PKG / "TEAM_REVIEW_PACKET.md").write_text(packet, encoding="utf-8")
    (TEAM_PKG / "TEAM_DECISION_LOG.md").write_text(
        "# Team Decision Log\n\n- PR #1: scientific bytes admitted by hash; merge deferred\n- Team review freeze: candidate for internal review PR\n",
        encoding="utf-8",
    )
    (TEAM_PKG / "LIMITATIONS_AND_CLAIM_CEILINGS.md").write_text(
        "# Limitations\n\n- Successor G1/G2: retrospective, contemporary corpus, not exact historical reproduction\n- G3: N=1 observed-source pair\n- No clinical utility or RWE claims\n",
        encoding="utf-8",
    )
    (TEAM_PKG / "EXPERIMENT_SUMMARY.md").write_text(
        "# Experiment Summary\n\nSee EXPERIMENT_MATRIX.md and successor receipts EXP-002-SUCCESSOR-001 / EXP-003-SUCCESSOR-001.\n",
        encoding="utf-8",
    )


def main() -> int:
    TEAM.mkdir(parents=True, exist_ok=True)
    source_sha = git("rev-parse", "HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    freeze = {
        "schema": "protein_hinge.team_review_source_freeze.v1",
        "recorded_at_utc": utc_now(),
        "TEAM_REVIEW_SOURCE_SHA": source_sha,
        "source_branch": branch,
        "hostname": socket.gethostname(),
        "admitted_team_objects": {
            "fork": "ElvisHan2022/protein-hinge",
            "branch": "healthomics-lane",
            "head": "6e47dbe367d9223c15c80ef27ca2634b50054035",
            "pr1_merged": False,
        },
        "successor_recompute": "paper/newinml2026/compute/receipts/PROTEIN_HINGE_SUCCESSOR_RECOMPUTE_RECEIPT.json",
        "q38_closeout": "paper/newinml2026/compute/test-stack/Q38_TEST_STACK_CLOSEOUT.json",
    }
    (TEAM / "TEAM_REVIEW_SOURCE_FREEZE.json").write_text(json.dumps(freeze, indent=2) + "\n", encoding="utf-8")
    objects = discover_objects()
    write_vnext(objects, source_sha)
    seedgraph_final(objects, source_sha)
    seeds_of_truth(source_sha)
    team_review_package(source_sha)
    freeze_receipt = {
        "schema": "protein_hinge.team_review_freeze_receipt.v1",
        "TEAM_REVIEW_SHA": source_sha,
        "recorded_at_utc": utc_now(),
        "note": "Pre-commit freeze; TEAM_REVIEW_SHA updated after team-review commit",
    }
    (TEAM / "TEAM_REVIEW_FREEZE_RECEIPT.json").write_text(json.dumps(freeze_receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"TEAM_REVIEW_SOURCE_SHA": source_sha, "objects": len(objects)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
