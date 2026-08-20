# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I044 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I044_REAL_TRANSPORT_PROPOSAL.md`
- `implementation/real_transport_proposal.py`
- `implementation/test_real_transport_proposal.py`
- `implementation/RUN_I043_EXECUTION_WRAPPER.md`
- I042 and prior authorization/readiness/capture files named in STATUS.

## I044 result
`build_real_transport_integration_proposal()` adds an inert proposal boundary over the exact I042/I043 one-GET scope.

Important behavior:
1. the I042 single-use lease hash/scope is independently revalidated;
2. the I043 execution request hash and lease/authorization bindings are independently revalidated;
3. scope remains exactly one production GET with no credentials/action;
4. proposal creation must occur inside the lease validity window;
5. exact request/lease/authorization/target scope is hash-bound;
6. seven mandatory future gates are recorded: fresh explicit real-user authorization, separate transport implementation review, DNS/destination policy, redirect policy, response resource limits, current source/ToS compliance evidence, and durable receipt binding;
7. synthetic or inferred consent is explicitly unacceptable;
8. the proposal carries no token, nonce, callback or network-capable object;
9. authorization/transport/network/value-movement flags remain false;
10. eight deterministic tests passed locally, including monkeypatched socket/getaddrinfo checks proving proposal construction does not call network primitives;
11. no DNS/HTTP or external action occurred.

## Immediate next run: I045
Build a deterministic offline review/approval packet over I044. Present the exact proposal and unresolved gates as a human-auditable checklist; distinguish `ready_for_human_decision` from `blocked_by_missing_evidence`; require current source-compliance evidence metadata; do not create or infer real authorization and do not enable transport.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
