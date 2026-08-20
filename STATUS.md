# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I049 — observation-to-resource routing integration**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I049_OBSERVATION_RESOURCE_ROUTING.md`
- `implementation/execution_routing_integration.py`
- `implementation/test_execution_routing_integration.py`
- `implementation/RUN_I048_RESOURCE_EXECUTION_ROUTER.md`
- I047 and earlier authorization/readiness/capture files.

## I049 outcome
The Resource / Execution Router is now downstream of the existing task observation/orchestrator gate. A task must first pass normalized policy/capability/quality/evaluator checks **and** carry evidence that proves open paid demand before `TaskEconomics` is constructed and resource routing is invoked.

Cheap execution cannot rescue prohibited, unsupported, policy-insufficient or demand-unproven work. Conversely, an upstream `accept_dry_run` can still be held by the router when explicit acceptance/dispute/non-payment/fee economics make the conservative route unattractive.

Combined `RoutedTaskObservation` records contain upstream economics/evidence plus router quotes/selected backend while `dry_run_only=true`, `execution_enabled=false`, `network_enabled=false` and `value_movement_enabled=false`. Seven deterministic bridge tests passed in an isolated interface-compatible harness; GitHub Actions was not dispatched.

## Current ranking
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Durable rules
- Demand/fill rate remains the dominant unknown.
- Missing capture is not evidence of zero demand.
- Production/test environments remain isolated.
- Capture-integrity labels are not demand/profitability labels.
- Authorization/proposal/review packets and synthetic consent/compliance fixtures are not real user authorization or real compliance proof.
- I039–I047 must never widen the exact single-request scope.
- Any future real authorization must be exact-packet-bound, short-lived, GET-only, no-credentials and no-action.
- A lease is single-use; replay/expiry must fail before any transport callback.
- I043 supports synthetic network-incapable transport only; I044–I047 add proposal/review/evidence/provenance contracts only and have no executable real-network path.
- `ready_for_human_decision` means evidence is adequate to ask, not that execution is authorized or safe to run.
- Manual compliance metadata is not reproducible compliance evidence and cannot cross the I047 bridge.
- Reproducible evidence must be bound to exact source content bytes/digest and fresh first-party policy conclusions.
- Every durable response must remain bound to exact request/receipt/body/manifest evidence.
- DNS/redirect/size/content-type gates remain upstream of evidence parsing.
- No irreversible or paid external action without explicit user authorization.
- Resource routing must separate sunk/fixed cost from marginal cost and must never assume ChatGPT/Codex subscription exposes a free autonomous API.
- Unavailable/credentialed/new-spend backends may be modeled for planning but may not become selected live execution paths without their blockers being explicitly cleared.
- Fast watcher architecture must obey source ToS/rate limits and perform local cheap filtering before AI; do not use frequent LLM polling by default.
- **Upstream observation/policy/demand state is authoritative. Resource routing may narrow eligibility but may never widen or rescue an upstream hold/reject.**
- `routing_economics` risk/fee inputs are explicit economic inputs; ordinary task metadata cannot silently alter router economics.
- Synthetic/default resource profiles are planning references, not evidence of actual user resource availability or current vendor pricing.

## Immediate next run — I050
Build a deterministic resource-profile evidence/calibration layer. Separate synthetic reference backends from measured/declared real available resources; bind availability, fixed/sunk cost, quota, electricity, latency, reliability/quality and interface constraints to explicit evidence/provenance. Unknown or stale resource parameters must remain planning-only. Keep execution/network/value movement disabled.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
