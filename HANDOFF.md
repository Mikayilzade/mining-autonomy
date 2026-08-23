# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I144 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest broad stage: `implementation/RUN_I142_I144_MARKET_SOURCE_EVIDENCE.md`.

## Current control chain
`I113 exact runtime -> I128/I129 local resource measurement -> I050/I066/I123 -> I130/I131/I133 conservative economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142 source evidence -> I143 source selection -> I140 bounded observation design -> I141 economic-test packet`.

I142/I143 prevent a public-looking market from being treated as observation-ready until task-read auth, fees/payout, polling/rate, geography/access and automation-permission facts are current and non-conflicting. I144 performed a narrow implementation revalidation, not broad discovery. Zentience remains blocked because current indexed fee semantics conflict and rate/geography/automation-scope evidence is incomplete.

## Immediate next broad run
Resolve one concrete machine-task source to I142 completeness from authoritative current public material. If Zentience cannot be resolved, explicitly defer/reject it and move to the next already-shortlisted machine-task source; do not restart broad discovery. When exact-current execution becomes available, also run the full local resource/runtime chain and rerun I136/I138 in the same broad stage where practical.

Only after both resource readiness and source evidence pass should I140/I141 be instantiated and exact bounded read-only observation authorization requested. Positive read-only economics still does not authorize paid task acceptance.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, registration, CAPTCHA/geofence/rate-limit/product-limit bypass or value movement without separate explicit authorization. No production market task-list GET has occurred yet.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Permitted sub-hour watchers use cheap polling -> local dedupe/filter -> selective AI only within provider limits. Fixed/sunk and marginal cost, energy, quota/opportunity cost, API/model fees, retries, maintenance, watcher/observation overhead and payment risk remain separate. Free/conditional CI is not assumed unlimited/free; paid APIs and future VPS preserve authorization gates.

## Git/CI
Keep automatic runtime triggers disabled. Prefer broad coherent stages and fail-closed artifacts over notification-generating expected failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.