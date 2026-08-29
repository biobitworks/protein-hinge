#!/usr/bin/env bash
# Resume PROTOCOL-NML-OVERNIGHT-001 from persisted STATE.json
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
exec python3 paper/newinml2026/protocols/PROTOCOL-NML-OVERNIGHT-001/run_protocol.py "$@"
