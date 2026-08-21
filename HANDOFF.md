# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I063 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I063_FEEDBACK_ATTESTED_OBSERVATION.md`
- `implementation/feedback_attested_observation.py`
- `implementation/test_feedback_attested_observation.py`
- `implementation/test_benchmark_feedback_integration.py`
- I062 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I063 result
The feedback path is now connected back into the I052 combined observation/attested-routing object without allowing measured resource data to mutate market evidence.

Important behavior:
1. original I052 task/observation/economics/demand evidence is retained intact;
2. exact task identity is required;
3. supplied reference backends + old attestations must reproduce the original I052 route before feedback is accepted;
4. raw pre-feedback evidence for the target backend must independently reproduce its prior attestation;
5. I062 remains the only parameter-replacement path, so only verified measured parameters can change;
6. the updated target attestation is substituted into the same backend set and the unchanged task is rerouted;
7. before/after route, evidence-bundle hashes, feedback receipt/evidence hashes and replaced parameters are bound into a provenance hash;
8. stale/unverified/backend-mismatched/provenance-mismatched feedback fails closed;
9. added explicit I062 regression tests plus seven I063 bridge tests; new files pass syntax compilation;
10. no network, credentials, paid spend, market submission or value movement occurred.

Target flow:
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> provenance-sealed local benchmark -> verified receipt -> narrow measured feedback -> exact I052 replay/provenance gate -> re-attestation -> unchanged-task reroute -> later separately authorized real gates`.

## Immediate next run: I064
Build append-only feedback history/audit over I063. Chain every update to previous calibrated state, receipt/evidence hashes and before/after routing hashes. Reject replayed/out-of-order receipts and stale parameter regression. Keep execution/network/value movement disabled.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. Benchmark feedback may only narrow/reprice a resource path; it cannot manufacture demand, permission, reliability or quality.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
