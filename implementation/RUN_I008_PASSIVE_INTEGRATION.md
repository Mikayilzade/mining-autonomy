# Implementation Run I008 — passive-service integration

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment
Experiment: **E4 integration**

## Objective
Integrate the bounded MCP benchmark capabilities into a reusable dry-run decision layer, make hosting/pricing economics explicit, and ensure CI structurally covers the complete implementation test suite. No publication, credentials, KYC, wallet, billing or external execution.

## Changes
Added `implementation/passive_service.py` with:
- `HostingTier` and `PassiveServiceOffer` contracts;
- a `PassiveServiceDecision` record analogous to the task evaluator's conservative decision output;
- unit contribution, fixed-hosting break-even, observed-demand projection and hosting-capacity gates;
- explicit `demand_unproven`, policy, margin, pricing/cost and capacity hold reasons;
- `publication_enabled=False` hard-coded regardless of caller input;
- bounded local execution only through the existing MCP capability registry.

Added `implementation/test_passive_service.py` covering:
- positive unit economics does **not** pass when demand is unknown;
- observed synthetic demand with free hosting can become `ready_for_observation`, never live publication;
- $9 hosting break-even at the current normalize-text assumptions is 1,127 calls/month;
- policy and free-tier capacity gates;
- bounded local capability execution.

Updated `.github/workflows/implementation-tests.yml`:
- explicitly installs pytest;
- runs all `implementation/` tests with `python -m pytest -q`;
- workflow changes themselves now trigger pull-request testing.

## Decision semantics
Passive services are intentionally not represented as guaranteed paid tasks. A listing with good per-call margin but no attributable paid utilization is held as `demand_unproven`. This prevents the orchestrator from confusing provider/listing availability with buyer demand.

The passive branch now has two distinct gates:
1. **unit economics gate** — creator revenue must exceed variable cost by absolute and ratio margins;
2. **utilization gate** — projected observed calls must cover fixed hosting and remain inside the modeled tier.

Even a decision of `ready_for_observation` remains dry-run-only. It means the economics are worth observing/testing, not that publication is authorized.

## Economics checkpoint
For `normalize_text` at $0.01/call, 80% creator share and $0.00001 synthetic variable reserve:
- contribution = $0.00799/call;
- free hosting break-even = 0 calls for fixed cash cost;
- $9 hosting break-even = 1,127 calls/month;
- 100 observed calls on free hosting would model $0.799/month before tax/withdrawal/maintenance.

These are model outputs, not demand evidence.

## Test-status honesty
CI is now structurally configured to install pytest and discover all evaluator/MCP/passive-service tests. This connector run did not inspect a completed workflow execution, so no green-CI claim is made here.

## Safety / action boundary
No account was created, no service published, no KYC submitted, no wallet created/funded, no paid infrastructure rented, no transaction signed, and no paid work accepted. `passive_service.py` contains no network client or settlement path.

## Outcome
E4 is no longer a standalone benchmark. It now participates in the implementation architecture through a conservative decision contract that explicitly distinguishes positive unit economics from proven demand and keeps publication hard-disabled.

## Next run — I009
1. Inspect the latest GitHub Actions result for the implementation workflow; fix any real failures rather than assuming tests pass.
2. Add a small offline orchestrator that can process both task opportunities (`evaluator.py`) and passive-service offers (`passive_service.py`) into a unified ranked observation queue without enabling execution/publication.
3. Rank candidates by expected monthly value only when demand evidence exists; unknown demand must remain incomparable/held rather than silently assumed.
4. Continue read-only demand evidence collection for PayanAgent and MCPize where public, attributable observations are available.

Project state: **IMPLEMENTATION IN PROGRESS**.
