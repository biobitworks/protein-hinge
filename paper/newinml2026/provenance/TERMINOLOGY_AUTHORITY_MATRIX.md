# Terminology Authority Matrix (Wave 5)

Generated: 2026-08-28 UTC. See `TERMINOLOGY_AUTHORITY_MATRIX.csv` and `TERMINOLOGY_SOURCE_RECEIPTS.jsonl` for machine-readable rows.

## Classification key

| Class | Meaning |
| --- | --- |
| STANDARDIZED_TERM | Normative definition from standards body |
| ESTABLISHED_RESEARCH_TERM | Peer-reviewed or canonical research usage |
| REGULATORY_TERM | FDA/ICH/NIH regulatory framing |
| PROJECT_OPERATIONAL_TERM | Defined in this work; cite nearest established concept |

## Project operational terms (explicit)

- **Synthetic fixture** — intentionally constructed input for deterministic software behavior testing.
- **Canonical contract fixture** — synthetic/curated fixture with expected outputs fixed before execution.
- **Observed source record** — record retrieved from an identified external source, not invented for testing.
- **External biological evidence** — source-backed biological record or publication used as evidence for a biological assertion.
- **Closed-vocabulary identity resolution** — map source strings to a frozen alias table; abstain when unresolved.

Operational terms are labeled *Operational term defined in this work* in the CSV while citing the nearest established concept (e.g., W3C PROV for provenance-adjacent terms; Chow/Geifman for abstention).

## Regulatory boundaries (not claimed by this paper)

- **Real-World Data / Real-World Evidence** — FDA definitions apply to patient-health data and derived clinical evidence. Protein Hinge pipeline audits and observed-source evaluations are **not** labeled RWE unless regulatory criteria are met.
- **Clinical evidence** — not claimed for computational repurposing hypotheses or null morphology benchmarks.

## Primary citations (selected)

1. W3C PROV — provenance model (`https://www.w3.org/TR/prov-dm/`)
2. Chow (1970) — reject option / abstention tradeoff (`10.1109/TIT.1970.1054470`)
3. Geifman & El-Yaniv (2017) — selective prediction
4. FDA RWE Program — RWD/RWE terminology boundaries
5. HGNC — human gene symbol/alias authority (`https://www.genenames.org/`)
6. UniProt — protein sequence accession practice (`https://www.uniprot.org/help/accessions`)
7. National Academies (2019) — reproducibility and replication (`10.17226/25303`)
