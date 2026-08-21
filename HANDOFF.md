# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I075 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I075_REAL_TRANSPORT_AUTHORIZATION_CONSUMPTION.md`
- `implementation/real_transport_authorization_consumption.py`
- `implementation/test_real_transport_authorization_consumption.py`
- `implementation/RUN_I074_REAL_TRANSPORT_AUTHORIZATION.md`

## I075 result
The exact pre-real-transport chain now includes deterministic single-use consumption of the I074 authorization. I075 revalidates I074 verification/authorization hashes and exact review/decision/scope bindings, enforces issue/expiry time and `max_consumptions=1`, and rejects replay/double-consumption.

A successful consumption creates only a hash-bound `single_use_real_transport_authorized_attempt_envelope`. It contains mandatory DNS resolution/private-address/pinning/rebinding gates, zero automatic redirects, a 1 MiB JSON-only response policy, and fresh first-party anonymous-read-only source-policy requirements. It still has no transport adapter and cannot perform DNS/HTTP.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market-side readiness -> exact human-decision request -> explicit observation decision verifier -> synthetic/offline lease rehearsal -> network-incapable handoff -> pre-real-transport review -> explicit real-transport decision verifier -> single-use authorization consumption/preflight -> adapter contract validation -> separately authorized exact real read-only observation`.

## Immediate next run: I076
Build a deterministic network-capable adapter contract validator over I075. Require a future adapter declaration to prove it can enforce the exact one-request/no-credentials/no-action scope plus every DNS/redirect/response/source-policy gate. Do not make the adapter executable and do not perform DNS/HTTP.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
