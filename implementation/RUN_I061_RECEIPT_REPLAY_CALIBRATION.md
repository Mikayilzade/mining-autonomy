# I061 — deterministic receipt replay and calibration feedback

Status: **completed** — 2026-08-21

Added `receipt_replay_calibration.py` as a deterministic replay/verifier over I060 local benchmark receipts.

The replay independently re-checks the exact I060 plan hash, task/backend/provenance/fixture/output identities, router marginal-cost quote, inert safety flags, runtime validity and explicit cost consistency. Tampered plan/provenance/fixture/output identity, non-inert flags, invalid runtime/cost facts, or a source receipt that was not already `receipt_verified_inert` fail closed to `hold`.

A verified replay may feed only directly measured local facts back into the I050 resource-calibration evidence model:
- fixed-fixture wall-clock runtime -> `latency_seconds`;
- explicitly measured energy cost -> `electricity_per_task_usd`.

Unknown energy remains unknown and emits no electricity evidence. One successful benchmark does **not** infer availability, programmatic access, quotas, parallelism, rate limits, reliability, quality probability, market demand, task acceptance/payment, or execution authorization. Reproducible feedback is bound to the exact I060 receipt hash as its source-content digest and to the exact reference backend hash.

Verification: **10 deterministic tests passed** in an isolated interface-compatible harness. Tests cover valid replay, unknown-energy preservation, plan/provenance/fixture/output tamper rejection, cost inconsistency/quote drift, inertness, no reliability/quality/demand/authorization inference, blocked feedback from an unverified replay, and reference-backend mismatch. GitHub Actions was not dispatched.

No network, credentials, market submission, paid spend or value movement occurred.

Next: **I062 — integrate verified I061 calibration feedback into the attested `python_local` resource path. Merge measured runtime/energy facts with existing I050 evidence without allowing a single receipt to overwrite unrelated parameters; require freshness/reference binding, surface conflicts explicitly, and show how verified benchmark evidence changes the router quote/selection in dry-run only.**
