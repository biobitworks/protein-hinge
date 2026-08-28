# REQ-007 Operator Packet

See `REQ007_OPERATOR_CHECKLIST.md` for the full attestation checklist.

## Status

`OPERATOR_REQUIRED` — automated agents cannot self-attest OpenReview profile, eligibility, or final submission confirmation.

## Exact operator steps

1. Log into OpenReview with the intended submission profile.
2. Verify author name, affiliation, and conflict fields match current records.
3. Confirm all co-authors satisfy NewInML 2026 eligibility criteria.
4. Verify submission deadline and timezone on the live workshop page.
5. Open `paper/newinml2026/manuscript/main_smoke.pdf` and confirm no identifying metadata in PDF properties.
6. Confirm anonymous supplement under `submission/anonymous/` contains no identifying strings.
7. Complete NeurIPS checklist answer macros in `manuscript/checklist.tex` (currently TODO placeholders).
8. Fill `REQ007_OPERATOR_RECEIPT_TEMPLATE.json` with attestation evidence (keep private emails out of public commits if needed).
9. Upload anonymous PDF + supplement to OpenReview when all REQ items PASS.

## Related receipts

- `submission/ANONYMIZATION_RECEIPT.json` — REQ-002 PASS
- `submission/SUBMISSION_READINESS.json` — terminal PARTIAL until REQ-007/008 attested
