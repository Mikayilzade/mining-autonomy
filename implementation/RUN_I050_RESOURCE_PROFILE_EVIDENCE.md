# Implementation Run I050 — resource-profile evidence and calibration

Date: 2026-08-21
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective

Prevent synthetic Resource / Execution Router defaults from being mistaken for current real resource availability or economics. Add a deterministic, transport-free calibration layer that binds every critical live-routing parameter to explicit fresh provenance before a resource profile can be considered calibrated.

## Changes

Added `implementation/resource_profile_evidence.py`.

The layer separates four practical states:

- synthetic reference values remain planning references only;
- incomplete/stale/conflicting/tampered evidence remains `planning_only`;
- complete current user-declared evidence becomes `calibrated_declared`;
- complete current reproducible measured/provider/system evidence becomes `calibrated_reproducible`.

Calibration is bound to the exact reference backend hash, so evidence for one router profile cannot silently be applied to a modified/different profile.

### Critical parameters

A complete profile currently requires evidence for:

1. current availability;
2. programmatic access;
3. credential requirement;
4. paid-account requirement;
5. new-spend requirement;
6. fixed monthly cost;
7. sunk/already-committed status;
8. remaining quota/capacity;
9. per-task electricity;
10. latency;
11. reliability probability;
12. quality probability;
13. parallelism;
14. rate limit.

Unknown values do not become zero. Missing evidence keeps the profile planning-only.

### Provenance / freshness

Each evidence record binds:

- evidence ID;
- backend ID;
- exact parameter/value;
- provenance class (`synthetic_reference`, `user_declared`, `measured_local`, `provider_first_party`, `system_probe`);
- source reference;
- UTC observation time;
- maximum age;
- exact reference-backend hash;
- source-content digest where reproducibility is claimed;
- deterministic evidence hash.

Measured/provider/system evidence requires a source-content digest. User declarations are kept visibly separate from reproducible measurements and never mislabeled as measured evidence.

Freshness is enforced against an explicit UTC verification time. Future-dated, stale, malformed, wrong-backend, wrong-reference, invalid-range and hash-tampered records fail closed. Conflicting simultaneously-current values for the same parameter also fail closed instead of choosing a convenient value.

### Materialization boundary

`materialize_calibrated_backend_fields()` can expose calibrated router fields only after a complete current attestation. It does **not** instantiate an executor, does not enable network access and emits an inert attestation marker with execution/network/value movement all false.

This creates a clean bridge for a later run to instantiate router backends from evidence without treating current synthetic `default_backend_families()` values as real measurements.

## Verification

Added `implementation/test_resource_profile_evidence.py`.

Ten deterministic tests cover:

1. complete reproducible calibration;
2. separate complete user-declared calibration state;
3. synthetic reference rejection for live calibration;
4. missing parameter fail-closed behavior;
5. stale and future-dated evidence rejection;
6. evidence-hash tamper and reference-backend binding;
7. conflicting current evidence rejection;
8. digest requirement for reproducible sources;
9. materialization only after complete attestation;
10. probability/parallelism range validation.

Isolated local verification: **10 passed**.

GitHub Actions was not dispatched; push-triggered CI remains disabled.

## Safety / external actions

No market/API production capture, credentials, account/login/KYC, paid API/server, wallet, task acceptance, publication, settlement or value movement occurred. The new module performs no transport and cannot execute a task.

No actual user hardware, subscription quota, electricity tariff, API price or provider limit was inferred from chat history. Until explicit current evidence is supplied/captured through an allowed path, those real resource parameters remain unknown.

## Outcome

The Resource / Execution Router can now distinguish an illustrative backend profile from a current evidence-backed resource profile. This closes the accounting/provenance gap identified after I048–I049: low synthetic cost can no longer be treated as proof that a backend is genuinely available, cheap, fast or reliable.

The economic/demand gap remains unchanged: no real paid-demand sample or monetization test has yet been performed.

## Next run — I051

Integrate I050 attestations into I049 routing. Default/synthetic backend families must remain explicit planning references; only complete current attested backend fields may enter a calibrated route set. Preserve upstream policy/demand precedence and keep execution/network/value movement disabled. Add queue-level reporting that distinguishes `reference_route`, `calibrated_declared_route`, `calibrated_reproducible_route` and `resource_evidence_missing`.

Project state: **IMPLEMENTATION IN PROGRESS**.
