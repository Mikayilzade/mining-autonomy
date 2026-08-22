# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I099 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I099_SYNTHETIC_EVIDENCE_SEQUENCING.md`
- `implementation/i099_synthetic_evidence_sequencer.py`
- `implementation/RUN_I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.md`
- `implementation/I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.json`
- `implementation/i098_fresh_execution_evidence_contract.py`
- `implementation/RUN_I097_OFFLINE_PACKET_VERIFIER.md`
- `implementation/I097_OFFLINE_PACKET_VERIFICATION_RESULT.json`
- `implementation/i097_offline_packet_verifier.py`
- `implementation/RUN_I096_FRESH_ONE_SHOT_REVIEW_PACKET.md`
- `implementation/I096_FRESH_ONE_SHOT_REVIEW_PACKET.json`

## I099 result
A new stdlib-only network-inert sequencer now proves the intended synthetic acquisition order by reusing I098 validators rather than duplicating them: policy/ToS first, then DNS/public-IP pins, then TLS bound to one accepted pin, then immediate anti-rebinding, then final I098 bundle construction, then an I097 compatibility projection.

The state machine fails closed on reordered or invalid evidence and refuses finalization when a component is missing. Embedded negative cases cover omission, reordering, stale policy, TLS outside the pin set, exact path/query drift and anti-rebinding set drift.

The I097 compatibility projection intentionally keeps `authorization=None`. Therefore even complete synthetic evidence cannot authorize transport: exact packet/evidence compatibility may pass while authorization remains false and the combined I097 result remains `BLOCKED`.

No DNS/HTTP/socket call, credentials, bidding, task acceptance, spend or value movement occurred. No authorization was manufactured. No CI workflow was dispatched. Runtime execution of the I099 self-test remains notification-safe verification debt because no isolated local repo runner was available in this run.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query contract -> I093 fresh-lineage integration -> I094 native-builder regression hardening -> I095 baseline-control isolation -> I096 fresh exact blocked review packet -> I097 offline packet verifier/authorization binding -> I098 fresh evidence artifact contract -> I099 synthetic evidence sequencing/I097 projection -> I100 execution-readiness manifest -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I100
Build a **network-inert execution-readiness manifest / dry-run verifier**. It should consume the existing I096/I097/I098/I099 contracts and expose every remaining prerequisite as explicit booleans, including exact packet/scope integrity, sequencing-contract availability, fresh-real-evidence absence/presence, exact explicit authorization absence/presence, resource-route eligibility, request-count boundary, credentials/value-movement prohibition and final readiness.

It must not resolve DNS, fetch policy pages, open sockets, perform HTTP, create/guess user authorization, or widen any prior permission. If a notification-safe local execution facility becomes available, use it to run the I099 embedded self-test; do not create repeated PR CI failures solely for evidence.

The production request still cannot be sent until a new explicit user authorization is bound to the exact I096 packet/scope and fresh real execution evidence exists at execution time.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. I048–I067 already provide the Resource / Execution Router and measured resource materialization/rerouting chain. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates. Resource routing never widens market/policy eligibility.

## Git/CI
Prefer one coherent commit per run where tooling permits. Keep push-triggered CI disabled; current implementation workflow is manual/pull-request only. Root documentation changes do not trigger it; `implementation/**` changes trigger only pull-request suite activity, not direct-main pushes. Avoid repeated failing PR pushes solely for baseline evidence because they can generate GitHub email spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
