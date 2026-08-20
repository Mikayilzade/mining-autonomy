# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I048 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I048_RESOURCE_EXECUTION_ROUTER.md`
- `implementation/resource_router.py`
- `implementation/test_resource_router.py`
- `implementation/RUN_I047_SOURCE_COMPLIANCE_REVIEW_BRIDGE.md`
- I046 and prior authorization/readiness/capture files named in STATUS.

## I048 result
`resource_router.py` adds the mandatory offline Resource / Execution Router foundation before any real monetization test.

Important behavior:
1. backend economics now separate per-task marginal cost from fixed/sunk monthly cost;
2. synthetic backend families cover deterministic Python/local execution, local CPU/GPU/model capacity, subscription-backed ChatGPT/Codex-style assistance, cheap/strong external APIs, free-tier CI/cloud, owned PC and future paid VPS/server;
3. subscription tooling is explicitly modeled as fixed/limited non-API support unless an actual autonomous programmatic interface exists — it is not treated as free unlimited API capacity;
4. already-paid/sunk fixed cost is visible but not charged in full to each task; non-sunk recurring cost is amortized only when an explicit task-volume allocation basis exists;
5. backend quotes include quota/capacity, latency, reliability × quality probability, parallelism/rate limits, electricity, API/model cost, retry/failure cost, maintenance time, opportunity cost and platform/payment risk;
6. task expected revenue is reduced by acceptance, dispute and non-payment probabilities plus platform/transaction/gas/withdrawal/conversion costs;
7. unavailable, credentialed, paid-account and new-spend resources remain `planning_only`; they cannot beat a currently available eligible backend in the dry-run route;
8. the route selects the lowest marginal-cost sufficiently reliable permitted currently available autonomous backend;
9. every action/execution flag remains false;
10. ten deterministic tests passed in an isolated local harness.

## Watcher direction
I048 also adds an inert watcher policy for future `poll` / `webhook` / `websocket` workers. A future standalone Python watcher may operate faster than chat-level automation when the source platform explicitly permits that cadence. Local parsing/filtering/deduplication must happen before AI; LLM-on-every-poll is rejected by default; rate-limit/product-limit bypass is rejected. Network remains disabled in I048.

Target future flow:
`cheap source watcher -> local deterministic filter/dedupe -> promising opportunity -> upstream policy/demand gates -> Resource Router -> selected backend -> execution only after all later live gates are explicitly cleared`.

## Immediate next run: I049
Integrate the Resource / Execution Router into the existing observation/orchestrator path. Convert accepted normalized task observations into router-compatible `TaskEconomics`, preserve upstream policy/demand state, and emit one combined inert dry-run record with opportunity economics plus selected backend. Add deterministic tests proving that unsafe/unsupported/no-demand work cannot become routable because a backend is cheap. Keep execution/network/value movement disabled.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or other access controls. Real network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume paid ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk resources with quota/capacity limits and explicit interface constraints. For live routing, only a genuinely available programmatic backend can be selected. Future APIs/VPS/paid services remain planning-only until their credentials/spend/ToS/geography gates are cleared.

## Git/CI
Prefer one coherent commit per implementation run where tooling permits. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
