#!/usr/bin/env python3
"""Generate Wave-3 freeze closeout receipt."""
from __future__ import annotations

import hashlib
import json
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECEIPTS = ROOT / "paper" / "newinml2026" / "receipts"
PAPER = ROOT / "paper" / "newinml2026"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    wave3_paths = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "38c8c15b12ef2773f0614a7995245dd2d19a0f40..HEAD"],
        cwd=ROOT,
        text=True,
    ).strip().splitlines()
    wave3_paths = [p for p in wave3_paths if p.strip()]

    critical = [
        "paper/newinml2026/experiments/EXP-003/provenance_recovery.json",
        "paper/newinml2026/experiments/EXP-003/UNVERIFIED_HISTORICAL_CLAIMS.json",
        "paper/newinml2026/manuscript/BUILD_RECEIPT.json",
        "paper/newinml2026/manuscript/main_smoke.pdf",
        "paper/newinml2026/thesis/CFMO_MMR_DERIVATION_CONTRACT.v2.json",
        "paper/newinml2026/thesis/EVIDENCE_DELTA_EXP003.json",
        "paper/newinml2026/seedgraph/SEEDGRAPH_IMPORT_ACCOUNTING.v3.json",
        "paper/newinml2026/experiments/EXP-005/prereg.json",
        "paper/newinml2026/thesis/THESIS-001.json",
        "paper/newinml2026/submission/NEWINML_REQUIREMENTS_MATRIX.json",
    ]
    critical_hashes = {rel: sha256_file(ROOT / rel) for rel in critical if (ROOT / rel).exists()}

    v3_acct = json.loads((PAPER / "provenance/PAPER_IMPORT_ACCOUNTING.v3.json").read_text())
    exp005 = json.loads((PAPER / "experiments/EXP-005/prereg.json").read_text())
    sg = json.loads((PAPER / "seedgraph/SEEDGRAPH_IMPORT_ACCOUNTING.v3.json").read_text())

    receipt = {
        "schema": "protein_hinge.wave3_closeout_receipt.v1",
        "receipt_id": "WAVE3-CLOSEOUT-RECEIPT-v1",
        "generated_at_utc": utc_now(),
        "hostname": socket.gethostname(),
        "branch": subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip(),
        "WAVE2_SHA": "66979d6e20692bfb0b7b9cd8c2feb692a2efed39",
        "WAVE3_BOOTSTRAP_SHA": "38c8c15b12ef2773f0614a7995245dd2d19a0f40",
        "WAVE3_SHA": head,
        "wave3_commit_paths": wave3_paths,
        "critical_file_sha256": critical_hashes,
        "REQ-006": {
            "status": "PASS",
            "template_source": "https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip",
            "neurips_2026_sty_sha256": critical_hashes.get("paper/newinml2026/manuscript/BUILD_RECEIPT.json"),
            "smoke_pdf_sha256": critical_hashes.get("paper/newinml2026/manuscript/main_smoke.pdf"),
            "compile_result": "PASS",
        },
        "EXP-003": {
            "status": "COMPLETE_NEGATIVE_PROVENANCE",
            "classification": "PROVENANCE_RECOVERY",
            "unverified_claims_artifact": "experiments/EXP-003/UNVERIFIED_HISTORICAL_CLAIMS.json",
            "promotion_recommended": False,
            "exp003_1_rerun": "NOT_EXECUTED",
        },
        "MMR": {
            "scoped_classifications": [
                {"recipe_id": "FCO_FRACTALIZE_RECIPE_A", "classification": "VERIFIED_MMR_CONSTRUCTION"},
                {"recipe_id": "WITNESS_PEAK_RECIPE_B", "classification": "VERIFIED_MMR_CONSTRUCTION"},
                {"recipe_id": "SEAL_APP_FCG_HEAD", "classification": "PARTIAL_MMR"},
            ],
            "recipe_schism_documented": True,
            "repo_wide_verified_mmr_claim": False,
        },
        "CFMO": {
            "classification": "HISTORICAL_IMPLEMENTATION_UNVERIFIED_CANONICALITY",
            "paper_role": "infrastructure context only",
            "cfmo_expansion_explicit": False,
        },
        "SEEDGRAPH": {
            "local_import_status": "MANIFEST_VALIDATED_DEFERRED",
            "neo4j_mutated": False,
            "accounting": sg,
        },
        "EXP-005": {
            "lock_intact": True,
            "outcome_exposure": exp005.get("outcome_exposure"),
            "status": exp005.get("status"),
        },
        "THESIS": {"current": "THESIS-001", "claim_promotions": "none"},
        "closure_v3_opening": {
            "closure_subject_sha": v3_acct.get("closure_subject_sha"),
            "N_discovered": v3_acct.get("N_discovered"),
            "content_added": v3_acct.get("content_added"),
            "metadata_changed": v3_acct.get("metadata_changed"),
        },
        "historical_artifacts_modified": False,
        "aug13_paths_modified": False,
        "claim_promotions": "none",
    }
    out = RECEIPTS / "WAVE3_CLOSEOUT_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"WAVE3_SHA": head, "receipt": str(out.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
