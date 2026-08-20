# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I048 — Resource / Execution Router foundation**
Last updated: **2026-08-20**

## Latest durable files
- `implementation/RUN_I048_RESOURCE_EXECUTION_ROUTER.md`
- `implementation/resource_router.py`
- `implementation/test_resource_router.py`
- `implementation/RUN_I047_SOURCE_COMPLIANCE_REVIEW_BRIDGE.md`
- I046 and earlier authorization/readiness/capture files.

## I048 outcome
The stack now has an explicit offline Resource / Execution Router foundation before any real monetization test. It distinguishes fixed/sunk cost from per-task marginal cost, models backend quota/capacity, latency, reliability/quality, parallelism/rate limits, electricity, API/model cost, retry/failure cost, maintenance time, opportunity cost and payment/acceptance risk.

Synthetic backend families cover deterministic local Python, local CPU/GPU/model capacity, subscription-backed ChatGPT/Codex-style assistance as a fixed/limited non-API support resource, cheap and stronger external APIs, free-tier CI/cloud, owned-PC execution and future paid VPS/server.

The router does not treat subscriptions as free unlimited APIs: subscription support remains non-programmatic/support-only unless an actual programmatic interface exists. Already-paid/sunk fixed cost is not charged in full to each task; non-sunk fixed recurring cost is only amortized when an explicit allocation basis exists.

Currently unavailable, credentialed, paid-account or new-spend backends remain planning-only and cannot outrank an available backend. Routing selects the lowest marginal-cost sufficiently reliable permitted available backend while every execution/action flag remains disabled.

A future watcher policy may use polling/webhook/WebSocket more frequently than chat-level automation only within source ToS/API/rate limits, with local deterministic filtering/deduplication before AI. I048 keeps network access disabled. Ten deterministic tests passed in an isolated local harness; GitHub Actions was not dispatched.

## Current ranking
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Durable rules
- Demand/fill rate remains the dominant unknown.
- Missing capture is not evidence of zero demand.
- Production/test environments remain isolated.
- Capture-integrity labels are not demand/profitability labels.
- Authorization/proposal/review packets and synthetic consent/compliance fixtures are not real user authorization or real compliance proof.
- I039–I047 must never widen the exact single-request scope.
- Any future real authorization must be exact-packet-bound, short-lived, GET-only, no-credentials and no-action.
- A lease is single-use; replay/expiry must fail before any transport callback.
- I043 supports synthetic network-incapable transport only; I044–I047 add proposal/review/evidence/provenance contracts only and have no executable real-network path.
- `ready_for_human_decision` means evidence is adequate to ask, not that execution is authorized or safe to run.
- Manual compliance metadata is not reproducible compliance evidence and cannot cross the I047 bridge.
- Reproducible evidence must be bound to exact source content bytes/digest and fresh first-party policy conclusions.
- Every durable response must remain bound to exact request/receipt/body/manifest evidence.
- DNS/redirect/size/content-type gates remain upstream of evidence parsing.
- No irreversible or paid external action without explicit user authorization.
- Resource routing must separate sunk/fixed cost from marginal cost and must never assume ChatGPT/Codex subscription exposes a free autonomous API.
- Unavailable/credentialed/new-spend backends may be modeled for planning but may not become selected live execution paths without their blockers being explicitly cleared.
- Fast watcher architecture must obey source ToS/rate limits and perform local cheap filtering before AI; do not use frequent LLM polling by default.

## Immediate next run — I049
Integrate the Resource / Execution Router into the existing observation/orchestrator path. Convert accepted normalized task observations into router-compatible `TaskEconomics`, preserve upstream policy/demand holds, and emit a combined inert dry-run record with opportunity economics plus selected backend. Add deterministic tests proving that unsafe/unsupported/no-demand work cannot become routable merely because a backend is cheap. Keep all execution/network/value movement disabled.

## Completion gate
Implementation is complete only when the documented stack either demonstrates positive economics on real permitted tests or reasonable candidates are exhausted by control passes. Until then: **IMPLEMENTATION IN PROGRESS**.
