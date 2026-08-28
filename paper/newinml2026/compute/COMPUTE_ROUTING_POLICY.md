# Compute Routing Policy — NewInML 2026

**Canonical controller:** magicSTUDIObox.local (Apple M1 Max, arm64, 32 GB RAM)  
**CUDA capable:** false  
**Policy version:** 2026-08-28-bootstrap

## Pressure snapshot (bootstrap time)

| Signal | Value |
|--------|-------|
| Load average | 12.30 / 11.18 / 10.64 |
| RAM | 32 GB |
| Disk `/` avail | ~25 GiB (33% used) |
| Swap | active (pages wired high) |

Local pressure is elevated. Prefer lightweight deterministic jobs; defer GPU batches
until preregistration complete.

## Job classes

| Class | Accelerator | Default route |
|-------|-------------|---------------|
| hash/git/provenance | CPU | LOCAL |
| FCO/FCG bookkeeping | CPU | LOCAL |
| SeedGraph ingest manifest | CPU | LOCAL |
| statistics / accounting audit | CPU | LOCAL |
| manuscript build | CPU | LOCAL |
| SGLang CUDA graph stress | NVIDIA CUDA | KAGGLE → DAYTONA → BLOCKED |
| large morphology recompute | CPU/GPU optional | LOCAL if frozen inputs fit RAM |

## Routing decision tree

```
1. CUDA required?
   yes → remote only (never magicSTUDIObox)
   no  → continue

2. Local pressure gates pass?
   (load < 16 AND avail_ram > 4GiB AND disk_avail > 5GiB)
   yes → LOCAL
   no  → queue or BLOCKED for heavy jobs; light hashing still LOCAL

3. Remote CUDA:
   a. Kaggle auth + quota OK? → KAGGLE
   b. else Daytona API key + quota OK? → DAYTONA GPU
   c. else → BLOCKED (ask operator)
```

## Remote job custody protocol

**LOCAL (before dispatch):**

1. Preregister experiment (Getting Science Done contract)
2. Freeze inputs; write `compute/dispatch/<run_id>/inputs/`
3. SHA-256 all inputs; write `DISPATCH_MANIFEST.json`

**REMOTE:**

1. Verify incoming hashes match manifest
2. Execute; capture full environment receipt
3. Hash outputs; write `REMOTE_RECEIPT.json`

**LOCAL (after retrieve):**

1. Recompute output SHA-256
2. Compare to remote receipt
3. Mismatch → QUARANTINE (no aggregation)
4. Match → ingest as EXPERIMENT_RESULT FCO successors

## Current readiness

| Host | Status | Notes |
|------|--------|-------|
| LOCAL magicSTUDIObox | READY (CPU) | canonical authority |
| Kaggle | CONFIG_PRESENT | `~/.kaggle/kaggle.json` exists; quota not verified this session |
| Daytona GPU | BLOCKED | `DAYTONA_API_KEY` unset |
| SGLang local | NOT_INSTALLED | expected on arm64 controller |

## Secrets

Never commit credentials. FCG stores secret-reference metadata only (path/env var name).

## Receipt fields (every work unit)

- hostname, architecture
- UTC timestamp
- CPU load, memory pressure, swap, free disk
- required accelerator
- estimated I/O footprint
- job class
- routing decision + reason
