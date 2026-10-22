# Manuscript claim audit

Against **canonical** `paper/newinml2026/manuscript/main.tex` (SHA-256 `fba9139d278665fefcfad8b69d2203585dbd9c3714e26ec8a02839a0ee393dec`). Elvis `paper/main.tex` is a separate, unmerged manuscript.

CSV: `CLAIM_EVIDENCE_AUDIT.csv`.

## Attention items from the audit brief

### 1. Silent-error language for G2

**Canonical:** SUPPORTED_EXACT that 382 exclusions are **not** a validated silent-error rate (`main.tex` Results G2).  
**Elvis:** CONTRADICTED relative to team claim ceiling (uses “silently wrong” / 51.2%). Not merged.

### 2. G1 generality despite one-gene concentration

Frozen replay: **16/16 residue mismatches are TAFAZZIN**. Canonical paper reports 16 as an accounting terminal and does **not** claim a gene-general silent-error rate. Elvis 14.0% over 114 naive emits would still be TAFAZZIN-concentrated for the mismatch numerator. Classification: canonical SUPPORTED_BOUNDED; Elvis overclaim if read as general.

### 3. “Six evidence types” vs table contents

**NOT_PROPOSITIONAL** in canonical package. Table 1 is experiment terminals (GAP, G3, G1/G2 successor/historical, morphology). There is no six-type evidence table.

### 4. Three versus five verdict states

**NOT_PROPOSITIONAL** in canonical package. Architecture figure is Admit | Abstain plus claim ceilings. Not a 3-of-5 or 5-state verdict table.

### 5. Merkle / committed-byte re-derivation

**SUPPORTED_BOUNDED.** Canonical claims SHA-256 leaf + manifest recomputation. It does **not** construct a Certificate Transparency Merkle audit tree. Elvis cites RFC 6962 more strongly than the admitted NewInML text.

### 6. Structure-prediction-tool experiment

**SUPPORTED_EXACT** that none is in admitted evidence (Limitations). Elvis methods language about a folding tool accepting a wrong FASTA is **CONTRADICTED** as an executed experiment.

### 7. “All 98 verified position by position”

**SUPPORTED_BOUNDED.** Emission requires `seq[pos-1] == named WT residue`. That is the guard predicate, not an independent biochemical verification of all 98.

### 8. +30 offset

**NOT_ESTABLISHED** (SOT-008). Not in canonical Results. This audit did not invent a new offset study.

### 9. Two runs a day apart

**INSUFFICIENT** as a designed experiment. Capture timestamps exist (ClinVar 2026-08-25; successor receipts 2026-08-28). Canonical paper does not claim a two-run reliability study.

### 10. Missing 100 records

**SUPPORTED_BOUNDED.** Mechanism recovered in frozen `clinvar_provenance.json` (TAFAZZIN 100 IDs, XML 16 503 275 bytes vs 10 MB JSON). Historical 742→642 corpus **not** reproduced.

### 11. 24.6% → 14.0%

**SUPPORTED_BOUNDED** as a **superseded Elvis/SOT** correction (frameshift classified before residue check). **Absent** from canonical Results (by design).

### 12. “We introduce / we show / we built”

Canonical voice is “we present / we frame / audits show.” **SUPPORTED_BOUNDED** as team-paper process language. Git authors are attribution evidence, not proof of human authorship. PR #1 scientific bytes are hash-admitted, not merged.

### 13. External/team-member PR attribution

PR #1 classified OPEN_HASH_ADMITTED_ONLY. Successor G1/G2 numbers **are** in the canonical paper; the Elvis silent-error manuscript is **not**. That split is correct and should stay explicit.

## Elvis vs canonical vs CI PDF

| Surface | Role |
| --- | --- |
| A. `biobitworks` `main.tex` | Canonical NewInML projection |
| B. Elvis `healthomics-lane` `paper/main.tex` | TEAM_CONTRIBUTION_NOT_MERGED; silent-error framing; generated tables |
| C. Local team-review PDF | Same SHA-256 as CI anonymous submission PDF `ded8f72e…` (Studio copies checked) |
| D. CI run 33264903580 | Authoritative anonymous PDF; `headSha=bc4b0d5` |

Live Elvis `main.tex` SHA-256 `28e16ac8…` ≠ admitted snapshot `e8e631d5…` (added `\date{}` hygiene). **Do not merge PR #1 from this audit.**
