# OpenReview Upload Packet

**Authority rule:** this committed file is an operator procedure, not a hash authority. Final hashes must come from the latest successful `NewInML final seal` GitHub Actions run after all submission repairs. Use the internal artifact `FINAL_CI_OPERATOR_RECEIPT.json` and upload the exact `newinml-anonymous-paper` artifact bytes from that same run.

## Paper

- Artifact: `newinml-anonymous-paper`
- Required source: latest successful final-seal CI run on the exact submission commit
- Required SHA-256: read from `FINAL_CI_OPERATOR_RECEIPT.json`
- Do **not** substitute an earlier local Studio PDF merely because it passes local reproducibility gates.

## Supplement

- OpenReview field: `OPERATOR_VERIFY_LIVE_FORM`
- If the live NewInML form exposes a supplementary-material field, use the `newinml-anonymous-reviewer-bundle` artifact from the **same** successful CI run.
- Verify the inner deterministic ZIP SHA-256 against `FINAL_CI_OPERATOR_RECEIPT.json` / `REVIEWER_BUNDLE.sha256`.
- Do not confuse the GitHub Actions artifact-wrapper digest with the inner deterministic reviewer ZIP digest.
- If the live form has no supplement field, upload no repository/GitHub link merely to expose the verifier.

## Author metadata

`OPERATOR_INFORMATION_REQUIRED`

Confirm intended author list/order, OpenReview profiles, NewInML eligibility, and authorship consent before submission.

## Deadline

- `2026-08-29 08:59 UTC`
- `2026-08-29 01:59 PDT (America/Los_Angeles)`

## Post-upload closure

Record the OpenReview submission/forum ID, submission timestamp, and the exact uploaded PDF SHA-256. Only then may `FINAL_SUBMISSION_SEAL=PASS` be emitted.
