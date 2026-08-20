# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I031 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I031_SYNTHETIC_EXECUTION_GATE.md`
- `implementation/execution_gate.py`
- `implementation/test_execution_gate.py`
- I030 preflight and prior capture pipeline files named in STATUS.

## I031 result
`execute_synthetic_read_only()` adds an authorization-to-execution gate around the I030 `ReadOnlyGetTransport` contract, but only with dependency-injected synthetic resolver/transport implementations.

Important behavior:
1. explicit exact-plan authorization is validated before resolver or transport invocation;
2. current time is injected deterministically and expired authorization fails before any dependency call;
3. each preflight request envelope is independently re-hashed before execution;
4. DNS resolution is a separate dependency and every returned address must be globally routable before GET;
5. 3xx responses or any `Location` header are rejected; no redirect following exists;
6. declared and actual response lengths are capped;
7. only allowlisted media types are accepted;
8. response receipts bind request hash, source URL, status, DNS result, media type, byte count and body SHA-256;
9. credentials/actions remain false and the execution receipt explicitly states synthetic transport only / no real network calls.

Verification: seven deterministic gate-focused tests passed in an isolated local harness. Full repository pytest was not invoked in this run; push-triggered CI remains disabled and workflow unchanged.

## Immediate next run: I032
Build the deterministic response-to-sanitized-capture bridge from I031 response receipts into the existing sealed receipt/evidence ingestion path. Use synthetic payloads only. Bind exact receipt hashes, content type, evidence classes and provenance timestamps; malformed/unexpected/oversized data must fail closed. Still no real HTTP/DNS.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules, or other access controls. Real network capture still requires separate explicit read-only authorization.

## Git/CI
Prefer one coherent commit per implementation run. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
