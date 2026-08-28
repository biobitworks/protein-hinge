# ORIGINAL CONTROLLER PROMPT — PROTOCOL-NML-OVERNIGHT-001

**Persisted:** 2026-08-28 UTC  
**Role:** Unattended execution controller  
**Project:** Protein Hinge → NewInML @ NeurIPS 2026  
**Host:** magicSTUDIObox.local  
**Repo:** /Users/byron/projects/active/protein-hinge  
**Branch:** paper/newinml-fcg-20260828  

## MISSION

Create and execute ONE durable, resumable, multi-wave scientific protocol through all currently eligible NewInML work. Do not require another Cursor prompt between waves. Persist protocol state to disk BEFORE execution. Restart using only repository state + protocol STATE.json.

Continue automatically through COMPLETE / COMPLETE_NEGATIVE / SKIPPED / BLOCKED / OPERATOR_REQUIRED when downstream independent work remains eligible.

HALT only when: custody failure could contaminate evidence; repository authority ambiguous; unauthorized credentials required; all remaining work is operator-only.

Never fabricate missing evidence.

## NON-NEGOTIABLE SCIENCE RULES

1. Historical evidence immutable (Aug 13, Wave 2/3/4 receipts, frozen experiments, thesis versions).
2. Negative results are results (NOT_FOUND, null, missing provenance, OOM, etc.).
3. No retroactive preregistration.
4. Claim ceiling: no therapeutic efficacy, biological rescue, clinical utility, RWE without direct evidence.
5. Infrastructure ≠ scientific validation (SeedGraph, FCO/FCG, MMR, Cloudflare OS, SGLang, CFMO).

## WAVES

- **W00** Bootstrap — freeze state, protocol FCO, opening closure
- **W01** Biocustody external provenance (EXP-002-PROV.1, EXP-003-PROV.1)
- **W02** Terminology, citations, data sources
- **W03** EXP-005 prospective replication (prereg only for readiness)
- **W04** EXP-006 null/negative reproduction
- **W05** Claim-gap repair (core thesis only)
- **W06** EXP-007 SGLang (optional; skip if not required)
- **W07** Thesis + claim audit
- **W08** Evidence-locked manuscript
- **W09** Anonymous submission package
- **W10** Final FCG/SeedGraph closeout

## RESOURCE ROUTER

Local first on magicSTUDIObox (hashing, FCG, SeedGraph, stats, LaTeX). CUDA → Kaggle → Daytona; else BLOCKED_REMOTE_COMPUTE. Hash mismatch → QUARANTINE.

## COMMIT POLICY

No force push. Dedicated commit per material wave. Push origin paper/newinml-fcg-20260828. Verify local HEAD == remote HEAD.

## RELOAD ON CONTEXT TRIM

Do NOT reconstruct from memory. Reload PROTOCOL.yaml, DAG.yaml, STATE.json, this file, PROJECT_CONTROL.yaml, AGENTS.md.

---

*Full controller specification provided in Cursor session initiating PROTOCOL-NML-OVERNIGHT-001 (sections A–V: protocol state machine, waves W00–W10, FCG deltas, final report requirements).*
