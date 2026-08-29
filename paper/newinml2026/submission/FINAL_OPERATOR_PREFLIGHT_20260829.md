# NewInML 2026 — Final Operator Preflight

Generated during the final corpus-audit window. This file is an operator control artifact, not part of the anonymous reviewer package.

## Canonical repository state

- Canonical branch: `main`
- PR #2: merged
- PR #4: merged (anonymous bundle/checklist seal repair)
- PR #1 (`ElvisHan2022/healthomics-lane`): open / not merged; admitted team bytes remain provenance references only

## Live venue deadline authority

The workshop website currently states:

- paper submission date: August 29, 2026
- all deadlines: 11:59 PM Anywhere on Earth (AoE)

This maps, under strict AoE conversion, to:

- `2026-08-30 11:59 UTC`

The current OpenReview NewInML venue listing now states:

- `2026-08-30 07:59 UTC`
- California: `2026-08-30 00:59 PDT`

Therefore:

- OpenReview closes 4 hours before the strict AoE conversion.
- Treat the live OpenReview cutoff as the executable deadline.
- Preserve the workshop AoE statement as venue-policy context.
- Do not assume the later strict-AoE timestamp can be used after the OpenReview form closes.

The previously recorded `2026-08-29 08:59 UTC / 2026-08-29 01:59 PDT` cutoff is `SUPERSEDED_INCORRECT` and must not be used by submission automation or operator checklists.

## Confirmed automated gates already present

Repository evidence contains:

- `dblblindworkshop` manuscript configuration
- NewInML workshop title in `main.tex`
- anonymization receipt: PASS / CLEAN at the latest audited candidate
- checklist present
- PR #4 strips the checklist instruction block from the built submission while retaining the checklist questions/answers/guidelines
- unresolved-reference/citation gate in final-seal CI
- Type 3 font gate in final-seal CI
- recursive anonymous reviewer-bundle identity scan
- G1 successor accounting: `364 = 98 + 266`
- G2 successor accounting: `746 = 364 + 382 + 0`
- final corpus audit: `PASS_WITH_OPERATOR_GATES`

These checks MUST pass on the exact final submission commit. Prior receipts are historical evidence only.

## Remaining machine-closeout items

1. Complete any final read-only corpus delta explicitly requested by the operator (SeedGraph/Overwatch/FCO lineage stores); do not start new experiments.
2. Complete substantive table/figure FCO mapping or explicitly classify non-propositional visual elements.
3. Audit checklist answers against reviewer-visible support; weaken `Yes` to `No`/`N/A` rather than overclaiming.
4. Run the final-seal CI on the exact final `main` SHA after all control/manuscript changes.
5. Use only the exact CI-generated `newinml-anonymous-paper` and, if enabled by the live form, the same-run anonymous reviewer bundle.
6. Capture `FINAL_CI_OPERATOR_RECEIPT.json` from that same run.
7. Verify the live OpenReview form's supplementary-material field before deciding whether to upload the anonymous verification ZIP.

## Elvis review integration

Elvis's suggested material is evidence input, not an automatic manuscript replacement. Final projection must preserve these audit decisions:

- no structure-prediction execution claim unless an execution receipt exists
- SOT-008 `+30` TAFAZZIN offset remains NOT_ESTABLISHED unless row-level proof closes
- G1 mismatch interpretation remains bounded to the supported one-gene/canonical-sequence context
- G2 `382/746` remains multi-gene/CNV exclusion / unsupported gene-specific attribution, not a blanket silent-error rate without an independent wrongness predicate
- rhetorical `honest zero` / `dominant failure mode` language remains removed or weakened
- historical stale values remain provenance-only, not current result values

## Reviewer-facing FCO / FCG verification

The final paper PDF itself should be treated internally as an FCO leaf with exact SHA-256 content identity. The anonymous reviewer bundle uses a narrower DRM-free submission-seal profile:

- SHA-256 payload leaf hashes
- canonical payload manifest
- SHA-256 manifest seal
- offline `VERIFY.md` / `verify.py`

Unless separately instantiated in the exact reviewer bundle, do not claim that this anonymous submission profile is Ed25519-signed, Merkle/MMR-backed, or fully FCO-v3 conformant.

Do not include GitHub repository URLs, searchable Git SHAs, contributor identities, Discord handles, emails, local paths, hostnames, or private graph metadata in the anonymous bundle.

If NewInML does not expose a supplementary-material field, do not link the public repository from the anonymous PDF. Retain the anonymous verification bundle for organizer request and/or camera-ready release.

## Operator-only gates before OpenReview submission

Final submission seal remains `OPERATOR_INFORMATION_REQUIRED` until all intended paper authors are confirmed.

Required per intended author:

- publication name
- author order
- OpenReview profile ready
- NewInML eligibility confirmed
- authorship consent

Also resolve:

- prior-work anonymity/self-citation strategy for the review copy
- contributor-only vs paper-author status for hackathon participants

## Exact final artifact gate

Before upload, require one successful final-seal CI run on the exact final `main` SHA and record:

- exact internal final source Git SHA
- exact anonymous PDF SHA-256 and byte count
- machine-recorded page-limit evidence
- final anonymization receipt
- final PDF metadata/font receipt
- final citation-closure receipt
- final Seeds-of-Truth graph hash
- final claim-evidence closure state
- anonymous payload manifest + seal receipt
- author metadata/operator attestation kept outside the anonymous artifact

Only the exact PDF bytes identified by the same-run CI receipt should be uploaded to OpenReview.

## Final terminal states

Allowed before upload:

- `READY_FOR_OPERATOR_SUBMISSION`
- `OPERATOR_INFORMATION_REQUIRED`
- `BLOCKED_VALIDATION`

After upload, record OpenReview submission/forum ID, submission timestamp, and exact uploaded PDF SHA-256. Only then may `FINAL_SUBMISSION_SEAL=PASS` be emitted.
