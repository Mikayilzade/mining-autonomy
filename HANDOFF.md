# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I094 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I094_NATIVE_EXACT_HTTPS_HARDENING.md`
- `implementation/native_exact_https_hardening.py`
- `implementation/final_real_observation_review_packet.py`
- `implementation/final_real_observation_decision.py`
- `implementation/final_network_adapter_invocation_gate.py`
- `implementation/final_single_use_transport_executor.py`

## I094 result
The I092/I093 canonical `https_path_query` contract is now enforced directly by the native I086/I087/I089/I090 entry points. Missing, non-canonical or drifted path/query data fails closed before transport. I089 emits the bound path into `request_spec`; I090 independently rejects malformed/missing path before calling an injected transport.

Native/downstream fixtures were migrated and exact-path regressions passed. The full pull-request suite finished at **634 passed / 48 failed**; the remaining failures are broad unrelated baseline/fixture debt rather than I094 exact-path failures. No live DNS/HTTP, credentials, spend, task acceptance, submission or value movement occurred.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only request -> explicit final review/decision -> fresh-evidence authorization consumption -> I089 final invocation gate -> I090 single-use executor -> I091 concrete pinned HTTPS/JSON boundary -> I092 exact path/query contract -> I093 fresh-lineage integration -> I094 native-builder regression hardening -> I095 baseline-control isolation -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I095
Run a control/baseline isolation pass for the 48 unrelated full-suite failures, preferably comparing the same complete test suite against current `main` without widening into broad refactoring. Record a stable focused I086–I094 regression set. If control proves the failures pre-existed, preserve them as baseline debt rather than mixing them into this safety chain. Remain offline/synthetic.

After I095, a fresh review packet may be prepared, but **no production request may be sent until a new explicit user authorization is bound to the exact one-shot packet and fresh policy/DNS evidence**.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; current implementation workflow is manual/pull-request only. Root documentation changes do not trigger it; `implementation/**` changes do trigger the pull-request suite.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
