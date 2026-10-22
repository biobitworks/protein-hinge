# Preprint prior-work matrix

**Audit:** `AUD-FINAL-TEAM-EVIDENCE-20260829` (prior-work reconciliation extension)  
**Recorded:** 2026-08-30  
**Scope:** Public Zenodo preprints overlapping Protein Hinge NewInML 2026 TEAM track  
**Method:** Independent Zenodo API/metadata verification + terminology-first repo search

Machine copy: `PREPRINT_PRIOR_WORK_MATRIX.csv`

## Summary

| Tier | DOI | Classification | Citation |
| --- | --- | --- | --- |
| Primary | 10.5281/zenodo.21210575 | SHARED_PREEXISTING_INFRASTRUCTURE / PRIOR_METHOD_WORK | **Required** if custody/provenance discussed |
| Secondary | 10.5281/zenodo.21382831 | SHARED_PREEXISTING_INFRASTRUCTURE / PRIOR_METHOD_WORK | **Recommended** if FCG architecture named |
| Optional | 10.5281/zenodo.21829929 | CONTEMPORANEOUS_SUCCESSOR_PRIOR_WORK | **Optional** — only if v4/v5 PASS/FAIL/ABSTAIN grammar cited |
| Background | 10.5281/zenodo.18109862 | METHOD_INFRASTRUCTURE_ONLY | Not required for NewInML manuscript |
| Not cited | 10.5281/zenodo.21830287 | METHOD_INFRASTRUCTURE_ONLY | Antigence governance; imported comparator only |
| Not cited | 10.5281/zenodo.21830361 | FUTURE_DIRECTION_ONLY | Shadow Dogma aging hypothesis |
| Not cited | 10.5281/zenodo.21830386 | NOT_RELEVANT | XenoDisorder disorder scoring |

## Verified candidate records (prompt list)

### A — 10.5281/zenodo.21210575

| Field | Value |
| --- | --- |
| Title | Fractal Custody Objects: route-comparable chain-of-custody for deterministic computational biology and AI-agent provenance |
| Author | Lee, Byron (ORCID 0000-0002-4925-4795) |
| Public date | 2026-07-05 |
| Type | Preprint (open) |
| Status | Published; concept DOI 10.5281/zenodo.21210574 |
| Key terms | Fractal Custody Objects, chain-of-custody, content addressing, Merkle, provenance, reproducibility, computational biology, AI-agent provenance |
| Protein Hinge overlap | **Direct infrastructure overlap** — manuscript §3–6 uses content-addressed custody, SHA-256 manifests, and names “Frozen Custody Graph” without prior-work citation |
| Scope class | SHARED_PREEXISTING_INFRASTRUCTURE; PRIOR_METHOD_WORK |
| Manuscript dependency | Uses custody vocabulary and byte-identity closure described in prior public work |
| Citation required | **Yes** (primary prior-work anchor) |
| Anonymity risk | **Medium** — author-attributed Zenodo record; use third-person citation; do not name operator in anonymous review copy unless camera-ready policy allows |
| Recommended section | Related Work (+ one sentence Reproducibility) |
| Recommended language | Third-person: prior work introduced content-addressed custody for computational biology and AI-agent provenance; Protein Hinge applies related concepts in a bounded biomedical verify-or-abstain workflow |
| Prohibited overclaim | Do not write “we introduce FCO/FCG” or “novel custody framework” without qualifying prior public FCO lineage |

### B — 10.5281/zenodo.21382831

| Field | Value |
| --- | --- |
| Title | Fractal Custody Objects and Graphs for Efficient, Verifiable AI Training and Computational Biology: A Registered Research Protocol… |
| Author | Lee, Byron |
| Public date | 2026-07-15 |
| Type | Preprint (open) |
| Status | Published; references 10.5281/zenodo.21210575 |
| Key terms | FCO, FCG, content addressing, selective replay, reproducibility, computational biology, graph-root reproduction |
| Protein Hinge overlap | **Architecture overlap** — figure pipeline ends in “FCG custody”; repo implements `fcg/store/` Merkle ledger |
| Scope class | SHARED_PREEXISTING_INFRASTRUCTURE; PRIOR_METHOD_WORK |
| Manuscript dependency | Secondary when FCG graph integration is named |
| Citation required | **Recommended** (secondary) |
| Anonymity risk | Medium (same program; third-person OK) |
| Recommended section | Related Work |
| Recommended language | Prior work formalized FCO/FCG as recursively content-addressed custody graphs with selective replay semantics |
| Prohibited overclaim | Do not claim Protein Hinge invented FCG graph construction |

