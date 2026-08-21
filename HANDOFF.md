# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I071 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I071_OBSERVATION_AUTHORIZATION_LEASE.md`
- `implementation/observation_authorization_lease.py`
- `implementation/test_observation_authorization_lease.py`
- `implementation/RUN_I070_HUMAN_DECISION_VERIFIER.md`

## I071 result
The project now has a deterministic single-use observation authorization lease over an explicit I070 authorize record. Issuance revalidates I070 and I069 hashes, keeps one anonymous production GET only, inherits/caps expiry to the I069 request window, and carries max-consumptions=1.

Synthetic consumption validates the exact attempt, forbids credentials/actions/network callbacks, verifies prior consumption receipt hashes and rejects replay/double-consumption. The lease and receipt remain offline artifacts; no real transport path exists.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market-side readiness -> exact human-decision request -> explicit decision verifier -> single-use observation lease -> lease-bound network-incapable transport handoff -> later separately reviewed real read-only transport`.

## Immediate next run: I072
Build a deterministic dependency-injected lease-bound transport handoff over I071. Accept only a fresh exact I071 synthetic consumption receipt, bind it to the lease/verification/request/scope hashes, and hand one immutable GET envelope to a network-incapable injected adapter. Reject stale/replayed/unbound/tampered receipts; perform no real DNS/HTTP.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. A future approval for one read-only observation must not imply any broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Authorization boundary
I069 request, I070 verified authorization, and I071 lease/consumption records are separately hash-bound. I071 is single-use and time-limited. Synthetic consumption is not evidence that a real network call occurred. Any future real transport must independently preserve the exact one-GET/no-credentials/no-action scope.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; do not create documentation-only notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
