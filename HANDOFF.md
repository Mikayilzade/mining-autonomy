# Handoff for Any Future Chat / Agent

Do not reconstruct this project from chat memory.

## Resume protocol
1. Open `Mikayilzade/mining-autonomy`.
2. Read `START_HERE.md`, `STATUS.md`, `METHODOLOGY.md`, `HANDOFF.md`, `RUN_LOG.md`, `CATALOG.md`, `implementation/RUN_LOG.md`, and latest files named in STATUS.
3. Trust repository state over chat memory; `STATUS.md` is authoritative.
4. Discovery Runs 001–062 are COMPLETE. Continue Implementation / Experiment Phase.

## Current checkpoint
Discovery Runs **001–062 COMPLETE**. Implementation Runs **I001–I029 COMPLETE**. Project: **IMPLEMENTATION IN PROGRESS**.

Latest files:
- `implementation/RUN_I029_CAPTURE_SESSION_PLANNER.md`
- `implementation/capture_session_planner.py`
- `implementation/test_capture_session_planner.py`
- I028 readiness and prior production-gap/evidence pipeline files named in STATUS.

## I029 result
`build_capture_session_plan()` converts I028 ready items into an exact deterministic no-network session plan.

Important behavior:
1. only ready production GET/no-credential/no-action items are admitted;
2. upstream priority order controls admission;
3. global request and session-time budgets are enforced;
4. per-host minimum intervals and rolling request-window limits are enforced;
5. admitted steps are emitted in exact chronological UTC order and grouped by host;
6. ready items outside the budget are deferred, not reclassified as negative demand;
7. blocked observability/environment sources remain in a separate remediation queue;
8. authorization remains false and no network call is performed.

Verification: nine deterministic tests passed in an isolated local harness. GitHub Actions workflow was unchanged and push-triggered CI remains disabled.

## Immediate next run: I030
Build a deterministic read-only transport preflight/envelope over I029. Bind each step to exact source, method, manifest item hash, expected evidence, provenance and rate data. Keep any transport dependency disabled until separate explicit read-only network authorization exists. Add failure-mode tests; do not perform real HTTP.

## Hard boundary
Do not spend money, create/fund wallets, submit KYC, accept paid work, publish monetized services, or settle transactions without explicit user authorization. Do not bypass CAPTCHA, geofencing, platform rules, or other access controls.

## Completion
Implementation remains incomplete until a permitted real test demonstrates positive economics or reasonable candidates are exhausted and confirmed by control passes.
