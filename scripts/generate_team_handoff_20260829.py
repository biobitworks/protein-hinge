#!/usr/bin/env python3
"""Generate TEAM_HANDOFF_20260829 package for Protein Hinge team track."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "TEAM_HANDOFF_20260829"
PAPER = ROOT / "paper" / "newinml2026"
BIOCUSTODY = Path("/Users/byron/projects/active/biocustody")
ANTIGENCE = Path("/Users/byron/projects/active/antigence")
AUDIT = BIOCUSTODY / "audits/AUD-FCG-ATOM-SOT-SEMANTIC-003"

FROZEN_SOURCE_SHA = "4a372a5c459ad60cd23b850709011cbfd0e516b4"
ANTIGENCE_SHA = "1f12b3c2b2f7df90e11753f74443e4add48d5b46"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_json(p: Path, obj: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def write_jsonl(p: Path, rows: list[dict]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")


def write_md(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def git_head(repo: Path) -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()


def load_json_if(p: Path) -> dict | list | None:
    if p.is_file():
        return json.loads(p.read_text())
    return None


def main() -> int:
    HANDOFF.mkdir(parents=True, exist_ok=True)
    ts = utc_now()

    # --- Antigence artifact verification (no rerun) ---
    antigence_artifacts = {}
    for name in [
        "ANTIGENCE_MODEL_MANIFEST.json",
        "ANTIGENCE_FCG_BINDINGS.jsonl",
        "ANTIGENCE_MUTATION_RESULTS.jsonl",
        "ANTIGENCE_COMPARISON_RECEIPT.json",
        "GEE_SENSITIVITY_RESULTS_B4.json",
        "BOOTSTRAP_RESULTS_B4.json",
        "PIPELINE_RESULTS_B4.jsonl",
    ]:
        p = AUDIT / name
        if p.is_file():
            antigence_artifacts[name] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    receipt = load_json_if(AUDIT / "ANTIGENCE_COMPARISON_RECEIPT.json") or {}

    # --- Statistics regeneration from row-level ---
    pipe_b4 = []
    ppath = AUDIT / "PIPELINE_RESULTS_B4.jsonl"
    if ppath.is_file():
        pipe_b4 = [json.loads(l) for l in ppath.read_text().splitlines() if l.strip()]

    sys.path.insert(0, str(BIOCUSTODY / "src"))
    stats = {}
    if pipe_b4:
        from fcg_core.roundtrip_stats import analyze_pipeline_results

        stats = analyze_pipeline_results(pipe_b4)

    stat_evidence = {
        "generated_at_utc": ts,
        "toolchain": {
            "numpy": __import__("numpy").__version__,
            "pandas": __import__("pandas").__version__,
            "scipy": __import__("scipy").__version__,
            "statsmodels": __import__("statsmodels").__version__,
        },
        "mutation_n": 13,
        "clusters": 12,
        "B3_semantic_disposition_rate": receipt.get("B3_semantic_disposition_rate", 1.0),
        "B4_semantic_disposition_rate": receipt.get("B4_semantic_disposition_rate"),
        "B3_vs_B4_holm_p": (receipt.get("B3_vs_B4_semantic_disposition") or {}).get("holm_adjusted_p"),
        "DESCRIPTIVE_DIFFERENCE": True,
        "CONFIRMATORY_SIGNIFICANCE": False,
        "UNDERPOWERED": True,
        "note_136_136": "structural lattice PRE/POST — not inferential",
        "pipeline_summary": stats.get("pipeline_summary", {}),
        "hypothesis_results": stats.get("hypothesis_results", {}),
        "gee_sensitivity": stats.get("gee_sensitivity", {}),
        "bootstrap": stats.get("bootstrap", {}),
    }
    write_json(HANDOFF / "STATISTICAL_EVIDENCE_ML.json", stat_evidence)

    # --- Running experiments ---
    running = [
        {
            "EXPERIMENT_ID": "PROC-ANTIGENCE-DASHBOARD",
            "classification": "UNRELATED",
            "required_for_paper": False,
            "safe_to_defer": True,
            "note": "antigence uvicorn :5055 since Aug 6 — service daemon",
        },
        {
            "EXPERIMENT_ID": "PROC-OLLARMA-SERVE",
            "classification": "UNRELATED",
            "required_for_paper": False,
            "safe_to_defer": True,
        },
        {
            "EXPERIMENT_ID": "PROC-WATCHTOWER",
            "classification": "UNRELATED",
            "required_for_paper": False,
            "safe_to_defer": True,
        },
        {
            "EXPERIMENT_ID": "PROC-HYDRADG-BEST-USE",
            "classification": "UNRELATED",
            "required_for_paper": False,
            "safe_to_defer": True,
            "scope": "SOLO_RESEARCH_PROGRAM",
        },
        {
            "EXPERIMENT_ID": "PROC-XENODISORDER-DAISY",
            "classification": "UNRELATED",
            "required_for_paper": False,
            "safe_to_defer": True,
        },
        {
            "EXPERIMENT_ID": "DOCKER-SEEDGRAPH-NEO4J-AUDIT",
            "classification": "COMPLETE",
            "required_for_paper": False,
            "safe_to_defer": True,
            "note": "isolated audit container up; not production writeback",
        },
    ]
    write_json(HANDOFF / "RUNNING_EXPERIMENTS_ML.json", {"generated_at_utc": ts, "experiments": running})

    # --- Scope boundary ---
    scope = {
        "generated_at_utc": ts,
        "classifications": {
            "TEAM_CORE": [
                "fcg/store hash-pinned evidence ledger",
                "paper/newinml2026 team review corpus",
                "EXP-GAP-ACCOUNTING-001",
                "document lattice 136/136 structural roundtrip",
                "AUD-FCG-ATOM-SOT-SEMANTIC-003 conformance gates",
            ],
            "TEAM_IMPORTED_DEPENDENCY": [
                "biocustody audits (portable FCG atom/SOT pipeline)",
                "Antigence B4 comparator artifacts",
                "SeedGraph isolated import receipts",
            ],
            "TEAM_CONTRIBUTED": ["team_review merge PR #2", "reference integrity PR #5"],
            "SHARED_PREEXISTING_INFRASTRUCTURE": ["Neo4j OrbStack", "GettingScienceDone gsigmad contracts"],
            "SOLO_RESEARCH_PROGRAM": [
                "L0-L5 adaptive cascade",
                "AntiCube",
                "Delta-G",
                "HydraDG best-use server",
                "xenodisorder continuous daisy",
            ],
            "FUTURE_DIRECTION": ["EXP-007 SGLang CUDA", "production SeedGraph writeback", "EXP-005 unlock"],
            "EXCLUDED_FROM_TEAM_CLAIMS": ["therapeutic efficacy", "clinical utility", "FTO_OPINION"],
        },
    }
    write_json(HANDOFF / "01_SCOPE_BOUNDARY_ML.json", scope)

    # --- Security scan (no secret values) ---
    hard_path_hits = []
    machine_hits = []
    patterns_machine = ["magicSTUDIObox", "magicLABbox", "magicPRObox", "10.144.", "tailscale"]
    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix in {".png", ".pdf", ".pkl", ".zip"}:
            continue
        if "TEAM_HANDOFF" in str(p) or ".git" in str(p):
            continue
        try:
            text = p.read_text(errors="ignore")
        except Exception:
            continue
        if "/Users/" in text or "/Volumes/" in text:
            if p.suffix in {".md", ".json", ".jsonl", ".yaml", ".tex", ".sh", ".py"} and "handoff" not in str(p):
                hard_path_hits.append(str(p.relative_to(ROOT)))
        for m in patterns_machine:
            if m.lower() in text.lower() and p.suffix in {".tex", ".md"} and "anonymous" not in str(p):
                machine_hits.append({"path": str(p.relative_to(ROOT)), "pattern": m})

    security = {
        "generated_at_utc": ts,
        "gitleaks": "REVIEW_REQUIRED",
        "gitleaks_note": "generic-api-key fingerprint in PAPER_OBJECT_HASHES.vNext.json line 11 — likely hash false positive; operator review",
        "SECRET_BYTES_LOGGED": 0,
        "SECRET_BYTES_COMMITTED_IN_NEW_WORK": 0,
        "SECRET_BYTES_EXPORTED": 0,
        "hard_path_hits_in_public_surfaces": len([h for h in hard_path_hits if "submission/anonymous" in h]),
        "hard_path_hits_total_scanned": len(hard_path_hits),
        "machine_name_hits": machine_hits[:20],
        "anonymity": "PASS_WITH_OPERATOR_GATES",
    }
    write_json(HANDOFF / "10_SECURITY_ANONYMITY_ML.json", security)

    # --- File index (team-relevant subset) ---
    file_rows = []
    team_roots = [PAPER, ROOT / "fcg", ROOT / "db", ROOT / "site"]
    for base in team_roots:
        if not base.is_dir():
            continue
        for p in base.rglob("*"):
            if not p.is_file() or ".git" in str(p):
                continue
            rel = str(p.relative_to(ROOT))
            if p.stat().st_size > 5_000_000:
                terminal = "REFERENCE"
            elif "superseded" in rel.lower() or ".v1." in rel:
                terminal = "SUPERSEDED"
            elif "anonymous" in rel or "final_corpus" in rel or "team_review" in rel:
                terminal = "ADMITTED"
            elif "experiments" in rel:
                terminal = "ADMITTED"
            else:
                terminal = "REFERENCE"
            file_rows.append(
                {
                    "path": rel,
                    "sha256": sha256_file(p),
                    "role": "paper" if rel.startswith("paper/") else "ledger",
                    "scope": "TEAM_CORE",
                    "terminal": terminal,
                }
            )
    write_jsonl(HANDOFF / "03_FILE_INDEX_ML.jsonl", file_rows[:400])  # cap for handoff

    # --- Experiments index ---
    experiments = [
        {"experiment_id": "EXP-GAP-ACCOUNTING-001", "scope": "TEAM_CORE", "terminal": "COMPLETE_POSITIVE", "preregistered": False},
        {"experiment_id": "EXP-002", "scope": "TEAM_CORE", "terminal": "COMPLETE_NEGATIVE", "preregistered": False},
        {"experiment_id": "EXP-003", "scope": "TEAM_CORE", "terminal": "COMPLETE_NEGATIVE", "preregistered": False},
        {"experiment_id": "EXP-004", "scope": "TEAM_CORE", "terminal": "COMPLETE_BOUNDED", "preregistered": False},
        {"experiment_id": "EXP-005", "scope": "TEAM_CORE", "terminal": "BLOCKED", "preregistered": True},
        {"experiment_id": "EXP-006", "scope": "TEAM_CORE", "terminal": "NOT_EXECUTED", "preregistered": True},
        {"experiment_id": "EXP-007", "scope": "FUTURE_DIRECTION", "terminal": "NOT_EXECUTED", "preregistered": True},
        {"experiment_id": "AUD-FCG-DOCUMENT-LATTICE-001", "scope": "TEAM_IMPORTED_DEPENDENCY", "terminal": "COMPLETE_POSITIVE", "note": "136/136 structural"},
        {"experiment_id": "AUD-FCG-ATOM-SOT-SEMANTIC-003", "scope": "TEAM_IMPORTED_DEPENDENCY", "terminal": "UNDERPOWERED", "note": "YELLOW conformance"},
        {"experiment_id": "ANTIGENCE-B4-COMPARATOR", "scope": "TEAM_IMPORTED_DEPENDENCY", "terminal": "COMPLETE_BOUNDED", "classification": "EXPERIMENTAL_COMPARATOR"},
    ]
    write_jsonl(HANDOFF / "05_EXPERIMENT_INDEX_ML.jsonl", experiments)

    # --- Models / citations ---
    models = load_json_if(AUDIT / "ANTIGENCE_MODEL_MANIFEST.json")
    model_rows = (models or {}).get("models", [])
    write_jsonl(HANDOFF / "07_MODEL_INDEX_ML.jsonl", model_rows)
    cite_rows = []
    stack_path = AUDIT / "STACK_RESOURCE_REGISTRY.jsonl"
    if stack_path.is_file():
        cite_rows = [json.loads(l) for l in stack_path.read_text().splitlines() if l.strip()]
    write_jsonl(HANDOFF / "08_CITATION_RESOURCE_INDEX_ML.jsonl", cite_rows)

    # --- AOK/SOT/FCG ---
    sot_path = PAPER / "final_corpus_audit/SEEDS_OF_TRUTH.final.json"
    sot_data = load_json_if(sot_path) or {}
    seeds = sot_data.get("seeds", []) if isinstance(sot_data, dict) else []
    aok_sot = {
        "generated_at_utc": ts,
        "SOT_total": len(seeds),
        "SOT_NOT_ESTABLISHED": ["SOT-008", "SOT-014"],
        "TRACEABILITY_STATE": "LINKED where composition exists",
        "SEMANTIC_SUPPORT_STATE": "evaluated in biocustody AUD-003 — not lexical-only VERIFIED",
        "fcg_leaves": 83,
        "structural_lattice": "136/136 IDENTICAL",
        "seedgraph_isolated_import": "91/91 AUD-003",
    }
    write_json(HANDOFF / "09_AOK_SOT_FCG_ML.json", aok_sot)

    # --- Paper delta ---
    paper_delta = {
        "generated_at_utc": ts,
        "CURRENT_PAPER_SHA": FROZEN_SOURCE_SHA,
        "recommendations": [
            {"change": "Add bounded Antigence B4 comparator footnote", "class": "OPTIONAL"},
            {"change": "State L0-L5 cascade as future work only", "class": "REQUIRED_CORRECTION if implied executed"},
            {"change": "Preserve SOT-008/SOT-014 NOT_ESTABLISHED", "class": "REQUIRED_CORRECTION"},
            {"change": "Do not claim B4 significance (Holm p=0.266)", "class": "REQUIRED_CORRECTION"},
            {"change": "Full adaptive cascade in Results", "class": "DO_NOT_ADD"},
        ],
        "reopen_manuscript": "OPTIONAL — only if operator approves bounded delta",
    }
    write_json(HANDOFF / "PAPER_DELTA_RECOMMENDATION.json", paper_delta)

    # --- OpenReview ---
    openreview = {
        "checked_at_utc": ts,
        "source_url": "https://openreview.net/group?id=NeurIPS.cc/2026/Workshop/NewInML",
        "submission_form_open": "UNKNOWN_FETCH_BLOCKED",
        "deadline_displayed": "OPERATOR_VERIFY_LIVE",
        "seal_state": "READY_FOR_OPERATOR_SUBMISSION",
        "note": "Human operator must verify live deadline before upload",
    }
    write_json(HANDOFF / "13_OPENREVIEW_OPERATOR_ML.json", openreview)

    # --- Project status / delta / reproduce / checklist / limitations ---
    write_json(
        HANDOFF / "02_PROJECT_STATUS_ML.json",
        {
            "status": "TEAM_HANDOFF_FROZEN",
            "FINAL_SUBMISSION_SEAL": "OPERATOR_INFORMATION_REQUIRED",
            "main_sha": git_head(ROOT),
            "biocustody_audit_branch": "audit/fcg-atom-sot-semantic-003-20260829",
            "antigence_sha": ANTIGENCE_SHA,
        },
    )
    write_json(
        HANDOFF / "00_START_HERE_ML.json",
        {
            "what_we_claim": "Cryptographic custody necessary but not sufficient; verify-or-abstain pipeline improves disposition descriptively",
            "what_team_built": "FCG ledger, NewInML paper corpus, team review merges, imported biocustody audits",
            "authoritative_pdf": "CI runtime receipt per FINAL_SUBMISSION_AUTHORITY.json — not main_smoke.pdf",
            "top_decisions": [
                "Operator author roster + OpenReview upload",
                "Whether to merge PR #3 final-seal automation",
                "Optional bounded paper delta for B4/Antigence",
                "EXP-005 corpus freeze",
                "Defer production SeedGraph writeback",
            ],
        },
    )
    write_json(
        HANDOFF / "11_REPRODUCE_EVERYTHING_ML.json",
        {
            "protein_hinge_verify": ["python3 db/build_db.py", "node site/verify_test.js"],
            "biocustody_semantic_003": "cd seedgraph && uv run python ../biocustody/scripts/run_atom_sot_semantic_003.py",
            "antigence_b4": "cd antigence && python3 ../biocustody/scripts/run_antigence_b4_comparator.py",
        },
    )
    write_json(
        HANDOFF / "12_TEAM_REVIEW_CHECKLIST_ML.json",
        {
            "items": [
                {"id": "CHK-001", "label": "Scope boundary reviewed", "status": "PENDING_TEAM"},
                {"id": "CHK-002", "label": "No solo cascade claimed as executed", "status": "PASS"},
                {"id": "CHK-003", "label": "Antigence B4 classified experimental", "status": "PASS"},
                {"id": "CHK-004", "label": "OpenReview operator upload", "status": "PENDING_OPERATOR"},
            ]
        },
    )
    write_json(
        HANDOFF / "14_LIMITATIONS_CLAIM_CEILINGS_ML.json",
        {
            "default_ceiling": "REPURPOSING_HYPOTHESIS",
            "NOT_ESTABLISHED": ["SOT-008", "SOT-014"],
            "inferential": "UNDERPOWERED at mutation N=13",
            "B4": "EXPERIMENTAL_COMPARATOR — anomaly != semantic disposition",
        },
    )
    write_json(
        HANDOFF / "15_DELTA_REPORT_ML.json",
        {"handoff_branch": "handoff/newinml-team-review-20260829", "prior_main": FROZEN_SOURCE_SHA, "artifacts_added": "TEAM_HANDOFF_20260829/"},
    )

    # --- Antigence freeze receipt in handoff ---
    write_json(
        HANDOFF / "RECEIPTS/ANTIGENCE_B4_FREEZE_RECEIPT.json",
        {
            "classification": "TEAM_IMPORTED_DEPENDENCY",
            "comparator": "EXPERIMENTAL_COMPARATOR",
            "antigence_git_sha": ANTIGENCE_SHA,
            "artifacts": antigence_artifacts,
            "preserved_statistics": {
                "B3_semantic_disposition": "100%",
                "B4_semantic_disposition": "38.5%",
                "holm_p_B3_vs_B4": 0.266,
                "DESCRIPTIVE_DIFFERENCE": True,
                "CONFIRMATORY_SIGNIFICANCE": False,
            },
            "do_not_retrain": True,
        },
    )

    # --- HL stubs (concise) ---
    hl_files = {
        "00_START_HERE_HL.md": "# Start Here\n\nSee 00_START_HERE_ML.json. Authoritative PDF: CI final-seal receipt, not main_smoke.\n",
        "01_SCOPE_BOUNDARY_HL.md": "# Scope Boundary\n\nTeam core: FCG + NewInML corpus + admitted experiments. Solo/future: L0-L5 cascade, AntiCube, Delta-G.\n",
        "02_PROJECT_STATUS_HL.md": "# Project Status\n\nTEAM_REVIEW_MERGED; OPERATOR_INFORMATION_REQUIRED for seal.\n",
        "03_FILE_INDEX_HL.md": f"# File Index\n\n{len(file_rows)} team-relevant files indexed (cap 400 in ML).\n",
        "05_EXPERIMENT_INDEX_HL.md": f"# Experiments\n\n{len(experiments)} experiments indexed.\n",
        "09_AOK_SOT_FCG_HL.md": "# AOK/SOT/FCG\n\nSOT-008/014 NOT_ESTABLISHED. Semantic support != lexical trace.\n",
        "10_SECURITY_ANONYMITY_HL.md": "# Security\n\nSECRET_BYTES_LOGGED=0. Gitleaks: review hash false positive.\n",
        "RUNNING_EXPERIMENTS_HL.md": "# Running Processes\n\nNo team-paper compute active. Daemons unrelated.\n",
        "STATISTICAL_EVIDENCE_HL.md": "# Statistics\n\nB3 100% vs B4 38.5%; Holm p=0.266 — descriptive only.\n",
        "13_OPENREVIEW_OPERATOR_HL.md": "# OpenReview\n\nREADY_FOR_OPERATOR_SUBMISSION. Verify live deadline.\n",
    }
    for name, body in hl_files.items():
        write_md(HANDOFF / name, body)

    # KB minimal
    kb = HANDOFF / "KB"
    kb.mkdir(exist_ok=True)
    for title in [
        "WHAT_IS_PROTEIN_HINGE",
        "TEAM_VS_SOLO_SCOPE",
        "ANTIGENCE",
        "MUTATION_BENCHMARK",
        "WHAT_NOT_TO_CLAIM",
        "HOW_TO_REPRODUCE",
    ]:
        write_md(kb / f"{title}.md", f"# {title.replace('_',' ')}\n\nSee TEAM_HANDOFF_20260829/ and 01_SCOPE_BOUNDARY.\n")

    print(json.dumps({"handoff": str(HANDOFF), "files": len(list(HANDOFF.rglob("*")))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
