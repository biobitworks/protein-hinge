# REQ-007 Operator Checklist — OpenReview / Author Attestation

**Status:** `REQ-007 = OPERATOR_PENDING` until human operator completes and signs receipt.

Automated agents must **not** fill attestation fields without operator evidence.

## Pre-submission checks (operator)

- [ ] OpenReview account accessible for intended submission profile
- [ ] Intended author profile active and selectable
- [ ] Author name spelling matches official affiliation records
- [ ] Current affiliation correct and complete
- [ ] Conflict-of-interest fields complete per venue policy
- [ ] Co-author list complete (if applicable after deanonymization phase)
- [ ] NewInML 2026 workshop page reachable; CFP/requirements reviewed
- [ ] All intended authors satisfy NewInML eligibility criteria
- [ ] Submission deadline and timezone cutoff verified on live site
- [ ] Anonymous PDF contains no author names, affiliations, or acknowledgments
- [ ] Anonymous supplement contains no identifying URLs, emails, or paths
- [ ] PDF metadata scrubbed (Title/Author/Producer fields)
- [ ] Figure filenames contain no identifying strings

## Evidence to attach in receipt

Record UTC timestamp, OpenReview username (non-public storage if needed), screenshot hash or operator note for each checked item.

## Terminal states

| State | Meaning |
| --- | --- |
| OPERATOR_PENDING | Checklist not yet attested |
| PASS | All items attested with evidence |
| FAIL | Blocking item failed verification |

## Related artifacts

- `submission/REQ007_OPERATOR_RECEIPT_TEMPLATE.json`
- `submission/ANONYMIZATION_SCAN.json` (REQ-002)
- `submission/SUBMISSION_READINESS.json`
