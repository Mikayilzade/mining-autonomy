# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I039 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I039_MINIMAL_PLAN_REDUCER.md`
- `implementation/minimal_plan_reducer.py`
- `implementation/test_minimal_plan_reducer.py`
- `implementation/RUN_I038_AUTHORIZATION_READINESS.md`
- I037 and prior capture/readiness/session/preflight files named in STATUS.

## I039 result
`build_minimal_plan_reduction()` converts an I038 multi-request replan decision into one exact inert I029/I030-compatible plan/preflight pair.

Important behavior:
1. I038 decision hash and original I028/I029/I030 hashes are independently revalidated;
2. every original request-binding hash is checked before selection;
3. the I038 target must match exactly one original envelope and one session step;
4. source URL, host, GET method, manifest item, environment, evidence, provenance, rate and timeout are preserved;
5. the selected step is renumbered to sequence 1 only for the new one-request plan;
6. old/new request-binding hashes remain explicit because sequence is part of the binding;
7. unselected originally planned requests become deferred with `minimal_authorization_scope_reduction` provenance;
8. the reduced I030 preflight binds the original I028 readiness packet and new I039 session-plan hash;
9. no-capture, already-minimal and blocked I038 states do not create a new actionable plan;
10. authorization remains false, credentials/network/action remain disabled;
11. eight deterministic tests passed in an isolated local harness;
12. no DNS/HTTP or external action occurred.

## Immediate next run: I040
Create a deterministic exact-authorization request packet over the I039 reduced one-request plan. Bind the reduced session/preflight hashes, exact GET scope, TTL and human-readable summary while still keeping authorization false, no usable nonce/credential and no network activity. Preserve no-op/blocked/already-minimal states.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
