# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I053 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I053_RESOURCE_CALIBRATION_ACQUISITION.md`
- `implementation/resource_calibration_acquisition.py`
- `implementation/test_resource_calibration_acquisition.py`
- `implementation/RUN_I052_ATTESTED_EXECUTION_BRIDGE.md`
- I051 and earlier resource-routing / authorization / readiness / capture files.

## I053 result
A concrete acquisition plan now exists for the first no-new-spend resource families (`deterministic_python` / `owned_pc`). It covers all I050 critical fields while separating what can be measured offline from what must be explicitly declared or supported by provider/system evidence.

The inert probe contract allows fixed-fixture local benchmarking only: no network, credentials, paid service or value movement. From a transcript it may derive demonstrated availability/programmatic access, p95 latency, reliability, conditional quality and bounded concurrency. It cannot infer hardware, electricity tariff/cost, quota, fixed/sunk accounting, credential/paid-account/new-spend requirements or subscription API access.

Target flow:
`cheap source watcher -> local filter/dedupe -> normalized task -> policy/rights/quality/demand gate -> TaskEconomics -> resource acquisition/evidence -> I050 attestation -> I051 attested Resource Router -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I054
Convert I053 probe summaries plus explicit declaration/energy inputs into I050 `ResourceEvidence` records. Preserve source-kind distinctions and exact reference/transcript/source digests. Missing fields must stay missing; do not fabricate completeness. Synthetic fixtures only.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing. Future APIs/VPS/paid services remain planning-only until credentials/spend/ToS/geography gates are cleared.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence then precedes backend selection. Neither a cheap backend nor a calibrated backend can rescue an upstream hold/reject.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
