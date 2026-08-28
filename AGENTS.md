# AGENTS.md

Operational notes for coding agents working in this repository.

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
