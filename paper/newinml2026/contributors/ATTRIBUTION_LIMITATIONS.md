# Attribution Limitations — NewInML 2026

**Generated:** 2026-08-28 UTC on magicSTUDIObox.local  
**Branch:** `paper/newinml-fcg-20260828` @ `94f8949f1bbcb63d8e80baadd0c5f380f01b9f92`

## Core limitation

Git author/committer metadata, PR metadata, and document headers are **attribution
evidence**. They are not cryptographic proof of human authorship, intent, or
original creation time independent of the repository.

## Contributors discovered (git history)

| Identity | Email | Commits | Attribution class |
|----------|-------|---------|-------------------|
| biobitworks | byron@biobitworks.com | 8 | GIT_AUTHOR_METADATA + GIT_COMMITTER_METADATA |

All 8 commits on `main` through `94f8949f` share identical author and committer
metadata. Human authorship evidence class: **UNKNOWN** (no independent signature).

## Named external contributions (document-attributed)

| Name | Role | Evidence class | Source |
|------|------|----------------|--------|
| Elvis | Convoke access holder; GAP prescripted demo handoff | DOCUMENT_ATTRIBUTION | `docs/ELVIS_COMPONENT.md`, `gap/elvis_prescripted_demo.json`, `docs/GAP_LANE_SPEC.md` §3 |
| OpenAI models | Subagent fan-out execution (bounded demo) | MODEL_GENERATED + PROBABILISTIC_MODEL_OUTPUT | `fco/agent_fanout/20260813Tfanout-elvis/` |
| Local Ollama models | Inventoried runtimes, not scientific generators | TOOL_RUNTIME | `model_trace/model_trace.json` |

## AI / model-generated material

The OpenAI fan-out lane (`scripts/run_openai_fanout.py`, FCOs under
`fco/agent_fanout/20260813Tfanout-elvis/`) produces **MODEL_GENERATED** outputs
custodied as FCOs. These outputs must not be promoted above their claim ceiling
without independent verification experiments.

## Origin artifact ambiguity

`ORIGIN_REVIEW.md` records receipt of `biocustody.zip` (BioCustody branding) later
published as `protein-hinge`. The zip is **UNAVAILABLE** under repo custody
(local path `/Users/byron/Downloads/biocustody.zip` not hashed in this bootstrap).
Provenance chain from zip → repo relies on operator assertion in `ORIGIN_REVIEW.md`
(**DIRECT_HUMAN_ASSERTION** via document, not independently verified here).

## Preserved disagreements / ambiguities

1. **Internal schema prefix `biocustody.*`** retained while visible branding is
   Protein Hinge — intentional per `ORIGIN_REVIEW.md`; may confuse external readers.
2. **Elvis Convoke wiring** — registry lists `LISTED_NOT_WIRED`; prescripted GAP
   demo uses handoff JSON, not live Convoke MCP responses.
3. **Hackday dependency gap** — `HACKDAY_STATE.yaml` referenced by ingest builders
   but absent; rebuild-from-source completeness is **UNAVAILABLE**.
4. **GAP abstention accounting mismatch** — historical `abstentions.json` reports
   zero while `candidates.csv` contains ABSTAIN rows; preserved as contradiction
   evidence pending EXP-GAP-ACCOUNTING-001.1.

## Operator guidance

When promoting claims, require at least one non-metadata evidence class where
 feasible: `DETERMINISTIC_COMPUTATION`, `VERIFIED_EMPIRICAL_RESULT`, or
`DIRECT_HUMAN_EVIDENCE` with explicit assertion record.

Do not collapse `GIT_*_METADATA` into `DIRECT_HUMAN_ASSERTION`.
