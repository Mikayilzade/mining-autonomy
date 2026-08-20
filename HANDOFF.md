# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I041 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I041_AUTHORIZATION_CONSENT.md`
- `implementation/authorization_consent.py`
- `implementation/test_authorization_consent.py`
- `implementation/RUN_I040_EXACT_AUTHORIZATION_REQUEST.md`
- I039 and prior authorization/readiness/capture files named in STATUS.

## I041 result
`verify_explicit_authorization_consent()` verifies only an explicit decision object bound to the exact I040 packet/request/scope and still inside the I040 TTL.

Important behavior:
1. I040 wrapper, inner request and scope hashes are independently revalidated;
2. only the exact-ready I040 state is eligible;
3. scope must remain exactly one production GET;
4. credentials and action remain forbidden;
5. the decision must be explicit `authorize` or `deny`;
6. decision binds wrapper hash, request hash and scope hash;
7. human scope acknowledgement is mandatory;
8. decision time must be inside the I040 request window and not future-dated;
9. widened max_requests/method/credentials/action scope fails closed;
10. authorize can emit a short-lived hash-bound execution authorization, but transport remains disabled;
11. deny emits no execution authorization;
12. synthetic fixtures are explicitly labeled and are never treated as real user consent;
13. eight deterministic tests passed locally;
14. no DNS/HTTP or external action occurred.

## Immediate next run: I042
Create a deterministic offline single-use authorization lease/consumption gate over I041. Bind one future execution attempt to the exact execution-authorization hash, enforce expiry and max_requests=1, reject replay/double-consumption, and keep transport disabled/dependency-injected. Use synthetic fixtures only; do not perform real DNS/HTTP.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
