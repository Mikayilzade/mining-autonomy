# Implementation Run I022 — inert sampling manifest / execution contract

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Turn the I021 production-evidence watchlist into a deterministic source-level sampling manifest that a future explicitly permitted read-only capture client can consume without granting any execution, authentication, task-acceptance, publication or money-moving authority.

## Changes
Added `implementation/sampling_manifest.py`.

The manifest now provides, per source:
- exact HTTPS source URL and `GET`-only method;
- expected evidence class;
- deterministic capture deadline when the platform is due;
- conservative project-side request budget / minimum interval;
- maximum acceptable source age for the existing capture freshness gate;
- explicit provenance requirements;
- explicit environment handling;
- hard `credentials_allowed=False`, `network_calls_performed=False`, `action_enabled=False`.

Default source contracts cover PayanAgent discovery + public receipts, OKX A2A documentation/observability gate, agent2agent.market public surface with environment held `unknown`, MCPize developer/monetization surfaces, and AgentGigs public surface.

Added `capture_bridge_spec()` to prepare exact offline parameters for the existing `observation_capture -> evidence_archive -> archive_replay` route after a separate permitted client has already produced a sanitized bundle. Production environment mapping is explicit; `unknown` remains `unknown` and is never silently promoted.

Added `implementation/test_sampling_manifest.py` covering inert defaults, deterministic deadlines/rate budgets, not-due behavior when fresh complete evidence exists, testnet isolation, unknown-environment fail-closed behavior, production bridge mapping and rejection of POST/off-host policies.

## Fresh public checkpoint
- PayanAgent first-party material still documents unauthenticated `GET /api/v1/discover` and `GET /api/v1/receipts`; catalog supply remains excluded from demand evidence.
- agent2agent.market still exposes a machine-readable public task-feed model, while its documented CLI onboarding remains Base Sepolia; environment therefore stays unproven/unknown in the manifest until a capture proves production.
- MCPize still documents 80% creator share and x402/USDC pay-per-call, but its 900+ server / 450+ publisher counts remain supply-side rather than attributable paid utilization.

## Safety / external actions
No login, KYC, API key, wallet, paid server/API, bid, task acceptance, service publication, transaction or settlement was performed. The manifest itself performs no network traffic.

## Git / CI
Push-triggered CI remains disabled; workflow unchanged. I022 is saved as one atomic commit.

## Outcome
The observation stack now has a deterministic bridge from `what to check` to `how a permitted read-only check must be described`, while preserving strict provenance, rate, environment and action boundaries.

## Next — I023
Add canonical serialization/hash signing for sampling manifests plus a capture-result receipt contract that proves which manifest item produced a sanitized bundle. Keep transport/network disabled by default; then prepare a mock/injected transport path for future permitted anonymous GET captures without adding credentials or action endpoints.
