# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I059 — session-attested routed provenance**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I059_SESSION_ROUTED_PROVENANCE.md`
- `implementation/session_routed_provenance.py`
- `implementation/test_session_routed_provenance.py`
- `implementation/RUN_I058_SESSION_ATTESTATION_IMPORT.md`
- I057 and earlier resource-routing / authorization / readiness / capture files.

## I059 outcome
The I058 `python_local` session import is now explicitly integrated with the I052 attested routing path. Any selected route must match the exact imported backend, calibration state and I050 evidence bundle hash.

The routed record preserves the immutable I057 session digest, probe transcript digest, transcript-file digest and I058 evidence hashes and seals them together with the selected route/task identity in a deterministic provenance-binding hash. Replay verification rejects session, selected backend, calibration, evidence-bundle or inertness drift.

Upstream policy/capability/quality/demand state remains authoritative: a complete calibrated local resource cannot rescue a held/rejected task, and an incomplete/stale/rejected I058 session cannot become a selected resource. New module/test syntax compilation passed; full pytest was not available in the isolated environment, so there is no green-CI claim. GitHub Actions was not dispatched.

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
- I057 session bundles bind exact transcript text, collector UTC time and immutable session identity before evidence replay.
- I057 declaration slots are limited to non-probe facts; partial declarations or partial energy measurements fail closed rather than being guessed.
- I058 incomplete sessions never cross into I050 attestation; complete sessions must still pass current I050 evidence checks.
- I058 preserves exact session digest, transcript file digest, probe transcript digest, evidence hashes and source-kind provenance across the import boundary.
- **I059 selected `python_local` routes must preserve exact I058 session/probe/evidence identity through I052. Backend/calibration/evidence/session drift fails closed.**
- **I059 provenance verification is evidence/routing integrity only; it is not execution authorization.**
- All routing remains dry-run only with execution/network/value movement disabled.

## Immediate next run — I060
Build an inert local execution-plan/receipt boundary over an I059-selected `python_local` route. Use a fixed deterministic fixture only; bind task/provenance/expected-output identities; measure local runtime and explicit energy/cost inputs where available; compare observed execution facts against the selected router quote; reject cost/quality/provenance drift. Keep market submission, network, credentials, paid spend and value movement disabled.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
