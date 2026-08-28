#!/usr/bin/env python3
"""Safe biocustody ZIP intake + G1/G2 provenance search (no execution)."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"
OUT = PAPER / "sources" / "biocustody_v0.2.0"
ZIP_PATH = Path("/Users/byron/projects/inbox/biocustody-stateshift-aws-bootstrap-v0.2.0.zip")
EVIDENCE_EXTRACT = Path(
    f"/Users/byron/projects/evidence/biocustody-stateshift-aws-bootstrap-v0.2.0/d78d9f00"
)

G1_CLAIMS = {
    "N_input_355": re.compile(r"\b355\b"),
    "N_protein_notation_239": re.compile(r"\b239\b"),
    "N_frameshift_113": re.compile(r"\b113\b"),
    "N_substitution_126": re.compile(r"\b126\b"),
    "N_naive_123": re.compile(r"\b123\b"),
    "N_loud_3": re.compile(r"\b3\b"),
    "N_silent_28": re.compile(r"\b28\b"),
}
G1_TERMS = re.compile(
    rb"frameshift|missense|HGVS|UniProt|FASTA|wild.?type|protein notation|array bounds",
    re.I,
)
G2_CLAIMS = {
    "N_fetched_742": re.compile(r"(?<!\d)742(?!\d)"),
    "N_downstream_642": re.compile(r"(?<!\d)642(?!\d)"),
    "N_multi_gene_287": re.compile(r"(?<!\d)287(?!\d)"),
    "N_discrepancy_100": re.compile(r"(?<!\d)100(?!\d)"),
}
G2_TERMS = re.compile(
    rb"ClinVar|CNV|copy.?number|multi.?gene|chromosome|gene attribution|pagination",
    re.I,
)
FLOAT_CONTEXT = re.compile(r"\d+\.\d+")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_fcg_hashes() -> dict[str, list[str]]:
    """content_sha256 -> [relative_paths]"""
    inv: dict[str, list[str]] = {}
    manifest = PAPER / "provenance" / "PAPER_SOURCE_MANIFEST.v4.jsonl"
    if not manifest.exists():
        manifest = PAPER / "provenance" / "PAPER_SOURCE_MANIFEST.v3.jsonl"
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        h = row.get("content_sha256") or row.get("sha256")
        rel = row.get("relative_path")
        if h and rel:
            inv.setdefault(h, []).append(rel)
    return inv


def is_text_candidate(name: str, size: int) -> bool:
    if size > 5_000_000 or size == 0:
        return False
    if any(x in name for x in (".venv/", "__MACOSX", "site-packages", ".pyc", ".png", ".jpg")):
        return False
    return any(
        name.lower().endswith(ext)
        for ext in (".py", ".md", ".json", ".csv", ".tsv", ".yaml", ".yml", ".txt", ".sql", ".sh")
    )


def security_check(name: str, size: int, compress_size: int) -> list[str]:
    issues = []
    if ".." in name or name.startswith("/"):
        issues.append("PATH_TRAVERSAL")
    if compress_size and size / max(compress_size, 1) > 200:
        issues.append("HIGH_COMPRESSION_RATIO")
    if name.endswith((".sh", ".exe", ".bat")):
        issues.append("EXECUTABLE")
    if name.endswith(".ipynb"):
        issues.append("NOTEBOOK")
    if name.endswith((".zip", ".tar", ".gz", ".bz2")) and not name.endswith(".json.gz"):
        issues.append("NESTED_ARCHIVE")
    return issues


def contextual_g1_match(text: str, rx: re.Pattern[str], label: str) -> bool:
    for m in rx.finditer(text):
        start = max(0, m.start() - 30)
        ctx = text[start : m.end() + 30]
        if FLOAT_CONTEXT.search(ctx) and label not in ("N_silent_28",):
            continue
        if any(k in ctx.lower() for k in ("count", "total", "n_", "fetched", "records", "aggregate", "=")):
            return True
    return False


def run_intake() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    expected_sha = "d78d9f006655920a25baf98e300dcb1c2bdca4899f7e3be112d4e29cdf420a20"
    h = hashlib.sha256()
    size = 0
    with ZIP_PATH.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            size += len(chunk)
    zip_sha = h.hexdigest()
    if zip_sha != expected_sha or size != 206174739:
        return {"status": "QUARANTINE", "reason": "hash_or_size_mismatch", "sha256": zip_sha, "size": size}

    fcg_hashes = load_fcg_hashes()
    seen_content: dict[str, str] = {}
    counts = Counter()
    members = []
    security_issues = []
    hash_matches = []
    g1_hits: list[dict] = []
    g2_hits: list[dict] = []
    g1_term_hits: list[str] = []
    g2_term_hits: list[str] = []

    with zipfile.ZipFile(ZIP_PATH) as z:
        for info in z.infolist():
            name = info.filename
            sec = security_check(name, info.file_size, info.compress_size)
            if sec:
                security_issues.append({"path": name, "issues": sec})
            terminal = "HASHED"
            content_sha = None
            duplicate_of = None
            excluded_reason = None
            if info.is_dir():
                terminal = "EXCLUDED"
                excluded_reason = "directory"
            elif any(x in name for x in (".venv/", "__MACOSX", "site-packages")):
                terminal = "EXCLUDED"
                excluded_reason = "venv_or_macosx"
            elif sec and "PATH_TRAVERSAL" in sec:
                terminal = "QUARANTINED"
            else:
                try:
                    data = z.read(info)
                    content_sha = sha256_bytes(data)
                    if content_sha in seen_content:
                        terminal = "DUPLICATE"
                        duplicate_of = seen_content[content_sha]
                    else:
                        seen_content[content_sha] = name
                    if content_sha in fcg_hashes:
                        hash_matches.append(
                            {
                                "zip_member": name,
                                "content_sha256": content_sha,
                                "fcg_paths": fcg_hashes[content_sha],
                                "classification": "EXACT_CONTENT_MATCH",
                            }
                        )
                    if is_text_candidate(name, info.file_size):
                        try:
                            text = data.decode("utf-8", errors="replace")
                            for label, rx in G1_CLAIMS.items():
                                if contextual_g1_match(text, rx, label):
                                    g1_hits.append(
                                        {"claim": label, "path": name, "context": text[max(0, rx.search(text).start() - 40) : rx.search(text).end() + 40][:120]}
                                    )
                            if G1_TERMS.search(data):
                                g1_term_hits.append(name)
                            for label, rx in G2_CLAIMS.items():
                                if contextual_g1_match(text, rx, label):
                                    g2_hits.append({"claim": label, "path": name, "context": text[max(0, rx.search(text).start() - 40) : rx.search(text).end() + 40][:120]})
                            if G2_TERMS.search(data):
                                g2_term_hits.append(name)
                        except Exception:
                            pass
                except Exception as e:
                    terminal = "FAILED"
                    excluded_reason = str(e)
            counts[terminal] += 1
            members.append(
                {
                    "archive_path": name,
                    "byte_size": info.file_size,
                    "compress_size": info.compress_size,
                    "content_sha256": content_sha,
                    "terminal_state": terminal,
                    "duplicate_of": duplicate_of,
                    "excluded_reason": excluded_reason,
                    "security_flags": sec,
                }
            )

    n = len(members)
    invariant = n == sum(counts.values())
    manifest_path = OUT / "ZIP_MEMBER_MANIFEST.jsonl"
    with manifest_path.open("w") as fh:
        for m in members:
            fh.write(json.dumps(m, sort_keys=True) + "\n")

    hash_lines = [f"{m['content_sha256']}  {m['archive_path']}" for m in members if m.get("content_sha256")]
    (OUT / "ZIP_MEMBER_HASHES.sha256").write_text("\n".join(hash_lines) + "\n")

    accounting = {
        "schema": "protein_hinge.biocustody.zip_accounting.v1",
        "generated_at_utc": utc_now(),
        "zip_path": str(ZIP_PATH),
        "zip_sha256": zip_sha,
        "zip_byte_count": size,
        "N_members": n,
        "N_hashed": counts["HASHED"],
        "N_duplicate": counts["DUPLICATE"],
        "N_excluded": counts["EXCLUDED"],
        "N_failed": counts["FAILED"],
        "N_quarantined": counts["QUARANTINED"],
        "invariant_ok": invariant,
        "expanded_byte_count": sum(m["byte_size"] for m in members if not m["archive_path"].endswith("/")),
    }
    (OUT / "ZIP_ACCOUNTING.json").write_text(json.dumps(accounting, indent=2) + "\n")

    security = {
        "receipt_id": "BIOCUSTODY-ZIP-SECURITY-v1",
        "generated_at_utc": utc_now(),
        "execution_allowed": False,
        "contents_executed": False,
        "archive_mutated": False,
        "issues_count": len(security_issues),
        "issues_sample": security_issues[:50],
        "status": "PASS_WITH_EXCLUSIONS" if not any("PATH_TRAVERSAL" in i["issues"] for i in security_issues) else "QUARANTINE",
    }
    (OUT / "ZIP_SECURITY_RECEIPT.json").write_text(json.dumps(security, indent=2) + "\n")

    # Extract only .git/objects and key docs for read-only git log (minimal)
    git_provenance = {"embedded_git_present": False, "commits": [], "remotes": []}
    with zipfile.ZipFile(ZIP_PATH) as z:
        git_files = [n for n in z.namelist() if "/.git/" in n]
        git_provenance["embedded_git_present"] = bool(git_files)
        git_provenance["git_file_count"] = len(git_files)

    if git_provenance["embedded_git_present"]:
        EVIDENCE_EXTRACT.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP_PATH) as z:
            prefix = "biocustody-stateshift-aws-bootstrap-v0.2.0/"
            for name in z.namelist():
                if not name.startswith(prefix + ".git/"):
                    continue
                rel = name[len(prefix) :]
                target = EVIDENCE_EXTRACT / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if name.endswith("/"):
                    continue
                if not target.exists():
                    target.write_bytes(z.read(name))
        git_dir = EVIDENCE_EXTRACT / ".git"
        if git_dir.exists():
            try:
                git_provenance["remotes"] = subprocess.check_output(
                    ["git", "--git-dir", str(git_dir), "remote", "-v"], text=True, stderr=subprocess.DEVNULL
                ).strip().splitlines()
                log = subprocess.check_output(
                    ["git", "--git-dir", str(git_dir), "log", "--oneline", "-20"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip().splitlines()
                git_provenance["commits"] = log
                git_provenance["HEAD"] = subprocess.check_output(
                    ["git", "--git-dir", str(git_dir), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
                ).strip()
            except subprocess.CalledProcessError as e:
                git_provenance["git_read_error"] = str(e)

    (OUT / "EMBEDDED_GIT_PROVENANCE.json").write_text(json.dumps(git_provenance, indent=2) + "\n")

    matches_path = OUT / "BIOCUSTODY_PROTEIN_HINGE_HASH_MATCHES.jsonl"
    with matches_path.open("w") as fh:
        for row in hash_matches:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    return {
        "accounting": accounting,
        "security": security,
        "hash_matches": len(hash_matches),
        "g1_hits": g1_hits[:30],
        "g2_hits": g2_hits[:30],
        "g1_term_files": len(set(g1_term_hits)),
        "g2_term_files": len(set(g2_term_hits)),
        "git_provenance": git_provenance,
    }


if __name__ == "__main__":
    print(json.dumps(run_intake(), indent=2)[:8000])
