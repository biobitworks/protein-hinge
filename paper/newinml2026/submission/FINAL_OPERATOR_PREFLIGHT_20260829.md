# NewInML 2026 — Final Operator Preflight

Generated during the final corpus-audit window. This file is an operator control artifact, not part of the anonymous reviewer package.

## Canonical repository state

- Canonical branch: `main`
- Verified merge commit after PR #2: `2ba0d923082200b135f17216a1d315a50564c60d`
- PR #2: merged
- PR #1 (`ElvisHan2022/healthomics-lane`): open / not merged; admitted team bytes remain provenance references only

## Live venue deadline authority

The workshop website currently states:

- paper submission date: August 29, 2026
- all deadlines: 11:59 PM AoE

The current OpenReview venue index, checked during this preflight, lists NewInML due:

- `2026-08-30 07:59 UTC`
- California: `2026-08-30 00:59 PDT`

Operational rule: treat the current OpenReview submission-system deadline as the executable cutoff. Preserve the workshop-page/OpenReview discrepancy as a source conflict. Do not delay submission to the later theoretical AoE cutoff.

## Confirmed automated gates already present

At merged-main state, repository evidence contains:

- `dblblindworkshop` manuscript configuration
- NewInML workshop title in `main.tex`
- anonymization receipt: PASS / CLEAN at the earlier team-review candidate
- checklist present and reported complete
- no unresolved LaTeX references in the earlier build receipt
- Type 3 fonts reported false in the earlier build receipt
- G1 successor accounting: `364 = 98 + 266`
- G2 successor accounting: `746 = 364 + 382 + 0`

These checks MUST be rerun on the exact final post-audit PDF; prior receipts are evidence of an earlier candidate, not authorization to skip final verification.

## Known stale or unresolved artifacts to close after Cursor corpus audit

1. Regenerate all submission receipts against the exact final `main` SHA after corpus-audit changes.
2. Replace broad abstract wording `Preregistered audits show` with evidence-class-accurate wording unless the final graph proves every referenced audit preregistered.
3. Synchronize EXP-006 wording from `cached` to reproduced-negative language where supported by the reproduction receipt.
4. In limitations, distinguish historical G1/G2 corpora from contemporary successor corpora (`historical ... not recovered`).
5. Resolve `elyaniv2010`: add authoritative JMLR BibTeX entry if cited, otherwise remove the dangling dependency.
6. Machine-compute `content_pages_excluding_references_and_checklist`; do not infer page compliance from `10 total` alone.
7. Regenerate final Seeds of Truth from repaired/final bytes; no final seed may remain `VERIFY_AFTER_FIXES` or `REPAIR_IN_PROGRESS`.
8. Reconcile final SOFTWARE requirements status from actual final environment/build, not historical PASS/PARTIAL text.
9. Strict final anonymity scan must inspect PDF metadata and recursive supplementary contents and fail closed if required tooling is unavailable.

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
- SOT-008 `+30` TAFAZZIN offset: admit only if row-level proof closes; otherwise keep bounded/withheld
- G2 terminology: do not call all `382/746` silent errors without an independent wrongness predicate

## Exact final artifact gate

Before upload, create one immutable final packet containing at minimum:

- exact final source Git SHA
- exact final PDF SHA-256
- exact content-page count excluding references/checklist
- final anonymization receipt
- final PDF metadata/font receipt
- final citation-closure receipt
- final Seeds-of-Truth graph hash
- final claim-evidence closure state
- author metadata/operator attestation kept outside the anonymous artifact

Only that exact PDF hash should be uploaded to OpenReview.

## Final terminal states

Allowed:

- `READY_FOR_OPERATOR_SUBMISSION`
- `OPERATOR_INFORMATION_REQUIRED`
- `BLOCKED_VALIDATION`

Do not emit `FINAL_SUBMISSION_SEAL=PASS` from an earlier candidate receipt.
