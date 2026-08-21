# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I057 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I057_LOCAL_CALIBRATION_SESSION.md`
- `implementation/local_calibration_session.py`
- `implementation/test_local_calibration_session.py`
- `implementation/RUN_I056_PYTHON_LOCAL_CALIBRATION_FIXTURE.md`
- I055 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I057 result
`local_calibration_session.py` packages the exact I056 `python_local` portable transcript into a deterministic local session.

The session binds exact transcript text, backend/reference hash, benchmark/output digest, collector-supplied `Z` UTC observation time and a plain transcript filename into an immutable identity. It exposes only non-probe declaration slots plus a separate optional energy-measurement slot. No synthetic/default resource value is copied into evidence.

Replay revalidates the I056/I053 transcript, verifies transcript/session hashes, attaches the explicit collector time, rebuilds I054 evidence and reports which I050 critical parameters are emitted/missing. Missing evidence remains `planning_only`. The CLI `create` path requires explicit `--enable-probe`; `replay` is local/network-free.

Target flow:
`cheap source watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I053 acquisition -> I054 evidence -> I050 attestation -> I051/I052 attested router -> I055 provenance packet -> I056 portable local fixture -> I057 session bundle/replay -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I058
Integrate I057 replay with the I050/I051 attestation boundary as an explicit import path. Only complete/current session evidence may become an attestation candidate; incomplete sessions remain planning-only. Preserve source-kind, session digest and transcript digest provenance. No market/network call.

## Verification caveat
I057 new module/test syntax compilation passed. Full pytest was not run because the isolated execution container could not resolve GitHub to fetch the repository dependency set. Do not treat I057 as a green-CI claim; run the focused tests when a complete checkout/runtime is available. GitHub Actions remains manual/PR-oriented and was not dispatched.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. I055–I057 must preserve exact provenance through any future routed result; neither cheap nor calibrated resources can rescue upstream ineligible work.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
