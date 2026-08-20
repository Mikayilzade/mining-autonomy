# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I030 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I030_TRANSPORT_PREFLIGHT.md`
- `implementation/transport_preflight.py`
- `implementation/test_transport_preflight.py`
- I029 session-planner and I028 readiness files named in STATUS.

## I030 result
`build_transport_preflight()` converts the I029 deterministic session plan plus the exact I028 readiness packet into integrity-bound, transport-inert request envelopes.

Important behavior:
1. every step is rebound through `manifest_item_sha256` to its exact readiness source/evidence/provenance/rate contract;
2. plan, readiness packet, envelope set and each request binding are SHA-256 bound;
3. source/host/schedule/manifest tampering, duplicate planned items, POST, credentials, actions and non-production rows fail closed;
4. localhost/private/non-global literal IP endpoints are rejected before transport;
5. future DNS execution policy must resolve then reject non-global addresses to reduce SSRF/DNS-rebinding risk;
6. `ReadOnlyGetTransport` is only a protocol contract and is not instantiated or called;
7. explicit read-only authorization is a separate exact-plan-hash envelope; its validator returns an inert validation receipt only;
8. transport/network/action flags remain false.

Verification: ten deterministic tests passed in an isolated local harness. GitHub Actions workflow was unchanged and push-triggered CI remains disabled.

## Immediate next run: I031
Build a deterministic authorization-to-execution gate around `ReadOnlyGetTransport` using only a fake/in-memory transport. Bind response receipts to request hashes and enforce redirect, DNS-resolution result, response-size and content-type limits at the adapter boundary. Prove absent/expired/mismatched authorization cannot invoke transport. Still perform no real HTTP request.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules, or other access controls. Real network capture still requires separate explicit read-only authorization.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
