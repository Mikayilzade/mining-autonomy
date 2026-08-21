# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I064 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I064_RESOURCE_FEEDBACK_HISTORY.md`
- `implementation/resource_feedback_history.py`
- `implementation/test_resource_feedback_history.py`
- `implementation/RUN_I063_FEEDBACK_ATTESTED_OBSERVATION.md`
- I062 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I064 result
The I063 measured-resource feedback path now has an append-only history/audit layer.

Important behavior:
1. only successful I063 refreshed route/hold updates are history-eligible;
2. the exact `CalibrationFeedback` must be supplied again and its receipt/evidence hashes must exactly match the I063 update;
3. evidence hashes are recomputed and freshness/future timestamps are rechecked at append time;
4. each entry binds the immutable task identity, original observation, before/after routing, target evidence bundles, replaced parameters and selected-backend transition;
5. every entry points to the previous entry hash and receives a canonical entry hash;
6. a next update must begin from the prior entry's `after_routing_hash`;
7. receipt and evidence hashes are single-use inside a history;
8. same-backend/same-parameter feedback cannot regress to equal/older observed evidence;
9. whole-history verification detects sequence gaps, previous-hash tamper, entry-hash tamper, routing discontinuity, replayed receipt/evidence and stale parameter regression;
10. all records remain dry-run/inert with execution/network/credentials/submission/value movement disabled.

Verification: seven deterministic tests passed in an isolated interface-compatible harness; module/test syntax compiled. GitHub Actions was not dispatched.

Target flow:
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> provenance-sealed local benchmark -> verified receipt -> narrow measured feedback -> exact I052 replay/provenance gate -> re-attestation -> unchanged-task reroute -> append-only feedback history -> later separately authorized real gates`.

## Immediate next run: I065
Build a deterministic verified-history summarizer/control gate. From a valid I064 chain, derive latest backend/parameter facts, selected-backend transitions and churn/anomaly flags without inventing reliability, quality, market demand or authorization. Emit a compact provenance-bound current-state snapshot for later experiment planning.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. Benchmark feedback may only narrow/reprice a resource path; it cannot manufacture demand, permission, reliability or quality. I064 history records provenance/order; it does not itself make a backend live-authorized.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
