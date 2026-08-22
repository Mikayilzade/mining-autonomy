# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I084 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I084_EXACT_REAL_READ_ONLY_INVOCATION_CONSUMPTION.md`
- `implementation/exact_real_read_only_invocation_consumption.py`
- `implementation/test_exact_real_read_only_invocation_consumption.py`
- `implementation/RUN_I083_EXACT_REAL_READ_ONLY_INVOCATION_DECISION.md`
- `implementation/exact_real_read_only_invocation_decision.py`

## I084 result
The exact I083 authorization can now be consumed once into a zero-network one-attempt envelope after independent revalidation of the I082 request, I083 human decision and I083 authorization. Request/decision/auth hashes, times, scope, adapter bindings, source lineage, no-credentials/no-action constraints and one-request ceiling must all remain exact. Valid prior receipts reject replay; malformed/tampered prior receipts fail closed.

The emitted envelope and receipt are inert: no network-capable adapter is reachable, no DNS/HTTP occurs, and neither artifact is an execution/payment/task token.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only invocation request -> fresh explicit I083 decision -> single-use I084 preflight -> real-transport safety preflight -> separately authorized one-shot real observation`.

## Immediate next run: I085
Build a deterministic real-transport safety preflight over the I084 envelope using injected evidence only. Require exact target/adapter/source binding, fresh first-party anonymous-read-only policy evidence, public-only DNS-resolution evidence with explicit anti-rebinding/address-pinning constraints, HTTPS/TLS-only, zero redirects, bounded JSON-only response and a one-request ceiling. Do not perform DNS/HTTP yet.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
