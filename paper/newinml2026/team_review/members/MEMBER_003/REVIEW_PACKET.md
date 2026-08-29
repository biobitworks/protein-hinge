# Review Packet — MEMBER_003

**TEAM_ROSTER=OPERATOR_REQUIRED** — replace MEMBER_ID with confirmed roster.

- Source Git SHA: `ab23f43df3e494fe3abbf32d8805081461112cef`
- Candidate PDF SHA256: `94c9e1f9c65c75443a907f6b22792f98f9a0824cc029442a4a302ab12c6de305`
- Manuscript: Verify-or-Abstain Evidence Pipelines

## Scope
Team core experiments only. Solo/future lanes excluded.

## Verification
```bash
git rev-parse HEAD
sha256sum paper/newinml2026/submission/NewInML2026_ProteinHinge_ANONYMOUS_FINAL_CANDIDATE.pdf
python3 db/build_db.py
node site/verify_test.js
```

## Decision required
Approve exact bytes or request changes. AI MUST NOT set APPROVED.
