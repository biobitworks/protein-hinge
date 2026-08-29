#!/usr/bin/env python3
"""Qwen3.8 governed canary — Ollarma first (no silent fallback), separate direct path."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = ROOT / "receipts"
MODEL = "qwen3.8:27b"
OLLARMA_HTTP = "http://127.0.0.1:8484/chat"
OLLAMA_CHAT = "http://127.0.0.1:11434/api/chat"
CANARY_VALUE = "Q38_CANARY_OK"

PROMPT = f"""Return ONLY a strict JSON object with exactly these keys:
  "model" (string)
  "canary" (string, must be exactly "{CANARY_VALUE}")
  "answer" (string, one word: OK)

No markdown. No explanation. JSON only."""


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def vm_swap_pages() -> dict:
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


def ollama_version() -> str:
    try:
        return subprocess.check_output(["ollama", "-v"], text=True).strip()
    except Exception:
        return "UNKNOWN"


def model_tags() -> list[dict]:
    with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=30) as resp:
        return json.loads(resp.read().decode()).get("models", [])


def verify_output(raw: str) -> tuple[bool, dict | None, str]:
    text = raw.strip()
    for candidate in (text, raw.strip()):
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                if obj.get("canary") != CANARY_VALUE:
                    return False, obj, "CANARY_MISMATCH"
                if not obj.get("answer"):
                    return False, obj, "MISSING_ANSWER"
                return True, obj, "PASS"
        except json.JSONDecodeError:
            pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return False, None, "NO_JSON_OBJECT"
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError as e:
        return False, None, f"JSON_PARSE:{e}"
    if obj.get("canary") != CANARY_VALUE:
        return False, obj, "CANARY_MISMATCH"
    if not obj.get("answer"):
        return False, obj, "MISSING_ANSWER"
    return True, obj, "PASS"


def ollarma_attempt(prompt: str, model: str, *, strict: bool) -> dict:
    body = {
        "message": prompt,
        "model": model,
        "temperature": 0,
        "strict_model_identity": strict,
    }
    req_raw = json.dumps(body)
    started = time.perf_counter()
    try:
        req = urllib.request.Request(
            OLLARMA_HTTP,
            data=req_raw.encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            parsed = json.loads(resp.read().decode())
    except Exception as exc:
        return {
            "execution_path": "Ollarma_HTTP_8484_chat",
            "status": "error",
            "reason_code": type(exc).__name__,
            "detail": str(exc),
            "latency_sec": round(time.perf_counter() - started, 3),
            "request_sha256": sha256_text(req_raw),
        }
    latency = round(time.perf_counter() - started, 3)
    status = parsed.get("status") or "answered"
    blocked = status == "blocked" or str(parsed.get("response", "")).startswith("BLOCKED:")
    return {
        "execution_path": "Ollarma_HTTP_8484_chat",
        "status": status,
        "blocked": blocked,
        "reason_code": parsed.get("reason_code"),
        "response": parsed.get("response", ""),
        "executed_model": parsed.get("model"),
        "latency_sec": latency,
        "request_sha256": sha256_text(req_raw),
    }


def ollama_direct(prompt: str, model: str) -> dict:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0, "num_predict": 256},
    }
    req_raw = json.dumps(payload)
    started = time.perf_counter()
    req = urllib.request.Request(
        OLLAMA_CHAT,
        data=req_raw.encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            data = json.loads(resp.read().decode())
    except Exception as exc:
        return {
            "execution_path": "EXECUTION_PATH_B_Ollama_API_direct",
            "status": "error",
            "blocked": True,
            "reason_code": type(exc).__name__,
            "detail": str(exc),
            "latency_sec": round(time.perf_counter() - started, 3),
            "request_sha256": sha256_text(req_raw),
        }
    msg = data.get("message") or {}
    return {
        "execution_path": "EXECUTION_PATH_B_Ollama_API_direct",
        "status": "ok",
        "blocked": False,
        "reason_code": None,
        "response": msg.get("content", ""),
        "executed_model": data.get("model", model),
        "latency_sec": round(time.perf_counter() - started, 3),
        "prompt_eval_count": data.get("prompt_eval_count"),
        "eval_count": data.get("eval_count"),
        "request_sha256": sha256_text(req_raw),
    }


def build_receipt(
    *,
    ollarma: dict,
    direct: dict | None,
    prompt_sha: str,
    settings_sha: str,
    tag_info: dict,
    swap_before: dict,
) -> dict:
    direct_ok = False
    direct_parsed = None
    direct_reason = "NOT_RUN"
    if direct:
        direct_ok, direct_parsed, direct_reason = verify_output(str(direct.get("response") or ""))

    ollarma_ok = False
    ollarma_parsed = None
    ollarma_reason = "NOT_RUN"
    if not ollarma.get("blocked") and ollarma.get("response"):
        ollarma_ok, ollarma_parsed, ollarma_reason = verify_output(str(ollarma.get("response")))

    ollarma_result = "PASS" if ollarma_ok else (
        ollarma.get("reason_code") or ("ERROR" if ollarma.get("status") == "error" else "FAIL")
    )
    direct_result = "PASS" if direct_ok else ("NOT_RUN" if direct is None else direct_reason)

    governed_path_pass = ollarma_ok
    overall_verified = ollarma_ok or direct_ok

    primary = ollarma if ollarma_ok else (direct or ollarma)
    raw = primary.get("response") or ""

    return {
        "receipt_id": "QWEN38_STUDIO_CANARY_RECEIPT",
        "schema": "protein_hinge.model_canary.v2",
        "generated_at_utc": utc_now(),
        "host": subprocess.check_output(["hostname"], text=True).strip(),
        "ollama_version": ollama_version(),
        "provider": "Ollama",
        "model_requested": MODEL,
        "model_effective": primary.get("executed_model") or MODEL,
        "model_digest": tag_info.get("digest"),
        "model_size_bytes": tag_info.get("size"),
        "parameter_size": tag_info.get("details", {}).get("parameter_size"),
        "quantization_level": tag_info.get("details", {}).get("quantization_level"),
        "capabilities": tag_info.get("capabilities"),
        "prompt_sha256": prompt_sha,
        "settings_sha256": settings_sha,
        "governed_path_pass": governed_path_pass,
        "ollarma_result": ollarma_result,
        "direct_ollama_result": direct_result,
        "overall_model_availability": "VERIFIED" if overall_verified else "UNVERIFIED",
        "ollarma_attempt": ollarma,
        "direct_ollama_attempt": direct,
        "raw_output": str(raw)[:8000],
        "raw_output_sha256": sha256_text(str(raw)) if raw else None,
        "parsed_output": ollarma_parsed if ollarma_ok else direct_parsed,
        "output_class": "PROBABILISTIC_MODEL_OUTPUT",
        "verifier_version": "q38_canary_validator.v1",
        "verifier_verdict": "PASS" if overall_verified else "FAIL",
        "verifier_reason": ollarma_reason if ollarma_ok else direct_reason,
        "token_counts": {
            "prompt_tokens": (direct or {}).get("prompt_eval_count"),
            "completion_tokens": (direct or {}).get("eval_count"),
        },
        "swap_pages_before": swap_before,
        "swap_pages_after": vm_swap_pages(),
        "resource_state": {
            "memory_pressure_note": "Studio 32GB; qwen3.8:27b cold load ~127-140s historically",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollarma-only", action="store_true")
    parser.add_argument("--direct-only", action="store_true")
    parser.add_argument("--no-direct-fallback", action="store_true")
    args = parser.parse_args()

    swap_before = vm_swap_pages()
    prompt_sha = sha256_text(PROMPT)
    settings = {"model": MODEL, "temperature": 0, "num_predict": 256, "strict_model_identity": True}
    settings_sha = sha256_text(json.dumps(settings, sort_keys=True))
    tag_info = next((m for m in model_tags() if m.get("name") == MODEL), {})

    ollarma = {"execution_path": "SKIPPED", "status": "skipped"}
    direct = None

    if not args.direct_only:
        ollarma = ollarma_attempt(PROMPT, MODEL, strict=True)
    if args.direct_only or (
        not args.ollarma_only
        and (ollarma.get("blocked") or ollarma.get("status") == "error")
        and not args.no_direct_fallback
    ):
        direct = ollama_direct(PROMPT, MODEL)

    receipt = build_receipt(
        ollarma=ollarma,
        direct=direct,
        prompt_sha=prompt_sha,
        settings_sha=settings_sha,
        tag_info=tag_info,
        swap_before=swap_before,
    )
    if receipt.get("eval_count") and receipt.get("latency_sec"):
        pass
    out_path = RECEIPTS / "QWEN38_STUDIO_CANARY_RECEIPT.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({
        "governed_path_pass": receipt["governed_path_pass"],
        "ollarma_result": receipt["ollarma_result"],
        "direct_ollama_result": receipt["direct_ollama_result"],
        "overall_model_availability": receipt["overall_model_availability"],
    }, indent=2))
    return 0 if receipt["overall_model_availability"] == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
