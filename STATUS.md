# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I055 — end-to-end calibration routing packet**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I055_CALIBRATION_ROUTING_PACKET.md`
- `implementation/calibration_routing_packet.py`
- `implementation/test_calibration_routing_packet.py`
- `implementation/RUN_I054_RESOURCE_EVIDENCE_ADAPTER.md`
- I053 and earlier resource-routing / authorization / readiness / capture files.

## I055 outcome
The full local resource-calibration path is now composed deterministically: I053 acquisition plan/summary -> I054 evidence -> I050 attestation -> I051/I052 attested dry-run routing.

Complete evidence preserves the exact I050 calibration class and evidence bundle hash through the routed task. Missing or stale resource evidence narrows an otherwise upstream-accepted task to hold. A complete calibrated backend cannot rescue a policy/demand reject. Collector-supplied probe observation time remains mandatory and is never replaced by current/commit time.

Six deterministic integration tests were added and both new Python files passed syntax compilation. The tests were not executed in this connector-only runtime; GitHub Actions was intentionally not dispatched.

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
- I051 reference-only resources are never selectable. Only complete current I050 attestations may enter calibrated routing.
- I052 upstream acceptance is required before attested routing; missing resource evidence narrows accept to hold; selected routes carry calibration class and evidence bundle hash.
- I053 local calibration acquisition must not infer hardware, electricity tariff/cost, quota, subscription API access or interface/accounting facts from a successful local probe.
- I054 emits only explicitly supplied/measured resource facts; it may not copy synthetic reference values into evidence.
- I054 system-probe evidence retains exact transcript digest, backend/benchmark binding and collector-supplied observation time.
- **I055 requires one exact provenance chain from acquisition through routed result; calibration class/evidence bundle hash may not change silently between I050 and I052.**
- **Missing/stale calibration evidence may only narrow an upstream accept to hold; complete resource evidence may never rescue an upstream hold/reject.**
- All routing remains dry-run only with execution/network/value movement disabled.

## Immediate next run — I056
Build a deterministic local calibration fixture/runner specification for `python_local`: fixed no-network benchmark, portable JSON transcript and replay verifier through I053–I055. Keep the runner opt-in/inert by default and do not infer accounting/electricity facts or perform real market/network calls.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
