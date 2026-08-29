#!/usr/bin/env python3
"""Capture and hash NewInML 2026 submission requirement sources."""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[3]
SUB = ROOT / "paper" / "newinml2026" / "submission"
SOURCES = SUB / "sources"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url: str, name: str) -> dict:
    req = Request(url, headers={"User-Agent": "protein-hinge-fcg/1.0"})
    data = urlopen(req, timeout=60).read()
    path = SOURCES / name
    path.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    return {
        "url": url,
        "local_path": str(path.relative_to(ROOT)),
        "sha256": digest,
        "byte_count": len(data),
        "media_type": "text/html" if name.endswith(".html") else "application/octet-stream",
        "retrieved_at_utc": utc_now(),
    }


def main() -> None:
    SOURCES.mkdir(parents=True, exist_ok=True)
    captures = [
        ("newinml2026_cfp.html", "https://newinml.github.io/NewInML2026NeurIPS/"),
        ("openreview_venues.html", "https://openreview.net/"),
    ]
    receipts = []
    for name, url in captures:
        try:
            receipts.append(fetch(url, name))
        except Exception as exc:
            receipts.append({"url": url, "local_path": None, "error": str(exc), "retrieved_at_utc": utc_now()})

    # NeurIPS 2026 style files — attempt media.neurips.cc
    style_url = "https://media.neurips.cc/Conferences/NeurIPS2026/Styles/neurips_2026.zip"
    try:
        receipts.append(fetch(style_url, "neurips_2026_style.zip"))
    except Exception as exc:
        receipts.append({"url": style_url, "local_path": None, "error": str(exc), "retrieved_at_utc": utc_now()})

    requirements = [
        {
            "requirement_id": "REQ-001",
            "source_artifact": "submission/sources/newinml2026_cfp.html",
            "quotation": "Format: 2–8 pages (excluding references) using the NeurIPS 2026 workshop template.",
            "status": "PARTIAL",
            "remediation": "Obtain and hash NeurIPS 2026 workshop LaTeX template when URL resolves",
            "affected": "manuscript/page_limit",
        },
        {
            "requirement_id": "REQ-002",
            "source_artifact": "submission/sources/newinml2026_cfp.html",
            "quotation": "Review process: Double-blind via OpenReview. Submissions must be fully anonymized.",
            "status": "FAIL",
            "remediation": "Remove author-identifying GitHub URLs and git metadata from anonymous PDF; use OpenReview profile",
            "affected": "submission/anonymous_artifact",
            "hard_gate": True,
        },
        {
            "requirement_id": "REQ-003",
            "source_artifact": "submission/sources/newinml2026_cfp.html",
            "quotation": "Non-archival: Work may be submitted to or published at other venues concurrently.",
            "status": "PASS",
            "remediation": None,
            "affected": "submission/venue_policy",
        },
        {
            "requirement_id": "REQ-004",
            "source_artifact": "submission/sources/newinml2026_cfp.html",
            "quotation": "Eligibility: Open to anyone who has not yet published at a top ML conference.",
            "status": "NOT_APPLICABLE",
            "remediation": "Operator attestation required",
            "affected": "submission/eligibility",
        },
        {
            "requirement_id": "REQ-005",
            "source_artifact": "submission/sources/newinml2026_cfp.html",
            "quotation": "Paper Submission Deadline: August 29, 2026",
            "status": "PASS",
            "remediation": None,
            "affected": "submission/deadline",
        },
        {
            "requirement_id": "REQ-006",
            "source_artifact": "submission/sources/newinml2026_cfp.html",
            "quotation": "Excluding submissions that are not serious: blank pages, topics not in ML, papers not following format.",
            "status": "PARTIAL",
            "remediation": "Template conformance check pending style zip capture",
            "affected": "manuscript/format",
            "hard_gate": True,
        },
        {
            "requirement_id": "REQ-007",
            "source_artifact": "submission/sources/openreview_venues.html",
            "quotation": "OpenReview profile must be up to date with publications and affiliations before submission.",
            "status": "PARTIAL",
            "remediation": "Operator must verify OpenReview profile current; not automatable here",
            "affected": "submission/openreview_profile",
            "hard_gate": True,
        },
    ]

    matrix = {
        "generated_at_utc": utc_now(),
        "hostname": subprocess.check_output(["hostname"], text=True).strip(),
        "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "requirements": requirements,
        "summary": {
            "captured_count": len([r for r in receipts if r.get("sha256")]),
            "PASS": sum(1 for r in requirements if r["status"] == "PASS"),
            "PARTIAL": sum(1 for r in requirements if r["status"] == "PARTIAL"),
            "FAIL": sum(1 for r in requirements if r["status"] == "FAIL"),
            "NOT_APPLICABLE": sum(1 for r in requirements if r["status"] == "NOT_APPLICABLE"),
            "hard_blockers": [r["requirement_id"] for r in requirements if r.get("hard_gate") and r["status"] != "PASS"],
        },
    }
    (SUB / "NEWINML_REQUIREMENTS_MATRIX.json").write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n")

    md_lines = ["# NewInML 2026 Requirements Matrix\n", f"Generated: {matrix['generated_at_utc']}\n"]
    for r in requirements:
        md_lines.append(f"## {r['requirement_id']}\n")
        md_lines.append(f"- **Status:** {r['status']}\n")
        md_lines.append(f"- **Source:** `{r['source_artifact']}`\n")
        md_lines.append(f"- **Requirement:** {r['quotation']}\n")
        if r.get("remediation"):
            md_lines.append(f"- **Remediation:** {r['remediation']}\n")
        md_lines.append("\n")
    (SUB / "NEWINML_REQUIREMENTS_MATRIX.md").write_text("".join(md_lines))

    source_receipt = {
        "generated_at_utc": utc_now(),
        "captures": receipts,
        "matrix_sha256": hashlib.sha256((SUB / "NEWINML_REQUIREMENTS_MATRIX.json").read_bytes()).hexdigest(),
    }
    (SUB / "NEWINML_SOURCE_RECEIPT.json").write_text(json.dumps(source_receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(matrix["summary"], indent=2))


if __name__ == "__main__":
    main()
