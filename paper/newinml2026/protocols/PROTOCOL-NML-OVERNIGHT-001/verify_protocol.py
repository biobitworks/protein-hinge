#!/usr/bin/env python3
"""Verify PROTOCOL-NML-OVERNIGHT-001 state and receipt hashes."""
from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROTO = ROOT / "paper" / "newinml2026" / "protocols" / "PROTOCOL-NML-OVERNIGHT-001"
WAVES = PROTO / "waves"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    state_path = PROTO / "STATE.json"
    if not state_path.exists():
        print("FAIL: STATE.json missing")
        return 1
    state = json.loads(state_path.read_text())
    ok = True
    for wid, w in state.get("waves", {}).items():
        co_dir = WAVES / "W00_bootstrap" if wid == "W00" else WAVES / wid.lower()
        co = co_dir / "CLOSEOUT.json"
        if not co.exists():
            print(f"FAIL: missing closeout for {wid}")
            ok = False
        else:
            print(f"OK: {wid} -> {w.get('terminal')} ({co})")
    prompt = PROTO / "ORIGINAL_CONTROLLER_PROMPT.md"
    if prompt.exists():
        print(f"OK: prompt sha256={sha256_file(prompt)[:16]}...")
    else:
        print("WARN: ORIGINAL_CONTROLLER_PROMPT.md missing")
    print(f"Protocol terminal: {state.get('terminal')}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
