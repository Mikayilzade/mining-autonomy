# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I038 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I038_AUTHORIZATION_READINESS.md`
- `implementation/authorization_readiness.py`
- `implementation/test_authorization_readiness.py`
- `implementation/RUN_I037_EVIDENCE_QUALITY_GATE.md`
- I036 and prior capture/readiness/session/preflight files named in STATUS.

## I038 result
`build_authorization_readiness_packet()` joins the exact I037 quality output, I036 history and I028–I030 contracts without performing network activity.

Important behavior:
1. I037 and I036 hashes are independently revalidated;
2. I036 must bind to the exact I029 session-plan hash and I030 transport-envelope-set hash;
3. I028 readiness, I029 plan and I030 envelope-set hashes are independently recomputed;
4. I030 request bindings are revalidated before selection;
5. capture-integrity recommendations remain explicitly separate from economic demand;
6. at most one production GET is selected as the minimal future observation;
7. if no repeat is warranted, result is no-capture-needed;
8. if repeat is warranted but no exact ready request exists, result is blocked;
9. if multiple requests exist, I038 requires a one-request replan rather than widening authorization;
10. a single-request existing plan may produce only an inert authorization draft with authorization still false;
11. eight deterministic tests passed in an isolated local harness;
12. no DNS/HTTP, credentials or action path was used.

## Immediate next run: I039
Create a deterministic minimal-plan reducer. For an I038 multi-request replan decision, reconstruct an exact one-request I029/I030-compatible session/preflight pair bound to the chosen request while preserving source, evidence, provenance, rate, manifest and safety semantics. If I038 says no capture is needed, emit a no-op reducer result. Still no real network request.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
