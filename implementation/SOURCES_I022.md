# Sources — Implementation Run I022

Evidence date: 2026-08-19

## PayanAgent
- https://payanagent.com/
  - First-party marketplace/API reference.
  - Documents unauthenticated `GET /api/v1/discover` and `GET /api/v1/receipts` plus request/bid/fulfill mechanics.
  - Catalog supply counts are not treated as demand.

## agent2agent.market
- https://agent2agent.market/
  - First-party task-exchange page.
  - Documents machine-readable public task browsing and worker lifecycle.
  - Current page also shows Base Sepolia in CLI onboarding examples, so the manifest keeps environment `unknown` until a capture proves production.

## MCPize
- https://mcpize.com/developers
  - First-party developer portal; 80% creator share and 900+ servers / 450+ publishers.
  - Counts remain supply-side only.
- https://mcpize.com/docs/monetization
  - First-party monetization guide; subscriptions and x402 pay-per-call in USDC.

## Internal implementation sources
- `implementation/sampling_planner.py`
- `implementation/observation_capture.py`
- `implementation/evidence_archive.py`
- `implementation/archive_replay.py`

## Evidence rule
Manifest source availability or monetization mechanics do not prove buyer demand, paid utilization or profitability. Environment must be explicit and production evidence cannot be inferred from testnet/unknown observations.
