# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I051 — attested resource routing**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I051_ATTESTED_RESOURCE_ROUTING.md`
- `implementation/resource_routing_attestation.py`
- `implementation/test_resource_routing_attestation.py`
- `implementation/RUN_I050_RESOURCE_PROFILE_EVIDENCE.md`
- I049 and earlier resource-routing / authorization / readiness / capture files.

## I051 outcome
Synthetic/default Resource Router backends are now planning references only. An unattested backend cannot be selected even if its illustrative marginal cost is lower than every real option.

Only complete current I050 attestations can enter the calibrated route set. User-declared resources remain explicitly `calibrated_declared_route`; measured/provider/system-backed resources remain `calibrated_reproducible_route`; missing/planning-only evidence yields `resource_evidence_missing`.

The calibrated path still obeys capability, quota, policy, success-probability and conservative-margin gates. Execution/network/value movement remain disabled. Seven deterministic tests were added; syntax compilation passed; GitHub Actions was not dispatched.

## Current ranking
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Durable rules
- Demand/fill rate remains the dominant unknown; missing capture is not zero demand.
- Production/test environments remain isolated; capture-integrity labels are not profitability labels.
- Authorization/proposal/review/synthetic consent are not real user authorization.
- I039–I047 exact single-request scope must never widen; real authorization must be short-lived, GET-only, no-credentials/no-action.
- No irreversible or paid external action without explicit user authorization.
- Resource routing separates sunk/fixed from marginal cost and never assumes ChatGPT/Codex subscription exposes a free autonomous API.
- Unavailable/credentialed/new-spend backends may be modeled but not selected live until blockers are cleared.
- Fast watcher architecture must obey ToS/rate limits and use cheap local filtering before AI.
- Upstream policy/demand evidence is authoritative; resource routing may narrow eligibility but never widen it.
- Synthetic/default resource profiles are planning references, not current evidence.
- I050 calibration requires fresh hash-bound evidence for all critical resource parameters; declarations remain distinct from reproducible measurements.
- **I051: reference-only resources are never selectable. Only complete current I050 attestations may enter calibrated routing.**
- Route state must expose `resource_evidence_missing`, `calibrated_declared_route`, or `calibrated_reproducible_route`; all remain dry-run only.

## Immediate next run — I052
Build the end-to-end `observe -> policy/demand gate -> TaskEconomics -> attested resource route` bridge. Require I049 upstream acceptance before any calibrated routing, carry resource evidence/calibration provenance into the combined record, and keep execution/network/value movement disabled.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
