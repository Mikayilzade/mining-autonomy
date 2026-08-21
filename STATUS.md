# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I057 — deterministic local calibration session bundle**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I057_LOCAL_CALIBRATION_SESSION.md`
- `implementation/local_calibration_session.py`
- `implementation/test_local_calibration_session.py`
- `implementation/RUN_I056_PYTHON_LOCAL_CALIBRATION_FIXTURE.md`
- I055 and earlier resource-routing / authorization / readiness / capture files.

## I057 outcome
The `python_local` calibration path now has a portable collector-bound offline session format around I056.

A session binds the exact I056 transcript text, backend/reference hash, benchmark/output digest, collector-supplied UTC timestamp and transcript filename into an immutable identity. It exposes explicit declaration slots only for non-probe critical facts and a separate optional measured-energy slot; it never backfills from synthetic/default resource profiles.

Offline replay verifies transcript/session bindings, rebuilds I054 evidence and reports `planning_only` until all I050 critical facts are explicitly evidenced. An opt-in CLI can create the fixed local probe session, and a network-free replay command prints the evidence/missing-field report. Syntax compilation passed for the new module/tests; full pytest was not run because the isolated container could not fetch repository dependencies, so no green-CI claim is made. GitHub Actions was not dispatched.

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
- I055 requires one exact provenance chain from acquisition through routed result; calibration class/evidence bundle hash may not change silently between I050 and I052.
- I056 local runner is opt-in and fixed-fixture only; successful local benchmark results prove runtime facts only.
- I056 portable transcripts preserve exact backend/reference/benchmark/output/I053-digest bindings; tampering fails closed.
- **I057 session bundles bind exact transcript text, collector UTC time and immutable session identity before evidence replay.**
- **I057 declaration slots are limited to non-probe facts; partial declarations or partial energy measurements fail closed rather than being guessed.**
- **I057 offline replay remains planning-only until every I050 critical parameter has explicit evidence; session packaging never upgrades missing facts.**
- All routing remains dry-run only with execution/network/value movement disabled.

## Immediate next run — I058
Integrate I057 session replay with the I050/I051 attestation boundary as an explicit import path. Convert only complete, current session evidence into an attestation candidate; keep incomplete sessions planning-only and preserve exact source-kind/session/transcript provenance. No market/network calls and no execution/value movement.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
