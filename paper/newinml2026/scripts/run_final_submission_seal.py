#!/usr/bin/env python3
"""Local final NewInML submission seal — mirrors CI workflow."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"
MANUSCRIPT = PAPER / "manuscript"
SUB = PAPER / "submission"
DIST = SUB / "dist"
BUNDLE = DIST / "reviewer_bundle"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_sha() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def build_pdf() -> Path:
    subprocess.check_call(["bash", "build.sh"], cwd=MANUSCRIPT)
    pdf = MANUSCRIPT / "main_smoke.pdf"
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise SystemExit("PDF build failed")
    return pdf


def check_log() -> None:
    log = MANUSCRIPT / "build" / "main.log"
    if not log.exists():
        raise SystemExit("missing build log")
    text = log.read_text(errors="replace")
    if re.search(r"LaTeX Warning: (There were undefined references|Citation .* undefined|Reference .* undefined)", text):
        raise SystemExit("unresolved references/citations")


def page_gate(pdf: Path) -> dict:
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    total = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    refs_page = checklist_page = None
    for p in range(1, total + 1):
        text = subprocess.check_output(
            ["pdftotext", "-f", str(p), "-l", str(p), "-layout", str(pdf), "-"],
            text=True,
            errors="replace",
        )
        if refs_page is None and re.search(r"(?mi)^\s*(?:\d+\s+)?References\s*$", text):
            refs_page = p
        if checklist_page is None and re.search(
            r"(?mi)(?:NeurIPS\s+Paper\s+Checklist|Paper\s+Checklist)", text
        ):
            checklist_page = p
    content_pages = (refs_page - 1) if refs_page else None
    status = (
        "PASS"
        if refs_page is not None
        and content_pages is not None
        and 2 <= content_pages <= 8
        else "BLOCKED_VALIDATION"
    )
    return {
        "schema": "protein_hinge.newinml.page_gate.v1",
        "pages_total": total,
        "references_first_page": refs_page,
        "checklist_first_page": checklist_page,
        "content_pages_excluding_references": content_pages,
        "page_limit_rule": "2-8 content pages excluding references",
        "status": status,
        "recorded_at_utc": utc_now(),
    }


def font_gate(pdf: Path) -> dict:
    out = subprocess.check_output(["pdffonts", str(pdf)], text=True, errors="replace")
    type3 = "Type 3" in out and bool(re.search(r"Type\s+3\b", out))
    return {"status": "FAIL" if type3 else "PASS", "type3_detected": type3}


def build_fco_bundle(pdf: Path, page_gate_doc: dict) -> tuple[Path, dict]:
    if DIST.exists():
        shutil.rmtree(DIST)
    payload = BUNDLE / "payload"
    payload.mkdir(parents=True)
    shutil.copy2(pdf, payload / "paper.pdf")
    anon = SUB / "anonymous"
    if anon.exists():
        for item in anon.rglob("*"):
            if item.is_file():
                rel = item.relative_to(anon)
                dest = payload / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
    (payload / "PAGE_GATE.json").write_text(json.dumps(page_gate_doc, indent=2) + "\n")
    (BUNDLE / "VERIFY.md").write_text(
        """# Reviewer verification — DRM-free FCO seal

Run `python3 verify.py`. The verifier recomputes SHA-256 for every payload leaf,
then recomputes the manifest hash and compares with FCO_SEAL.json.

The seal proves byte identity and manifest closure only. It does not prove
biological truth, therapeutic efficacy, or correctness of every scientific inference.
"""
    )
    rows = []
    for p in sorted(x for x in payload.rglob("*") if x.is_file()):
        rel = p.relative_to(BUNDLE).as_posix()
        rows.append((rel, sha256_file(p), p.stat().st_size))
    manifest = "".join(f"{h}  {path}\n" for path, h, _ in rows)
    (BUNDLE / "FCO_PAYLOAD_MANIFEST.sha256").write_text(manifest)
    mh = hashlib.sha256(manifest.encode()).hexdigest()
    pdfh = next(h for path, h, _ in rows if path == "payload/paper.pdf")
    seal = {
        "schema": "protein_hinge.anonymous_fco_seal.v1",
        "algorithm": "SHA-256",
        "seal_semantics": "sha256(manifest_bytes); DRM-free content identity only",
        "payload_leaf_count": len(rows),
        "manifest_sha256": mh,
        "paper_pdf_sha256": pdfh,
        "git_identity_in_anonymous_bundle": False,
    }
    (BUNDLE / "FCO_SEAL.json").write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n")
    verify_py = BUNDLE / "verify.py"
    verify_py.write_text(
        """#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
root = Path(__file__).resolve().parent
manifest_path = root / 'FCO_PAYLOAD_MANIFEST.sha256'
seal = json.loads((root / 'FCO_SEAL.json').read_text())
failures = []
for line in manifest_path.read_text().splitlines():
    expected, rel = line.split('  ', 1)
    p = root / rel
    if not p.is_file():
        failures.append(f'MISSING {rel}')
        continue
    actual = hashlib.sha256(p.read_bytes()).hexdigest()
    if actual != expected:
        failures.append(f'HASH_MISMATCH {rel}')
if hashlib.sha256(manifest_path.read_bytes()).hexdigest() != seal['manifest_sha256']:
    failures.append('MANIFEST_HASH_MISMATCH')
pdf_hash = hashlib.sha256((root / 'payload/paper.pdf').read_bytes()).hexdigest()
if pdf_hash != seal['paper_pdf_sha256']:
    failures.append('PAPER_HASH_MISMATCH')
if failures:
    print('\\n'.join(failures))
    sys.exit(1)
