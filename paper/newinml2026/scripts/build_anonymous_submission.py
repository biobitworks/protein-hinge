#!/usr/bin/env python3
"""Build sanitized anonymous reviewer package for REQ-002."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "paper" / "newinml2026" / "submission" / "anonymous"

# Minimal reproduction surface — no full repo copy.
EXPORTS = [
    ("gap/normalize.py", "methods/normalize.py"),
    ("gap/alias_table.json", "methods/alias_table.json"),
    ("gap/rules.py", "methods/rules.py"),
    ("paper/newinml2026/experiments/EXP-004/DATA_CONTRACT.json", "methods/DATA_CONTRACT.json"),
    ("paper/newinml2026/manuscript/main_smoke.pdf", "receipts/main_smoke.pdf"),
    ("paper/newinml2026/manuscript/BUILD_RECEIPT.json", "receipts/BUILD_RECEIPT.json"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    for sub in ["requirements", "methods", "evaluation", "receipts", "figures", "data"]:
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
        manifest.append({"anonymous_path": dst_rel, "content_sha256": sha256_file(dst), "source_class": "sanitized_export"})
    (OUT / "data" / "manifest.json").write_text(json.dumps({"objects": manifest}, indent=2) + "\n")
    (OUT / "README.md").write_text(
        sanitize_text(
            "# Anonymous Review Package\n\nSanitized subset for double-blind review. "
            "Full private provenance graph retained outside this export.\n"
        )
    )
    (OUT / "reproduce.sh").write_text(
        "#!/bin/sh\nset -e\npython3 methods/normalize.py\npython3 -c \"import json; json.load(open('methods/alias_table.json'))\"\n"
    )
    (OUT / "reproduce.sh").chmod(0o755)
    (OUT / "CLAIM_EVIDENCE_MATRIX.md").write_text(
        "# Claim Evidence Matrix (anonymous)\n\n| Claim | Evidence class | Object ID |\n|-------|----------------|----------|\n"
        "| G3 contract deterministic | DETERMINISTIC_CONTRACT_TEST | EXP-004 lane A |\n"
    )
    print(json.dumps({"exported": len(manifest), "root": str(OUT.relative_to(ROOT))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
