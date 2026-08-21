# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I059 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I059_SESSION_ROUTED_PROVENANCE.md`
- `implementation/session_routed_provenance.py`
- `implementation/test_session_routed_provenance.py`
- `implementation/RUN_I058_SESSION_ATTESTATION_IMPORT.md`
- I057 and prior resource-routing / authorization / readiness / capture files named in STATUS.

## I059 result
`session_routed_provenance.py` closes the provenance gap between the portable local resource-calibration session and the selected attested route.

Important behavior:
1. this path is restricted to `python_local`;
2. I058 import/attestation replay happens before resource selection;
3. upstream policy/capability/quality/demand gates remain authoritative;
4. incomplete/stale/rejected session attestations cannot become selected resources;
5. any selected backend must equal the I058 backend and carry the exact I050 attestation state/evidence bundle hash;
6. the I057 session digest, I056 probe transcript digest, transcript-file digest and I058 evidence hashes remain explicit;
7. a deterministic binding hash seals those identities to the routed external task/state and selected backend/calibration/evidence identity;
8. serialized replay rejects session/backend/calibration/evidence-bundle/inertness drift;
9. no execution/network/value movement is enabled.

Target flow:
`cheap source watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> I053 acquisition -> I054 evidence -> I050 attestation -> I051/I052 attested router -> I055 provenance -> I056 portable local fixture -> I057 session -> I058 attestation import -> I059 provenance-sealed selected route -> later explicit execution/economic gates`.

## Immediate next run: I060
Build an inert local execution-plan/receipt boundary over an I059-selected `python_local` route. Use a fixed deterministic fixture only, bind exact task/provenance/expected-output identities, capture local runtime and explicit energy/cost inputs where available, and compare observed facts with the selected router quote. Cost/quality/provenance drift must fail closed. Do not submit market work or enable network, credentials, paid spend or value movement.

## Verification caveat
I059 new module/test syntax compilation passed. Full pytest was not available in the isolated execution environment, so do not treat I059 as a green-CI claim. GitHub Actions remains manual/PR-oriented and was not dispatched.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, settle transactions, use real credentials or bypass CAPTCHA/geofencing/rate limits/platform rules without explicit user authorization. Real market/network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk limited resources with interface constraints. Only genuinely available programmatic backends with current evidence may be considered for future live routing.

## Routing precedence
Policy/demand evidence precedes resource economics. Resource evidence precedes backend selection. I055–I059 preserve exact provenance through the routed result; neither cheap nor calibrated resources can rescue upstream ineligible work.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or documentation-only Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
