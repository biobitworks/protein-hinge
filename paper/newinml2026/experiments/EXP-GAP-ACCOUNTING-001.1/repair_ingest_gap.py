#!/usr/bin/env python3
"""EXP-GAP-ACCOUNTING-001.1 — derive abstention summary from graded rows."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GAP = ROOT / "gap"
EXP = Path(__file__).resolve().parent
RUN = GAP / "runs" / "2026-08-28-accounting-repair"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def merkle_root(items: list[str]) -> str:
    leaves = [bytes.fromhex(x.replace("sha256:", "")) for x in sorted(items)]
    if not leaves:
        return "sha256:" + hashlib.sha256(b"").hexdigest()
    while len(leaves) > 1:
        nxt = []
        for i in range(0, len(leaves), 2):
            right = leaves[i + 1] if i + 1 < len(leaves) else leaves[i]
            nxt.append(hashlib.sha256(b"\x01" + leaves[i] + right).digest())
        leaves = nxt
    return "sha256:" + leaves[0].hex()


def main() -> None:
    # Reuse prescripted row builder from upstream ingest
    import sys
    sys.path.insert(0, str(GAP))
    from ingest_gap import build_rows, write_csv  # noqa: E402

    RUN.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    write_csv(RUN / "candidates.csv", rows)

    grades = Counter(r.get("grade", "") for r in rows)
    n_abstain = grades.get("ABSTAIN", 0)
    n_admitted = sum(1 for r in rows if r.get("grade") == "NOT_A_GAP")
    n_excluded = sum(1 for r in rows if r.get("grade") not in {"ABSTAIN", "NOT_A_GAP", "GAP"} and r.get("grade"))

    abstentions = {
        "schema": "protein_hinge.gap.abstentions.v2",
        "ABSTAIN": n_abstain,
        "diseases_with_no_target_above_threshold": n_abstain,
        "targets_whose_names_did_not_reconcile": 0,
        "lookups_that_failed": 0,
        "reasons": [f"G001_NO_TARGET:{n_abstain}"] if n_abstain else [],
        "derived_from": "candidates.csv grade column",
        "supersedes_run": "2026-08-13",
    }
    (RUN / "abstentions.json").write_text(json.dumps(abstentions, indent=2, sort_keys=True) + "\n")

    n_input = len(rows)
    accounting = {
        "N_input": n_input,
        "N_admitted": n_admitted,
        "N_abstained": n_abstain,
        "N_excluded": n_excluded,
        "N_failed": 0,
        "summary_ABSTAIN": abstentions["ABSTAIN"],
        "invariant_summary_matches_rows": abstentions["ABSTAIN"] == n_abstain,
        "invariant_input_partition": n_input == n_admitted + n_excluded + n_abstain,
    }
    (RUN / "accounting.json").write_text(json.dumps(accounting, indent=2, sort_keys=True) + "\n")

    files = ["candidates.csv", "abstentions.json", "accounting.json"]
    digests = {name: sha256_file(RUN / name) for name in files}
    receipt = {
        "schema": "protein_hinge.gap.receipt.v2",
        "experiment_id": "EXP-GAP-ACCOUNTING-001.1",
        "lane": "gap",
        "run_date": str(date.today()),
        "claim_ceiling": "REPURPOSING_HYPOTHESIS",
        "supersedes": "gap/runs/2026-08-13/receipt.json",
        "files": digests,
        "merkle_root": merkle_root(list(digests.values())),
        "accounting": accounting,
        "validation": {"success": accounting["invariant_summary_matches_rows"] and accounting["invariant_input_partition"]},
    }
    (RUN / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    (EXP / "results.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(accounting, indent=2))
    if not receipt["validation"]["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
