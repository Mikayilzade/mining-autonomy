# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I054 — I053 probe/declaration to I050 ResourceEvidence adapter**
Last updated: **2026-08-21**

## Latest durable files
- `implementation/RUN_I054_RESOURCE_EVIDENCE_ADAPTER.md`
- `implementation/resource_evidence_adapter.py`
- `implementation/test_resource_evidence_adapter.py`
- `implementation/RUN_I053_RESOURCE_CALIBRATION_ACQUISITION.md`
- I052 and earlier resource-routing / authorization / readiness / capture files.

## I054 outcome
The stack now has a deterministic adapter from I053 local calibration inputs into exact I050 `ResourceEvidence` records.

Offline probe facts preserve `system_probe` provenance and are bound to the transcript digest/reference-backend hash. Explicit accounting/interface facts remain `user_declared`; measured electricity cost requires explicit energy-per-task + tariff inputs and a source digest. Missing fields are never backfilled from synthetic reference profiles.

Probe summaries must match backend/benchmark, remain inert, include collector-supplied measurement time and be internally consistent with their latency/reliability/quality/parallelism/rate-limit summary fields. Duplicate parameter inputs fail closed. Ten deterministic tests were added; they were not executed in this connector-only runtime and GitHub Actions was not dispatched.

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
- **I054 must emit only explicitly supplied/measured resource facts; it may not copy synthetic reference values into evidence.**
- **I054 system-probe evidence must retain exact transcript digest, backend/benchmark binding and collector-supplied observation time; current/commit time must never be substituted.**
- `user_declared`, `system_probe` and `measured_local` provenance classes must remain distinct through I050 attestation and later routing.
- All routing remains dry-run only with execution/network/value movement disabled.

## Immediate next run — I055
Build a deterministic end-to-end calibration packet composing I053 acquisition summary -> I054 evidence -> I050 attestation -> I051/I052 attested dry-run routing. Prove that missing/stale resource evidence narrows routing to hold and that complete synthetic fixtures preserve calibration class and evidence bundle hashes end to end. Keep execution/network/value movement disabled.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
