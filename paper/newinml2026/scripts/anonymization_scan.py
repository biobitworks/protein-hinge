#!/usr/bin/env python3
"""Deterministic anonymization scanner for REQ-002."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
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
    # A standalone 40-hex token is a likely Git object/commit identity. Do not
    # match 64-hex SHA-256 values used by the anonymous FCO seal.
    ("git_sha40", re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.I)),
]

BLOCKING_LABELS = {
    "Byron",
    "biobitworks",
    "email",
    "/Users/",
    "github.com/biobitworks",
    "git_sha40",
}


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
                    "disposition": "BLOCKING_LEAK" if label in BLOCKING_LABELS else "REMEDIATED",
                }
            )
    return findings


def inspect_pdf_metadata(path: Path) -> tuple[list[dict], dict]:
    """Fail-closed PDF metadata inspection. Missing tool => BLOCKED_VALIDATION."""
    inspection = {
        "tool": "pdfinfo",
        "path": str(path),
        "command": f"pdfinfo {path}",
    }
    if not path.exists():
        inspection.update({"status": "BLOCKED_VALIDATION", "reason": "pdf_missing"})
        return [], inspection
    if not shutil.which("pdfinfo"):
        inspection.update({"status": "BLOCKED_VALIDATION", "reason": "pdfinfo_missing"})
        return [], inspection
    try:
        meta = subprocess.check_output(["pdfinfo", str(path)], text=True, stderr=subprocess.STDOUT)
        version = subprocess.check_output(["pdfinfo", "-v"], text=True, stderr=subprocess.STDOUT).strip()
        inspection.update({"status": "PASS", "tool_version": version.splitlines()[0] if version else None})
    except subprocess.CalledProcessError as e:
        inspection.update({"status": "BLOCKED_VALIDATION", "reason": "pdfinfo_failed", "error": str(e)})
        return [], inspection
    out = []
    for label, rx in PATTERNS:
        if rx.search(meta):
            out.append(
                {
                    "pattern": label,
                    "path": str(path.relative_to(ROOT)),
                    "disposition": "BLOCKING_LEAK" if label in BLOCKING_LABELS else "REMEDIATED",
                    "source": "pdf_metadata",
                }
            )
    inspection["metadata_sha256"] = hashlib.sha256(meta.encode()).hexdigest()
    return out, inspection


def main() -> int:
    targets = [SUB / "anonymous"]
    manuscript_files = [
        ROOT / "paper/newinml2026/manuscript/main.tex",
        ROOT / "paper/newinml2026/manuscript/references.bib",
        ROOT / "paper/newinml2026/manuscript/main_smoke.pdf",
    ]
    all_findings: list[dict] = []
    pdf_inspections: list[dict] = []
    validation_blocked = False
    for path in manuscript_files:
        if path.exists() and path.suffix in {".py", ".md", ".json", ".csv", ".tex", ".bib", ".yaml", ".yml", ".sh"}:
            all_findings.extend(scan_file(path))
        elif path.suffix == ".pdf":
            findings, inspection = inspect_pdf_metadata(path)
            pdf_inspections.append(inspection)
            if inspection.get("status") == "BLOCKED_VALIDATION":
                validation_blocked = True
            all_findings.extend(findings)
    for base in targets:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_dir():
                continue
            if path.suffix in {".py", ".md", ".json", ".csv", ".tex", ".bib", ".yaml", ".yml", ".sh"}:
                all_findings.extend(scan_file(path))
            elif path.suffix == ".pdf":
                findings, inspection = inspect_pdf_metadata(path)
                pdf_inspections.append(inspection)
                if inspection.get("status") == "BLOCKED_VALIDATION":
                    validation_blocked = True
                all_findings.extend(findings)
    blocking = [f for f in all_findings if f["disposition"] == "BLOCKING_LEAK"]
    if validation_blocked:
        terminal = "BLOCKED_VALIDATION"
        req_status = "BLOCKED_VALIDATION"
    elif blocking:
        terminal = "BLOCKING_LEAK"
        req_status = "FAIL"
    else:
        terminal = "CLEAN"
        req_status = "PASS"
    scan = {
        "generated_at_utc": utc_now(),
        "targets": [str(t.relative_to(ROOT)) for t in targets],
        "N_findings": len(all_findings),
        "N_blocking": len(blocking),
        "findings": all_findings,
        "pdf_inspections": pdf_inspections,
        "terminal": terminal,
    }
    receipt = {
        "receipt_id": "ANONYMIZATION-RECEIPT-v1",
        "generated_at_utc": utc_now(),
        "scan_terminal": terminal,
        "REQ-002_status": req_status,
        "N_blocking": len(blocking),
        "N_remediated": sum(1 for f in all_findings if f["disposition"] == "REMEDIATED"),
        "pdf_metadata_inspected": not validation_blocked and bool(pdf_inspections),
    }
    (SUB / "ANONYMIZATION_SCAN.json").write_text(json.dumps(scan, indent=2) + "\n")
    (SUB / "ANONYMIZATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    return 0 if terminal == "CLEAN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
