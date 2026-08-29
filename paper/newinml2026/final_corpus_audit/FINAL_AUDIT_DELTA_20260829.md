# NewInML 2026 — Final Audit Delta

**Purpose:** successor audit over the previously recorded `FINAL_CORPUS_AUDIT=PASS_WITH_OPERATOR_GATES`. Historical audit artifacts are not overwritten.

## Current authority boundary

- Current audited `main` before this repair branch: `89e56b229553b2294e46c78ac4118e785875b507`.
- CI run `33237727026` successfully built the anonymous paper and produced a valid SHA-256 manifest seal.
- That CI paper is clean as a main-paper candidate, but the reviewer ZIP from that run is **not safe to submit as supplementary material** because it contains a stale historical build receipt with an unredacted 40-hex Git object identity and contradictory build metadata.
- The committed `OPENREVIEW_UPLOAD_PACKET.md` and `FINAL_SUBMISSION_FCO_RECEIPT.json` describe the local Studio build, not the later CI-authoritative PDF. They are historical/local reproducibility receipts, not the final OpenReview upload authority.

## Submission-critical defects found

### D-001 — Checklist instruction block leaked into PDF

The rendered PDF contains the NeurIPS checklist instruction text, including `Delete this instruction block`, despite the template explicitly requiring that block to be removed.

**State before repair:** FAIL_SUBMISSION_CONFORMANCE  
**Repair:** build-time stripping of only `%%% BEGIN INSTRUCTIONS %%%` through `%%% END INSTRUCTIONS %%%`, retaining the checklist heading/questions/answers/guidelines.  
**Closure requirement:** final CI extracted PDF must not contain `Delete this instruction block`.

### D-002 — Anonymous reviewer ZIP contains source identity

`payload/receipts/BUILD_RECEIPT.json` in CI run `33237727026` contains a standalone 40-character Git SHA. It also reports an obsolete one-page PDF SHA and `font_embed_check=PARTIAL`.

This contradicts `FCO_SEAL.json` field `git_identity_in_anonymous_bundle=false`.

**State before repair:** FAIL_ANONYMOUS_SUPPLEMENT  
**Repair:** remove historical local build receipts and duplicate PDF copies from the anonymous export; generate an anonymous CI runtime receipt without Git/source identity; block standalone 40-hex Git identities recursively.  
**Closure requirement:** post-construction anonymous bundle scan PASS.

### D-003 — Multiple competing “final” receipts

Committed local receipt:

- source: `a81f331989cb014508c76a4b9647cf4e6ba53ed5`
- PDF: `b0812833...`

CI source binding from run `33237727026`:

- source: `89e56b229553b2294e46c78ac4118e785875b507`
- PDF: `997a234a...`
- manifest: `04488246...`

**State:** AUTHORITY_CONFLICT  
**Resolution rule:** for OpenReview, only the latest successful final-seal CI runtime receipt after all repairs is authoritative. Local receipts remain reproducibility evidence only.

## Reviewer/checklist semantic audit

The following checklist answers require human/Cursor reconciliation before final freeze; do not silently preserve a `Yes` when the reviewer-visible paper/supplement does not establish it.

1. **Experimental result reproducibility** — current `Yes` says manifests and preregistrations are in supplementary material, but the current anonymous subset does not contain preregistrations or full G1/G2/EXP-006 reproduction material. Either expand the anonymous supplement or answer `No` with the exact bounded reproduction scope.
2. **Experiments compute resources** — current `Yes` points to compute receipts, while the reviewer-visible paper does not give per-experiment worker/memory/time detail. Prefer `No` unless those details are added to the anonymous paper/supplement.
3. **Licenses for existing assets** — current `Yes` says assets are credited in bibliography/provenance, but the checklist asks that licenses/terms be explicitly mentioned. Verify ClinVar/UniProt and relevant code/data terms in reviewer-visible material; otherwise answer `No` with a bounded justification.
4. **Declaration of LLM usage** — current `Yes` says LLM usage is disclosed in the Reproducibility section, but the current PDF section does not contain that disclosure. Either add one bounded sentence (LLMs assisted orchestration/drafting but were not measurement authorities) or use the checklist answer appropriate under the venue wording.
5. **Broader impacts** — current `N/A` means no societal impact. Given the biomedical evidence-pipeline context, confirm this is intended; a short bounded benefit/risk sentence may be more defensible.

These are review-integrity issues, not invitations to strengthen scientific claims.

## Table/figure FCO closure

