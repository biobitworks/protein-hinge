# Disk Cleanup Operator Plan — magicSTUDIObox

**Recorded:** 2026-08-28  
**Data volume before audit:** ~96% used (~15 GiB free on `/System/Volumes/Data`)  
**Goal:** materially more than 12 GiB free before any ~100 GB remote model pull

## Ranked consumers (do not purge autonomously)

| Location | Size | Classification | Notes |
|----------|------|----------------|-------|
| `/Volumes/CELLICO_FAST/cellico/models/ollama` | ~275G | REQUIRED_ACTIVE | Primary Ollama store (`OLLAMA_MODELS`); includes `qwen3.8:27b` |
| `/Volumes/magicBLACKbox/ollama-models` | ~86G | DUPLICATE / REPRODUCIBLE_CACHE | Symlink target `~/.ollama/models`; verify canonical store before any purge |
| `/Users/byron/projects/active/sids-proteome-validation` | ~42G | REQUIRED_ACTIVE | Scientific dataset lane |
| `/Users/byron/projects/active/xenodisorder` | ~12G | REQUIRED_ACTIVE | Package + assets |
| `/Users/byron/projects/active/overwatch` | ~8G | REQUIRED_ACTIVE | Portfolio truth |
| `/Users/byron/projects/active/hydradg-morning-goldenpath-20260827` | ~1.9G | REPRODUCIBLE_CACHE | Dated HydraDG snapshot |
| `/Users/byron/projects/active/hydradg-cursor-closeout-20260827` | ~1.9G | REPRODUCIBLE_CACHE | Dated HydraDG snapshot |
| `~/Downloads` | ~2.4G | UNKNOWN | Manual review |
| `paper/newinml2026/compute/test-stack/` | <1M | REQUIRED_EVIDENCE | Qwen baseline receipts |

## Never purge during Q38 work

- `qwen3.8:27b` and its digest `22130167…`
- Unique experiment evidence under `paper/newinml2026/`
- HydraDG historical `LOCAL_LIVE_MODEL_RECEIPT.json`

## Safe-to-purge candidates (operator approval required)

1. **Duplicate HydraDG closeout trees** (`hydradg-morning-goldenpath-20260827`, `hydradg-cursor-closeout-20260827`) if superseded by git-tagged eval bundles — potential ~3.8G
2. **Stale build caches** (`node_modules/.cache`, `__pycache__`, `.pytest_cache`) after project-specific confirmation — variable
3. **Downloads** subfolders with known installers/archives — review manually (~2.4G cap)

## Recommended sequence

1. Confirm `OLLAMA_MODELS=/Volumes/CELLICO_FAST/cellico/models/ollama` remains canonical; do not delete from magicBLACKbox until deduped.
2. Archive or delete dated HydraDG duplicate checkouts after operator sign-off.
3. Empty Trash and clear old Xcode/DerivedData if present (not inventoried here).
4. Re-check `df -h /System/Volumes/Data`; target ≥25 GiB free before Daytona Flash-Next pull authorization.

## Cleanup performed this session

**None** — policy requires operator approval; report only.
