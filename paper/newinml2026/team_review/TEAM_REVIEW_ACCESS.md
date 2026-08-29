# Team Review Access — Local + GitHub

**Purpose:** Team members pull review artifacts from GitHub; magicPRObox holds the same tracked bytes locally for operator upload and offline review.

## Canonical remote

```bash
git clone https://github.com/biobitworks/protein-hinge.git
cd protein-hinge
git checkout main
git pull origin main
```

**Current `main`:** check `PROJECT_CONTROL.yaml` → `current_state.CANONICAL_PAPER_SOURCE_SHA`

## Team review entry points (GitHub = local for tracked files)

| Surface | Path |
| --- | --- |
| Human start | `TEAM_HANDOFF_20260829/00_START_HERE_HL.md` |
| Machine index | `TEAM_HANDOFF_20260829/00_START_HERE_ML.json` |
| Team review packet | `paper/newinml2026/team_review/TEAM_REVIEW_PACKET.md` |
| Identified review PDF | `paper/newinml2026/team_review/main_review.pdf` |
| Claim closure | `paper/newinml2026/team_review/CLAIM_EVIDENCE_MATRIX.vFinal.csv` |
| Seeds of truth | `paper/newinml2026/team_review/SEEDS_OF_TRUTH.vFinal.json` |
| Per-member framework | `paper/newinml2026/team_review/members/MEMBER_*/` |
| Approval status | `paper/newinml2026/team_review/TEAM_APPROVAL_STATUS.md` |

## Submission draft (anonymous — for OpenReview)

| Surface | Path |
| --- | --- |
| Probox review index | `paper/newinml2026/submission/probox_review/PROBOX_REVIEW_INDEX.md` |
| Upload PDF | `paper/newinml2026/submission/probox_review/NewInML2026_ProteinHinge_ANONYMOUS_SUBMISSION.pdf` |
| CI authority | `paper/newinml2026/submission/probox_review/FINAL_CI_OPERATOR_RECEIPT.json` |
| Reviewer bundle (optional) | `paper/newinml2026/submission/probox_review/newinml_anonymous_reviewer_bundle.zip` |

## Evidence ledger (shared via git)

The FCG custody store is **committed**, not local-only:

- `fcg/store/` — content-addressed evidence atoms (small; fully in repo)
- Large upstream parquets are **not** vendored; re-fetch via manifests under `paper/newinml2026/`

## Local-only / generated (gitignored)

Do not expect these on GitHub:

- `paper/newinml2026/submission/dist/`
- `paper/newinml2026/submission/seedgraph_delta/content_store/`
- `.env`, credentials

## Verify you have the submission PDF

```bash
shasum -a 256 paper/newinml2026/submission/probox_review/NewInML2026_ProteinHinge_ANONYMOUS_SUBMISSION.pdf
# expect: ded8f72e299642a7f8ed4fc0f5318b1e961c413b5640acaa6cda6d65880448ab
```

Compare against `FINAL_CI_OPERATOR_RECEIPT.json` → `paper_pdf_sha256`.

## Team approval

Per-member `REVIEW_DECISION.template.json` files under `members/MEMBER_*/` await operator-attested human decisions. See `TEAM_APPROVAL_STATUS.md`.
