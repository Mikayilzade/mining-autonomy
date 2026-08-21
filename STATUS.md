# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I056 — opt-in local python calibration fixture/runner**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I056_PYTHON_LOCAL_CALIBRATION_FIXTURE.md`
- `implementation/python_local_calibration_fixture.py`
- `implementation/test_python_local_calibration_fixture.py`
- `implementation/RUN_I055_CALIBRATION_ROUTING_PACKET.md`
- I054 and earlier resource-routing / authorization / readiness / capture files.

## I056 outcome
The first concrete resource-calibration backend fixture now exists for `python_local`. It is a fixed deterministic JSON transform, disabled unless explicitly opted in, and performs no network, credential, spend or value-moving action.

An opted-in local runner records only facts the I053 probe is allowed to demonstrate and emits a portable JSON transcript bound to the exact backend/reference hash, benchmark id, expected output digest, observations and I053 transcript digest. Replay fails closed on tampering or binding mismatches and can feed the verified probe summary through I055.

The fixture deliberately does not infer electricity/accounting/quota/account/interface facts. Replaying a successful transcript without separate evidence for those fields remains `planning_only` / hold. Eight deterministic tests were added; GitHub Actions was not dispatched and push-triggered CI remains disabled.

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
- I055 requires one exact provenance chain from acquisition through routed result; calibration class/evidence bundle hash may not change silently between I050 and I052.
- Missing/stale calibration evidence may only narrow an upstream accept to hold; complete resource evidence may never rescue an upstream hold/reject.
- **I056 local runner is opt-in and fixed-fixture only. A successful local benchmark proves only exact observed runtime facts, never accounting/electricity/quota/subscription/API/market facts.**
- **I056 portable transcripts must preserve exact backend/reference/benchmark/output/I053-digest bindings; tampering fails closed before evidence/routing.**
- All routing remains dry-run only with execution/network/value movement disabled.

## Immediate next run — I057
Build a deterministic local calibration session bundle around I056: explicit collector timestamp, transcript file digest, separate declaration template for non-probe critical fields, optional energy-measurement slot, and a one-command offline replay/report contract. Keep collection opt-in; do not infer missing resource facts and do not perform market/network calls.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
