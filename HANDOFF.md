# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I096 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I096_FRESH_ONE_SHOT_REVIEW_PACKET.md`
- `implementation/I096_FRESH_ONE_SHOT_REVIEW_PACKET.json`
- `implementation/RUN_I095_BASELINE_CONTROL_ISOLATION.md`
- `implementation/I095_FOCUSED_REGRESSION_SET.txt`
- `implementation/RUN_I094_NATIVE_EXACT_HTTPS_HARDENING.md`
- `implementation/native_exact_https_hardening.py`
- `implementation/final_real_observation_review_packet.py`
- `implementation/final_real_observation_decision.py`
- `implementation/final_network_adapter_invocation_gate.py`
- `implementation/final_single_use_transport_executor.py`

## I096 result
A fresh review-only packet now binds PayanAgent to exactly one anonymous production `GET` of `https://payanagent.com/api/v1/requests?status=open&limit=1`. Current official docs were revalidated on 2026-08-22 and recorded in the packet. Exact scope SHA-256 is `df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e`; packet SHA-256 is `0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56`.

The packet is deliberately blocked: no explicit user authorization is bound, and fresh policy/ToS, DNS/pinning and TLS/transport evidence are absent. It is not an execution token. No DNS/HTTP request, credentials, bidding, registration, payment or value movement occurred. No CI workflow was dispatched because repeated failing PR runs had already caused notification spam.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query contract -> I093 fresh-lineage integration -> I094 native-builder regression hardening -> I095 baseline-control isolation -> I096 fresh exact blocked review packet -> I097 offline packet verifier/authorization binding -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I097
Implement an **offline packet verifier / authorization-binding checkpoint**. Recompute the exact I096 scope and packet hashes; reject host/path/scope drift; require any future explicit authorization artifact to name the exact I096 packet hash; reject absent/stale policy/DNS/pinning/transport evidence; keep network execution impossible. Do not perform DNS/HTTP and do not manufacture user authorization.

After I097, the production request still cannot be sent until a new explicit user authorization is bound to this exact packet and fresh policy/DNS evidence is available at execution time.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates. Resource routing never widens market/policy eligibility.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; current implementation workflow is manual/pull-request only. Root documentation changes do not trigger it; `implementation/**` changes do trigger the pull-request suite. Avoid repeated failing PR pushes solely for baseline evidence because they can generate GitHub email spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