### C — 10.5281/zenodo.21829929

| Field | Value |
| --- | --- |
| Title | Fractal Custody Objects — v4/v5 publication-version package with Vithia companion evidence |
| Author | Lee, Byron |
| Public date | 2026-08-06 |
| Type | Preprint (open); new version of 10.5281/zenodo.21210575 |
| Key terms | PASS, FAIL, ABSTAIN, claim grammar, bounded claims, remediation, clinical/therapeutic claim ceilings |
| Protein Hinge overlap | **Partial semantic overlap** — manuscript uses Abstain terminals and claim ceilings but does not import v4/v5 claim-grammar machinery or Vithia companion |
| Scope class | CONTEMPORANEOUS_SUCCESSOR_PRIOR_WORK |
| Manuscript dependency | **Weak** — Abstain cites Chow/selective prediction; ceilings are team-local |
| Citation required | **Optional only** if team explicitly ties terminal grammar to FCO v4/v5 |
| Anonymity risk | Medium–high (Vithia companion named in record; omit companion from anonymous text) |
| Recommended section | Omit unless team adopts FCO v4 grammar citation |
| Prohibited overclaim | Do not cite merely because it is newer |

## Additional candidates (terminology search)

| PREPRINT_ID | DOI | Overlap class | Scope | Notes |
| --- | --- | --- | --- | --- |
| ANTIGENCE-T0 | 10.5281/zenodo.18109862 | METHOD_INFRASTRUCTURE_ONLY | TEAM_IMPORTED_DEPENDENCY | ANTIGENCE-B4-COMPARATOR experiment; not a Results claim |
| ANTIGENCE-CUSTODY | 10.5281/zenodo.21830287 | METHOD_INFRASTRUCTURE_ONLY | TEAM_IMPORTED_DEPENDENCY | AI-output custody matrix; demo/pitch only |
| SHADOW-DOGMA-V2 | 10.5281/zenodo.21830361 | FUTURE_DIRECTION_ONLY | REMOVE_FROM_TEAM_CLAIMS | SeedGraph/seeds-of-truth vocabulary; aging hypothesis track |
| XENODISORDER | 10.5281/zenodo.21830386 | NOT_RELEVANT | SOLO_RESEARCH_PROGRAM | PTM disorder scoring; no admitted Protein Hinge experiment dependency |

**Excluded (do not add):** HydraDG solo lane, Cloudmer/Vithia model preprints beyond optional 21829929 companion note, unrelated portfolio Zenodo records without admitted experiment linkage.

## Hackathon / presentation provenance (bounded)

| Artifact | Classification | Manuscript use |
| --- | --- | --- |
| `docs/AI_PRESENTATION_BRIEF.json` | PRESENTATION_ONLY | Do not cite in anonymous paper |
| `model_trace/aws_hackathon_context.json` | TEAM_HACKATHON_OUTPUT | Internal provenance only |
| `paper/newinml2026/provenance/HACKATHON_TIMELINE_PROVENANCE.vNext.json` | PUBLIC_PROJECT_METADATA | Operator/team review |
| `paper/newinml2026/sources/biocustody_v0.2.0/` | PRIOR_METHOD_WORK | Predecessor zip; not TEAM_CORE invention |
| Post-hackathon GAP/ClinVar/FASTA successors | POST_HACKATHON_TEAM_WORK | TEAM_CORE / TEAM_CONTRIBUTED per experiment inventory |

Anonymous manuscript should **not** name the hackathon event unless scientifically necessary.

## Discord team-member evidence

| Field | Value |
| --- | --- |
| SOURCE_CLASS | DIRECT_TEAM_MEMBER_COMMUNICATION |
| TRANSPORT | DISCORD |
| PROJECT_SCOPE | TEAM_CONTRIBUTED |
| GitHub crosswalk | `paper/newinml2026/audit/ELVIS_DISCORD_GITHUB_CROSSWALK.json` |
| Authorship | OPERATOR_INFORMATION_REQUIRED — Git cannot establish intellectual authorship |
| Version policy | Preserve Discord upload hash **and** GitHub successor; do not silently replace |

Discord-supplied Elvis materials include stale numbers (24.6%, 51.2%) **prohibited** in canonical Results.
