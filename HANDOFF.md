# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I074 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I074_REAL_TRANSPORT_AUTHORIZATION.md`
- `implementation/real_transport_authorization.py`
- `implementation/test_real_transport_authorization.py`
- `implementation/RUN_I073_PRE_REAL_TRANSPORT_REVIEW.md`

## I074 result
The exact pre-real-transport chain now includes a deterministic explicit decision verifier over I073. It independently revalidates the I073 packet hash/state/scope/inert flags and accepts only a fresh, human-acknowledged decision bound to the exact `pre_real_transport_review_sha256` plus exact scope hash.

Authorize decisions must reproduce the exact one-production-GET/no-credentials/no-action scope. Stale, replayed, future-dated, pre-review, tampered or widened decisions fail closed. A clean explicit deny creates no authorization. A clean explicit authorize can create only a 30–300 second hash-bound single-use authorization record with `max_consumptions=1`; it does not enable DNS/HTTP or any value-moving capability.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market-side readiness -> exact human-decision request -> explicit observation decision verifier -> synthetic/offline lease rehearsal -> network-incapable handoff -> pre-real-transport review -> explicit real-transport decision verifier -> single-use real-transport authorization consumption/preflight -> separately authorized exact real read-only observation`.

## Immediate next run: I075
Build a deterministic single-use consumption/preflight gate over the I074 authorization record. Revalidate the verification record, authorization record, decision/review/scope bindings and expiry; reject replay/double-consumption; emit only an immutable authorized-attempt envelope carrying mandatory DNS/redirect/response-size/content-type/source-policy gates. Keep network transport absent.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
