# Implementation Run I029 — deterministic capture-session planner

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Convert the I028 capture-readiness packet into an exact chronological no-network session plan without granting network authorization or performing any HTTP request.

## Changes
Added `implementation/capture_session_planner.py`:
- accepts only I028 packets that remain authorization=false, GET-only, no-credentials, dry-run and action-disabled;
- admits only `ready_for_future_explicit_read_only_capture` rows;
- preserves I027/I028 priority order for budget admission;
- enforces a global request budget and total session-time budget;
- enforces each source's conservative per-host minimum interval and rolling request-window ceiling;
- groups admitted requests by host and emits an exact UTC chronological sequence;
- defers otherwise-ready sources when request/time budget is exhausted;
- keeps blocked observability/environment sources in a separate remediation queue;
- rejects non-HTTPS, credentialed, non-production, self-authorizing or action-enabled inputs fail-closed.

Added `implementation/test_capture_session_planner.py` with deterministic coverage for same-host spacing, rolling-window caps, cross-host parallel slots, request/time budget deferral, blocked remediation, HTTPS enforcement, self-authorization rejection and replay determinism.

## Verification
Nine deterministic tests passed in an isolated local harness (`9 passed`). GitHub Actions workflow was not changed; push-triggered CI remains disabled.

## Safety / external actions
No HTTP request, account/login/KYC, API key, wallet, payment, task acceptance, bid, service publication, paid API, paid server or settlement occurred. The produced plan explicitly remains `explicit_read_only_network_authorization_required`, `authorization_granted=false`, `network_calls_performed=false`, `credentials_allowed=false`, `dry_run_only=true`, and `action_enabled=false`.

## Outcome
The production-gap pipeline now reaches a reproducible session-level execution plan while preserving host rate contracts and a hard no-network boundary. Missing evidence remains unknown rather than negative demand.

## Next run — I030
Build a deterministic read-only transport preflight/envelope over the I029 session plan. Bind each step to its exact source URL, method, manifest item hash, expected evidence classes, host/rate contract and provenance fields; expose a dependency-injected transport interface that remains disabled unless a separate explicit read-only network authorization token/envelope is supplied. Add failure-mode tests, but still perform no real HTTP request.

Project state: **IMPLEMENTATION IN PROGRESS**.
