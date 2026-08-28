# Known Gaps — NewInML 2026 Bootstrap

**Updated:** 2026-08-28 UTC  
**Branch:** `paper/newinml-fcg-20260828`

## Critical (blocks claim promotion)

| ID | Gap | Evidence | Mitigation |
|----|-----|----------|------------|
| GAP-001 | Abstention summary ≠ ABSTAIN row count in Aug 13 run | `candidates.csv` vs `abstentions.json` | EXP-GAP-ACCOUNTING-001.1 (repair run) |
| GAP-002 | `HACKDAY_STATE.yaml` missing | `ORIGIN_REVIEW.md` | Record UNAVAILABLE; optional recovery from hackday repo |
| GAP-003 | Origin `biocustody.zip` not in repo custody | `ORIGIN_REVIEW.md` | Operator hash zip or EXCLUDED with reason |
| GAP-004 | Live Convoke/Open Targets unwired | `fto/registry_digests.json` | Explicit REFUTED claim; prescripted demo only |

## Experiment / reproducibility

| ID | Gap | Status |
|----|-----|--------|
| EXP-G-001 | G1 28/123 residue verification source not recovered | COMPLETE_NEGATIVE (EXP-002) |
| EXP-G-002 | G2 CNV batch accounting incomplete | NOT_STARTED |
| EXP-G-003 | G3 identity-resolution uses same symbol both sides in prescripted demo | NOT_STARTED |
| EXP-G-004 | Frozen-corpus replication not preregistered | NOT_STARTED |
| EXP-G-005 | Null morphology portable rebuild not verified | NOT_STARTED |
| EXP-G-006 | SGLang CUDA stress not executed | PREREGISTERED |

## Infrastructure

| ID | Gap | Status |
|----|-----|--------|
| INF-001 | SeedGraph live import not executed | PENDING |
| INF-002 | Cloudflare OS upstream not pinned | NOT_PINNED |
| INF-003 | Daytona GPU auth unset | BLOCKED |
| INF-004 | Kaggle quota/GPU not verified | UNKNOWN |
| INF-005 | SGLang not installed locally | EXPECTED (arm64 controller) |

## Attribution / provenance

| ID | Gap | Notes |
|----|-----|-------|
| ATTR-001 | Single git identity all commits | human authorship UNKNOWN |
| ATTR-002 | Elvis handoff JSON not live API | DOCUMENT_ATTRIBUTION only |
| ATTR-003 | OpenAI fan-out outputs MODEL_GENERATED | verify before scientific reuse |

## Semantic / design

| ID | Gap | Notes |
|----|-----|-------|
| SEM-001 | MMR cited but not applied to ranking | design vs implementation |
| SEM-002 | `biocustody.*` schema prefix vs Protein Hinge branding | intentional per ORIGIN_REVIEW |
| SEM-003 | NewInML requirements/template not in repo | UNAVAILABLE until operator supplies |

## Resolved this session

| ID | Resolution |
|----|------------|
| CTRL-001 | No AGENTS.md/PROJECT_CONTROL.yaml on GitHub → proposed on paper branch |
| ACCT-001 | Paper source accounting invariant N_discovered == sum(terminals) → PASS (186) |
