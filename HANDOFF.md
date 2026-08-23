# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I132 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest broad stage: `implementation/RUN_I130_I132_BROAD_RESOURCE_ECONOMICS.md`.

## Current resource/economics chain
`fixed local probe + I126 config invariants + I128 quota/rate semantics + I129 verified energy receipt -> I054/I050 -> I066 -> I123 portfolio route -> I130 conservative sensitivity -> I131 watcher/acquisition overhead -> I132 pre-observation readiness`.

I130 prevents reliance on a single optimistic point estimate. I131 models a future high-frequency watcher without requiring frequent LLM calls: permitted cheap polling, local dedupe/filtering, then AI only for promising survivors. ChatGPT/Codex subscription remains fixed/sunk limited support and is not assumed to provide autonomous API access.

## Immediate next broad run
When exact-current execution becomes available, run the complete no-spend local chain in one stage: I113, I128/I129, I050/I066/I123, then I130 and I131. Emit one current conservative resource-readiness packet. If positive, prepare but do not execute the one-shot market observation authorization boundary. If local execution cannot be made reproducibly economic, move to the next already-ranked backend family rather than broad discovery.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit bypass or value movement without separate explicit authorization. No production GET yet.

## Git/CI
Keep automatic runtime triggers disabled. Prefer broad coherent stages; expected fail-closed states should be artifacts, not notification-generating CI failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.