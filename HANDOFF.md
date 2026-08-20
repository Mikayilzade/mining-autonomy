# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I042 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I042_AUTHORIZATION_LEASE.md`
- `implementation/authorization_lease.py`
- `implementation/test_authorization_lease.py`
- `implementation/RUN_I041_AUTHORIZATION_CONSENT.md`
- I040 and prior authorization/readiness/capture files named in STATUS.

## I042 result
`issue_single_use_authorization_lease()` and `consume_single_use_authorization_lease()` add a replay-safe offline one-request budget over exact I041 authorization.

Important behavior:
1. I041 consent-verification and embedded execution-authorization hashes are independently revalidated;
2. only a valid `authorize` result is leaseable;
3. lease scope remains exactly one production GET;
4. credentials/action/transport remain forbidden;
5. the lease inherits the original authorization expiry and cannot be issued outside that window;
6. a synthetic attempt is hash-bound to both lease and execution authorization;
7. widened request count/method/environment/credentials/action is rejected;
8. prior consumption receipts are hash-validated;
9. any prior valid consumed receipt for the same lease causes replay/double-consumption rejection;
10. successful offline consumption emits zero remaining requests;
11. no DNS/HTTP occurs and consumption is not evidence a network request happened;
12. synthetic-fixture status is preserved;
13. eight deterministic tests passed locally.

## Immediate next run: I043
Create a deterministic dependency-injected execution wrapper over I042. It must consume a fresh lease before invoking transport, use a synthetic stub by default, and expose a hard `allow_real_transport=False` default. Tests must prove no real transport path is available by default. Do not perform real DNS/HTTP.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
