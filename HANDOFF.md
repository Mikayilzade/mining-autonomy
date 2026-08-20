# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I049 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I049_OBSERVATION_RESOURCE_ROUTING.md`
- `implementation/execution_routing_integration.py`
- `implementation/test_execution_routing_integration.py`
- `implementation/RUN_I048_RESOURCE_EXECUTION_ROUTER.md`
- I047 and prior authorization/readiness/capture files named in STATUS.

## I049 result
`execution_routing_integration.py` now bridges the existing orchestrator task path to the I048 Resource / Execution Router.

Important behavior:
1. `observe_task()` always runs first;
2. upstream policy/capability/quality/evaluator and demand-evidence state is authoritative;
3. upstream `hold` or `reject` returns immediately with no `TaskEconomics`, no router call and no selected backend;
4. only `accept_dry_run` tasks are converted to `TaskEconomics`;
5. optional fee/acceptance/dispute/non-payment inputs live under explicit `routing_economics`, preventing ordinary task metadata from silently changing router economics;
6. resource routing can only narrow eligibility — an upstream accept may become a router hold, but a hold/reject can never become routable;
7. subscription-backed ChatGPT/Codex-style assistance remains support-only/non-programmatic unless a real supported interface exists;
8. combined routed records keep execution/network/value movement disabled;
9. seven deterministic bridge tests passed in an isolated interface-compatible harness;
10. no real external action occurred.

Target flow is now:
`cheap source watcher -> local filter/dedupe -> normalized task -> policy/rights/quality/demand gate -> TaskEconomics -> Resource Router -> selected backend dry-run -> later explicit live gates`.

## Immediate next run: I050
Build a deterministic resource-profile evidence/calibration layer. Separate synthetic reference profiles from measured or explicitly declared resources actually available to the user/system. Bind availability, fixed/sunk cost, quotas/capacity, electricity, latency, reliability/quality, parallelism/rate limits and interface constraints to provenance/freshness. Unknown or stale resource parameters must remain planning-only.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules or access controls. Real network capture still requires separate explicit read-only authorization.

## Resource-accounting boundary
Do not assume paid ChatGPT/Codex subscription includes separate API usage or free programmatic execution. Treat already-paid subscriptions as fixed/sunk resources with quota/capacity and interface constraints. For live routing, only a genuinely available programmatic backend with current evidence may be selected. Future APIs/VPS/paid services remain planning-only until credentials/spend/ToS/geography gates are cleared.

## Routing precedence
Policy/demand evidence precedes resource economics. No backend — regardless of cost, speed or quality — can make unsafe, unsupported, policy-insufficient or unproven-demand work eligible.

## Git/CI
Prefer one coherent commit per implementation run where tooling permits. Do not re-enable push-triggered CI or make documentation-only changes trigger Actions. Current workflow remains manual/PR-oriented to avoid notification spam.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
