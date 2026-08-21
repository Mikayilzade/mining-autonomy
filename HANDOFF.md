# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I072 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I072_LEASE_BOUND_TRANSPORT_HANDOFF.md`
- `implementation/lease_bound_transport_handoff.py`
- `implementation/test_lease_bound_transport_handoff.py`
- `implementation/RUN_I071_OBSERVATION_AUTHORIZATION_LEASE.md`

## I072 result
The single-use authorization chain now reaches a dependency-injected but explicitly network-incapable adapter boundary. I072 revalidates lease/consumption hashes, exact verification/request/scope bindings and freshness, then emits one immutable anonymous production GET envelope with `network_calls_allowed=0`.

The built-in recorder only hashes the envelope. Any adapter marked network-capable is rejected before callback; any returned record claiming network activity is rejected. This is not evidence of real demand or a real network observation.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market-side readiness -> exact human-decision request -> explicit decision verifier -> single-use lease -> network-incapable handoff -> pre-real-transport review -> later separately authorized real read-only observation`.

## Immediate next run: I073
Build a deterministic pre-real-transport review packet over I072. It must revalidate the exact handoff/envelope chain and current readiness, enumerate all remaining DNS/redirect/content-type/size/source-policy/real-authorization gates, and perform no DNS/HTTP.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
