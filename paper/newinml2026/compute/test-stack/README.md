# Qwen3.8 Successor Model Panel — Test Stack

Governed matched comparison: **qwen3.8:27b** (Studio) vs **qwen3.8-flash-next:125b-a6b-nvfp4** (Daytona H200).

## Resume canary

```bash
python3 paper/newinml2026/compute/test-stack/scripts/qwen38_studio_canary.py
```

## Key artifacts

| Artifact | Path |
|----------|------|
| Model panel contract | `MODEL_PANEL_QWEN38_SUCCESSOR_V1.json` |
| Studio canary receipt | `receipts/QWEN38_STUDIO_CANARY_RECEIPT.json` |
| Daytona preflight | `receipts/DAYTONA_PREFLIGHT.json` |
| EXP-Q38-COMP-001 | `experiments/EXP-Q38-COMP-001/EXPERIMENT_RECEIPT.json` |
| Usage provenance matrix | `MODEL_USAGE_PROVENANCE_MATRIX.csv` |

## Known infrastructure findings

1. **Ollarma 35s local inference timeout** blocks cold/warm `qwen3.8:27b` via `/chat`; direct Ollama API fallback used for canary with receipt annotation.
2. **Daytona** blocked (`DAYTONA_API_KEY` absent) — flash-next comparison pending operator credentials.
3. **No historical qwen3.8-flash-next execution** found in searched projects.
