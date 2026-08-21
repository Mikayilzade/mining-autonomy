# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I056 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I056_PYTHON_LOCAL_CALIBRATION_FIXTURE.md`
- `implementation/python_local_calibration_fixture.py`
- `implementation/test_python_local_calibration_fixture.py`
- `implementation/RUN_I055_CALIBRATION_ROUTING_PACKET.md`
- I054 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I056 result
`python_local_calibration_fixture.py` turns the I053 abstract local acquisition contract into one concrete fixed no-network benchmark for `python_local`.

The runner is disabled by default and requires explicit opt-in. It executes only a deterministic local JSON transform and records latency/success/output-digest/quality observations. The portable transcript binds the exact backend/reference hash, benchmark id, expected output digest, every observation, observed parallelism and the exact I053 transcript digest.

Replay fails closed on tampering/binding mismatches and can feed the verified summary through I055. Probe success still does not prove electricity cost, fixed/sunk accounting, quota, subscription/API access, account requirements, market compatibility or profitability; those remain separate evidence inputs.

Target flow:
`cheap source watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I053 acquisition -> I054 evidence -> I050 attestation -> I051/I052 attested router -> I055 provenance packet -> I056 portable local fixture/replay -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I057
Build a deterministic local calibration session bundle around I056: collector-supplied observation timestamp, transcript-file digest, explicit declaration template for non-probe critical fields, optional energy-measurement slot and one-command offline replay/report. Keep collection opt-in and market/network-free.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. I055/I056 must preserve exact provenance through the routed result; neither cheap nor calibrated resources can rescue upstream ineligible work.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
