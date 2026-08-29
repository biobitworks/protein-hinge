# Cloudflare OS Integration — NewInML 2026

**Role:** agent/workspace/security/control surface — **not** scientific source of truth  
**Canonical authority:** magicSTUDIObox.local (`paper/newinml2026/`, git, SHA-256, SeedGraph)

## Upstream pin

```json
{
  "status": "NOT_PINNED",
  "upstream_repo": null,
  "upstream_commit": null,
  "pinned_at_utc": null,
  "note": "No Cloudflare OS checkout identified in protein-hinge workspace during bootstrap"
}
```

See `cloudflareos/UPSTREAM_PIN.json` for machine-readable record.

## Integration boundaries

| Responsibility | Owner |
|----------------|-------|
| Canonical git state | magicSTUDIObox |
| FCO/FCG custody | magicSTUDIObox |
| SHA-256 hashes | magicSTUDIObox |
| Experiment validation / aggregation | magicSTUDIObox |
| SeedGraph ingest promotion | magicSTUDIObox (gated) |
| Paper status UI | Cloudflare OS (adapter) |
| Experiment queue UI | Cloudflare OS (adapter) |
| Agent orchestration | Cloudflare OS (adapter) |
| Gatekeeper policy | Cloudflare OS (adapter) |
| Human approvals | Cloudflare OS (adapter) |
| CUDA dispatch requests | Cloudflare OS → compute router → Kaggle/Daytona |

## Gatekeeper restrictions (desired)

- Write operations to `paper/newinml2026/provenance/`
- Compute launch without prereg receipt
- SeedGraph promotion / live writeback
- Publication/export of manuscript projections
- External provider calls (OpenAI, Convoke, etc.)

Every mediated action → custody event receipt under `cloudflareos/receipts/`.

## Local development path

When upstream is pinned, run via documented Wrangler/workerd dev path only.
Do not vendor uncontrolled `main` into scientific evidence.

## Bootstrap status

- Integration: **NOT_STARTED**
- Local runtime: **NOT_VERIFIED**
- Adapters: **NOT_IMPLEMENTED**

## Next step

Operator selects upstream Cloudflare OS repo + commit for `UPSTREAM_PIN.json`,
then narrow adapter spec in `SKILLS/` and `GATEKEEPERS/`.
