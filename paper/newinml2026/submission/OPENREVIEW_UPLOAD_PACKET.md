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

## Deadline authority

- Official CFP date: `2026-08-29`
- Official CFP policy: `23:59 AoE`
- Strict AoE conversion: `2026-08-30 11:59 UTC`
- Current live OpenReview deadline: `2026-08-30 07:59 UTC`
- California: `2026-08-30 00:59 PDT (America/Los_Angeles)`
- OpenReview is 4 hours earlier than strict AoE.

**Operational rule:** use the live OpenReview cutoff (`2026-08-30 07:59 UTC / 00:59 PDT`) as the executable submission deadline. Preserve the later strict-AoE value as contextual CFP policy, not as permission to submit after the OpenReview form closes.

The previously recorded `2026-08-29 08:59 UTC / 01:59 PDT` OpenReview cutoff is superseded and must not be used.

## Post-upload closure

Record the OpenReview submission/forum ID, submission timestamp, and the exact uploaded PDF SHA-256. Only then may `FINAL_SUBMISSION_SEAL=PASS` be emitted.
