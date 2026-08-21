# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I058 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I058_SESSION_ATTESTATION_IMPORT.md`
- `implementation/session_attestation_import.py`
- `implementation/test_session_attestation_import.py`
- `implementation/RUN_I057_LOCAL_CALIBRATION_SESSION.md`
- I056 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I058 result
`session_attestation_import.py` is the explicit boundary from I057 portable local sessions to I050 resource-profile attestation.

Important behavior:
1. I057 session replay/integrity/inertness runs first;
2. I054 evidence is independently rebuilt from the exact session transcript, collector time, declarations and energy measurement;
3. rebuilt emitted/missing parameters, source kinds and completeness must exactly match the I057 replay report;
4. immutable session digest, transcript file digest, probe transcript digest, evidence hashes and source kinds remain explicit in the import result;
5. incomplete sessions return `planning_only_incomplete_session` with no attestation candidate;
6. complete evidence still passes through I050 freshness/reference/hash/value validation at explicit UTC `now`;
7. only `calibrated_declared` or `calibrated_reproducible` I050 states become attestation candidates;
8. no execution/network/value movement is enabled.

Target flow:
`cheap source watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I053 acquisition -> I054 evidence -> I050 attestation -> I051/I052 attested router -> I055 provenance -> I056 portable local fixture -> I057 session bundle -> I058 attestation import -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I059
Integrate I058 into the I052/I055 routed provenance path for `python_local`. A selected routed record must carry and verify the exact I058 session digest, probe transcript digest and I050 evidence bundle hash. Any drift between session import, attestation and routed result must fail closed. Upstream policy/demand gates remain authoritative.

## Verification caveat
I058 new module/test syntax compilation passed. Full pytest was not run because the isolated execution container could not fetch the repository dependency set. Do not treat I058 as a green-CI claim. GitHub Actions remains manual/PR-oriented and was not dispatched.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. I055–I058 must preserve exact provenance through any future routed result; neither cheap nor calibrated resources can rescue upstream ineligible work.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
