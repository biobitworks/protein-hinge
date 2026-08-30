#!/usr/bin/env python3
"""Emit structured ledgers for the 2026-08-29/30 final team-evidence audit.

This script writes JSON/CSV/JSONL from frozen audit observations collected in
this session. It does not mutate manuscript sources.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
REPO = ROOT


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8")


NOW = "2026-08-30T02:20:00Z"
REPO_HEAD = "a2550d589594ae6e440885bc68a618f3b852764d"
CI_SOURCE = "bc4b0d575d130af3f335b712ec1763c164d7d74b"
PR2_MERGE = "2ba0d923082200b135f17216a1d315a50564c60d"
CI_RUN = "33264903580"
PDF_SHA = "ded8f72e299642a7f8ed4fc0f5318b1e961c413b5640acaa6cda6d65880448ab"
BUNDLE_SHA = "c64812be34132242e166e862fe4197091de73abf56d32fc175d7424ad8cb20d8"
PR1_ADMITTED = "6e47dbe367d9223c15c80ef27ca2634b50054035"
PR1_LIVE = "d0e992be47f9a4cf858a5317d0111daf817943a6"
MAIN_TEX = "fba9139d278665fefcfad8b69d2203585dbd9c3714e26ec8a02839a0ee393dec"

CLINVAR = "3aa5e6723563a567fc2b77733a2ee1bd4707c5d254b2537192851c143c1fc2ec"
FASTA_WT = "98f31f1ce20f4f919e6463b026ab321ee3617acaf3c1e1e02a555ae289ed4565"
FASTA_VAR = "355d8e96bc6123427d6e05f305bb017cc09acaf3f6bdfc1255874a6ad561cd9d"
BUILD_FASTA = "5e01e23d3af90cf2a6ff02f29be32b099e60ae18e73cdbfd43cedcc3ab449c59"
BUILD_CLINVAR = "7eaaabf737646f956580f5c02109f6c8fb3feaa02e1e8243948fda5526752545"
CLINVAR_PROV = "8d48e76e61bb9c906ad237238b1c957d3f1807d42b75b644f4987b62790591b1"
FASTA_LANE = "b78535c0d77d0f62e1f530fbd66bde091e6879251645dadfe85b516c9627906d"
PAPER_METRICS = "dad6d7ec5123215fec16847630cb721c5da9830c4fdff05cb4cae51b4976cf11"
EXP002S = "dcdcd6376c6a154b3c95bd3b9dc6c94667013eda83aeab7f50ee3cba5b834df5"
EXP003S = "d4d1764f9f5645d019b5178dc84b3a87890a9b2515cacf224e146aafb37a6615"
GAP_RES = "13373d683c15c09bc59dd29c086def24230d5106171826d746ade1bc523c5853"
GAP_SCRIPT = "898fd2052aae47495602d1d3fc94cc9fb14fda3b28231b5c9c0664df2e52662e"
G3_MATCH = "41efd4d18f708170e09094271313efb025986a10930c06433183fa40b4024235"
G3_SCRIPT = "53395a636f01d73ccdb7e2d56d095bd296ec7e34424e49dc1b5e4cc84380bb58"
EXP006_REPRO = "1e3c797c912281f0d3388686a7dcf012bdd4b4adab905ecbcb760c62d45f37bd"
RANKING = "e93d3ce7526049c8904e36e6e1aeefc2558c38b3032c8c348342390d8cf30b51"
ELVIS_MAIN_ADMIT = "e8e631d5a36f34cf74a6f960f6d5cc2e7b9c8245f05dc312d664b779fe596b3b"
ELVIS_MAIN_LIVE = "28e16ac85eff7aee13b939d5225fa22c9501e13c5d7051c858b81aa776666fd1"
RESULTS_TEX = "2e1e12791f8ea707d819425a9dc17e1ed46e591a9fe6b52b97abdef39b3105c0"


def git_authority() -> dict:
    return {
        "schema": "protein_hinge.final_team_evidence_audit.git_authority.v1",
        "recorded_at_utc": NOW,
        "execution": {
            "requested_host": "magicSTUDIObox.local",
            "cockpit_host": "magicPRObox.local",
            "evidence_host_queried": "magicSTUDIObox.local",
            "studio_protein_hinge_head": REPO_HEAD,
            "studio_worktree_clean": True,
            "studio_unpushed_vs_origin_main": [],
            "pr1_review_worktree": {
                "path": "/Users/byron/projects/active/protein-hinge-pr1-review-20260828",
                "head": PR1_ADMITTED,
                "state": "detached HEAD, clean",
            },
        },
        "REPO_HEAD_SHA": REPO_HEAD,
        "branch_at_audit_start": "main",
        "origin_url": "https://github.com/biobitworks/protein-hinge.git",
        "backup_remote": "ssh://magicSTUDIObox.local/Volumes/magicDATAbox/git_backups/protein-hinge.git",
        "origin_main": REPO_HEAD,
        "tags": [],
        "CANONICAL_PAPER_SOURCE_SHA": CI_SOURCE,
        "CANONICAL_PAPER_SOURCE_NOTE": "PROJECT_CONTROL.yaml current_state + CI run headSha. Distinct from stale paper/newinml2026/provenance/CANONICAL_PAPER_SOURCE.yaml which still lists PR#2 merge 2ba0d923.",
        "HISTORICAL_TEAM_REVIEW_FREEZE_SHA": PR2_MERGE,
        "STALE_CANONICAL_PAPER_SOURCE_YAML": PR2_MERGE,
        "CI_AUTHORITATIVE_PDF_SOURCE_SHA": CI_SOURCE,
        "CI_RUN_ID": CI_RUN,
        "CI_WORKFLOW": "NewInML final seal",
        "CI_CONCLUSION": "success",
        "CI_URL": f"https://github.com/biobitworks/protein-hinge/actions/runs/{CI_RUN}",
        "FINAL_PDF_SHA256": PDF_SHA,
        "ANONYMOUS_BUNDLE_SHA256": BUNDLE_SHA,
        "manuscript_unchanged_after_ci_source": True,
        "commits_after_ci_source": [
            "003c579 Document local probox vs GitHub team review access paths.",
            "a2550d5 Update probox review index with team GitHub access links.",
        ],
        "live_github_refs_resolved": {
            "biobitworks/protein-hinge main": {
                "expected_approx": "a2550d589594ae6e440885bc68a618f3b852764d",
                "actual": REPO_HEAD,
                "match": True,
            },
            "audit/newinml-team-green-yellow-20260829": {
                "expected_approx": "411d5816cf5724a0031d21d2fd5da8bbfe09a41b",
                "actual": "411d5816cf5724a0031d21d2fd5da8bbfe09a41b",
                "merged": True,
                "pr": 7,
            },
            "ElvisHan2022/protein-hinge healthomics-lane": {
                "expected_approx": PR1_LIVE,
                "actual": PR1_LIVE,
                "admitted_snapshot_used_by_successors": PR1_ADMITTED,
                "live_diverged_from_admitted_snapshot": True,
                "clinvar_tsv_unchanged_live_vs_admitted": True,
                "elvis_main_tex_diverged": True,
            },
        },
        "SIGNATURE_STATE": "NOT_SIGNED",
    }


def experiments() -> list[dict]:
    common = {
        "preregistration_sha256": None,
        "environment": "magicSTUDIObox.local python3",
        "validators": [],
        "contradictions": [],
        "superseded_by": None,
        "notes": "",
    }

    def e(**kw):
        row = dict(common)
        row.update(kw)
        return row

    return [
        e(
            experiment_id="EXP-GAP-ACCOUNTING-001",
            title="GAP semantic-accounting retrospective audit",
            scope_class="TEAM_CORE",
            purpose="Show historical hardcoded abstention summary disagrees with row grades",
            preregistration_state="RETROSPECTIVE_NOT_PREREGISTERED",
            source_commit="gap/runs/2026-08-13 (immutable)",
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-13",
            script="gap/ingest_gap.py (historical hardcoded abstentions)",
            script_sha256=None,
            frozen_inputs=["gap/runs/2026-08-13/candidates.csv"],
            input_sha256=[],
            raw_outputs=["gap/runs/2026-08-13/abstentions.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["gap/runs/2026-08-13/"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="Results GAP accounting; Table 1 N=4 successor not this run",
            claim_ceiling="semantic audit",
            rerun_history=["original 2026-08-13", "not mutated"],
            notes="Historical summary all zeros; 3 ABSTAIN rows. Defect: hardcoded abstentions dict.",
        ),
        e(
            experiment_id="EXP-GAP-ACCOUNTING-001.1",
            title="GAP accounting repaired rerun",
            scope_class="TEAM_CORE",
            purpose="Derive abstention summary from graded rows; restore invariants",
            preregistration_state="PREREGISTERED",
            preregistration_sha256=sha256_file(REPO / "paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/prereg.json")
            if (REPO / "paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/prereg.json").exists()
            else None,
            source_commit="94f8949f1bbcb63d8e80baadd0c5f380f01b9f92",
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28T06:56:00Z",
            script="paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/repair_ingest_gap.py",
            script_sha256=GAP_SCRIPT,
            frozen_inputs=["gap/elvis_prescripted_demo.json"],
            input_sha256=[],
            raw_outputs=[
                "gap/runs/2026-08-28-accounting-repair/candidates.csv",
                "gap/runs/2026-08-28-accounting-repair/abstentions.json",
                "gap/runs/2026-08-28-accounting-repair/accounting.json",
            ],
            output_sha256=[
                "d197113efa30f0425de3368b9a5e7ba325340b9511fbfa7b7c6e9abea6e727e6",
                "afdecf16f68b5f1596af76471ef181acb05a16302d353ba4053dc1b54ceb5816",
                "03502a9931df3ed14edf646931f6e791da907f22ae042739cdf81cb4d6c9b50f",
            ],
            derived_outputs=["paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/results.json"],
            validators=["invariant_summary_matches_rows", "invariant_input_partition"],
            receipt=["paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/results.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_POSITIVE",
            manuscript_surface="Results GAP; Table 1 N=4",
            claim_ceiling="REPURPOSING_HYPOTHESIS / semantic audit",
            rerun_history=["2026-08-28 successor", "2026-08-30 hash re-verify MATCH"],
            notes="This audit re-hashed repair outputs; all three files MATCH results.json.",
        ),
        e(
            experiment_id="EXP-001",
            title="Alias for EXP-GAP-ACCOUNTING-001",
            scope_class="TEAM_CORE",
            purpose="Paper matrix alias",
            preregistration_state="ALIAS",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-13",
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=[],
            output_sha256=[],
            derived_outputs=[],
            receipt=[],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="none as distinct ID",
            claim_ceiling="semantic audit",
            rerun_history=[],
            notes="Alias only; do not double-count as extra experiment.",
        ),
        e(
            experiment_id="EXP-002",
            title="G1 sequence/residue verification — provenance recovery",
            scope_class="TEAM_CORE",
            purpose="Locate historical G1 counts (355/239/123/28) in admitted custody",
            preregistration_state="RETROSPECTIVE",
            source_commit="40256c628903185a37eeddce3635b4573c1c4d54",
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28T07:02:00Z",
            script=None,
            script_sha256=None,
            frozen_inputs=["protein-hinge git tree"],
            input_sha256=[],
            raw_outputs=["paper/newinml2026/experiments/EXP-002/provenance_recovery.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/experiments/EXP-002/provenance_recovery.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="Results provenance; historical counts excluded",
            claim_ceiling="audit only",
            rerun_history=["2026-08-28 search COMPLETE_NEGATIVE"],
            notes="Historical 28/123=22.8% NOT_FOUND in repo custody.",
        ),
        e(
            experiment_id="EXP-002-PROV.1",
            title="G1 external biocustody zip recovery",
            scope_class="TEAM_CORE",
            purpose="Search admitted biocustody bootstrap zip for G1 derivation chain",
            preregistration_state="RETROSPECTIVE",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28",
            script=None,
            script_sha256=None,
            frozen_inputs=["biocustody-stateshift-aws-bootstrap-v0.2.0.zip"],
            input_sha256=[],
            raw_outputs=["paper/newinml2026/experiments/EXP-002-PROV.1/PROVENANCE_REPORT.md"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/experiments/EXP-002-PROV.1/"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="Results provenance recovery 206 MB package",
            claim_ceiling="audit only",
            rerun_history=[],
            notes="COMPLETE_NEGATIVE_PROVENANCE; numeric substring matches rejected.",
        ),
        e(
            experiment_id="EXP-002-SUCCESSOR-001",
            title="G1 contemporary successor evaluation",
            scope_class="TEAM_CONTRIBUTED",
            purpose="Run sequence guard on admitted contemporary ClinVar subset",
            preregistration_state="RETROSPECTIVE_SUCCESSOR",
            source_commit=PR1_ADMITTED,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28T22:50:00Z",
            script="scripts/build_fasta_lane.py (PR#1 hash-admitted, not in main tree)",
            script_sha256=BUILD_FASTA,
            frozen_inputs=[
                "data/healthomics/clinvar_subset.tsv",
                "data/fasta/consensus_genes.fasta",
            ],
            input_sha256=[CLINVAR, FASTA_WT],
            raw_outputs=["data/fasta/variants.fasta", "site/assets/fasta_lane.json"],
            output_sha256=[FASTA_VAR, FASTA_LANE],
            derived_outputs=["paper/newinml2026/experiments/EXP-002-SUCCESSOR-001/EXPERIMENT_RECEIPT.json"],
            validators=["364=98+266"],
            receipt=[
                "paper/newinml2026/experiments/EXP-002-SUCCESSOR-001/EXPERIMENT_RECEIPT.json",
                "paper/newinml2026/compute/receipts/PROTEIN_HINGE_SUCCESSOR_RECOMPUTE_RECEIPT.json",
                "paper/newinml2026/final_team_evidence_audit/G1_FROZEN_RECOMPUTE_RECEIPT.json",
            ],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_BOUNDED",
            manuscript_surface="Results G1 successor; Table 1 N=364",
            claim_ceiling="SEQUENCE_RECORD / retrospective",
            rerun_history=[
                "Elvis lane capture 2026-08-25",
                "successor receipt 2026-08-28",
                "Studio ARTIFACT_RECOMPUTE_PASS 2026-08-29 (exact_source_reproduction=false, live_refetch=false)",
                "this audit frozen replay 2026-08-30 MATCH without UniProt fetch",
            ],
            notes="Bytes hash-admitted from PR#1; not checked into biobitworks main. All 16 residue mismatches TAFAZZIN-only. Not historical reproduction.",
        ),
        e(
            experiment_id="EXP-003",
            title="G2 CNV attribution — provenance recovery",
            scope_class="TEAM_CORE",
            purpose="Locate historical 742/642/100/287 in admitted custody",
            preregistration_state="RETROSPECTIVE",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28",
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["paper/newinml2026/experiments/EXP-003/UNVERIFIED_HISTORICAL_CLAIMS.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/experiments/EXP-003/PROVENANCE_REPORT.md"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="Results provenance; silent-error rate forbidden for historical",
            claim_ceiling="audit only",
            rerun_history=[],
            notes="742-row corpus NOT reproduced. Terminology: do not use silent error rate for unverified historical ratios.",
        ),
        e(
            experiment_id="EXP-003-PROV.1",
            title="G2 external recovery",
            scope_class="TEAM_CORE",
            purpose="External package search for G2 chain",
            preregistration_state="RETROSPECTIVE",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28",
            script=None,
            script_sha256=None,
            frozen_inputs=["biocustody zip"],
            input_sha256=[],
            raw_outputs=[],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/experiments/EXP-003-PROV.1/"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="Results provenance",
            claim_ceiling="audit only",
            rerun_history=[],
        ),
        e(
            experiment_id="EXP-003-SUCCESSOR-001",
            title="G2 contemporary successor evaluation",
            scope_class="TEAM_CONTRIBUTED",
            purpose="CNV/multi-gene exclusion accounting on contemporary fetch",
            preregistration_state="RETROSPECTIVE_SUCCESSOR",
            source_commit=PR1_ADMITTED,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28T22:50:00Z",
            script="scripts/build_clinvar_evidence.py (PR#1 hash-admitted)",
            script_sha256=BUILD_CLINVAR,
            frozen_inputs=["data/healthomics/clinvar_subset.tsv", "data/healthomics/clinvar_provenance.json"],
            input_sha256=[CLINVAR, CLINVAR_PROV],
            raw_outputs=["model_trace/paper_metrics.json"],
            output_sha256=[PAPER_METRICS],
            derived_outputs=["paper/newinml2026/experiments/EXP-003-SUCCESSOR-001/EXPERIMENT_RECEIPT.json"],
            validators=["746=364+382+0"],
            receipt=["paper/newinml2026/experiments/EXP-003-SUCCESSOR-001/EXPERIMENT_RECEIPT.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_BOUNDED",
            manuscript_surface="Results G2 successor; Table 1 N=746",
            claim_ceiling="retrospective accounting; not silent-error rate",
            rerun_history=[
                "ClinVar capture 2026-08-25 including TAFAZZIN 100-ID XML/JSON ceiling failure + split-retry",
                "successor receipt 2026-08-28",
                "this audit: TSV row count 364 MATCH; 746/382 from frozen clinvar_provenance.json reconciliation (not live NCBI refetch)",
            ],
            notes="live_refetch_performed=false on 2026-08-29 recompute. Historical 742 NOT reproduced. 382 is predicate exclusion, not validated silent-error.",
        ),
        e(
            experiment_id="EXP-004",
            title="G3 identity-resolution ablation",
            scope_class="TEAM_CORE",
            purpose="Lane A contract fixtures; Lane B N=1 observed-source bypass; wiring defect",
            preregistration_state="PREREGISTERED",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28T07:46:00Z",
            script="paper/newinml2026/experiments/EXP-004/run_g3_audit.py",
            script_sha256=G3_SCRIPT,
            frozen_inputs=["gap/alias_table.json", "gap/runs/2026-08-13/programs.csv"],
            input_sha256=["8c4dc1a0fae530e2eec58d7312a01187b03d2071dde51995411ac775a2c2d01b"],
            raw_outputs=[
                "paper/newinml2026/experiments/EXP-004/lane_a_contract_results.json",
                "paper/newinml2026/experiments/EXP-004/matched_ablation_results.json",
                "paper/newinml2026/experiments/EXP-004/evaluation_wiring_defect.json",
            ],
            output_sha256=[G3_MATCH],
            derived_outputs=["paper/newinml2026/experiments/EXP-004/closeout.json"],
            validators=["Lane A 5/5", "wiring self-compare EXACT"],
            receipt=["paper/newinml2026/experiments/EXP-004/closeout.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="UNDERPOWERED",
            manuscript_surface="Results identity guard; Table 1 N=1 / synth.",
            claim_ceiling="descriptive; no population error rate",
            rerun_history=["2026-08-28 COMPLETE_ABLATION"],
            notes="EXPERIMENT_MATRIX.md incorrectly listed a second EXP-004 as NOT_STARTED; closeout is COMPLETE_ABLATION with N=1. Alias COMPLETE_UNDERPOWERED_N1.",
        ),
        e(
            experiment_id="EXP-005",
            title="Frozen-corpus independent replication",
            scope_class="TEAM_CORE",
            purpose="Independent corpus replication (locked prereg, incomplete metric/corpus)",
            preregistration_state="PREREGISTERED_LOCKED",
            preregistration_sha256=None,
            source_commit="40256c628903185a37eeddce3635b4573c1c4d54",
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-28T07:02:00Z lock; never executed",
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["paper/newinml2026/experiments/EXP-005/READINESS_AUDIT.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/experiments/EXP-005/READINESS_AUDIT.json"],
            deterministic_or_probabilistic="NOT_EXECUTED",
            terminal_state="NOT_EXECUTED",
            manuscript_surface="Experimental Design; Limitations; explicitly not executed",
            claim_ceiling="none — no result",
            rerun_history=[],
            notes="BLOCKED on corpus freeze + primary metric. Do not convert to failure. Handoff index said BLOCKED; matrix said PREREGISTERED_LOCKED. Canonical: NOT_EXECUTED / BLOCKED readiness.",
        ),
        e(
            experiment_id="EXP-006",
            title="Morphology/null reproduction",
            scope_class="TEAM_CORE",
            purpose="Reproduce cached CPJUMP1-derived null ranking vs shuffle",
            preregistration_state="REPLICATION",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time="cached 2026-08-13T15:18:33Z; receipt 2026-08-28T07:58:09Z",
            script="scripts/magicstudiobox_repurposing_queue.py (in biocustody zip)",
            script_sha256=None,
            frozen_inputs=["data/partner/candidate_ranking.csv", "data/partner/evaluation.json"],
            input_sha256=[RANKING],
            raw_outputs=["paper/newinml2026/experiments/EXP-006/reproduction_result.json"],
            output_sha256=[EXP006_REPRO],
            derived_outputs=[],
            validators=["exact_match_cached=true"],
            receipt=["paper/newinml2026/experiments/EXP-006/EXPERIMENT_RECEIPT.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_NEGATIVE",
            manuscript_surface="Results null benchmark; Table 1 N=50",
            claim_ceiling="REPURPOSING_HYPOTHESIS",
            rerun_history=["Kaggle/cached 2026-08-13", "exact cached reproduction 2026-08-28"],
            notes="known_pair_rank=28/50; enrichment_vs_shuffle=0.246<1. Full CPJUMP1 profiles not held locally. EXPERIMENT_MATRIX.md stale (NOT_STARTED). Handoff 05_EXPERIMENT_INDEX stale (NOT_EXECUTED).",
        ),
        e(
            experiment_id="EXP-007",
            title="SGLang CUDA graph-break stress",
            scope_class="OUT_OF_TEAM_SCOPE",
            purpose="Remote CUDA exploratory (Kaggle/Daytona)",
            preregistration_state="PREREGISTERED",
            source_commit=None,
            execution_host="KAGGLE/DAYTONA (not executed)",
            execution_time=None,
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["paper/newinml2026/experiments/SGLANG_GRAPH_BREAK_PREREG.md"],
            output_sha256=[],
            derived_outputs=[],
            receipt=[],
            deterministic_or_probabilistic="NOT_EXECUTED",
            terminal_state="NOT_EXECUTED",
            manuscript_surface="none (future direction)",
            claim_ceiling="none",
            rerun_history=[],
            notes="FUTURE_DIRECTION. Apple Silicon host cannot run CUDA locally.",
        ),
        e(
            experiment_id="AUD-FCG-DOCUMENT-LATTICE-001",
            title="FCG document lattice structural round-trip",
            scope_class="TEAM_IMPORTED_DEPENDENCY",
            purpose="PRE/POST structural identity of document lattice objects",
            preregistration_state="IMPORTED_AUDIT",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time=None,
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["biocustody/audits/AUD-FCG-DOCUMENT-LATTICE-001/COVERAGE_METRICS.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["biocustody/audits/AUD-FCG-DOCUMENT-LATTICE-001/AUDIT_RECEIPT.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="COMPLETE_BOUNDED",
            manuscript_surface="not a manuscript results table; team handoff 136/136",
            claim_ceiling="structural custody only",
            rerun_history=[],
            notes="PRE_POST_IDENTITY_COVERAGE 136/136. TABLE_PROPOSITIONAL_CELL_CLOSURE 21 cells PENDING. Semantic AOK 50/56. Not a protein-hinge science result.",
        ),
        e(
            experiment_id="AUD-FCG-ATOM-SOT-ROUNDTRIP-002",
            title="FCG atom/SOT round-trip predecessor",
            scope_class="TEAM_IMPORTED_DEPENDENCY",
            purpose="Predecessor of SEMANTIC-003",
            preregistration_state="IMPORTED_AUDIT",
            source_commit=None,
            execution_host="magicSTUDIObox.local",
            execution_time=None,
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=[],
            output_sha256=[],
            derived_outputs=[],
            receipt=["biocustody/audits/AUD-FCG-ATOM-SOT-ROUNDTRIP-002/AUDIT_RECEIPT.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="SUPERSEDED",
            manuscript_surface="none",
            claim_ceiling="imported comparator infrastructure",
            rerun_history=[],
            superseded_by="AUD-FCG-ATOM-SOT-SEMANTIC-003",
            notes="Predecessor audit in biocustody.",
        ),
        e(
            experiment_id="AUD-FCG-ATOM-SOT-SEMANTIC-003",
            title="FCG atom/SOT semantic conformance",
            scope_class="TEAM_IMPORTED_DEPENDENCY",
            purpose="Semantic atom/SOT gates; YELLOW conformance",
            preregistration_state="PREREGISTERED",
            preregistration_sha256="7638b5bae382c44c889cb80004e6adad49778ba29a8fe1914dcbcc24fa5796c8",
            source_commit="79f69b89bc009ba4260a39096d6dae8f952bac41",
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-29T10:08:07Z",
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["biocustody/audits/AUD-FCG-ATOM-SOT-SEMANTIC-003/AUDIT_RECEIPT.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["biocustody/audits/AUD-FCG-ATOM-SOT-SEMANTIC-003/AUDIT_RECEIPT.json"],
            deterministic_or_probabilistic="DETERMINISTIC_COMPUTATION",
            terminal_state="UNDERPOWERED",
            manuscript_surface="not claimed as confirmatory in NewInML results",
            claim_ceiling="YELLOW / UNDERPOWERED",
            rerun_history=[],
            notes="FINAL_VALIDATION_COLOR=YELLOW. scientific_terminal=UNDERPOWERED. Imported from biocustody.",
        ),
        e(
            experiment_id="ANTIGENCE-B4-COMPARATOR",
            title="Antigence B4 AIS comparator freeze",
            scope_class="TEAM_IMPORTED_DEPENDENCY",
            purpose="Frozen comparator statistics; do not retrain",
            preregistration_state="FROZEN_COMPARATOR",
            source_commit="antigence 1f12b3c2b2f7df90e11753f74443e4add48d5b46",
            execution_host="magicSTUDIObox.local",
            execution_time="2026-08-29T16:05:00Z",
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["TEAM_HANDOFF_20260829/RECEIPTS/ANTIGENCE_B4_FREEZE_RECEIPT.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["TEAM_HANDOFF_20260829/RECEIPTS/ANTIGENCE_B4_FREEZE_RECEIPT.json"],
            deterministic_or_probabilistic="PROBABILISTIC_MODEL_OUTPUT",
            terminal_state="COMPLETE_BOUNDED",
            manuscript_surface="OUTSIDE current paper results (handoff: OUTSIDE_CURRENT_PAPER / FUTURE_DIRECTION in terminal ledger B0-B4)",
            claim_ceiling="descriptive difference only; holm p=0.266 NOT confirmatory",
            rerun_history=["do_not_retrain=true"],
            notes="B3 13/13 vs B4 5/13 semantic disposition; false-claim acceptance 0% both. GEE NOT_ESTIMABLE. Not a core NewInML Results claim.",
        ),
        e(
            experiment_id="EXP-Q38-COMP-001",
            title="Qwen3.8 local vs Daytona Flash-Next canary",
            scope_class="OUT_OF_TEAM_SCOPE",
            purpose="Compute-stack canary, not manuscript science",
            preregistration_state="EXPLORATORY",
            source_commit=None,
            execution_host="magicSTUDIObox.local / Daytona blocked",
            execution_time="2026-08-28T16:00:00Z",
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=["paper/newinml2026/compute/test-stack/experiments/EXP-Q38-COMP-001/EXPERIMENT_RECEIPT.json"],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/compute/test-stack/experiments/EXP-Q38-COMP-001/EXPERIMENT_RECEIPT.json"],
            deterministic_or_probabilistic="PROBABILISTIC_MODEL_OUTPUT",
            terminal_state="BLOCKED",
            manuscript_surface="none",
            claim_ceiling="DESCRIPTIVE_EXPLORATORY",
            rerun_history=[],
            notes="Remote Daytona condition NOT_EXECUTED (API key absent at that receipt). Out of team paper claims.",
        ),
        e(
            experiment_id="SOT-008-TAFAZZIN-PLUS30",
            title="+30 residue-offset TAFAZZIN case study",
            scope_class="TEAM_CONTRIBUTED",
            purpose="Row-level proof of +30 isoform offset",
            preregistration_state="SOT_OPEN",
            source_commit=None,
            execution_host=None,
            execution_time=None,
            script=None,
            script_sha256=None,
            frozen_inputs=[],
            input_sha256=[],
            raw_outputs=[],
            output_sha256=[],
            derived_outputs=[],
            receipt=["paper/newinml2026/final_corpus_audit/SEEDS_OF_TRUTH.final.json"],
            deterministic_or_probabilistic="NOT_EXECUTED",
            terminal_state="NOT_EXECUTED",
            manuscript_surface="ABSENT from canonical main.tex; present in Elvis methods / SOT",
            claim_ceiling="NOT_ESTABLISHED",
            rerun_history=[],
            notes="PROJECT_CONTROL still lists SOT-008 as blocked. This audit did not launch a new offset study. Residue mismatches are 16/16 TAFAZZIN; +30 mechanism not row-proven.",
        ),
    ]


def numerical_claims() -> list[dict]:
    """Scientific/calculated numbers from canonical manuscript + listed Elvis/SOT values."""
    rows = []

    def add(**kw):
        rows.append(kw)

    # Canonical manuscript scientific numbers
    add(
        NUMERICAL_CLAIM_ID="NC-001",
        manuscript_location="main.tex Results GAP",
        displayed_value="3",
        exact_unrounded_value="3",
        raw_source="gap/runs/2026-08-13/candidates.csv grade=ABSTAIN count",
        raw_source_sha256="historical candidates.csv (immutable run dir)",
        row_level_data="3 ABSTAIN of 4 rows",
        transformation_script="row count (historical ingest did not derive summary)",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="count(grade==ABSTAIN)=3 vs summary zeros",
        output_artifact="gap/runs/2026-08-13/abstentions.json",
        output_sha256="",
        rendering_step="prose in main.tex",
        manuscript_inclusion_path="main.tex:85",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-002",
        manuscript_location="main.tex Results GAP successor",
        displayed_value="N_input=4, N_admitted=1, N_abstained=3, summary=3",
        exact_unrounded_value="4/1/3/3",
        raw_source="gap/runs/2026-08-28-accounting-repair/",
        raw_source_sha256="candidates.csv sha256:d197113efa30f0425de3368b9a5e7ba325340b9511fbfa7b7c6e9abea6e727e6",
        row_level_data="4 rows",
        transformation_script="paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/repair_ingest_gap.py",
        script_sha256=GAP_SCRIPT,
        parameters_config="prescripted N=4",
        deterministic_calculation="invariants true",
        output_artifact="paper/newinml2026/experiments/EXP-GAP-ACCOUNTING-001.1/results.json",
        output_sha256=GAP_RES,
        rendering_step="MANUAL_TEX_TRANSCRIPTION from receipt",
        manuscript_inclusion_path="main.tex:71,85",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-003",
        manuscript_location="main.tex Table 1 / G3 Lane B / Limitations",
        displayed_value="1",
        exact_unrounded_value="1",
        raw_source="paper/newinml2026/experiments/EXP-004/matched_ablation_results.json",
        raw_source_sha256=G3_MATCH,
        row_level_data="1 pair TAZ/cardiolipin module -> TAZ",
        transformation_script="paper/newinml2026/experiments/EXP-004/run_g3_audit.py",
        script_sha256=G3_SCRIPT,
        parameters_config="Lane B observed-source",
        deterministic_calculation="N_bypass_admitted=1",
        output_artifact="matched_ablation_results.json",
        output_sha256=G3_MATCH,
        rendering_step="MANUAL_TEX_TRANSCRIPTION",
        manuscript_inclusion_path="main.tex:73,87,98",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-004",
        manuscript_location="main.tex G1 successor",
        displayed_value="364=98+266",
        exact_unrounded_value="364=98+266",
        raw_source="clinvar_subset.tsv + consensus_genes.fasta (PR#1 hash-admitted)",
        raw_source_sha256=CLINVAR,
        row_level_data="364 ClinVar rows",
        transformation_script="scripts/build_fasta_lane.py apply_variant (frozen FASTA, no UniProt fetch)",
        script_sha256=BUILD_FASTA,
        parameters_config="HGVS_P parser; classify frameshift before residue check",
        deterministic_calculation="this audit 2026-08-30 replay MATCH",
        output_artifact="EXP-002-SUCCESSOR-001/EXPERIMENT_RECEIPT.json + G1_FROZEN_RECOMPUTE_RECEIPT.json",
        output_sha256=EXP002S,
        rendering_step="MANUAL_TEX_TRANSCRIPTION",
        manuscript_inclusion_path="main.tex:74,89",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-005",
        manuscript_location="main.tex G1 abstention breakdown",
        displayed_value="frameshift 131, no protein notation 118, residue mismatch 16, position out of range 1",
        exact_unrounded_value="131+118+16+1=266",
        raw_source="same as NC-004",
        raw_source_sha256=CLINVAR,
        row_level_data="266 abstention rows; residue_mismatch all TAFAZZIN",
        transformation_script="scripts/build_fasta_lane.py",
        script_sha256=BUILD_FASTA,
        parameters_config="",
        deterministic_calculation="kinds Counter MATCH",
        output_artifact="G1_FROZEN_RECOMPUTE_RECEIPT.json",
        output_sha256="",
        rendering_step="MANUAL_TEX_TRANSCRIPTION",
        manuscript_inclusion_path="main.tex:89",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-006",
        manuscript_location="main.tex G2 successor",
        displayed_value="746=364+382+0",
        exact_unrounded_value="746=364+382+0",
        raw_source="data/healthomics/clinvar_provenance.json reconciliation",
        raw_source_sha256=CLINVAR_PROV,
        row_level_data="TSV kept rows=364 (header+364 data lines=365)",
        transformation_script="scripts/build_clinvar_evidence.py gene_specific predicate (frozen provenance, no live NCBI)",
        script_sha256=BUILD_CLINVAR,
        parameters_config="MAX_GENES_PER_VARIANT=3; CNV_OBJ_TYPES copy number loss/gain",
        deterministic_calculation="reconciliation.balanced=true; TSV rows MATCH kept",
        output_artifact="EXP-003-SUCCESSOR-001/EXPERIMENT_RECEIPT.json",
        output_sha256=EXP003S,
        rendering_step="MANUAL_TEX_TRANSCRIPTION",
        manuscript_inclusion_path="main.tex:75,91",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
        notes="746/382 not recomputed by live NCBI refetch; verified from frozen provenance JSON + TSV row count. exact_source_reproduction=false on 2026-08-29 receipt.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-007",
        manuscript_location="main.tex G2 100-ID failure",
        displayed_value="100-ID; ~16.5 MB XML vs 10 MB JSON",
        exact_unrounded_value="ids=100; XML=16503275 bytes; max=10MB",
        raw_source="clinvar_provenance.json batch_failures[0]",
        raw_source_sha256=CLINVAR_PROV,
        row_level_data="TAFAZZIN batch",
        transformation_script="scripts/build_clinvar_evidence.py fetch_summaries",
        script_sha256=BUILD_CLINVAR,
        parameters_config="ESummary JSON conversion ceiling",
        deterministic_calculation="reason string contains 16503275 and 10MB",
        output_artifact="clinvar_provenance.json",
        output_sha256=CLINVAR_PROV,
        rendering_step="prose approximation ~16.5 MB",
        manuscript_inclusion_path="main.tex:91",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
        notes="Displayed ~16.5 MB is rounded from 16503275 bytes (16.503275e6).",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-008",
        manuscript_location="main.tex G2 historical 742",
        displayed_value="742-row corpus not reproduced",
        exact_unrounded_value="742",
        raw_source="UNVERIFIED_HISTORICAL_CLAIMS.json N_fetched",
        raw_source_sha256="",
        row_level_data="none recovered",
        transformation_script="provenance search EXP-003",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="historical_exact_reproduction=NO",
        output_artifact="paper/newinml2026/experiments/EXP-003/UNVERIFIED_HISTORICAL_CLAIMS.json",
        output_sha256="",
        rendering_step="prose",
        manuscript_inclusion_path="main.tex:91",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
        notes="Value is a quarantined historical claim that the paper correctly says was NOT reproduced.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-009",
        manuscript_location="main.tex provenance 206 MB",
        displayed_value="206 MB",
        exact_unrounded_value="not re-measured this audit",
        raw_source="EXP-002-PROV.1 PROVENANCE_REPORT.md",
        raw_source_sha256="",
        row_level_data="",
        transformation_script="",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="package size from prior receipt; zip not rehashed this session",
        output_artifact="paper/newinml2026/experiments/EXP-002-PROV.1/PROVENANCE_REPORT.md",
        output_sha256="",
        rendering_step="prose",
        manuscript_inclusion_path="main.tex:93",
        final_state="PARTIAL_TRACE",
        in_canonical_manuscript=True,
        notes="Prior audit asserts SHA-256 verified 206 MB bootstrap; this session did not re-hash the zip bytes.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-010",
        manuscript_location="main.tex morphology null",
        displayed_value="28/50; enrichment vs shuffle <1",
        exact_unrounded_value="rank=28; N=50; enrichment=0.24638253360287107",
        raw_source="data/partner/evaluation.json",
        raw_source_sha256="ede568677be5d45412f359153ebd60ada87b23ec93db6a33f9e836bce1bea62f",
        row_level_data="data/partner/candidate_ranking.csv",
        transformation_script="cached shuffle block (seed 260813, 1000 iterations)",
        script_sha256="",
        parameters_config="shuffle_seed=260813, iterations=1000",
        deterministic_calculation="reproduction_result.json exact_match=true vs cached",
        output_artifact="paper/newinml2026/experiments/EXP-006/reproduction_result.json",
        output_sha256=EXP006_REPRO,
        rendering_step="MANUAL_TEX_TRANSCRIPTION",
        manuscript_inclusion_path="main.tex:78,95",
        final_state="VERIFIED_FROM_FROZEN_PROBABILISTIC_OUTPUT",
        in_canonical_manuscript=True,
        notes="Shuffle is seeded; cached exact match. Full morphology pipeline not locally re-executed.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-011",
        manuscript_location="main.tex Lane A",
        displayed_value="synth. / 5 fixtures implied by receipt not printed",
        exact_unrounded_value="N_total=5 N_pass=5",
        raw_source="lane_a_contract_results.json",
        raw_source_sha256="",
        row_level_data="5 fixture rows",
        transformation_script="run_g3_audit.py",
        script_sha256=G3_SCRIPT,
        parameters_config="alias_table",
        deterministic_calculation="5/5 PASS",
        output_artifact="paper/newinml2026/experiments/EXP-004/lane_a_contract_results.json",
        output_sha256="",
        rendering_step="table says synth. not 5",
        manuscript_inclusion_path="main.tex:72,87",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=True,
        notes="Manuscript does not print 5; contract PASS is the claim.",
    )
    # Listed values NOT in canonical manuscript
    add(
        NUMERICAL_CLAIM_ID="NC-E-114",
        manuscript_location="Elvis paper generated/results.tex \\GOneNaive; NOT in canonical main.tex",
        displayed_value="114",
        exact_unrounded_value="114=98+16",
        raw_source="paper_metrics.json guards.G1.naive_emits",
        raw_source_sha256=PAPER_METRICS,
        row_level_data="emitted + residue_mismatch",
        transformation_script="scripts/build_paper_metrics.py / fasta lane",
        script_sha256="",
        parameters_config="naive = would-emit if residue guard skipped",
        deterministic_calculation="this audit 98+16=114 MATCH",
        output_artifact="Elvis generated/results.tex",
        output_sha256=RESULTS_TEX,
        rendering_step="generated macros in Elvis paper only",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=False,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-14PCT",
        manuscript_location="Elvis \\GOneRate 14.0%; NOT canonical",
        displayed_value="14.0%",
        exact_unrounded_value="16/114=0.140350877... displayed 0.1404 in paper_metrics",
        raw_source="paper_metrics.json rate",
        raw_source_sha256=PAPER_METRICS,
        row_level_data="16 residue_mismatch / 114 naive_emits",
        transformation_script="16/114",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="16/114=0.14035087719298245",
        output_artifact="results.tex \\GOneRate",
        output_sha256=RESULTS_TEX,
        rendering_step="generated",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=False,
        notes="Canonical paper reports 16 as an abstention terminal, not a 14.0% silent-error rate.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-512",
        manuscript_location="Elvis \\GTwoRate 51.2%; NOT canonical",
        displayed_value="51.2%",
        exact_unrounded_value="382/746=0.512064343...",
        raw_source="paper_metrics.json G2 rate 0.5121",
        raw_source_sha256=PAPER_METRICS,
        row_level_data="382 excluded / 746 fetched",
        transformation_script="382/746",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="382/746",
        output_artifact="results.tex",
        output_sha256=RESULTS_TEX,
        rendering_step="generated",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=False,
        notes="Canonical manuscript explicitly refuses silent-error rate language for the 382 exclusions.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-40-58",
        manuscript_location="Elvis missense 40 truncating 58; NOT canonical",
        displayed_value="40 / 58",
        exact_unrounded_value="40 missense + 58 nonsense = 98 emitted",
        raw_source="this audit kinds + paper_metrics",
        raw_source_sha256=PAPER_METRICS,
        row_level_data="",
        transformation_script="apply_variant kind",
        script_sha256=BUILD_FASTA,
        parameters_config="",
        deterministic_calculation="40+58=98 MATCH",
        output_artifact="G1_FROZEN_RECOMPUTE_RECEIPT.json",
        output_sha256="",
        rendering_step="Elvis macros",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=False,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-3OF8",
        manuscript_location="Elvis 3 of 8 genes zeroed; NOT canonical",
        displayed_value="3 of 8",
        exact_unrounded_value="PGS1, PHB2, CHCHD3",
        raw_source="paper_metrics.json genes_reduced_to_zero",
        raw_source_sha256=PAPER_METRICS,
        row_level_data="per_gene enforced=0 for those three",
        transformation_script="G2 per-gene",
        script_sha256=BUILD_CLINVAR,
        parameters_config="",
        deterministic_calculation="count(enforced==0 and naive>0)=3; PHB naive=0 not counted as reduced-to-zero in that list",
        output_artifact="paper_metrics.json",
        output_sha256=PAPER_METRICS,
        rendering_step="Elvis prose",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=False,
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-246",
        manuscript_location="Elvis 24.6% superseded G1 rate",
        displayed_value="24.6%",
        exact_unrounded_value="historical/stale; successor 16/114=14.0%",
        raw_source="STALE_NUMBER_REGISTRY.json / Elvis main.tex",
        raw_source_sha256=ELVIS_MAIN_ADMIT,
        row_level_data="defect: residue check after variant-class assignment inflated mismatch",
        transformation_script="order-of-operations repair in build_fasta_lane.py",
        script_sha256=BUILD_FASTA,
        parameters_config="classify frameshift BEFORE residue check",
        deterministic_calculation="superseded; not a current result",
        output_artifact="STALE_NUMBER_REGISTRY.json",
        output_sha256="",
        rendering_step="Elvis methods discusses correction; canonical omits 24.6%",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="VERIFIED_DETERMINISTIC",
        in_canonical_manuscript=False,
        notes="Correctly treated as SUPERSEDED. Canonical does not display 24.6%.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-SIXPP",
        manuscript_location="Elvis main.tex 'roughly six percentage points' G2",
        displayed_value="roughly six percentage points",
        exact_unrounded_value="historical 287/642=0.447 vs 382/746=0.512 → ~6.5 pp",
        raw_source="UNVERIFIED_HISTORICAL 287/642 vs contemporary 382/746",
        raw_source_sha256="",
        row_level_data="historical 287/642 NOT recovered as row corpus",
        transformation_script="",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="contemporary rate verified; historical denominator unverified",
        output_artifact="Elvis main.tex line ~221",
        output_sha256=ELVIS_MAIN_ADMIT,
        rendering_step="Elvis prose",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="PARTIAL_TRACE",
        in_canonical_manuscript=False,
        notes="Delta uses an unverified historical ratio. Canonical paper does not claim the six-point G2 correction.",
    )
    add(
        NUMERICAL_CLAIM_ID="NC-E-PLUS30",
        manuscript_location="SOT-008 / Elvis methods; NOT canonical",
        displayed_value="+30",
        exact_unrounded_value="",
        raw_source="SEEDS_OF_TRUTH; no row-level proof in protein-hinge main",
        raw_source_sha256="",
        row_level_data="NOT FOUND this audit",
        transformation_script="",
        script_sha256="",
        parameters_config="",
        deterministic_calculation="",
        output_artifact="",
        output_sha256="",
        rendering_step="",
        manuscript_inclusion_path="NOT_IN_CANONICAL",
        final_state="NOT_ESTABLISHED",
        in_canonical_manuscript=False,
        notes="Do not silently repair. Residual mismatches concentrated in TAFAZZIN does not prove +30 offset.",
    )
    return rows


def main() -> None:
    ga = git_authority()
    dump(OUT / "GIT_AUTHORITY.json", ga)

    exps = experiments()
    dump_jsonl(OUT / "EXPERIMENT_INVENTORY.jsonl", exps)

    nums = numerical_claims()
    dump(OUT / "NUMERICAL_CLAIM_LEDGER.json", {
        "schema": "protein_hinge.numerical_claim_ledger.v1",
        "generated_at_utc": NOW,
        "canonical_manuscript_sha256": MAIN_TEX,
        "claims": nums,
        "counts": {
            "total_tracked": len(nums),
            "in_canonical": sum(1 for r in nums if r.get("in_canonical_manuscript")),
            "canonical_verified_deterministic": sum(
                1 for r in nums if r.get("in_canonical_manuscript") and r["final_state"] == "VERIFIED_DETERMINISTIC"
            ),
            "canonical_verified_frozen_probabilistic": sum(
                1 for r in nums if r.get("in_canonical_manuscript") and r["final_state"] == "VERIFIED_FROM_FROZEN_PROBABILISTIC_OUTPUT"
            ),
            "canonical_partial": sum(
                1 for r in nums if r.get("in_canonical_manuscript") and r["final_state"] == "PARTIAL_TRACE"
            ),
            "canonical_manual": sum(
                1 for r in nums if r.get("in_canonical_manuscript") and r["final_state"] == "MANUAL_VALUE"
            ),
            "canonical_unresolved": sum(
                1 for r in nums
                if r.get("in_canonical_manuscript")
                and r["final_state"] in {"MANUAL_VALUE", "CONFLICTING", "NOT_ESTABLISHED"}
            ),
        },
        "hand_typed_generator_claim": {
            "elvis_main_tex_claims_nothing_typed_by_hand": True,
            "canonical_main_tex_claims_llm_not_measurement_authority": True,
            "canonical_table_generated_from_macros": False,
            "canonical_table_matches_receipts": True,
            "MANUAL_VALUE_scientific_canonical": 0,
        },
    })

    # CSV numerical
    fields = [
        "NUMERICAL_CLAIM_ID", "manuscript_location", "displayed_value", "exact_unrounded_value",
        "raw_source", "raw_source_sha256", "transformation_script", "script_sha256",
        "output_artifact", "output_sha256", "final_state", "in_canonical_manuscript",
    ]
    with (OUT / "NUMERICAL_CLAIM_LEDGER.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in nums:
            w.writerow(r)

    # Tables
    tables = [
        {
            "TABLE_ID": "tab:results",
            "manuscript": "canonical main.tex",
            "source_data_sha256": [GAP_RES, EXP002S, EXP003S, G3_MATCH, EXP006_REPRO],
            "calculation_script_sha256": GAP_SCRIPT,
            "parameters_sha256": None,
            "output_data_sha256": None,
            "generated_tex_sha256": None,
            "manuscript_source_sha256": MAIN_TEX,
            "generated_from_row_level": "PARTIAL — values match receipts; table body is hand-authored LaTeX not build_paper_tex.py",
            "closure": "PASS_WITH_BOUNDED_GAPS",
            "notes": "Only table in canonical NewInML manuscript.",
        },
        {
            "TABLE_ID": "Elvis AblationTable (G1/G2 silent-error rates)",
            "manuscript": "ElvisHan2022 paper/generated/results.tex",
            "source_data_sha256": [PAPER_METRICS, RESULTS_TEX],
            "calculation_script_sha256": None,
            "parameters_sha256": None,
            "output_data_sha256": RESULTS_TEX,
            "generated_tex_sha256": RESULTS_TEX,
            "manuscript_source_sha256": ELVIS_MAIN_ADMIT,
            "generated_from_row_level": "YES via build_paper_tex.py in fork",
            "closure": "NOT_IN_CANONICAL_PACKAGE",
            "admission": "ADMIT_AS_REFERENCE / TEAM_CONTRIBUTION_NOT_MERGED",
        },
        {
            "TABLE_ID": "Elvis PerGeneTable",
            "manuscript": "Elvis generated/results.tex",
            "source_data_sha256": [PAPER_METRICS],
            "calculation_script_sha256": None,
            "parameters_sha256": None,
            "output_data_sha256": RESULTS_TEX,
            "generated_tex_sha256": RESULTS_TEX,
            "manuscript_source_sha256": ELVIS_MAIN_ADMIT,
            "generated_from_row_level": "YES in fork",
            "closure": "NOT_IN_CANONICAL_PACKAGE",
        },
        {
            "TABLE_ID": "Elvis DeclineTable",
            "manuscript": "Elvis generated/results.tex",
            "source_data_sha256": [FASTA_LANE],
            "calculation_script_sha256": BUILD_FASTA,
            "parameters_sha256": None,
            "output_data_sha256": RESULTS_TEX,
            "generated_tex_sha256": RESULTS_TEX,
            "manuscript_source_sha256": ELVIS_MAIN_ADMIT,
            "generated_from_row_level": "YES in fork; values MATCH this audit G1 replay",
            "closure": "NOT_IN_CANONICAL_PACKAGE",
        },
    ]
    dump_jsonl(OUT / "TABLE_PROVENANCE_LEDGER.jsonl", tables)

    figures = [
        {
            "FIGURE_ID": "fig:pipeline",
            "classification": "CONCEPTUAL",
            "caption": "Verify-or-abstain evidence pipeline",
            "source": "paper/newinml2026/manuscript/main.tex figure environment",
            "renderer_tool": "LaTeX fbox/parbox",
            "rendered_artifact_hash": MAIN_TEX,
            "empirical": False,
            "notes": "Not an empirical result graphic.",
        },
        {
            "FIGURE_ID": "Elvis figures/workflow_dag.svg",
            "classification": "CONCEPTUAL",
            "source": "ElvisHan2022 fork",
            "renderer_tool": "SVG",
            "rendered_artifact_hash": "642bab937abf3b2fad74defac633f8423312bf9ea0022d264ca1ab6b60b4aca1",
            "admission": "TEAM_CONTRIBUTION_ONLY",
            "empirical": False,
        },
        {
            "FIGURE_ID": "playwright 07/08 screenshots",
            "classification": "UI_SCREENSHOT",
            "admission": "TEAM_CONTRIBUTION_ONLY / EXCLUDE_FROM_ANONYMOUS_PACKAGE",
            "empirical": False,
        },
    ]
    dump_jsonl(OUT / "FIGURE_PROVENANCE_LEDGER.jsonl", figures)

    notebooks = [
        {
            "finding": "NO_JUPYTER_NOTEBOOKS",
            "search": [
                "/Users/byron/projects/active/protein-hinge",
                "Studio protein-hinge worktree",
            ],
            "count": 0,
            "NOTEBOOK_PROVENANCE_GAP": False,
            "notes": "No .ipynb in team paper path. EXP-006 used cached JSON/CSV not a notebook.",
        }
    ]
    dump_jsonl(OUT / "NOTEBOOK_PROVENANCE_LEDGER.jsonl", notebooks)

    reruns = [
        {
            "experiment_id": "EXP-GAP-ACCOUNTING-001",
            "chain": [
                {"step": "original", "when": "2026-08-13", "result": "summary zeros vs 3 ABSTAIN rows"},
                {"step": "defect", "what": "hardcoded abstentions dict ingest_gap.py:119-124"},
                {"step": "repair", "script": "repair_ingest_gap.py"},
                {"step": "rerun", "when": "2026-08-28", "id": "EXP-GAP-ACCOUNTING-001.1", "result": "invariants pass"},
                {"step": "current_canonical", "verify": "2026-08-30 file hashes MATCH results.json"},
            ],
            "earliest_divergent_dependency": "gap/ingest_gap.py hardcoded abstentions",
        },
        {
            "experiment_id": "G1 / EXP-002-SUCCESSOR-001",
            "chain": [
                {"step": "historical_unverified", "values": "28/123=22.8% or 24.6% naive rate", "status": "NOT_FOUND / SUPERSEDED"},
                {"step": "defect", "what": "residue check before variant-class assignment inflated mismatch bucket (frameshifts counted as mismatches)"},
                {"step": "repair", "what": "classify frameshift BEFORE residue check in build_fasta_lane.py"},
                {"step": "rerun", "when": "2026-08-25 capture; 16/114=14.0% Elvis metric; 98 emitted"},
                {"step": "canonical_paper", "what": "reports 16 as accounting terminal not 14.0% silent-error rate"},
                {"step": "this_audit", "when": "2026-08-30", "result": "frozen replay MATCH 364=98+266; 16/16 mismatches TAFAZZIN"},
            ],
            "earliest_divergent_dependency": "apply_variant classification order",
            "do_not_average": True,
        },
        {
            "experiment_id": "G2 / EXP-003-SUCCESSOR-001",
            "chain": [
                {"step": "historical_unverified", "values": "742 fetched / 642 kept / 100 missing / 287 CNV", "status": "NOT_FOUND_IN_REPO_CUSTODY"},
                {"step": "defect", "what": "100-ID TAFAZZIN ESummary XML 16503275 bytes > 10MB JSON ceiling; also historical corpus not in git"},
                {"step": "repair", "what": "split-and-retry; contemporary capture 2026-08-25"},
                {"step": "rerun", "result": "746/364/382/0 balanced"},
                {"step": "canonical_paper", "what": "reports contemporary accounting; refuses silent-error rate; 742 not reproduced"},
            ],
            "earliest_divergent_dependency": "missing historical G2 derivation chain + NCBI batch JSON ceiling",
            "do_not_average": True,
        },
        {
            "experiment_id": "EXP-006",
            "chain": [
                {"step": "original", "when": "2026-08-13T15:18:33Z", "result": "rank 28, enrichment 0.246"},
                {"step": "reproduction", "when": "2026-08-28", "result": "exact_match_cached true; negative retained"},
            ],
        },
        {
            "experiment_id": "citations/reference integrity",
            "chain": [
                {"step": "PR#5", "sha": "4a372a5c459ad60cd23b850709011cbfd0e516b4"},
                {"step": "PR#7", "what": "ClinVar/CPJUMP1 resource citations closed"},
            ],
        },
    ]
    dump_jsonl(OUT / "RERUN_LINEAGE.jsonl", reruns)

    # Team member delta
    prs = [
        {
            "PR": 1,
            "contributor": "ElvisHan2022",
            "title": "Healthomics lane",
            "state": "OPEN",
            "base_ref": "main",
            "base_sha": "94f8949f1bbcb63d8e80baadd0c5f380f01b9f92",
            "head_ref": "ElvisHan2022:healthomics-lane",
            "head_sha_live": PR1_LIVE,
            "head_sha_admitted_snapshot": PR1_ADMITTED,
            "merged": False,
            "admitted_into_canonical_team_evidence": "HASH_ADMITTED_ONLY — not merged",
            "scientific_contribution": "ClinVar subset, FASTA lane, G1/G2 successor metrics, generated paper macros",
            "manuscript_contribution": "Separate paper/main.tex (silent-error framing) NOT merged into NewInML main.tex",
            "conflicts_successors": f"live {PR1_LIVE} diverged from admitted {PR1_ADMITTED}; clinvar TSV same; elvis main.tex diverged (date{{}} hygiene)",
            "material_files_n": 52,
        },
        {
            "PR": 2,
            "contributor": "biobitworks",
            "title": "NewInML 2026 team-review candidate freeze",
            "state": "MERGED",
            "base_sha": "3ab2d2a476bbac7e4df402aaf126e0791cc5d41a",
            "head_sha": "ed55b792c74eade6850f9c3559cc881dd81960fa",
            "merge_commit": PR2_MERGE,
            "merged": True,
            "admitted_into_canonical_team_evidence": True,
            "scientific_contribution": "Paper FCG, experiments, GAP repair, thesis, NewInML manuscript projection",
            "manuscript_contribution": "Canonical team-review manuscript freeze",
            "conflicts_successors": "Superseded as live HEAD by later PRs 4-7 and probox commits",
        },
        {
            "PR": 3,
            "contributor": "biobitworks",
            "title": "CI: deterministic NewInML final seal",
            "state": "CLOSED_NOT_MERGED",
            "head_sha": "ca29ae9e403e3f68a33ae6c94dadead5f27c3b72",
            "merged": False,
            "admitted_into_canonical_team_evidence": "SUPERSEDED by PR#4 workflow file",
            "scientific_contribution": "none",
            "manuscript_contribution": "CI workflow only",
            "conflicts_successors": "PR#4",
        },
        {
            "PR": 4,
            "contributor": "biobitworks",
            "title": "Submission audit repair",
            "state": "MERGED",
            "merge_commit": "1542176674f4535ffdfd06d1f2262bc61fc601e0",
            "merged": True,
            "admitted_into_canonical_team_evidence": True,
            "scientific_contribution": "none (hygiene/gates)",
            "manuscript_contribution": "SUBMISSION_HYGIENE_FIX + build.sh",
        },
        {
            "PR": 5,
            "contributor": "biobitworks",
            "title": "template and reference integrity",
            "state": "MERGED",
            "merge_commit": "4a372a5c459ad60cd23b850709011cbfd0e516b4",
            "merged": True,
            "admitted_into_canonical_team_evidence": True,
            "scientific_contribution": "bibliography/citation closure",
            "manuscript_contribution": "references.bib + smoke pdf",
        },
        {
            "PR": 6,
            "contributor": "biobitworks",
            "title": "ML/HL team handoff",
            "state": "MERGED",
            "merge_commit": "ab23f43df3e494fe3abbf32d8805081461112cef",
            "merged": True,
            "admitted_into_canonical_team_evidence": True,
            "scientific_contribution": "none new experiments",
            "manuscript_contribution": "handoff package; not manuscript body",
        },
        {
            "PR": 7,
            "contributor": "biobitworks",
            "title": "GREEN/YELLOW closeout",
            "state": "MERGED",
            "head_sha": "411d5816cf5724a0031d21d2fd5da8bbfe09a41b",
            "merge_commit": "411d5816cf5724a0031d21d2fd5da8bbfe09a41b",
            "merged": True,
            "admitted_into_canonical_team_evidence": True,
            "scientific_contribution": "claim SOT/AOK closure refresh; experiment terminal inventory (partially stale vs this audit)",
            "manuscript_contribution": "resource citations ClinVar/CPJUMP1",
        },
    ]
    with (OUT / "TEAM_MEMBER_DELTA_MATRIX.csv").open("w", newline="", encoding="utf-8") as fh:
        fields = [
            "PR", "contributor", "title", "state", "head_sha_live", "head_sha_admitted_snapshot",
            "merge_commit", "merged", "admitted_into_canonical_team_evidence",
            "scientific_contribution", "manuscript_contribution", "conflicts_successors",
        ]
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in prs:
            w.writerow(r)

    # scope matrix
    scope_rows = [
        {"item": "fcg/store evidence ledger", "class": "TEAM_CORE"},
        {"item": "verify-or-abstain architecture + NewInML manuscript", "class": "TEAM_CORE"},
        {"item": "GAP accounting 001 / 001.1", "class": "TEAM_CORE"},
        {"item": "EXP-002/003 provenance negatives", "class": "TEAM_CORE"},
        {"item": "EXP-004 G3 ablation", "class": "TEAM_CORE"},
        {"item": "EXP-005 locked not executed", "class": "TEAM_CORE"},
        {"item": "EXP-006 cached null", "class": "TEAM_CORE"},
        {"item": "PR#1 ClinVar/FASTA successor bytes (hash-admitted)", "class": "TEAM_CONTRIBUTED"},
        {"item": "PR#1 Elvis silent-error manuscript", "class": "TEAM_CONTRIBUTION_NOT_MERGED"},
        {"item": "AUD-FCG document lattice / atom-SOT", "class": "TEAM_IMPORTED_DEPENDENCY"},
        {"item": "Antigence B4 comparator", "class": "TEAM_IMPORTED_DEPENDENCY"},
        {"item": "SeedGraph local import receipts", "class": "TEAM_IMPORTED_DEPENDENCY"},
        {"item": "biocustody zip bootstrap", "class": "TEAM_IMPORTED_DEPENDENCY"},
        {"item": "gsigmad / GettingScienceDone contracts", "class": "SHARED_PREEXISTING_INFRASTRUCTURE"},
        {"item": "Neo4j OrbStack SeedGraph", "class": "SHARED_PREEXISTING_INFRASTRUCTURE"},
        {"item": "HydraDG / L0-L5 / AntiCube / Delta-G", "class": "SOLO_RESEARCH_PROGRAM"},
        {"item": "EXP-007 SGLang CUDA", "class": "FUTURE_DIRECTION"},
        {"item": "production SeedGraph writeback", "class": "FUTURE_DIRECTION"},
        {"item": "therapeutic efficacy / RWE / FTO_OPINION", "class": "REMOVE_FROM_TEAM_CLAIMS"},
        {"item": "author roster / OpenReview metadata / +30 row proof", "class": "OPERATOR_INFORMATION_REQUIRED"},
        {"item": "EXP-Q38 compute canary", "class": "OUT_OF_TEAM_SCOPE"},
    ]
    with (OUT / "TEAM_SCOPE_MATRIX.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["item", "class"])
        w.writeheader()
        w.writerows(scope_rows)

    # claims
    claims = [
        {"id": "C01", "statement": "Hash-valid custody can be semantically inconsistent (zero vs three abstentions)", "class": "SUPPORTED_EXACT", "evidence": "EXP-GAP-001 / 001.1"},
        {"id": "C02", "statement": "Successor GAP run restores invariants N=4/1/3", "class": "SUPPORTED_EXACT", "evidence": "EXP-GAP-001.1 hashes MATCH"},
        {"id": "C03", "statement": "G3 deterministic contract passes", "class": "SUPPORTED_EXACT", "evidence": "Lane A 5/5"},
        {"id": "C04", "statement": "N=1 bypass unsupported identity admission", "class": "SUPPORTED_BOUNDED", "evidence": "Lane B N=1; not a rate"},
        {"id": "C05", "statement": "Historical G3 wiring reconcile(symbol,symbol)", "class": "SUPPORTED_EXACT", "evidence": "evaluation_wiring_defect.json"},
        {"id": "C06", "statement": "G1/G2 historical corpora not recovered", "class": "SUPPORTED_EXACT", "evidence": "EXP-002/003 COMPLETE_NEGATIVE"},
        {"id": "C07", "statement": "G1 successor 364=98+266 breakdown", "class": "SUPPORTED_EXACT", "evidence": "frozen replay 2026-08-30"},
        {"id": "C08", "statement": "G2 successor 746=364+382+0", "class": "SUPPORTED_BOUNDED", "evidence": "frozen provenance JSON + TSV; no live NCBI this audit"},
        {"id": "C09", "statement": "382 is not a validated silent-error rate", "class": "SUPPORTED_EXACT", "evidence": "canonical wording matches EXP-003 terminology ceiling"},
        {"id": "C10", "statement": "G1 generality / residue mismatches as general silent errors", "class": "NOT_PROPOSITIONAL", "evidence": "canonical does not claim gene-general silent-error; 16/16 TAFAZZIN — Elvis paper overclaims relative to this"},
        {"id": "C11", "statement": "Morphology null retained negative 28/50 enrichment<1", "class": "SUPPORTED_BOUNDED", "evidence": "cached exact match; full CPJUMP1 not local"},
        {"id": "C12", "statement": "EXP-005 not executed", "class": "SUPPORTED_EXACT", "evidence": "READINESS_AUDIT"},
        {"id": "C13", "statement": "No structure-prediction execution in admitted evidence", "class": "SUPPORTED_EXACT", "evidence": "Limitations; Elvis structure-tool language CONTRADICTED for team paper"},
        {"id": "C14", "statement": "all 98 verified position by position", "class": "SUPPORTED_BOUNDED", "evidence": "apply_variant only emits if residue matches; not an independent second assay"},
        {"id": "C15", "statement": "+30 offset", "class": "NOT_ESTABLISHED", "evidence": "SOT-008"},
        {"id": "C16", "statement": "two runs a day apart", "class": "INSUFFICIENT", "evidence": "capture timestamps 2026-08-25 vs successor receipts 2026-08-28; not a designed two-run experiment in canonical paper"},
        {"id": "C17", "statement": "missing 100 records", "class": "SUPPORTED_BOUNDED", "evidence": "mechanism recovered on contemporary capture; historical 742/642 not reproduced"},
        {"id": "C18", "statement": "24.6% → 14.0% correction", "class": "SUPPORTED_BOUNDED", "evidence": "Elvis/SOT only; canonical omits rates; order-of-operations repair is real"},
        {"id": "C19", "statement": "six evidence types vs table contents", "class": "NOT_PROPOSITIONAL", "evidence": "canonical Table 1 is experiment terminals not six evidence types"},
        {"id": "C20", "statement": "three vs five verdict-state wording", "class": "NOT_PROPOSITIONAL", "evidence": "canonical uses Admit|Abstain plus ceilings; not a 3-of-5 verdict table"},
        {"id": "C21", "statement": "Merkle / committed-byte re-derivation", "class": "SUPPORTED_BOUNDED", "evidence": "canonical claims SHA-256 leaf/manifest recompute not a CT Merkle audit tree; Elvis cites RFC6962 more strongly"},
        {"id": "C22", "statement": "We present / we frame (group paper voice)", "class": "SUPPORTED_BOUNDED", "evidence": "multi-contributor git; PR#1 not merged; Git metadata ≠ human authorship proof"},
        {"id": "C23", "statement": "Numbers not accepted from LLM as measurement authority", "class": "SUPPORTED_BOUNDED", "evidence": "G1/G2/GAP/G3/EXP-006 paths exist; table is hand-transcribed from receipts"},
        {"id": "C24", "statement": "Silent error language for G2 in canonical paper", "class": "SUPPORTED_EXACT", "evidence": "canonical refuses silent-error rate for 382"},
    ]
    with (OUT / "CLAIM_EVIDENCE_AUDIT.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "statement", "class", "evidence"])
        w.writeheader()
        w.writerows(claims)

    # group effort metrics
    terminals = [e["terminal_state"] for e in exps]
    ge = {
        "schema": "protein_hinge.group_effort_evidence_audit.v1",
        "proposition": (
            "A multi-contributor scientific software/paper workflow can preserve "
            "explicit provenance, deterministic derivation, abstention, negative "
            "results, and contribution boundaries across Git collaboration, "
            "experiment repair, manuscript generation, and submission review."
        ),
        "study_class": "SYSTEMS_PROCESS_OBSERVATION",
        "not_a_controlled_human_subject_study": True,
        "no_causality_or_population_validity_claimed": True,
        "generated_at_utc": NOW,
        "metrics": {
            "contributors_represented_git": ["biobitworks", "ElvisHan2022"],
            "relevant_prs": 7,
            "prs_merged": 5,
            "prs_open": 1,
            "prs_closed_unmerged": 1,
            "admitted_source_objects_pr1_hash": "ADMIT_TO_PAPER paths hashed; bytes not in main tree",
            "experiment_objects_inventoried": len(exps),
            "positive_terminals": sum(1 for t in terminals if t == "COMPLETE_POSITIVE"),
            "negative_null_terminals": sum(1 for t in terminals if t in {"COMPLETE_NEGATIVE", "COMPLETE_NULL"}),
            "bounded_terminals": sum(1 for t in terminals if t == "COMPLETE_BOUNDED"),
            "underpowered_terminals": sum(1 for t in terminals if t == "UNDERPOWERED"),
            "blocked_terminals": sum(1 for t in terminals if t == "BLOCKED"),
            "not_executed_terminals": sum(1 for t in terminals if t == "NOT_EXECUTED"),
            "superseded_terminals": sum(1 for t in terminals if t == "SUPERSEDED"),
            "corrected_results_visible": ["GAP 0 vs 3", "G1 24.6%->14.0% Elvis", "G2 742 not reproduced"],
            "contradictions_preserved": True,
            "operator_required_decisions": [
                "FINAL_SUBMISSION_SEAL OPERATOR_INFORMATION_REQUIRED",
                "SOT-008 +30",
                "SOT-020 contributor roster",
                "PR#1 merge/no-merge",
            ],
            "canonical_numerical_claims_tracked": sum(1 for r in nums if r.get("in_canonical_manuscript")),
            "canonical_numerical_MANUAL_VALUE": 0,
            "canonical_tables": 1,
            "canonical_tables_closed_or_bounded": 1,
            "canonical_figures": 1,
            "canonical_figures_classified": 1,
            "notebooks": 0,
            "contributor_deltas_admitted": "PR2-7 merged; PR1 hash-admitted not merged",
            "contributor_deltas_not_admitted": "Elvis silent-error manuscript, UI screenshots, live post-6e47dbe tex hygiene",
        },
        "finding_bounded": (
            "On this corpus, Git collaboration plus hash-admitted fork artifacts plus "
            "explicit negative/not-executed terminals did preserve contribution boundaries "
            "and most canonical numerical claims with machine paths. The observation is "
            "descriptive of protein-hinge NewInML 2026, not a generalizable causal result."
        ),
    }
    dump(OUT / "GROUP_EFFORT_EVIDENCE_AUDIT.json", ge)

    # AUDIT_STATE + gates
    gates = {
        "GIT_AUTHORITY_GATE": "PASS_WITH_BOUNDED_GAPS",
        "TEAM_SCOPE_GATE": "PASS",
        "EXPERIMENT_ACCOUNTING_GATE": "PASS_WITH_BOUNDED_GAPS",
        "RERUN_LINEAGE_GATE": "PASS",
        "NUMERICAL_CLAIM_GATE": "PASS_WITH_BOUNDED_GAPS",
        "TABLE_PROVENANCE_GATE": "YELLOW",
        "FIGURE_PROVENANCE_GATE": "PASS",
        "NOTEBOOK_PROVENANCE_GATE": "NOT_APPLICABLE",
        "CLAIM_EVIDENCE_GATE": "PASS_WITH_BOUNDED_GAPS",
        "GROUP_EFFORT_AUDIT_GATE": "PASS",
        "ANONYMITY_GATE": "PASS",
    }
    gate_notes = {
        "GIT_AUTHORITY_GATE": "Stale CANONICAL_PAPER_SOURCE.yaml (2ba0d923) vs live CI source bc4b0d5; cockpit Pro with Studio queried.",
        "EXPERIMENT_ACCOUNTING_GATE": "EXPERIMENT_MATRIX.md and handoff 05_EXPERIMENT_INDEX_ML.jsonl stale vs receipts.",
        "NUMERICAL_CLAIM_GATE": "206 MB bootstrap PARTIAL_TRACE this session; G2 746 from frozen provenance not live refetch.",
        "TABLE_PROVENANCE_GATE": "Canonical Table 1 hand-transcribed from receipts; Elvis Tables generated but not in canonical package. No independent Table 2-4 in NewInML main.tex.",
        "NOTEBOOK_PROVENANCE_GATE": "Zero notebooks.",
        "ANONYMITY_GATE": "CI receipt ANONYMITY_GATE PASS; this audit did not mutate anonymous bundle.",
    }
    audit_state = {
        "schema": "protein_hinge.final_team_evidence_audit.state.v1",
        "audit_id": "AUD-FINAL-TEAM-EVIDENCE-20260829",
        "generated_at_utc": NOW,
        "daisy": "CLOSEOUT",
        "gates": gates,
        "gate_notes": gate_notes,
        "REPO_HEAD_SHA": REPO_HEAD,
        "CANONICAL_PAPER_SOURCE_SHA": CI_SOURCE,
        "CI_RUN_ID": CI_RUN,
        "FINAL_PDF_SHA256": PDF_SHA,
        "manuscript_modified": False,
        "SIGNATURE_STATE": "NOT_SIGNED",
        "llm_in_science_leaf": False,
    }
    dump(OUT / "AUDIT_STATE.json", audit_state)

    counts = {
        "COMPLETE_POSITIVE": sum(1 for e in exps if e["terminal_state"] == "COMPLETE_POSITIVE"),
        "COMPLETE_NEGATIVE": sum(1 for e in exps if e["terminal_state"] == "COMPLETE_NEGATIVE"),
        "COMPLETE_BOUNDED": sum(1 for e in exps if e["terminal_state"] == "COMPLETE_BOUNDED"),
        "UNDERPOWERED": sum(1 for e in exps if e["terminal_state"] == "UNDERPOWERED"),
        "BLOCKED": sum(1 for e in exps if e["terminal_state"] == "BLOCKED"),
        "NOT_EXECUTED": sum(1 for e in exps if e["terminal_state"] == "NOT_EXECUTED"),
        "SUPERSEDED": sum(1 for e in exps if e["terminal_state"] == "SUPERSEDED"),
        "total": len(exps),
    }
    dump(OUT / "FINAL_AUDIT_RECEIPT.json", {
        "schema": "protein_hinge.final_team_evidence_audit.receipt.v1",
        "audit_id": "AUD-FINAL-TEAM-EVIDENCE-20260829",
        "recorded_at_utc": NOW,
        "cockpit_host": "magicPRObox.local",
        "evidence_host": "magicSTUDIObox.local",
        "BASE_SHA": REPO_HEAD,
        "CANONICAL_PAPER_SOURCE_SHA": CI_SOURCE,
        "CI_AUTHORITATIVE_PDF_SHA256": PDF_SHA,
        "CI_RUN_ID": CI_RUN,
        "gates": gates,
        "experiment_counts": counts,
        "missed_core_experiments": 0,
        "canonical_numerical_total": sum(1 for r in nums if r.get("in_canonical_manuscript")),
        "canonical_numerical_unresolved": sum(
            1 for r in nums
            if r.get("in_canonical_manuscript")
            and r["final_state"] in {"MANUAL_VALUE", "CONFLICTING", "NOT_ESTABLISHED"}
        ),
        "canonical_numerical_partial": sum(
            1 for r in nums if r.get("in_canonical_manuscript") and r["final_state"] == "PARTIAL_TRACE"
        ),
        "tables_canonical": 1,
        "tables_closed": 0,
        "tables_bounded": 1,
        "figures_canonical": 1,
        "figures_classified": 1,
        "notebooks": 0,
        "manuscript_change_recommended": "MINIMAL_RECOMMENDED",
        "ready_for_independent_chatgpt_review": "YES",
        "SIGNATURE_STATE": "NOT_SIGNED",
        "llm_in_science_leaf": False,
    })

    print("wrote ledgers to", OUT)
    print("experiment_counts", counts)


if __name__ == "__main__":
    main()
