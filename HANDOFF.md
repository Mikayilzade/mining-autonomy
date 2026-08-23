# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I138 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest broad stage: `implementation/RUN_I136_I138_BROAD_EXPERIMENT_READINESS.md`.

## Current control chain
`I113 exact runtime -> I128/I129 local resource measurement -> I050/I066/I123 backend evidence/base economics -> I130 stress + I131 watcher overhead -> I133 conservative route -> I136 conservative portfolio -> I137 existing-resource fallback -> I138 experiment readiness`.

I136 requires evidence and conservative economics together across the whole backend portfolio. I137 keeps fallback inside already-defined resources instead of reopening discovery. I138 emits exactly one next-action state and keeps observation/execution/network/spend/task-acceptance/value-movement disabled even when all readiness gates are true.

## Immediate next broad run
Do not split the next executable stage into micro-checkpoints. At the first exact-current executable checkout, run I113 + I128/I129 -> I050/I066/I123 -> I133/I136 -> I138 in one broad cycle. If trustworthy no-spend local energy telemetry and an explicit real tariff exist, materialize `python_local`; otherwise preserve the gap.

If local materialization/economics fails, use I137/I134 in the same broad cycle where practical to move to the next existing no-new-spend evidence branch. Under the current acquisition model that is free/conditional CI after `python_local` has been attempted. CI quota/capacity/policy must be evidenced separately and may not be inferred from a green workflow.

Fresh market/policy evidence and exact one-shot observation authorization remain independent later gates. No production GET yet.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, CAPTCHA/geofence/rate-limit/product-limit bypass or value movement without separate explicit authorization.

## Resource boundary
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API.
- Watchers may use permitted sub-hour polling via ordinary code/webhook/WebSocket/cron, but local deterministic filter/dedupe precedes selective AI and platform limits must be obeyed.
- Fixed/sunk cost, true marginal cost, energy, quota/opportunity cost, AI/API fees, retry cost, human maintenance, watcher overhead and platform/payment risk remain explicit.
- Free/conditional CI is not assumed unlimited/free; paid APIs and future VPS preserve credentials/spend/infrastructure gates.

## Git/CI
Keep automatic runtime triggers disabled. Prefer broad coherent stages. Expected fail-closed outcomes belong in artifacts rather than notification-generating failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.