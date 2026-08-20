# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I043 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I043_EXECUTION_WRAPPER.md`
- `implementation/execution_wrapper.py`
- `implementation/test_execution_wrapper.py`
- `implementation/RUN_I042_AUTHORIZATION_LEASE.md`
- I041 and prior authorization/readiness/capture files named in STATUS.

## I043 result
`execute_with_single_use_lease()` adds a synthetic-only dependency-injected execution boundary over I042.

Important behavior:
1. the execution request is hash-bound to the exact lease and execution authorization;
2. scope remains exactly one production GET with no credentials/action;
3. `allow_real_transport=False` is mandatory in I043 and `True` fails closed;
4. network-capable/non-synthetic dependencies are rejected;
5. the wrapper consumes the I042 lease before invoking the transport callback;
6. expiry or prior-consumption replay therefore prevents callback invocation;
7. accepted transport is explicitly `synthetic_stub` and `network_capable=False`;
8. response must state `network_calls_performed=false`;
9. result binds request, lease, authorization, consumption and response hashes;
10. eight deterministic tests passed locally;
11. no DNS/HTTP or external action occurred.

## Immediate next run: I044
Build an inert deterministic real-transport integration proposal contract. It should state what exact fresh evidence, packet-bound explicit user authorization and safety gates would be required before a later integration could replace the synthetic dependency for one GET. The proposal itself must have no executable transport and tests must prove it cannot invoke network activity.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
