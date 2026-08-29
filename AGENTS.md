# Protein Hinge — Agent Guide

Operational notes for coding agents working in this repository, plus the NewInML
2026 paper control plane when working under `paper/newinml2026/`.

## What this repo is

Protein Hinge is a self-contained, hash-pinned evidence ledger plus a browser
demo. The ledger of record is `fcg/store/` (content-addressed, append-only).
Everything else is a **projection** of that store and is regenerated from it,
never hand-edited. If a projection and the store disagree, the store is right.

## Environment setup

Prerequisites present on a normal dev box:

- Python 3.12+
- Node.js 18+ (tested on Node 22)

Install dependencies:

```bash
pip3 install -r requirements.txt   # matplotlib, networkx, numpy, pandas, python-dotenv
npm install                        # cytoscape, @strands-agents/sdk
```

## Run and verify

```bash
python3 db/build_db.py        # rebuild the SQLite projection from fcg/store/
node site/verify_test.js      # replay the browser Merkle verifier headlessly
python3 fto/fto.py            # registry status + the FTO_OPINION refusal
python3 db/serve.py 8787      # serve the local browser demo, then open http://localhost:8787
```

Expected healthy signals:

- `db/build_db.py` prints `self-check ... OK` and the merkle root
  `sha256:d98a2972e57a8e9c2f3111e224950d4ae74c65a6cfc18d064eb07014d4d589a4`.
- `node site/verify_test.js` prints `OVERALL PASS` (62/62 leaves recompute on
  both the WebCrypto and in-page SHA-256 paths, and a one-character tamper
  moves the root).
- `fto/fto.py` refuses `FTO_OPINION` and caps at `CLEARANCE_SEARCH_RECORD`.

Credentials never enter the repo. Optional API/AWS keys live only in a local,
git-ignored `.env` (see `.env.example`).

## Cursor Cloud specific instructions

The Cursor Cloud base image ships Python 3.12 but does **not** include
`python3.12-venv` / `ensurepip`, and `apt-get install python3.12-venv` has no
installation candidate on that image. Creating a virtualenv therefore fails
with "ensurepip is not available".

Install the Python dependencies into the user/system site packages instead:

```bash
pip3 install --break-system-packages -r requirements.txt
```

Node and npm are already on `PATH`; `npm install` works without changes. To run
the dashboard for a manual/GUI check, serve it and open the printed URL:

```bash
python3 db/serve.py 8787   # http://localhost:8787
```

## Guardrails for scientific / evidence work

- Use only permitted public, synthetic, or de-identified data.
- Never place secrets in source or evidence artifacts.
- Preserve original representations as custody leaves; projections are derived,
  never authoritative.
- Keep scientific evidence separate from licensing/FTO state.
- Do not call a predicted counter-perturbation "measured rescue"; the claim
  ceiling is `REPURPOSING_HYPOTHESIS` and is enforced in code.
- Missing adapters/inputs are not `PASS`.
- Deterministic builds must reproduce; every reported metric must be computed
  from admitted inputs, never invented.

---

# NewInML 2026 — Agent Control Plane (PROPOSAL)

**Status:** MERGED to `main` (NewInML 2026 team-review + audit wave); submission seal **OPERATOR_INFORMATION_REQUIRED**  
**Canonical controller:** magicSTUDIObox (`magicSTUDIObox.local`, arm64)  
**Evidence authority:** local git + SHA-256 custody under `paper/newinml2026/`

## Role

You are an execution controller for the NewInML 2026 paper provenance, experiment,
and reproducibility program. The manuscript is a **projection** of the FCG; it is
not the canonical source.

## Non-negotiables

1. **magicSTUDIObox** is the canonical controller and evidence authority.
2. This host is Apple Silicon — **no local CUDA / SGLang GPU experiments**.
3. CUDA workloads route to preregistered remote hosts (Kaggle preferred, Daytona GPU fallback).
4. Never overwrite historical FCO/FCG objects; add immutable successors.
5. Git SHA ≠ SHA-256. Compute SHA-256 over exact artifact bytes.
6. Do not claim SIGNED / Merkle / MMR unless the exact construction and receipt exist.
7. Git metadata is **attribution evidence**, not proof of human authorship.
8. Negative, null, failed, and contradictory results are first-class evidence.

## Daisy chain

```
OFFER → ACCEPT → EXECUTE → VERIFY → CLOSEOUT
PI → PM → SWE → ARBITER/REVIEWER → OPERATOR (only when required)
```

Terminal states: `COMPLETE | NEGATIVE | BLOCKED | QUARANTINED | SKIPPED`

## Paper workspace

```
paper/newinml2026/
  control/          PROJECT_CONTROL.yaml, policies
  provenance/       manifests, hashes, import accounting
  sources/          source artifact registry
  contributors/     attribution audit
  datasets/         dataset snapshots
  experiments/      preregistrations, runs, results
  claims/           claim-evidence matrix
  thesis/           versioned thesis objects
  manuscript/       paper sections (projection only)
  figures/          figure custody
  submission/       anonymous submission artifacts
  receipts/         operation receipts
  seedgraph/        ingest manifests
  compute/          routing policy, dispatch manifests
  cloudflareos/     upstream pin, adapters (non-canonical UI/control)
```

## Experiment numbering

| ID | Lane | Classification |
|----|------|----------------|
| EXP-GAP-ACCOUNTING-001 | GAP semantic accounting audit | EXPLORATORY |
| EXP-GAP-ACCOUNTING-001.1 | GAP accounting repaired rerun | REPLICATION |
| EXP-001 | GAP semantic-accounting audit (paper matrix alias) | EXPLORATORY |
| EXP-002 | G1 sequence/residue verification ablation | EXPLORATORY |
| EXP-003 | G2 CNV attribution ablation | EXPLORATORY |
| EXP-004 | G3 identity-resolution ablation | EXPLORATORY |
| EXP-005 | Frozen-corpus independent replication | REPLICATION |
| EXP-006 | Morphology/null reproduction | REPLICATION |
| EXP-007 | SGLang CUDA graph-break stress | EXPLORATORY |

Existing observed results MUST NOT be retroactively labeled confirmatory.

## Related repos (read-only unless explicitly scoped)

| Repo | Path | Role |
|------|------|------|
| gettingsciencedone | `/Users/byron/projects/active/gettingsciencedone` | experiment contracts, gsigmad skills |
| seedgraph | `/Users/byron/projects/active/seedgraph` | seedKG ingest |
| overwatch | `/Users/byron/projects/active/overwatch` | portfolio truth (writeback gated) |

## Acceptance gates

See `paper/newinml2026/control/PAPER_FCG_PLAN.md` §Acceptance Gates.

## First action on session start

1. Confirm hostname + git identity.
2. Read `PROJECT_CONTROL.yaml`.
3. Read `paper/newinml2026/provenance/PAPER_IMPORT_ACCOUNTING.json`.
4. Read latest thesis version under `paper/newinml2026/thesis/`.
5. Do not start paper prose until custody graph bootstrap is current.
