# Preprint prior-work suggestions (review only)

**Status:** REVIEW_ONLY — no `main.tex` edits in this audit step  
**Audit:** prior-work reconciliation extension on `AUD-FINAL-TEAM-EVIDENCE-20260829`

## Boundary rule

| Class | Meaning for Protein Hinge TEAM track |
| --- | --- |
| TEAM_CORE | GAP repair, G1/G2/G3 evaluations, EXP-006 null, claim ceilings, verify-or-abstain **biomedical application** |
| SHARED_PREEXISTING_INFRASTRUCTURE | FCO/FCG content-addressed custody, Merkle ledger, byte-identity manifests |
| PRIOR_METHOD_WORK | Public Zenodo FCO lineage predating NewInML manuscript freeze |
| TEAM_CONTRIBUTED | Successor ClinVar/FASTA bytes from open PR #1 (hash-admitted, not merged) |
| CONTEMPORANEOUS_SUCCESSOR_PRIOR_WORK | FCO v4/v5 grammar package — cite only if explicitly adopted |

Do **not** relabel prior FCO/FCG publications as Protein Hinge invention.

## Citation recommendations

### Required (if custody/provenance discussed — current manuscript does)

**PRIMARY:** `10.5281/zenodo.21210575`  
Fractal Custody Objects (2026-07-05). Earliest public FCO custody concept in scope.

Proposed third-person wording (Related Work):

> Prior work introduced a content-addressed custody framework for deterministic computational biology and AI-agent provenance \cite{lee2026fco}.

### Recommended (FCG named in figure and §6)

**SECONDARY:** `10.5281/zenodo.21382831`  
FCO/FCG architecture and selective-replay protocol record (2026-07-15).

Proposed wording:

> Related work extended custody objects into fractal custody graphs (FCG) with selective replay and graph-root reproduction semantics \cite{lee2026fcg}.

### Optional (only if v4/v5 grammar explicitly adopted)

**OPTIONAL:** `10.5281/zenodo.21829929`  
FCO v4/v5 PASS/FAIL/ABSTAIN claim-grammar package (2026-08-06).

**Default recommendation: omit.** The canonical manuscript grounds Abstain in Chow and selective-prediction literature \cite{chow1970,geifman2017} and uses team-local claim ceilings. It does not invoke FCO v4/v5 remediation machinery or the Vithia companion record.

### Not recommended for NewInML main text

- 10.5281/zenodo.18109862 (Antigence tier-0 overview)
- 10.5281/zenodo.21830287 (Antigence custody matrix)
- 10.5281/zenodo.21830361 (Shadow Dogma)
- 10.5281/zenodo.21830386 (XenoDisorder)

## What Protein Hinge itself contributed (TEAM_CORE novelty)

Keep novelty focused on admitted team evidence:

1. **Biomedical verify-or-abstain application** — terminal states, row invariants, identity guards on ClinVar/FASTA-admitted subsets
2. **GAP accounting correction** — historical 0 vs 3 abstention mismatch and successor invariant repair
3. **G3 identity evaluation** — N=1 observed-source ablation with bypass admission
4. **G1/G2 provenance-negative findings** — historical corpora not recovered; contemporary successor evaluations bounded
5. **Negative/not-executed retention** — EXP-006 null, EXP-005 not executed, historical numbers quarantined
6. **Explicit claim ceilings** — no RWE, efficacy, or population error-rate claims

## Novelty wording audit (`main.tex`)

| ID | Current text | Prior-work conflict | Team scope | Action |
| --- | --- | --- | --- | --- |
| N01 | Abstract: “We present an evidence-pipeline reliability study…” | Low — presents audit results not FCO invention | TEAM_CORE | **KEEP** |
| N02 | Intro: “We frame this work as an evidence-pipeline control problem…” | Low — application framing | TEAM_CORE | **KEEP** |
| N03 | §3 figure: “→ FCG custody” | **Yes** — FCG named without prior-work citation | SHARED_PREEXISTING_INFRASTRUCTURE | **CITE_PRIOR_WORK** (+ optional **QUALIFY**: “project FCG ledger”) |
| N04 | §6: “Frozen Custody Graph” | **Yes** — FCG term without citation | SHARED_PREEXISTING_INFRASTRUCTURE | **CITE_PRIOR_WORK** |
| N05 | §6: “content-addressed as immutable evidence objects… SHA-256” | **Yes** — method described without prior FCO cite | PRIOR_METHOD_WORK | **CITE_PRIOR_WORK** or **QUALIFY** as “following prior content-addressed custody practice” |
| N06 | Title/throughout: “verify-or-abstain” | Partial — abstain theory cited (Chow); custody layer uncited | TEAM_CORE + PRIOR_METHOD_WORK | **KEEP** abstain cites; **CITE_PRIOR_WORK** for custody layer |
| N07 | No occurrences of “we introduce FCO/FCG”, “novel”, “first” in `main.tex` | None detected | — | **KEEP** (good) |
| N08 | Checklist: “new proposed method” boilerplate | NeurIPS template language only | — | **OPERATOR_REVIEW** if camera-ready edit pass |

**No conflicts requiring REMOVE.** Primary gap is missing prior-work citations where FCG/custody infrastructure is named.

## Anonymity considerations

- Zenodo FCO records are author-attributed (Lee, Byron). Anonymous review may use third-person citations without author names in prose if bibliography is deferred to camera-ready — see `paper/newinml2026/audit/PRIOR_WORK_ANONYMITY_DECISION.md` (OPERATOR_INFORMATION_REQUIRED).
- Do not name hackathon events or Discord channels in anonymous manuscript.
- Do not cite Vithia companion URLs from 21829929 in anonymous text.

## Team approval needed before sealed PDF change

1. Accept primary citation 10.5281/zenodo.21210575 (and secondary 21382831 if FCG kept in figure)
2. Choose anonymity variant for prior-work bibliography
3. Approve or reject optional 21829929 cite
4. Confirm no merge of PR #1 Elvis silent-error tables into NewInML Results
