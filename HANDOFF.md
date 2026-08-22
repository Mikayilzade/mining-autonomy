# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I083 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I083_EXACT_REAL_READ_ONLY_INVOCATION_DECISION.md`
- `implementation/exact_real_read_only_invocation_decision.py`
- `implementation/test_exact_real_read_only_invocation_decision.py`
- `implementation/RUN_I082_EXACT_REAL_READ_ONLY_INVOCATION_REQUEST.md`
- `implementation/exact_real_read_only_invocation_request.py`

## I083 result
The I082 one-GET human-review request now has a deterministic fresh explicit decision verifier. It revalidates the exact request hash/state/TTL, exact scope/hash, adapter and synthetic invocation lineage, implementation/source/readiness bindings and inert safety flags. The human decision must preserve every binding and remain single-use with credentials/task acceptance/submission/value movement forbidden.

Deny emits no authorization. Authorize emits only a short-lived request-expiry-capped single-use unconsumed authorization for at most one future network request. Prior decision hashes may be supplied to fail closed on replay. The verifier itself never exposes network-capable transport or performs DNS/HTTP.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only invocation request -> fresh explicit I083 decision -> single-use I084 preflight -> separately authorized one-shot real observation`.

## Immediate next run: I084
Build the exact single-use consumption/preflight for the I083 authorization. Require a live unconsumed hash-valid authorization bound to the exact I082 request and I083 decision, unchanged one-GET scope and source lineage. Reject replay, expiry and tampering. Emit only one zero-network attempt envelope plus a hash-bound consumption receipt; do not perform DNS/HTTP.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
