# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I061 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I061_RECEIPT_REPLAY_CALIBRATION.md`
- `implementation/receipt_replay_calibration.py`
- `implementation/test_receipt_replay_calibration.py`
- `implementation/RUN_I060_LOCAL_EXECUTION_RECEIPT.md`
- I059 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I061 result
`receipt_replay_calibration.py` closes the feedback gap between the I060 fixed-fixture benchmark receipt and I050 resource calibration.

Important behavior:
1. no fixture is re-executed during replay;
2. exact I060 plan hash, task/backend/provenance/fixture/output identities and router quote are revalidated;
3. all dry-run/network/credentials/submission/value-movement flags must remain inert;
4. invalid runtime, inconsistent explicit costs, quote drift or a non-verified source receipt fails closed;
5. verified runtime can become `measured_local` `latency_seconds` evidence for the exact fixed fixture;
6. explicitly measured energy can become `electricity_per_task_usd`; unknown energy emits no electricity evidence;
7. feedback evidence is bound to the exact I060 receipt hash and exact reference-backend hash;
8. one benchmark never infers reliability, quality probability, availability, quota, parallelism/rate limits, market demand, acceptance/payment or authorization;
9. ten deterministic tests passed in an isolated interface-compatible harness;
10. no network, credentials, paid spend, market submission or value movement occurred.

Target flow:
`cheap source watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> calibrated resource evidence -> attested Resource Router -> provenance-sealed python_local dry-run route -> I060 fixed-fixture benchmark receipt -> I061 replay -> narrowly measured calibration feedback -> later dry-run quote recalibration -> separately authorized real observation/execution gates`.

## Immediate next run: I062
Integrate verified I061 feedback into the attested `python_local` path. Merge runtime/energy evidence with existing I050 evidence without replacing unrelated parameters, require current exact reference binding, surface conflicts, and show dry-run router quote/selection deltas. Do not enable execution/network/value movement.

## Verification caveat
I061 logic was exercised with **10 passing deterministic tests** in an isolated interface-compatible harness. GitHub Actions remains manual/PR-oriented and was not dispatched.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. I055–I061 preserve exact provenance through the selected route and local benchmark feedback; benchmark economics cannot manufacture demand or permission.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
