#!/usr/bin/env python3
"""Governed Qwen3.8 Ollarma re-test: 1 cold + 3 warm trials."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "receipts"
MODEL = "qwen3.8:27b"
DIGEST = "22130167c4c20e20c7b71454612966ca8e8171e9b3cc8ab6ce8aa6cbfec79643"
OLLARMA = "http://127.0.0.1:8484/chat"
CANARY = "Q38_CANARY_OK"
PROMPT = f"""Return ONLY a strict JSON object with exactly these keys:
  "model" (string)
  "canary" (string, must be exactly "{CANARY}")
  "answer" (string, one word: OK)

No markdown. No explanation. JSON only."""
PROMPT_SHA = "23a0a3110682f984b4f5153450fc904332cc8ad5271cffd532c135f136a7f7f5"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def vm_swap() -> dict:
    try:
        out = subprocess.check_output(["vm_stat"], text=True)
        pages = {}
        for line in out.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                pages[k.strip()] = int(v.strip().rstrip(".").replace(",", "") or 0)
        return pages
    except Exception:
        return {}


def evict_model(model: str) -> None:
    payload = json.dumps({"model": model, "prompt": "", "keep_alive": "0s"}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=30)
    except Exception:
        pass


def verify(raw: str) -> tuple[bool, str]:
    try:
        obj = json.loads(raw.strip())
    except json.JSONDecodeError:
        return False, "NO_JSON"
    if obj.get("canary") != CANARY:
        return False, "CANARY_MISMATCH"
    return True, "PASS"


def trial(label: str, *, evict_before: bool) -> dict:
    if evict_before:
        evict_model(MODEL)
        time.sleep(2)
    swap_before = vm_swap()
    body = json.dumps({
        "model": MODEL,
        "message": PROMPT,
        "strict_model_identity": True,
        "temperature": 0,
    }).encode()
    t0 = time.perf_counter()
    req = urllib.request.Request(
        OLLARMA,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        parsed = json.loads(resp.read().decode())
    latency = round(time.perf_counter() - t0, 3)
    raw = str(parsed.get("response") or "")
    ok, reason = verify(raw) if parsed.get("status") != "blocked" else (False, parsed.get("reason_code"))
    executed = parsed.get("model")
    digest_match = None
    tags = json.loads(urllib.request.urlopen("http://127.0.0.1:11434/api/tags").read())
    for m in tags.get("models", []):
        if m.get("name") == MODEL:
            digest_match = m.get("digest") == DIGEST
            break
    return {
        "trial": label,
        "evict_before": evict_before,
        "start_utc": utc_now(),
        "latency_sec": latency,
        "requested_model": MODEL,
        "executed_model": executed,
        "executed_digest_match": digest_match,
        "status": parsed.get("status"),
        "reason_code": parsed.get("reason_code"),
        "verifier": reason,
        "verdict": "PASS" if ok and executed and digest_match else "FAIL",
        "raw_output_sha256": sha256_text(raw) if raw else None,
        "swap_before": swap_before,
        "swap_after": vm_swap(),
    }


def main() -> int:
    trials = [trial("cold_1", evict_before=True)]
    for i in range(1, 4):
        trials.append(trial(f"warm_{i}", evict_before=False))

    all_pass = all(t["verdict"] == "PASS" for t in trials)
    receipt = {
        "receipt_id": "QWEN38_OLLARMA_GOVERNED_RECEIPT",
        "schema": "protein_hinge.model_canary.governed_trials.v1",
        "generated_at_utc": utc_now(),
        "host": subprocess.check_output(["hostname"], text=True).strip(),
        "model_requested": MODEL,
        "frozen_digest": DIGEST,
        "prompt_sha256": PROMPT_SHA,
        "strict_model_identity": True,
        "ollarma_policy_note": "OLLARMA_MODEL_LOAD_TIMEOUT_SECONDS=180 for cold loads",
        "trials": trials,
        "summary": {
            "cold_pass": trials[0]["verdict"] == "PASS",
            "warm_pass_count": sum(1 for t in trials[1:] if t["verdict"] == "PASS"),
            "strict_model_identity_pass": all_pass,
        },
    }
    out = RECEIPTS / "QWEN38_OLLARMA_GOVERNED_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt["summary"], indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
