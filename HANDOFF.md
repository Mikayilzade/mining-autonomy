# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I040 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I040_EXACT_AUTHORIZATION_REQUEST.md`
- `implementation/exact_authorization_request.py`
- `implementation/test_exact_authorization_request.py`
- `implementation/RUN_I039_MINIMAL_PLAN_REDUCER.md`
- I038 and prior authorization/readiness/capture files named in STATUS.

## I040 result
`build_exact_authorization_request()` converts only I039's exact reduced one-request plan into a human-reviewable inert authorization-request packet.

Important behavior:
1. I039 reduction hash and inert flags are independently revalidated;
2. only `reduced_to_exact_single_get_plan` constructs a concrete request packet;
3. reduced session plan and reduced full preflight are independently hashed and bound;
4. exactly one production GET is required;
5. the request-binding hash is independently recomputed;
6. session-plan step and transport envelope must match exactly;
7. scope preserves source, host, manifest item, evidence classes, provenance, rate and timeout semantics;
8. TTL is constrained to 60–900 seconds;
9. human-readable scope explicitly states one GET, no credentials, no action and expiry;
10. authorization nonce/token remain null and authorization remains false;
11. no-capture, blocked and already-minimal I039 states stay non-actionable;
12. eight deterministic tests passed locally;
13. no DNS/HTTP or external action occurred.

## Immediate next run: I041
Create a deterministic offline authorization-consent verifier over I040. It must require a future explicit decision object bound to the exact I040 request/scope and TTL. Use synthetic consent fixtures only. Do not treat previous chat messages as consent and do not enable real transport.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
