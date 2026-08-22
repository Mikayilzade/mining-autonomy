# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I103 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I103_SYNTHETIC_RESOURCE_ROUTE_QUARANTINE.md`
- `implementation/i100_execution_readiness_manifest.py`
- `implementation/RUN_I102_I101_I100_COMPATIBILITY_ADAPTER.md`
- `implementation/I102_SYNTHETIC_COMPATIBILITY_FIXTURES.json`
- `implementation/i102_i101_i100_compatibility_adapter.py`
- `implementation/RUN_I101_FRESH_REAL_EVIDENCE_ROUTE_CONTRACT.md`
- `implementation/I101_FRESH_REAL_EVIDENCE_ROUTE_CONTRACT.json`
- `implementation/i101_fresh_real_evidence_route_contract.py`
- `implementation/RUN_I100_EXECUTION_READINESS_MANIFEST.md`
- `implementation/I100_EXECUTION_READINESS_RESULT.json`
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

## I103 result
The preferred notification-safe isolated runtime path was attempted first, but the available local environment could not resolve GitHub. Repeated failing PR CI was intentionally not used merely to produce evidence.

The fallback specified by the previous `STATUS.md` was therefore completed: I100 now independently rejects any Resource / Execution Router route with `synthetic_fixture=true`. Even when `current_materialized_resource`, `policy_eligible`, `capacity_available` and `conservative_margin_positive` are all true, `resource_route_not_synthetic=false`, `resource_route_eligible=false`, and the readiness result remains `BLOCKED`.

A dedicated all-green-but-synthetic regression was added to I100 `_self_test`. Runtime execution of the self-test remains verification debt; I103 does not claim runtime PASS.

The current chain remains `BLOCKED`: no fresh real policy/DNS/TLS/rebinding evidence exists, no current eligible non-synthetic Resource Router route is materialized, no exact explicit authorization exists, and the I099-I102/I100 runtime regression receipt remains absent. No production DNS/HTTP/socket/TLS call, credentials, bidding, task acceptance, spend or value movement occurred. No CI workflow was dispatched.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query contract -> I093 fresh-lineage integration -> I094 native-builder regression hardening -> I095 baseline-control isolation -> I096 fresh exact blocked review packet -> I097 offline packet verifier/authorization binding -> I098 fresh evidence artifact contract -> I099 synthetic evidence sequencing/I097 projection -> I100 execution-readiness manifest -> I101 fresh-real-evidence/route-materialization contract -> I102 compatibility adapter/synthetic fixtures -> I103 synthetic-route quarantine hardening -> I104 local verification receipt/preauthorization blocker separation -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I104
Prefer a **notification-safe local verification receipt harness** when an isolated repository runtime is actually available. It should run I099, I100, I101 and I102 embedded self-tests, hash exact module versions, and emit one machine-readable PASS/FAIL receipt without GitHub Actions, network transport, production evidence acquisition or authorization creation.

If runtime execution remains unavailable, add a machine-readable preauthorization blocker report keeping these categories distinct and non-substitutable: fresh-real execution evidence; current materialized non-synthetic route; exact explicit authorization; runtime-regression verification debt.

Do not perform the production GET and do not repeatedly push failing PR CI solely for evidence.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. I048–I067 implement the core Resource / Execution Router; I101 defines production route materialization; I102 proves the network-inert compatibility shape; I103 independently quarantines synthetic route provenance at I100. Only genuinely available programmatic backends with current reproducible non-synthetic evidence may be live candidates. Resource routing never widens market/policy eligibility.

Future watchers may poll faster than hourly using Python/webhook/WebSocket/cron only when API/ToS permits. They should use cheap polling -> local filter/dedupe -> AI only for promising work and must not attempt to bypass ChatGPT scheduling limits or platform controls.

## Git/CI
Prefer one coherent commit per run where tooling permits. Keep push-triggered CI disabled; implementation workflow remains manual/pull-request only. Root documentation changes do not trigger it. Avoid repeated failing PR pushes solely for baseline evidence because they can generate GitHub email spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
