# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory. Read repository state first.

## Resume protocol
Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in `STATUS.md`.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I147 COMPLETE as scoped checkpoints**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest broad stage: `implementation/RUN_I145_I147_PAYANAGENT_SOURCE_NARROWING.md`.

## Current control chain
`I113 exact runtime -> I128/I129 local resource measurement -> I050/I066/I123 -> I130/I131/I133 conservative economics -> I136 portfolio -> I137 fallback -> I138 readiness -> I142 source evidence -> I145 PayanAgent checkpoint -> I143 source selection -> I140 bounded observation design -> I141 economic-test packet`.

## Current source result
Zentience is deferred for the active implementation path because authoritative/public representations still leave fee/polling/geography questions insufficiently clear for I142.

PayanAgent is the active source target. Current first-party docs observed 2026-08-23 explicitly establish public request list/detail GETs, current zero platform fee, direct provider payout semantics, public endpoint rate limit of 30 requests/minute/IP, and explicit API-first autonomous/programmatic usage. The only I142 source blocker left is `geography_access_rule`; reviewed first-party material does not state supported countries/global eligibility/Azerbaijan eligibility, and documentation silence is not treated as permission.

Future observation parameters are prepared but not promoted: 5-second polling candidate interval, 20-request hard cap, public requests/receipts only, local dedupe first, stop on 401/403/429/Retry-After/challenge/geography/policy drift, and no bid/accept/fulfill/register/wallet/payment action.

## Immediate next broad run
Try one authoritative-first-party pass to resolve PayanAgent geography/access. If the provider publishes no explicit rule, preserve the blocker and move the source branch to `policy_contact_or_user-local-access-required` rather than guessing. Do not reopen discovery.

When exact-current executable checkout becomes available, run the whole resource chain in one broad cycle: I113 + I128/I129 -> I136/I138. Only after both resource readiness and source evidence pass should I140/I141 be instantiated and exact bounded read-only observation authorization requested/used.

## Hard boundary
No spend, KYC, wallets, paid work acceptance, publication, settlement, real credentials, registration, CAPTCHA/geofence/rate-limit/product-limit bypass or value movement without separate explicit authorization. No production market task-list/receipt GET has occurred yet.

## Resource boundary
ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API. Permitted sub-hour watchers use cheap polling -> local dedupe/filter -> selective AI only within provider limits. Fixed/sunk and marginal cost, energy, quota/opportunity cost, API/model fees, retries, maintenance, watcher/observation overhead and payment risk remain separate. Free/conditional CI is not assumed unlimited/free; paid APIs and future VPS preserve authorization gates.

## Git/CI
Keep automatic runtime triggers disabled. Prefer broad coherent stages and fail-closed artifacts over notification-generating expected failures.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.