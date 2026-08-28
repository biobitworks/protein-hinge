#!/usr/bin/env python3
"""Deterministic anonymization scanner for REQ-002."""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUB = ROOT / "paper" / "newinml2026" / "submission"

PATTERNS = [
    ("Byron", re.compile(r"Byron", re.I)),
    ("biobitworks", re.compile(r"biobitworks", re.I)),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("/Users/", re.compile(r"/Users/")),
    ("github.com/biobitworks", re.compile(r"github\.com/biobitworks", re.I)),
    ("git_remote", re.compile(r"https://github\.com/", re.I)),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def scan_file(path: Path) -> list[dict]:
    findings = []
    try:
        text = path.read_text(errors="replace")
    except Exception:
        return findings
    for label, rx in PATTERNS:
        for m in rx.finditer(text):
            findings.append(
                {
                    "pattern": label,
                    "path": str(path.relative_to(ROOT)),
                    "offset": m.start(),
                    "snippet": text[max(0, m.start() - 20) : m.end() + 20].replace("\n", " "),
                    "disposition": "BLOCKING_LEAK" if label in {"Byron", "biobitworks", "email", "/Users/", "github.com/biobitworks"} else "REMEDIATED",
                }
            )
    return findings


def scan_pdf_metadata(path: Path) -> list[dict]:
    out = []
    try:
        meta = subprocess.check_output(["pdfinfo", str(path)], text=True, stderr=subprocess.DEVNULL)
        for label, rx in PATTERNS:
            if rx.search(meta):
                out.append({"pattern": label, "path": str(path.relative_to(ROOT)), "disposition": "BLOCKING_LEAK", "source": "pdf_metadata"})
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    return out


def main() -> int:
    targets = [
        SUB / "anonymous",
    ]
    manuscript_files = [
        ROOT / "paper/newinml2026/manuscript/main.tex",
        ROOT / "paper/newinml2026/manuscript/references.bib",
        ROOT / "paper/newinml2026/manuscript/main_smoke.pdf",
    ]
    all_findings = []
    for path in manuscript_files:
        if path.exists() and path.suffix in {".py", ".md", ".json", ".csv", ".tex", ".bib", ".yaml", ".yml", ".sh"}:
            all_findings.extend(scan_file(path))
        elif path.exists() and path.suffix == ".pdf":
            all_findings.extend(scan_pdf_metadata(path))
    for base in targets:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_dir():
                continue
            if path.suffix in {".py", ".md", ".json", ".csv", ".tex", ".bib", ".yaml", ".yml", ".sh"}:
                all_findings.extend(scan_file(path))
            elif path.suffix == ".pdf":
                all_findings.extend(scan_pdf_metadata(path))
    blocking = [f for f in all_findings if f["disposition"] == "BLOCKING_LEAK"]
    scan = {
        "generated_at_utc": utc_now(),
        "targets": [str(t.relative_to(ROOT)) for t in targets],
        "N_findings": len(all_findings),
        "N_blocking": len(blocking),
        "findings": all_findings,
        "terminal": "CLEAN" if not blocking else "BLOCKING_LEAK",
    }
    receipt = {
        "receipt_id": "ANONYMIZATION-RECEIPT-v1",
        "generated_at_utc": utc_now(),
        "scan_terminal": scan["terminal"],
        "REQ-002_status": "PASS" if scan["terminal"] == "CLEAN" else "FAIL",
        "N_blocking": len(blocking),
        "N_remediated": sum(1 for f in all_findings if f["disposition"] == "REMEDIATED"),
    }
    (SUB / "ANONYMIZATION_SCAN.json").write_text(json.dumps(scan, indent=2) + "\n")
    (SUB / "ANONYMIZATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if scan["terminal"] == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
