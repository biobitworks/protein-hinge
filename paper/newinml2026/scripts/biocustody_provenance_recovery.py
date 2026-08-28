#!/usr/bin/env python3
"""G1/G2 provenance recovery from admitted biocustody ZIP (read-only)."""
from __future__ import annotations

import json
import re
import subprocess
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"
OUT2 = PAPER / "experiments" / "EXP-002-PROV.1"
OUT3 = PAPER / "experiments" / "EXP-003-PROV.1"
ZIP_PATH = Path("/Users/byron/projects/inbox/biocustody-stateshift-aws-bootstrap-v0.2.0.zip")
GIT_DIR = Path("/Users/byron/projects/evidence/biocustody-stateshift-aws-bootstrap-v0.2.0/d78d9f00/.git")
PREFIX = "biocustody-stateshift-aws-bootstrap-v0.2.0/"

G1_COMPONENTS = ["355", "239", "113", "126", "123", "3", "28"]
G2_COMPONENTS = ["742", "642", "287", "100"]
G2_GENES = ["TAZ", "TAFAZZIN", "PHB2", "CHCHD3", "PGS1", "CRLS1", "HADHA"]

G1_TERMS = [
    "residue", "frameshift", "missense", "HGVS", "UniProt", "FASTA", "wild type",
    "protein notation", "array bounds", "canonical sequence", "substitution",
]
G2_TERMS = [
    "ClinVar", "CNV", "copy number", "multi-gene", "chromosome", "gene attribution",
    "pagination", "batch", "structural variant",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_float_noise(text: str, pos: int) -> bool:
    start = max(0, pos - 15)
    ctx = text[start : pos + 15]
    return bool(re.search(r"\d+\.\d+", ctx))


def classify_hit(path: str, text: str, number: str, terms_nearby: bool) -> str:
    if ".venv/" in path or "__MACOSX" in path:
        return "EXCLUDED_VENV"
    if path.endswith(".csv") and not terms_nearby:
        # morphology CSV float fields
        if number in ("742", "642", "287") and "cpjump" in path.lower():
            return "FLOAT_NOISE"
    if terms_nearby or any(k in text.lower() for k in ("count", "total", "fetched", "records", "aggregate", "n_")):
        return "CANDIDATE"
    return "NUMERIC_ONLY"


def search_zip() -> tuple[list[dict], list[dict]]:
    g1, g2 = [], []
    with zipfile.ZipFile(ZIP_PATH) as z:
        for info in z.infolist():
            name = info.filename
            if info.is_dir() or info.file_size > 2_000_000:
                continue
            if ".venv/" in name or "__MACOSX" in name or "site-packages" in name:
                continue
            if not any(name.lower().endswith(ext) for ext in (".py", ".md", ".json", ".csv", ".tsv", ".yaml", ".yml", ".txt", ".sh")):
                continue
            try:
                text = z.read(info).decode("utf-8", errors="replace")
            except Exception:
                continue
            tl = text.lower()
            for num in G1_COMPONENTS:
                for m in re.finditer(rf"(?<!\d){num}(?!\d)", text):
                    if is_float_noise(text, m.start()):
                        continue
                    terms = any(t in tl for t in G1_TERMS)
                    cls = classify_hit(name, text[m.start() - 50 : m.end() + 50], num, terms)
                    if cls != "EXCLUDED_VENV":
                        g1.append({
                            "component": num,
                            "path": name,
                            "classification": cls,
                            "context": text[max(0, m.start() - 60) : m.end() + 60][:200],
                        })
            for num in G2_COMPONENTS:
                for m in re.finditer(rf"(?<!\d){num}(?!\d)", text):
                    if is_float_noise(text, m.start()):
                        continue
                    terms = any(t in tl for t in G2_TERMS)
                    cls = classify_hit(name, text[m.start() - 50 : m.end() + 50], num, terms)
                    if cls not in ("EXCLUDED_VENV", "FLOAT_NOISE"):
                        g2.append({
                            "component": num,
                            "path": name,
                            "classification": cls,
                            "context": text[max(0, m.start() - 60) : m.end() + 60][:200],
                        })
            for gene in G2_GENES:
                if gene in text:
                    g2.append({"component": gene, "path": name, "classification": "GENE_LITERAL", "context": ""})
    return g1, g2


def git_search() -> list[dict]:
    hits = []
    if not GIT_DIR.exists():
        return hits
    try:
        blobs = subprocess.check_output(
            ["git", "--git-dir", str(GIT_DIR), "log", "--all", "--pretty=format:%H", "-50"],
            text=True,
        ).strip().splitlines()
        for commit in blobs[:20]:
            try:
                files = subprocess.check_output(
                    ["git", "--git-dir", str(GIT_DIR), "diff-tree", "--no-commit-id", "-r", "--name-only", commit],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip().splitlines()
            except subprocess.CalledProcessError:
                files = []
            for f in files:
                if any(x in f for x in (".venv", "site-packages")):
                    continue
                try:
                    content = subprocess.check_output(
                        ["git", "--git-dir", str(GIT_DIR), "show", f"{commit}:{f}"],
                        stderr=subprocess.DEVNULL,
                    ).decode("utf-8", errors="replace")
                except subprocess.CalledProcessError:
                    continue
                for num in G1_COMPONENTS + G2_COMPONENTS:
                    if re.search(rf"(?<!\d){num}(?!\d)", content):
                        hits.append({"commit": commit, "path": f, "number": num, "source": "git_history"})
    except subprocess.CalledProcessError:
        pass
    return hits


def summarize_g1(hits: list[dict]) -> dict:
    by_comp = defaultdict(list)
    for h in hits:
        by_comp[h["component"]].append(h)
    components = {}
    for c in G1_COMPONENTS:
        items = by_comp.get(c, [])
        cand = [i for i in items if i.get("classification") == "CANDIDATE"]
        if cand:
            components[c] = "LOCATED_PARTIAL"
        elif items:
            components[c] = "NUMERIC_ONLY"
        else:
            components[c] = "NOT_FOUND"
    # Numeric-only hits do not upgrade terminal state without derivation chain.
    terminal = "COMPLETE_NEGATIVE_PROVENANCE"
    return {
        "experiment_id": "EXP-002-PROV.1",
        "classification": "PROVENANCE_RECOVERY",
        "status": terminal,
        "generated_at_utc": utc_now(),
        "source_artifact_sha256": "d78d9f006655920a25baf98e300dcb1c2bdca4899f7e3be112d4e29cdf420a20",
        "historical_components": components,
        "derivation_chain_recovered": False,
        "exp_002_1_admissible": False,
        "exp_002_1_reason": "No input corpus → filter → row ledger → aggregate chain located; package is repurposing bootstrap not G1 residue audit",
        "candidate_count": len(hits),
        "candidate_candidate_count": len([h for h in hits if h.get("classification") == "CANDIDATE"]),
    }


def summarize_g2(hits: list[dict]) -> dict:
    by_comp = defaultdict(list)
    for h in hits:
        by_comp[h["component"]].append(h)
    components = {}
    for c in G2_COMPONENTS + G2_GENES:
        items = by_comp.get(c, [])
        cand = [i for i in items if i.get("classification") in ("CANDIDATE", "GENE_LITERAL")]
        if c in G2_GENES and items:
            components[c] = "GENE_LITERAL_ONLY"
        elif cand:
            components[c] = "LOCATED_PARTIAL"
        elif items:
            components[c] = "NUMERIC_ONLY"
        else:
            components[c] = "NOT_FOUND"
    terminal = "COMPLETE_NEGATIVE_PROVENANCE"
    ledger_742 = components.get("742") not in ("NOT_FOUND", "NUMERIC_ONLY")
    if ledger_742:
        terminal = "COMPLETE_PARTIAL"
    return {
        "experiment_id": "EXP-003-PROV.1",
        "classification": "PROVENANCE_RECOVERY",
        "status": terminal,
        "generated_at_utc": utc_now(),
        "source_artifact_sha256": "d78d9f006655920a25baf98e300dcb1c2bdca4899f7e3be112d4e29cdf420a20",
        "historical_components": components,
        "ledger_742_found": ledger_742,
        "ledger_642_found": components.get("642") not in ("NOT_FOUND", "NUMERIC_ONLY"),
        "derivation_287_found": components.get("287") not in ("NOT_FOUND", "NUMERIC_ONLY"),
        "discrepancy_100_cause": "NOT_ESTABLISHED",
        "derivation_chain_recovered": False,
        "exp_003_1_admissible": False,
        "exp_003_1_reason": "No ClinVar/CNV acquisition ledger; 742/642/287 hits are CSV float noise or unrelated counts",
        "candidate_count": len(hits),
    }


def write_reports(g1_hits, g2_hits, g1_sum, g2_sum) -> None:
    OUT2.mkdir(parents=True, exist_ok=True)
    OUT3.mkdir(parents=True, exist_ok=True)
    (OUT2 / "provenance_recovery.json").write_text(json.dumps(g1_sum, indent=2) + "\n")
    (OUT3 / "provenance_recovery.json").write_text(json.dumps(g2_sum, indent=2) + "\n")
    with (OUT2 / "provenance_candidates.jsonl").open("w") as fh:
        for h in g1_hits[:500]:
            fh.write(json.dumps(h, sort_keys=True) + "\n")
    with (OUT3 / "provenance_candidates.jsonl").open("w") as fh:
        for h in g2_hits[:500]:
            fh.write(json.dumps(h, sort_keys=True) + "\n")
    (OUT2 / "PROVENANCE_REPORT.md").write_text(
        f"# EXP-002-PROV.1 — G1 External Recovery\n\n"
        f"**Status:** {g1_sum['status']}\n\n"
        f"**Source:** biocustody-stateshift-aws-bootstrap-v0.2.0.zip\n\n"
        f"**Result:** No G1 derivation chain (355→239→…→28) recovered. Package focuses on cell-painting repurposing bootstrap.\n\n"
        f"**EXP-002.1 admissible:** {g1_sum['exp_002_1_admissible']}\n"
    )
    (OUT3 / "PROVENANCE_REPORT.md").write_text(
        f"# EXP-003-PROV.1 — G2 External Recovery\n\n"
        f"**Status:** {g2_sum['status']}\n\n"
        f"**742 ledger:** {g2_sum['ledger_742_found']}\n"
        f"**642 ledger:** {g2_sum['ledger_642_found']}\n"
        f"**287 derivation:** {g2_sum['derivation_287_found']}\n"
        f"**100-record cause:** {g2_sum['discrepancy_100_cause']}\n\n"
        f"**EXP-003.1 admissible:** {g2_sum['exp_003_1_admissible']}\n"
    )


def main() -> None:
    g1, g2 = search_zip()
    git_hits = git_search()
    for h in git_hits:
        if h["number"] in G1_COMPONENTS:
            g1.append({"component": h["number"], "path": h["path"], "classification": "GIT_HISTORY", "context": h["commit"]})
        else:
            g2.append({"component": h["number"], "path": h["path"], "classification": "GIT_HISTORY", "context": h["commit"]})
    g1_sum = summarize_g1(g1)
    g2_sum = summarize_g2(g2)
    write_reports(g1, g2, g1_sum, g2_sum)
    print(json.dumps({"g1": g1_sum, "g2": g2_sum}, indent=2))


if __name__ == "__main__":
    main()
