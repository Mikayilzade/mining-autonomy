# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I116 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I116_RUNTIME_RUNNER_STALE_ARTIFACT_TIMEOUT_HARDENING.md`
- `implementation/i113_local_runtime_chain_runner.py`
- `implementation/RUN_I115_NOTIFICATION_SAFE_MANUAL_RUNTIME_BACKEND.md`
- `.github/workflows/implementation-tests.yml`
- `implementation/RUN_I114_RUNTIME_AVAILABILITY_RECHECK.md`
- `implementation/RUN_I113_LOCAL_RUNTIME_CHAIN_RUNNER.md`
- `implementation/RUN_I112_I111_MANIFEST_OFFLINE_VERIFIER.md`
- `implementation/i112_i111_manifest_offline_verifier.py`
- `implementation/RUN_I111_PREOBSERVATION_ARTIFACT_MANIFEST.md`
- `implementation/i111_preobservation_artifact_manifest.py`
- `implementation/RUN_I110_I109_RESULT_CHAIN_CONTRACT.md`
- `implementation/i110_i109_result_chain_contract.py`
- `implementation/RUN_I109_LINEAGE_PREAUTHORIZATION_CONSISTENCY.md`
- `implementation/i109_lineage_preauthorization_consistency.py`
- `implementation/RUN_I108_RUNTIME_RECEIPT_LINEAGE_ANTI_REPLAY.md`
- `implementation/i108_runtime_receipt_lineage_validator.py`
- `implementation/RUN_I107_RUNTIME_RECEIPT_BINDING_CONTRACT.md`
- `implementation/i107_runtime_receipt_binding_validator.py`
- `implementation/RUN_I106_NOTIFICATION_SAFE_LOCAL_RUNTIME_RECEIPT_HARNESS.md`
- `implementation/i106_local_runtime_receipt.py`
- `implementation/RUN_I105_PREAUTHORIZATION_CONSISTENCY_VALIDATION.md`
- `implementation/i105_preauthorization_consistency_validator.py`
- `implementation/RUN_I104_PREAUTHORIZATION_BLOCKER_REPORT.md`
- `implementation/I104_PREAUTHORIZATION_BLOCKERS.json`
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

## I116 result
I116 fixed two concrete correctness defects in the already-selected I113 runtime path. I113 now removes each step's expected output immediately before that step, so stale artifacts cannot be mistaken for fresh evidence, and it catches timeout/process-launch failures so they become explicit `FAIL_CLOSED` receipt entries instead of escaping before the receipt is written. The I113 receipt schema is now v2 and PASS requires return code 0 plus a fresh expected output.

I115 remains the execution backend: `.github/workflows/implementation-tests.yml` is manual-only `workflow_dispatch`, read-only and notification-safer than the former PR-triggered path. The available connector still cannot dispatch that workflow, so no runtime result was fabricated.

Current state remains `BLOCKED`: fresh-real evidence absent; eligible non-synthetic current route absent; exact authorization absent; current exact-source runtime regression receipt chain absent.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query contract -> I093 fresh-lineage integration -> I094 native-builder regression hardening -> I095 baseline-control isolation -> I096 fresh exact blocked review packet -> I097 offline packet verifier/authorization binding -> I098 fresh evidence artifact contract -> I099 synthetic evidence sequencing/I097 projection -> I100 execution-readiness manifest -> I101 fresh-real-evidence/route-materialization contract -> I102 compatibility adapter/synthetic fixtures -> I103 synthetic-route quarantine hardening -> I104 blocker separation -> I105 deterministic consistency validation -> I106 notification-safe local runtime receipt harness -> I107 receipt binding contract -> I108 exact-source lineage/stale-replay hardening -> I109 lineage-aware preauthorization consistency -> I110 exact I109 result/source-chain contract -> I111 compact pre-observation artifact manifest -> I112 offline exact-current I111 manifest verifier -> I113 v2 one-command repository-local runtime chain -> I115 manual-only GitHub-hosted execution backend -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run
Do **not** add another source-only safety layer unless implementation inspection finds a concrete new gap.

When manual dispatch capability is available, run `implementation-runtime-chain` once on current `main`. Only if I113 v2 returns `PASS_BLOCKED` may the runtime-regression evidence be treated as current. Even then, fresh-real market/policy/DNS/TLS/rebinding evidence, a current materialized eligible non-synthetic Resource Router route with positive conservative margin, and exact explicit user authorization remain separate independent blockers.

Do not perform the production GET and do not revive automatic PR CI solely to create evidence.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. I048-I067 implement the core Resource / Execution Router; I101 defines production route materialization; I102 proves the network-inert compatibility shape; I103 quarantines synthetic provenance; I104 separates the four preauthorization blockers; I105-I112 preserve exact source/result lineage; I113 v2 orchestrates the local chain with fresh-output/timeout hardening; I115 is the manual-only free/conditional CI execution backend. Only genuinely available programmatic backends with current reproducible non-synthetic evidence may be live candidates. Resource routing never widens market/policy eligibility.

Future watchers may poll faster than hourly using Python/webhook/WebSocket/cron only when API/ToS permits. They should use cheap polling -> local filter/dedupe -> AI only for promising work and must not attempt to bypass ChatGPT scheduling limits or platform controls.

## Git/CI
Prefer one coherent commit per run where tooling permits. Keep push-triggered CI disabled. The implementation runtime workflow is manual-only. Avoid repeated failing CI solely for baseline evidence because it can generate GitHub email spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
