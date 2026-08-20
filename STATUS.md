# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I050 — resource-profile evidence and calibration**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I050_RESOURCE_PROFILE_EVIDENCE.md`
- `implementation/resource_profile_evidence.py`
- `implementation/test_resource_profile_evidence.py`
- `implementation/RUN_I049_OBSERVATION_RESOURCE_ROUTING.md`
- I048 and earlier resource-routing / authorization / readiness / capture files.

## I050 outcome
The Resource / Execution Router now has a deterministic evidence/calibration layer that prevents synthetic reference profiles from being mistaken for real current resources.

Fourteen critical parameters — availability, programmatic/interface constraints, credentials/paid-account/new-spend requirements, fixed/sunk cost, quota, electricity, latency, reliability, quality, parallelism and rate limits — must be bound to fresh explicit provenance before a profile can calibrate.

Synthetic defaults, missing/stale/future/conflicting evidence, invalid ranges, reference-profile mismatch and hash tampering all fail closed to `planning_only`. Complete user-declared profiles are kept distinct as `calibrated_declared`; complete measured/provider/system evidence can become `calibrated_reproducible`. Measured/provider/system claims require a source-content digest. Ten deterministic tests passed locally; GitHub Actions was not dispatched.

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
- Reproducible source-compliance evidence must be bound to exact source content bytes/digest and fresh first-party policy conclusions.
- Every durable response must remain bound to exact request/receipt/body/manifest evidence.
- DNS/redirect/size/content-type gates remain upstream of evidence parsing.
- No irreversible or paid external action without explicit user authorization.
- Resource routing must separate sunk/fixed cost from marginal cost and must never assume ChatGPT/Codex subscription exposes a free autonomous API.
- Unavailable/credentialed/new-spend backends may be modeled for planning but may not become selected live execution paths without their blockers being explicitly cleared.
- Fast watcher architecture must obey source ToS/rate limits and perform local cheap filtering before AI; do not use frequent LLM polling by default.
- **Upstream observation/policy/demand state is authoritative. Resource routing may narrow eligibility but may never widen or rescue an upstream hold/reject.**
- `routing_economics` risk/fee inputs are explicit economic inputs; ordinary task metadata cannot silently alter router economics.
- Synthetic/default resource profiles are planning references, not evidence of actual user resource availability or current vendor pricing.
- **A resource profile is not calibrated unless all critical I050 parameters have fresh, hash-bound evidence. Unknown/stale/conflicting/tampered parameters remain planning-only.**
- User-declared evidence must remain visibly distinct from reproducible measured/provider/system evidence; do not upgrade declarations into measurements.
- Reproducible resource claims require source-content digests and exact reference-backend binding.

## Immediate next run — I051
Integrate I050 attestations into I049 routing. Default/synthetic backends must remain explicit reference/planning routes; only complete current attested backend fields may enter a calibrated route set. Add deterministic route-state reporting for reference vs declared vs reproducible calibration, while preserving upstream policy/demand precedence and keeping execution/network/value movement disabled.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
