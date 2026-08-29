#!/usr/bin/env python3
"""Build sanitized anonymous reviewer package for REQ-002.

This export is intentionally minimal. It must never copy repository/source
identity, historical local build receipts, or duplicate copies of the final PDF.
The final PDF and CI-generated receipts are added later by the seal workflow.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper" / "newinml2026" / "submission" / "anonymous"

# Minimal anonymous reproduction surface. The CI seal workflow adds the exact
# final paper leaf and runtime page/build receipts after all final gates pass.
EXPORTS = [
    ("gap/normalize.py", "methods/normalize.py"),
    ("gap/alias_table.json", "methods/alias_table.json"),
    ("gap/rules.py", "methods/rules.py"),
    ("paper/newinml2026/experiments/EXP-004/DATA_CONTRACT.json", "methods/DATA_CONTRACT.json"),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sanitize_text(text: str) -> str:
    repl = [
        ("biobitworks", "[REDACTED_ORG]"),
        ("Byron", "[REDACTED]"),
        ("byron@", "[REDACTED_EMAIL]"),
        ("/Users/byron", "[REDACTED_PATH]"),
        ("github.com/biobitworks", "[REDACTED_URL]"),
        ("magicSTUDIObox.local", "[REDACTED_HOST]"),
    ]
    for old, new in repl:
        text = text.replace(old, new)
    return text


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    for sub in ["methods", "data"]:
        (OUT / sub).mkdir(parents=True)

    manifest = []
    for src_rel, dst_rel in EXPORTS:
        src = ROOT / src_rel
        dst = OUT / dst_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in {".py", ".json", ".md", ".yaml", ".yml", ".tex", ".bib"}:
            dst.write_text(sanitize_text(src.read_text()))
        else:
            shutil.copy2(src, dst)
        manifest.append(
            {
                "anonymous_path": dst_rel,
                "content_sha256": sha256_file(dst),
                "source_class": "sanitized_export",
            }
        )

    (OUT / "data" / "manifest.json").write_text(
        json.dumps({"objects": manifest}, indent=2) + "\n"
    )
    (OUT / "README.md").write_text(
        "# Anonymous Review Package\n\n"
        "This is a deliberately minimal double-blind verification subset. The final seal workflow "
        "adds the exact submitted PDF and runtime receipts after validation. The included methods "
        "exercise the deterministic G3 normalization/guard contract; they do not claim to reproduce "
        "the unrecovered historical G1/G2 corpora or every experiment reported in the paper.\n"
    )
    (OUT / "reproduce.sh").write_text(
        "#!/bin/sh\nset -e\npython3 methods/normalize.py\n"
        "python3 -c \"import json; json.load(open('methods/alias_table.json'))\"\n"
    )
    (OUT / "reproduce.sh").chmod(0o755)
    (OUT / "CLAIM_EVIDENCE_MATRIX.md").write_text(
        "# Claim Evidence Matrix (anonymous)\n\n"
        "| Claim | Evidence class | Object ID | Reproduction scope |\n"
        "|-------|----------------|-----------|--------------------|\n"
        "| G3 contract deterministic | DETERMINISTIC_CONTRACT_TEST | EXP-004 lane A | Included |\n"
        "| Historical G1/G2 exact reproduction | NOT_ESTABLISHED | provenance audit | Not claimed |\n"
        "| Structure-prediction execution | NEGATIVE_BOUNDARY | claim ceiling | Not executed |\n"
    )
    print(
        json.dumps(
            {"exported": len(manifest), "root": str(OUT.relative_to(ROOT))},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
