# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I087 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I087_FINAL_REAL_OBSERVATION_DECISION.md`
- `implementation/final_real_observation_decision.py`
- `implementation/RUN_I086_FINAL_REAL_OBSERVATION_REVIEW_PACKET.md`
- `implementation/final_real_observation_review_packet.py`
- `implementation/RUN_I085_REAL_TRANSPORT_SAFETY_PREFLIGHT.md`

## I087 result
The exact I086 final review packet now has an explicit final decision verifier. Only a fresh exact packet-hash-bound `authorize`/`deny` decision inside the packet TTL is accepted. Deny emits no authorization. Authorize emits at most a short-lived single-use unconsumed authorization capped by packet expiry and bound to the exact adapter/target/scope/source/hostname/pinned-address/evidence/transport contract.

The authorization remains inert: network-capable transport is unreachable, and execution-time safety-evidence freshness plus DNS pinning/anti-rebinding revalidation remain mandatory. It is not task/payment permission and no DNS/HTTP occurred.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only invocation request -> fresh explicit I083 decision -> single-use I084 preflight -> injected-evidence I085 transport safety -> immutable I086 final human review packet -> explicit I087 final decision -> separately consumed one-shot real observation`.

## Immediate next run: I088
Build a separately consumed final authorization preflight over I087 + exact I086 packet. Revalidate authorization freshness/single-use state and exact bindings, require fresh injected I085-style safety/DNS evidence at consumption time, reject replay, and emit only a zero-network one-attempt execution envelope plus receipt. Do not perform DNS/HTTP.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
