# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I090 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I090_SINGLE_USE_TRANSPORT_EXECUTOR.md`
- `implementation/final_single_use_transport_executor.py`
- `implementation/test_final_single_use_transport_executor.py`
- `implementation/RUN_I089_FINAL_NETWORK_ADAPTER_INVOCATION_GATE.md`
- `implementation/final_network_adapter_invocation_gate.py`

## I090 result
The I089 one-shot gate now has a deterministic dependency-injected executor. It rejects stale/tampered/replayed gates before touching the callable, consumes the attempt on callable exception or rejected result, and accepts only a one-request pinned-peer/TLS-hostname/no-re-resolution/zero-redirect/valid-JSON/bounded-size result. Success emits a hash-bound invocation receipt and response attestation.

The executor itself performs no DNS/HTTP and confers no credentials/task/payment/value permission. A future concrete live adapter must derive its transport claims from actual socket/TLS state rather than untrusted result metadata.

## Target flow
`cheap watcher -> local filter/dedupe -> policy/rights/quality/demand gate -> TaskEconomics -> evidence-calibrated Resource Router -> measured feedback/current resource materialization -> market readiness -> exact human-decision/authorization lineage -> network-incapable handoff/review -> adapter/source binding -> activation request/decision/consumption -> synthetic invocation-bound replay -> exact real-read-only invocation request -> explicit final review/decision -> I088 fresh-evidence authorization consumption -> I089 final network-capable invocation gate -> I090 single-use transport executor -> I091 concrete attested transport boundary -> separately authorized one-shot real observation -> measured demand/economics feedback`.

## Immediate next run: I091
Build a concrete pinned-address HTTPS/JSON transport boundary whose peer-IP, TLS/SNI, redirect and byte-limit metadata is derived from the adapter itself. Test it only with offline/injected socket/TLS/HTTP doubles. No live request until a fresh exact authorization/safety chain separately permits one read-only observation.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. One read-only observation can never imply broader permission.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Only genuinely available programmatic backends with current reproducible evidence may be future live candidates.

## Git/CI
Prefer one coherent commit per run. Keep push-triggered CI disabled; current implementation workflow is manual/pull-request only and documentation changes alone do not trigger it.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