print('FCO_SEAL_VERIFY=PASS')
print('manifest_sha256=' + seal['manifest_sha256'])
print('paper_pdf_sha256=' + pdf_hash)
"""
    )
    verify_py.chmod(0o755)
    subprocess.check_call([sys.executable, str(verify_py)], cwd=BUNDLE)
    zip_path = DIST / "newinml_anonymous_reviewer_bundle.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p in sorted(x for x in BUNDLE.rglob("*") if x.is_file()):
            rel = p.relative_to(BUNDLE).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            zf.writestr(info, p.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return zip_path, seal


def table_figure_maps() -> None:
    tables = [
        {"table_id": "tab:results", "cell_id": "r-g1-n", "value": "364", "seed_ids": ["SOT-007"], "source": "EXP-002-SUCCESSOR-001"},
        {"table_id": "tab:results", "cell_id": "r-g2-n", "value": "746", "seed_ids": ["SOT-010"], "source": "EXP-003-SUCCESSOR-001"},
        {"table_id": "tab:results", "cell_id": "r-exp006", "value": "50", "seed_ids": ["SOT-013"], "source": "EXP-006"},
    ]
    figures = [
        {"figure_id": "fig:pipeline", "element": "pipeline_sketch", "seed_ids": ["SOT-003"], "claim_ceiling": "architecture only"},
    ]
    with (SUB / "FINAL_TABLE_FCO_MAP.jsonl").open("w") as fh:
        for row in tables:
            fh.write(json.dumps(row) + "\n")
    with (SUB / "FINAL_FIGURE_FCO_MAP.jsonl").open("w") as fh:
        for row in figures:
            fh.write(json.dumps(row) + "\n")


def main() -> int:
    source_sha = git_sha()
    pdf_path = build_pdf()
    check_log()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        run1 = Path(tmp.name)
    shutil.copy2(pdf_path, run1)
    h1 = sha256_file(run1)
    build_pdf()
    h2 = sha256_file(pdf_path)
    run1.unlink(missing_ok=True)
    repro = h1 == h2
    pg = page_gate(pdf_path)
    fg = font_gate(pdf_path)
    (SUB / "PAGE_GATE.json").write_text(json.dumps(pg, indent=2) + "\n")
    zip_path, seal = build_fco_bundle(pdf_path, pg)
    table_figure_maps()
    subprocess.check_call([sys.executable, str(PAPER / "scripts/anonymization_scan.py")], cwd=ROOT)
    anon = json.loads((SUB / "ANONYMIZATION_RECEIPT.json").read_text())
    seeds_hash = json.loads((PAPER / "final_corpus_audit/SEEDS_OF_TRUTH.final.json").read_text())["derivation_hash"]
    candidate = SUB / "NewInML2026_ProteinHinge_ANONYMOUS_FINAL_CANDIDATE.pdf"
    shutil.copy2(pdf_path, candidate)
    receipt = {
        "schema": "protein_hinge.final_submission_fco_receipt.v1",
        "recorded_at_utc": utc_now(),
        "source_git_sha": source_sha,
        "final_pdf_sha256": h2,
        "final_pdf_bytes": pdf_path.stat().st_size,
        "reproducible_build_gate": "PASS" if repro else "FAIL",
        "build_sha256_run1": h1,
        "build_sha256_run2": h2,
        "anonymous_bundle_sha256": sha256_file(zip_path),
        "anonymous_manifest_sha256": seal["manifest_sha256"],
        "paper_pdf_leaf_sha256": seal["paper_pdf_sha256"],
        "seeds_graph_hash": seeds_hash,
        "page_gate": pg["status"],
        "content_pages_excluding_references": pg.get("content_pages_excluding_references"),
        "font_gate": fg["status"],
        "anonymity_gate": anon.get("REQ-002_status"),
        "citation_gate": "PASS",
        "FINAL_SUBMISSION_SEAL": "READY_FOR_OPERATOR_SUBMISSION" if pg["status"] == "PASS" and repro and anon.get("REQ-002_status") == "PASS" else "BLOCKED_VALIDATION",
        "operator_author_metadata": "OPERATOR_INFORMATION_REQUIRED",
    }
    (SUB / "FINAL_SUBMISSION_FCO_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    md = f"""# Final Submission FCO Receipt

- Source SHA: `{source_sha}`
- PDF SHA256: `{h2}`
- Reproducible build: {'PASS' if repro else 'FAIL'}
- Page gate: {pg['status']} (content pages: {pg.get('content_pages_excluding_references')})
- FCO seal: PASS
- FINAL_SUBMISSION_SEAL: {receipt['FINAL_SUBMISSION_SEAL']}
"""
    (SUB / "FINAL_SUBMISSION_FCO_RECEIPT.md").write_text(md)
    (SUB / "OPENREVIEW_UPLOAD_PACKET.md").write_text(
        f"""# OpenReview Upload Packet

## Paper
- Path: `paper/newinml2026/manuscript/main_smoke.pdf`
- SHA-256: `{h2}`
- Bytes: {pdf_path.stat().st_size}

## Supplement
- OpenReview field: NOT_VERIFIED (operator must confirm live form)
- Anonymous bundle: `{zip_path.relative_to(ROOT)}`
- Bundle SHA-256: `{sha256_file(zip_path)}`

## Author metadata
- OPERATOR_INFORMATION_REQUIRED

## Deadline
- 2026-08-29 08:59 UTC
- 2026-08-29 01:59 PDT (America/Los_Angeles)
"""
    )
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["FINAL_SUBMISSION_SEAL"] == "READY_FOR_OPERATOR_SUBMISSION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
