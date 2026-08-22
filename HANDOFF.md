# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I098 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.md`
- `implementation/I098_FRESH_EXECUTION_EVIDENCE_CONTRACT.json`
- `implementation/i098_fresh_execution_evidence_contract.py`
- `implementation/RUN_I097_OFFLINE_PACKET_VERIFIER.md`
- `implementation/I097_OFFLINE_PACKET_VERIFICATION_RESULT.json`
- `implementation/i097_offline_packet_verifier.py`
- `implementation/RUN_I096_FRESH_ONE_SHOT_REVIEW_PACKET.md`
- `implementation/I096_FRESH_ONE_SHOT_REVIEW_PACKET.json`
- `implementation/RUN_I095_BASELINE_CONTROL_ISOLATION.md`
- `implementation/RUN_I094_NATIVE_EXACT_HTTPS_HARDENING.md`
- `implementation/final_real_observation_review_packet.py`
- `implementation/final_real_observation_decision.py`
- `implementation/final_network_adapter_invocation_gate.py`
- `implementation/final_single_use_transport_executor.py`

## I098 result
The exact I096 production observation now has a deterministic fresh-evidence artifact contract. `i098_fresh_execution_evidence_contract.py` is stdlib-only and network-incapable. It requires four hash-bound components — current official policy/ToS evidence, fresh DNS/public-IP pins, fresh TLS/transport evidence connected to one of those pins, and an immediate anti-rebinding revalidation reproducing the same public-address set.

All evidence remains bound to packet SHA-256 `0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56`, scope SHA-256 `df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e`, and the exact one-shot `GET` target. Freshness is fail-closed: policy 6h, DNS/TLS 5m, anti-rebinding 60s, with final expiry equal to the earliest component expiry. Private/loopback/reserved pins are rejected; exact path drift is rejected.

Embedded offline self-tests passed using synthetic evidence. Current production state is still deliberately `BLOCKED`: no fresh real evidence and no explicit user authorization exist. The I098 artifact itself has `network_capable=false`, `execution_token=false` and can never authorize transport.

No DNS/HTTP, credentials, bidding, task acceptance, spend or value movement occurred. No CI workflow was dispatched.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query contract -> I093 fresh-lineage integration -> I094 native-builder regression hardening -> I095 baseline-control isolation -> I096 fresh exact blocked review packet -> I097 offline packet verifier/authorization binding -> I098 fresh evidence artifact contract -> I099 synthetic sequencing/compatibility harness -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I099
Build a **network-inert synthetic evidence acquisition/sequencing harness**. It should prove the exact order `policy -> DNS/pins -> TLS-to-pin -> anti-rebinding -> final bundle -> I097 compatibility projection` using synthetic fixtures only and fail closed on omitted/stale/reordered/drifted evidence. Do not resolve DNS, fetch policy pages, open sockets, perform HTTP or manufacture user authorization.

After I099, the production request still cannot be sent until a new explicit user authorization is bound to the exact I096 packet and fresh real evidence exists at execution time.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. I048–I067 already provide the Resource / Execution Router and measured resource materialization/rerouting chain. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates. Resource routing never widens market/policy eligibility.

## Git/CI
Prefer one coherent commit per run where tooling permits. Keep push-triggered CI disabled; current implementation workflow is manual/pull-request only. Root documentation changes do not trigger it; `implementation/**` changes trigger only pull-request suite activity, not direct-main pushes. Avoid repeated failing PR pushes solely for baseline evidence because they can generate GitHub email spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
