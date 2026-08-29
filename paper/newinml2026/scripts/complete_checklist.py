#!/usr/bin/env python3
"""Fill NeurIPS checklist answers for team-review freeze."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "manuscript" / "checklist.tex"
text = path.read_text()
answers = [
    ("Claims", r"\answerYes{}", "Abstract and Introduction state audit scope, ceilings, and non-claims (Section 1, abstract)."),
    ("Limitations", r"\answerYes{}", "Section 6 and Discussion enumerate N=1 ablation, unrecovered historical corpora, and no clinical/RWE claims."),
    ("Theory assumptions and proofs", r"\answerNA{}", "No formal theorems; pipeline architecture only."),
    ("Experimental result reproducibility", r"\answerYes{}", "Frozen custody graph, SHA-256 manifests, and preregistrations in supplementary materials."),
    ("Open access to data and code", r"\answerNo{}", "Anonymous supplementary package provides manifests and scripts; full public release deferred post-review."),
    ("Experimental setting/details", r"\answerYes{}", "Section 4 and Table 1 specify units, guards, and N for each experiment."),
    ("Experiment statistical significance", r"\answerNA{}", "Primary GAP/G1/G2 results are deterministic full-corpus accounting counts, not sampled inferential estimates."),
    ("Experiments compute resources", r"\answerYes{}", "Compute receipts document local CPU audits; no large GPU training in paper scope."),
    ("Code of ethics", r"\answerYes{}", "No human subjects; public database subsets only; ethics guidelines reviewed."),
    ("Broader impacts", r"\answerNA{}", "Infrastructure audit paper; no deployed clinical system."),
    ("Safeguards", r"\answerNA{}", "No high-risk model release in submission scope."),
    ("Licenses for existing assets", r"\answerYes{}", "ClinVar, UniProt, and cited packages referenced in bibliography and provenance manifests."),
    ("New assets", r"\answerNA{}", "No new public dataset release; custody artifacts are audit outputs."),
    ("Crowdsourcing and research with human subjects", r"\answerNA{}", "No crowdsourcing or human-subjects research."),
    ("Institutional review board", r"\answerNA{}", "No human-subjects research."),
    ("Declaration of LLM usage", r"\answerYes{}", "LLMs used in agent-assisted audit workflows; not core methodology; disclosed in reproducibility section."),
]
for _title, ans, just in answers:
    text = text.replace(
        r"\item[] Answer: \answerTODO{} % Replace by \answerYes{}, \answerNo{}, or \answerNA{}.",
        rf"\item[] Answer: {ans}",
        1,
    )
    text = text.replace(r"\item[] Justification: \justificationTODO{}", rf"\item[] Justification: {just}", 1)
path.write_text(text)
print("checklist updated", len(answers), "items")
