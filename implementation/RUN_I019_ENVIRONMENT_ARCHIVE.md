# Implementation Run I019 — sanitized append-only evidence archive + environment isolation

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Persist I018 capture reports in a deterministic sanitized archive while making production/testnet separation an integrity property rather than a reporting convention.

## Changes
Added `implementation/evidence_archive.py`.

The archive layer:
- accepts only already-generated dry-run capture reports;
- validates capture-report schema/version, registry membership, hashes, HTTPS provenance and normalized demand/utilization fields;
- persists only normalized observation metadata, not raw platform payloads or buyer identities;
- requires every observation to be explicitly classified as `production`, `testnet` or `unknown` (default is fail-closed `unknown`);
- hash-binds each sanitized entry to its source report;
- maintains a per-entry SHA-256 chain and a top-level archive SHA-256;
- rejects duplicate bundle hashes;
- supports deterministic canonical JSON export/import;
- verifies schema, archive hash, entry hashes, chain continuity and append-only prefix semantics on reload;
- exposes a production scorecard that includes **only** `environment == production` and reports testnet/unknown exclusions separately;
- preserves the prior non-extrapolation rule: no cross-snapshot paid-value sum or revenue extrapolation.

Added `implementation/test_evidence_archive.py` with eight isolated tests covering testnet exclusion, unknown exclusion, production inclusion, deterministic round-trip, tamper detection, duplicate rejection, append-only enforcement and invalid-environment rejection.

Local isolated result: **8 passed**.

## Fresh public read-only checkpoint — 2026-08-19
### PayanAgent
The current first-party site still documents anonymous `GET /api/v1/discover` and public `GET /api/v1/receipts`, while seller/request/bid/fulfill actions require an API key. The site still claims 24,000+ live offers/services, but that remains catalog supply rather than attributable buyer demand. No raw timestamped production request/receipt payload was captured in this run, so production utilization remains unmeasured.

### agent2agent.market
The current public app still displays `Open tasks 0` and explicitly identifies the network as `base-sepolia`. This observation is therefore **testnet** evidence and is now structurally excluded from production scoring by the new archive layer. The first-party homepage continues to document machine-native task browsing, acceptance/submission and USDC settlement mechanics.

### MCPize
Current first-party pages still document standard 80% developer revenue share for new servers, x402 per-call USDC payments on Base, and free Base Sepolia testing. Publisher analytics/payment history remain tied to developer/dashboard context; no publisher account or wallet was created.

## Safety / external actions
No account/login/KYC, API key, wallet creation/funding, task acceptance, bid, submission, service publication, paid API/server, transaction or settlement occurred. No network-fetch or value-moving code was added.

## Git / CI
Push-triggered CI remains disabled and no workflow change was made. This stage is intended as one atomic commit containing code, tests, docs, sources and checkpoint updates.

## Outcome
The evidence pipeline can no longer accidentally interpret an observed testnet zero as production zero-demand. Portable observation history is now deterministic, sanitized, tamper-evident and append-only, with explicit environment isolation.

The main bottleneck remains the same: attributable **production** demand/utilization data for the strongest candidate markets is not publicly captured yet.

## Next — I020
1. Add an environment-aware replay bridge from sanitized archive entries into the unified observation/orchestrator reporting path, preserving production-only economics.
2. Add explicit evidence-age/freshness state to archive scorecards so old production observations cannot silently remain "latest viable" evidence.
3. Continue read-only PayanAgent production request/receipt observation; save only attributable raw payload-derived sanitized evidence if genuinely accessible.
4. Keep agent2agent `base-sepolia` observations quarantined as testnet and continue looking only for a clearly identified production surface.
5. Keep MCPize utilization gated unless public attributable payment data becomes available.
