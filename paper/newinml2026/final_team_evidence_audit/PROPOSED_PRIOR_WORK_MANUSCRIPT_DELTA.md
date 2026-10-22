# Proposed prior-work manuscript delta (human review only)

**Status:** PROPOSAL_ONLY — `main.tex` and sealed PDF unchanged in this audit  
**Canonical source SHA:** `bc4b0d575d130af3f335b712ec1763c164d7d74b`  
**Sealed PDF SHA-256:** `ded8f72e299642a7f8ed4fc0f5318b1e961c413b5640acaa6cda6d65880448ab`

---

## Delta 1 — Add Related Work paragraph (prior FCO custody)

| Field | Content |
| --- | --- |
| **CURRENT** | §2 cites selective prediction, PROV-DM, HGNC/UniProt, reproducibility, FDA RWE — no FCO/FCG prior work |
| **PROPOSED** | Add after first paragraph of §2: “Prior work introduced content-addressed custody objects and fractal custody graphs for deterministic computational biology and AI-agent provenance, establishing byte-identity closure via SHA-256 manifests and Merkle-style aggregation \cite{lee2026fco,lee2026fcg}. Protein Hinge applies related custody machinery within a bounded verify-or-abstain biomedical evidence workflow; semantic terminal states and row invariants are evaluated separately from hash validity.” |
| **REASON** | Manuscript §3–6 names FCG and describes content-addressed custody without citing public predecessor preprints |
| **PRIOR_WORK_SOURCE** | 10.5281/zenodo.21210575 (primary); 10.5281/zenodo.21382831 (secondary) |
| **TEAM_SCOPE_CONSEQUENCE** | Preserves TEAM_CORE credit for biomedical audits; relocates infrastructure invention to PRIOR_METHOD_WORK |
| **ANONYMITY_CONSIDERATION** | Bibliography entries may be camera-ready if double-blind policy requires; third-person prose avoids “we built FCO” |

---

## Delta 2 — Qualify figure caption (FCG label)

| Field | Content |
| --- | --- |
| **CURRENT** | Figure 1 pipeline ends “→ **FCG custody**” with caption “Custody without semantic checks…” |
| **PROPOSED** | “→ **project FCG ledger**” or retain “FCG custody” but add footnote: “FCG denotes fractal custody graph storage as in prior work \cite{lee2026fcg}.” |
| **REASON** | Bare “FCG custody” reads as first introduction of the term |
| **PRIOR_WORK_SOURCE** | 10.5281/zenodo.21382831 |
| **TEAM_SCOPE_CONSEQUENCE** | Clarifies infrastructure vs team semantic-layer contribution |
| **ANONYMITY_CONSIDERATION** | Low risk |

---

## Delta 3 — Reproducibility section one-sentence prior-work anchor

| Field | Content |
| --- | --- |
| **CURRENT** | §6: “Artifacts… reside in the project Frozen Custody Graph.” |
| **PROPOSED** | “Artifacts… reside in the project frozen custody graph (FCG) ledger, following content-addressed custody conventions established in prior work \cite{lee2026fco}.” |
| **REASON** | Names FCG implementation without lineage |
| **PRIOR_WORK_SOURCE** | 10.5281/zenodo.21210575 |
| **TEAM_SCOPE_CONSEQUENCE** | Separates ledger mechanism (prior) from experiment receipts (team) |
| **ANONYMITY_CONSIDERATION** | Medium — cite in bib even if deferred |

---

## Delta 4 — Bibliography entries (proposed keys)

```bibtex
@misc{lee2026fco,
  author = {Lee, Byron},
  title = {Fractal Custody Objects: route-comparable chain-of-custody for deterministic computational biology and {AI}-agent provenance},
  year = {2026},
  doi = {10.5281/zenodo.21210575},
  url = {https://doi.org/10.5281/zenodo.21210575},
  note = {Zenodo preprint}
}

@misc{lee2026fcg,
  author = {Lee, Byron},
  title = {Fractal Custody Objects and Graphs for Efficient, Verifiable {AI} Training and Computational Biology},
  year = {2026},
  doi = {10.5281/zenodo.21382831},
  url = {https://doi.org/10.5281/zenodo.21382831},
  note = {Zenodo preprint; registered protocol record}
}
```

**Optional (omit by default):**

```bibtex
@misc{lee2026fcov4,
  author = {Lee, Byron},
  title = {Fractal Custody Objects --- v4/v5 publication-version package},
  year = {2026},
  doi = {10.5281/zenodo.21829929},
  note = {Cite only if FCO v4/v5 PASS/FAIL/ABSTAIN grammar adopted}
}
```

---

## Delta 5 — Abstract (no change recommended)

| Field | Content |
| --- | --- |
| **CURRENT** | “We present an evidence-pipeline reliability study…” |
| **PROPOSED** | **No change** |
| **REASON** | Abstract correctly scopes team empirical contribution; does not claim FCO invention |
| **PRIOR_WORK_SOURCE** | N/A |
| **TEAM_SCOPE_CONSEQUENCE** | TEAM_CORE empirical claims preserved |
| **ANONYMITY_CONSIDERATION** | N/A |

---

## Delta 6 — Optional hygiene (from prior audit; not prior-work driven)

| Field | Content |
| --- | --- |
| **CURRENT** | TAFAZZIN concentration in G1 successor not explicit in prose |
| **PROPOSED** | One Results sentence: all 16 residue mismatches in successor G1 evaluation were TAFAZZIN |
| **REASON** | Reduces reviewer over-generalization |
| **PRIOR_WORK_SOURCE** | Team experiment receipts (SOT-008 partial; +30 NOT_ESTABLISHED) |
| **TEAM_SCOPE_CONSEQUENCE** | Bounded descriptive; does not claim +30 offset |
| **ANONYMITY_CONSIDERATION** | Low |

---

## Prohibited edits (do not apply)

- Do not write “We introduce FCO/FCG.”
- Do not merge PR #1 Elvis silent-error tables (24.6%, 51.2%, structure-prediction claims).
- Do not promote SOT-008 +30 offset (NOT_ESTABLISHED, nonblocking).
- Do not alter sealed PDF without team approval after reviewing this file.

## Scientific acceptability of sealed PDF as-is

The sealed PDF is **scientifically acceptable on team evidence** — claim ceilings, negative retention, and bounded successor evaluations are consistent with receipts. The **prior-work citation gap** is a **provenance/novelty hygiene** issue, not a falsification of reported numbers. Team should approve citation deltas before camera-ready.
