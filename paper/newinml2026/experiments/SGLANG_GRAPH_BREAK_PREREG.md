# SGLang CUDA Graph-Break Stress — Preregistration (EXP-007)

**Status:** PREREGISTERED (not executed)  
**Classification:** EXPLORATORY  
**Host:** REMOTE CUDA ONLY (Kaggle preferred; Daytona fallback)  
**Local controller:** magicSTUDIObox.local (must preregister + hash inputs before dispatch)

## Scientific question

When runtime execution changes, fragments, graph-breaks, fails, or falls back, can
incomplete or incompatible output silently enter the scientific aggregate without an
explicit terminal-state/provenance record?

This is **not** primarily an SGLang performance paper. CUDA graph modes are a
controlled execution stressor for verify-or-abstain/accounting architecture.

## Primary acceptance criterion

```
scientific_accounting_violations == 0
```

Graph-break, crash, fallback, timeout, or OOM are acceptable **experiment results**
if they become explicit FAILURE/ABSTENTION FCOs and do not enter valid aggregates.

## Pinned versions (to be filled at dispatch — do not fabricate)

| Component | Pin field | Bootstrap status |
|-----------|-----------|------------------|
| SGLang | commit / pip version | NOT_INSTALLED locally |
| PyTorch | version + CUDA build | remote only |
| CUDA | driver + toolkit | remote only |
| sgl-kernel / FlashInfer | versions | remote only |
| Python | version | remote only |
| Container image | digest | TBD at Kaggle/Daytona dispatch |
| Model | exact revision/digest | TBD — frozen before run |

**First remote step:** `python -m sglang.launch_server --help` on pinned install;
use flags supported by **that** version only.

## Condition matrix

| Condition | Mode | Purpose |
|-----------|------|---------|
| C0 | CUDA graph disabled / eager | control |
| C1 | full CUDA graph | nominal fast path |
| C2 | torch.compile piecewise CUDA graph | partial capture |
| C3 | breakable CUDA graph | intentional break handling |
| C4 | deliberate unsupported-op stress | forced graph-break |

Held constant across conditions:

- model + exact revision/digest
- prompt corpus + seed set
- sampling config + max tokens
- batch/context matrix

## Metrics

- TTFT, throughput, p50/p95/p99 latency
- peak VRAM, OOM count, request failures
- graph-break/capture log messages
- number of terminal records emitted
- output equivalence vs C0 (where applicable)
- **scientific_accounting_violations** (primary)

## Custody protocol

1. LOCAL: freeze prompts/config; hash; write `compute/dispatch/EXP-007/`
2. REMOTE: verify hashes; execute; capture env receipt + logs
3. LOCAL: retrieve; re-hash; semantic contract check; ingest or QUARANTINE

## Blockers (bootstrap)

- SGLang not installed on magicSTUDIObox (expected)
- Daytona API key unset
- Kaggle config present; quota/GPU availability not verified
- Model + corpus not yet frozen for this paper scope

## Failure handling

Any silent aggregate inclusion → QUARANTINE entire condition run.
Partial outputs without terminal state → CONTRADICTION FCO linked to THESIS.
