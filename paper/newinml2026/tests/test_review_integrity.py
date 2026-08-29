"""Regression tests for NewInML review integrity gates."""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / "paper" / "newinml2026"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


class ProtocolTerminalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rp = load_module("run_protocol", PAPER / "protocols/PROTOCOL-NML-OVERNIGHT-001/run_protocol.py")

    def test_all_complete(self) -> None:
        waves = {f"W{i:02d}": {"terminal": "COMPLETE"} for i in range(11)}
        self.assertEqual(self.rp.derive_overall_terminal(waves), "COMPLETE")

    def test_one_blocked(self) -> None:
        waves = {"W00": {"terminal": "COMPLETE"}, "W01": {"terminal": "BLOCKED"}}
        self.assertEqual(self.rp.derive_overall_terminal(waves), "BLOCKED")

    def test_one_quarantined(self) -> None:
        waves = {"W00": {"terminal": "COMPLETE"}, "W01": {"terminal": "QUARANTINED"}}
        self.assertEqual(self.rp.derive_overall_terminal(waves), "QUARANTINED")


class BootstrapHashingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.boot = load_module("bootstrap", PAPER / "scripts/bootstrap_team_review_closeout.py")

    def test_manifest_self_exclude(self) -> None:
        self.assertIn("PAPER_SOURCE_MANIFEST.vNext.jsonl", self.boot.MANIFEST_SELF_EXCLUDE)

    def test_verify_pass_stable(self) -> None:
        import subprocess

        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        ha, hb = self.boot.verify_pass_stable(sha)
        self.assertEqual(ha, hb)


class AnonymizationFailClosedTests(unittest.TestCase):
    def test_missing_pdfinfo_blocks(self) -> None:
        anon = load_module("anon", PAPER / "scripts/anonymization_scan.py")
        missing = ROOT / "paper/newinml2026/manuscript/__no_such__.pdf"
        findings, inspection = anon.inspect_pdf_metadata(missing)
        self.assertEqual(inspection["status"], "BLOCKED_VALIDATION")
        self.assertEqual(findings, [])


class GitShaValidationTests(unittest.TestCase):
    def test_content_commit_is_commit(self) -> None:
        boot = load_module("bootstrap2", PAPER / "scripts/bootstrap_team_review_closeout.py")
        import subprocess

        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        boot.validate_git_sha(sha)

    def test_malformed_sha_rejected(self) -> None:
        boot = load_module("bootstrap3", PAPER / "scripts/bootstrap_team_review_closeout.py")
        with self.assertRaises(Exception):
            boot.validate_git_sha("5da12c619b230fd8d971fe4e599a15b420ae794d")


if __name__ == "__main__":
    unittest.main()
