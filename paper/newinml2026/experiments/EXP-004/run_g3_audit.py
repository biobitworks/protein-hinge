#!/usr/bin/env python3
"""EXP-004 Lane A contract tests and Lane B audit + matched ablation."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
GAP = ROOT / "gap"
EXP = ROOT / "paper" / "newinml2026" / "experiments" / "EXP-004"
sys.path.insert(0, str(GAP))
from normalize import load_aliases, reconcile  # noqa: E402
from rules import grade_candidate  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lane_a_contract() -> dict:
    cases = [
        ("TTR", "TTR", "EXACT"),
        ("PDCD1", "PD-1", "MAPPED"),
        ("TAZ", "tafazzin", "UNRESOLVED"),
        ("CFB", "factor c", "UNRESOLVED"),
        ("PARP1", "", "UNRESOLVED"),
    ]
    rows = []
    for canonical, raw, expected in cases:
        got = reconcile(canonical, raw)
        rows.append(
            {
                "canonical_string": canonical,
                "raw_source_string": raw,
                "C0_outcome": got["outcome"],
                "expected": expected,
                "pass": got["outcome"] == expected,
            }
        )
    return {
        "lane": "A",
        "classification": "DETERMINISTIC_CONTRACT_TEST",
        "fixture_source": "gap/normalize.py _self_test cases + alias_table.json",
        "alias_table_sha256": sha256_file(GAP / "alias_table.json"),
        "N_total": len(rows),
        "N_pass": sum(1 for r in rows if r["pass"]),
        "rows": rows,
        "status": "PASS" if all(r["pass"] for r in rows) else "FAIL",
    }


def lane_b_audit() -> dict:
    pairs = []
    programs = GAP / "runs" / "2026-08-13" / "programs.csv"
    if programs.exists():
        for row in csv.DictReader(programs.open()):
            pairs.append(
                {
                    "raw_source_string": row.get("target_raw", ""),
                    "canonical_string": row.get("target_symbol", ""),
                    "raw_source_object_id": "gap/runs/2026-08-13/programs.csv",
                    "canonical_source_object_id": "gap/alias_table.json + OpenTargets canonical",
                    "alias_evidence": "gap/alias_table.json",
                    "expected_terminal": reconcile(row["target_symbol"], row["target_raw"])["outcome"],
                    "provenance_quality": "admitted_aug13_program_row",
                }
            )
    return {
        "lane": "B",
        "classification": "REAL_SOURCE_IDENTIFIER_AUDIT",
        "N_pairs": len(pairs),
        "pairs": pairs,
        "status": "COMPLETE" if pairs else "COMPLETE_NEGATIVE_PROVENANCE",
    }


def bypass_reconcile(canonical: str, raw: str) -> dict:
    """C1: identity guard bypassed — raw admitted without reconciliation."""
    return {"outcome": "BYPASS_ADMITTED", "target_symbol": raw or canonical, "alias_used": ""}


def matched_ablation(pairs: list[dict]) -> dict:
    rows = []
    for p in pairs:
        c0 = reconcile(p["canonical_string"], p["raw_source_string"])
        c1 = bypass_reconcile(p["canonical_string"], p["raw_source_string"])
        c0_row = {"target_symbol": p["canonical_string"], "target_reconcile": c0["outcome"], "association_score": 1.0, "drug_program": "x", "stage": "Preclinical", "n_trials": 0, "prior_trials": "", "lookup_failed": False}
        c1_row = dict(c0_row)
        c1_row["target_reconcile"] = "EXACT"
        c1_row["target_symbol"] = c1["target_symbol"]
        rows.append(
            {
                "raw_source_string": p["raw_source_string"],
                "canonical_string": p["canonical_string"],
                "C0_state": c0["outcome"],
                "C1_state": c1["outcome"],
                "C0_downstream_grade": grade_candidate(c0_row)["grade"],
                "C1_downstream_grade": grade_candidate(c1_row)["grade"],
                "C0_admissible": grade_candidate(c0_row)["grade"] != "ABSTAIN",
                "C1_admissible": grade_candidate(c1_row)["grade"] != "ABSTAIN",
                "metric_label": "unsupported_identity_admission" if c1["outcome"] == "BYPASS_ADMITTED" and c0["outcome"] == "UNRESOLVED" else "descriptive",
            }
        )
    return {"executed": bool(rows), "rows": rows, "N_bypass_admitted": sum(1 for r in rows if r["C1_admissible"] and not r["C0_admissible"])}


def wiring_defect_test() -> dict:
    """Prove reconcile(x,x) cannot exercise raw-vs-canonical disagreement."""
    biased = []
    for sym in ["TAZ", "PDCD1", "CFB", "UNKNOWN_GENE"]:
        r = reconcile(sym, sym)
        if r["outcome"] != "EXACT":
            biased.append(sym)
    return {
        "label": "EVALUATION_WIRING_DEFECT",
        "historical_invocation": "gap/ingest_gap.py reconcile(row['target_symbol'], row['target_symbol'])",
        "claim": "Self-comparison forces EXACT for any nonempty equal strings; cannot detect raw-vs-canonical mismatch",
        "test_symbols_checked": ["TAZ", "PDCD1", "CFB", "UNKNOWN_GENE"],
        "all_exact_under_self_compare": len(biased) == 0,
        "successor": "Use separate raw_source_string field (see gap/runs/2026-08-13/programs.csv target_raw)",
        "regression_test": "PASS" if len(biased) == 0 else "FAIL",
    }


def main() -> int:
    EXP.mkdir(parents=True, exist_ok=True)
    la = lane_a_contract()
    lb = lane_b_audit()
    ablation = matched_ablation(lb["pairs"]) if lb["pairs"] else {"executed": False}
    defect = wiring_defect_test()
    (EXP / "lane_a_contract_results.json").write_text(json.dumps(la, indent=2) + "\n")
    (EXP / "lane_b_source_audit.json").write_text(json.dumps(lb, indent=2) + "\n")
    (EXP / "matched_ablation_results.json").write_text(json.dumps(ablation, indent=2) + "\n")
    (EXP / "evaluation_wiring_defect.json").write_text(json.dumps(defect, indent=2) + "\n")
    if lb["pairs"]:
        terminal = "COMPLETE_ABLATION" if ablation["executed"] else "COMPLETE_CONTRACT_ONLY"
    else:
        terminal = "COMPLETE_CONTRACT_ONLY"
    summary = {"lane_a": la["status"], "lane_b": lb["status"], "terminal": terminal, "wiring_defect": defect["regression_test"]}
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