`FINAL_TABLE_FCO_MAP.jsonl` maps only three numeric cells (G1 N, G2 N, EXP-006 N) even though the primary table contains multiple scientific row/column values (`Experiment`, `Unit`, `Guard`, `Condition`, `N`, `Ceiling`). Therefore:

`FULL_TABLE_CELL_FCO_CLOSURE = NOT_ESTABLISHED`

`FINAL_FIGURE_FCO_MAP.jsonl` maps the architecture figure as one aggregate element. This is adequate for a coarse architecture-only ceiling but is not element-level closure of labels/arrows/caption clauses.

For the user's requested exhaustive FCO treatment, generate v2 maps covering every substantive table cell and figure/caption element, or explicitly declare decorative/non-claim cells excluded by rule.

## Corpus exhaustiveness audit

The previous final-corpus freeze is useful but is **not exhaustive over all requested sources**:

- Included roots: Protein Hinge, SeedGraph, Overwatch, HydraDG, Ollarma, GettingScienceDone.
- Omitted from the freeze despite direct FCO/FCG lineage relevance: standalone `biobitworks/biocustody` and `biobitworks/fractal-custody-objects`.
- Live SeedGraph Neo4j inventory recorded only total node count; Protein-Hinge-scoped search is explicitly `DEFERRED_LOCAL_MANIFEST_IMPORT`.
- `DATABASE_QUERY_LEDGER.jsonl` contains only `MATCH (n) RETURN count(n)` for SeedGraph.
- Overwatch crosswalk is explicitly `PARTIAL` / deferred to operator.
- OrbStack inventory found `prothub`, `fractal-waves-db`, and `overwatch-db`, but no Protein-Hinge relevance queries are recorded for them.
- Publication database inventory records only `references.bib`; it does not establish that all local publication stores/caches were queried.

Therefore:

`CORPUS_EXHAUSTIVENESS = NOT_ESTABLISHED`

This does **not** invalidate the bounded manuscript results. It means the audit must not claim that every potentially relevant local knowledge atom has been exhausted.

### Minimum deadline-safe corpus closure

Run read-only, relevance-scoped searches only; do not start new experiments:

- SeedGraph Neo4j: Protein Hinge, NewInML, known experiment IDs, SOT IDs, relevant content hashes, TAZ/TAFAZZIN, G1/G2/G3, EXP-006.
- Overwatch DB/repo: Protein Hinge project state, experiment/source pointers, stale/contradictory claim state.
- `prothub` and `fractal-waves-db`: exact Protein-Hinge identifiers/known hashes only; if no hits, record `NO_RELEVANT_HITS`.
- standalone BioCustody/FCO repos: terminology/prior-work provenance only; do not import unrelated folding/biosecurity claims into this paper.
- publication stores: inventory and query only if present; official publisher metadata remains citation authority.

Any new contradictory atom outranks a new supportive atom.

## Prior-work/FCO terminology boundary

Standalone FCO prior work describes stronger constructions including domain-separated Merkle schemes, signatures, and/or MMR semantics. The anonymous reviewer bundle currently uses a simpler `sha256(manifest_bytes)` submission profile.

Do not claim that the anonymous bundle is FCO v3, signed, Merkle, or MMR conformant unless those exact constructions are present. It is safe to describe it as a **DRM-free anonymous submission seal/profile** and to represent the exact PDF bytes as an FCO leaf in the internal FCG.

## Scientific blocks that must remain blocks

- SOT-008 `+30` TAFAZZIN offset: `NOT_ESTABLISHED` unless row-level proof closes.
- SOT-014 historical measurement-correction chain: retain bounded historical/supersession status unless exact row lineage closes.
- G2 `382/746`: multi-gene/CNV exclusion / unsupported gene-specific attribution, not a blanket silent-error rate.
- No structure-prediction execution claim.
- No therapeutic efficacy, clinical utility, biological rescue, treatment recommendation, population biomedical error-rate, or RWE claim.
- EXP-005 remains not executed.

## Required terminal state before upload

Main paper can become `READY_FOR_OPERATOR_SUBMISSION` only after:

1. repaired final CI run passes;
2. exact CI PDF visually reviewed;
3. checklist semantic answers reconciled;
4. CI runtime receipt names one authoritative paper hash;
5. current anonymous reviewer bundle contains no Git/source identity;
6. author/OpenReview/eligibility/consent operator gates are complete.

`FINAL_SUBMISSION_SEAL=PASS` remains prohibited until the exact OpenReview submission ID/receipt is captured.
