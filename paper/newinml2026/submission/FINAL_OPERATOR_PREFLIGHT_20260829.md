# NewInML 2026 — Final Operator Preflight

Generated during the final corpus-audit window. This file is an operator control artifact, not part of the anonymous reviewer package.

## Canonical repository state

- Canonical branch: `main`
- PR #2: merged
- PR #1 (`ElvisHan2022/healthomics-lane`): open / not merged; admitted team bytes remain provenance references only

## Live venue deadline authority

The workshop website currently states:

- paper submission date: August 29, 2026
- all deadlines: 11:59 PM AoE

The current OpenReview NewInML venue listing states:

- `2026-08-29 08:59 UTC`
- California: `2026-08-29 01:59 PDT`

Operational rule: treat the live OpenReview submission-system cutoff as authoritative for execution and submit before 01:59 PDT. Preserve the workshop-page AoE wording as a source conflict. Do not rely on the later theoretical AoE conversion.

Correction note: an earlier preflight draft incorrectly recorded an Aug. 30 OpenReview cutoff. That value is RETRACTED and must not be used by any submission automation or operator checklist.

## Confirmed automated gates already present

Repository evidence contains:

- `dblblindworkshop` manuscript configuration
- NewInML workshop title in `main.tex`
- anonymization receipt: PASS / CLEAN at the latest audited candidate
- checklist present and reported complete
- no unresolved LaTeX references in the earlier build receipt
- Type 3 fonts reported false in the earlier build receipt
- G1 successor accounting: `364 = 98 + 266`
- G2 successor accounting: `746 = 364 + 382 + 0`
- final corpus audit: `PASS_WITH_OPERATOR_GATES`

These checks MUST be rerun on the exact final post-audit PDF; prior receipts are evidence of earlier candidates, not authorization to skip final verification.

## Remaining machine-closeout items

1. Project the final audited Seeds of Truth into canonical `main.tex` without importing NOT_ESTABLISHED claims.
2. Replace broad abstract wording `Preregistered audits show` with evidence-class-accurate wording unless the final graph proves every referenced audit preregistered.
3. Synchronize EXP-006 wording from `cached` to reproduced-negative language where supported by the reproduction receipt.
4. In limitations, distinguish historical G1/G2 corpora from contemporary successor corpora (`historical ... not recovered`).
5. Resolve `elyaniv2010`: add authoritative JMLR BibTeX entry if cited, otherwise remove the dangling dependency.
6. Machine-compute and record the content-page gate; do not infer compliance from total pages alone.
7. Regenerate final submission receipts against the exact final source bytes.
8. Strict final anonymity scan must inspect extracted PDF text, PDF metadata, filenames, and recursive supplementary contents and fail closed if required tooling is unavailable.

## Elvis review integration

Elvis's suggested material is evidence input, not an automatic manuscript replacement. Final projection must preserve these audit decisions:

- no structure-prediction execution claim unless an execution receipt exists
- SOT-008 `+30` TAFAZZIN offset remains NOT_ESTABLISHED unless row-level proof closes
- G1 mismatch interpretation remains bounded to the supported one-gene/canonical-sequence context
- G2 `382/746` remains multi-gene/CNV exclusion / unsupported gene-specific attribution, not a blanket silent-error rate without an independent wrongness predicate
- rhetorical `honest zero` / `dominant failure mode` language remains removed or weakened
- historical stale values remain provenance-only, not current result values

## Reviewer-facing FCO / FCG verification

The final paper PDF itself should be treated as an FCO leaf with an exact SHA-256 content identity. A reviewer verification bundle, if the NewInML OpenReview form exposes a supplementary-material upload, should be a self-contained anonymous ZIP containing:

- the exact anonymous PDF
- anonymous reproduction subset
- anonymous claim/evidence map
- SHA-256 payload manifest
- FCO seal receipt
- offline `VERIFY.md` and `verify.py`

The seal is DRM-free. It is content addressing and manifest closure, not encryption, licensing, or access control. "Unsealing" means recomputing all payload hashes and the manifest hash and confirming closure.

Do not include GitHub repository URLs, Git SHAs that can trivially deanonymize the authors, contributor identities, Discord handles, emails, local paths, or private graph metadata in the anonymous bundle.

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

Before upload, create one immutable final packet containing at minimum:

- exact internal final source Git SHA
- exact anonymous PDF SHA-256
- machine-recorded page-limit evidence
- final anonymization receipt
- final PDF metadata/font receipt
- final citation-closure receipt
- final Seeds-of-Truth graph hash
- final claim-evidence closure state
- anonymous FCO payload manifest + seal receipt
- author metadata/operator attestation kept outside the anonymous artifact

Only that exact PDF hash should be uploaded to OpenReview.

## Final terminal states

Allowed:

- `READY_FOR_OPERATOR_SUBMISSION`
- `OPERATOR_INFORMATION_REQUIRED`
- `BLOCKED_VALIDATION`

Do not emit `FINAL_SUBMISSION_SEAL=PASS` from an earlier candidate receipt.
