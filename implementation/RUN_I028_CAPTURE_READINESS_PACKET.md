# Implementation Run I028 — deterministic capture-readiness packet

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Convert the I027 selected read-only observation queue into an exact, deterministic no-network readiness packet for a future separately authorized capture.

The packet must preserve:
1. exact sealed-manifest/source identity;
2. GET-only/no-credential/no-action constraints;
3. expected evidence class and required environment;
4. provenance checklist and conservative source rate budget;
5. explicit authorization state;
6. a fail-closed distinction between technically ready production observations and sources blocked by observability/environment requirements.

## Changes

### `capture_readiness.py`
Added `build_capture_readiness_packet(priority_plan, manifest_envelope)`.

The module revalidates the I027 plan and sealed manifest, then requires every selected row to match the exact scheduled manifest item by platform, source URL, item index and manifest-item SHA-256.

It rejects:
- manifest/plan hash mismatch;
- unscheduled items;
- duplicate selected items;
- non-GET methods;
- credential-enabled, network-enabled or action-enabled manifest items;
- malformed/self-inconsistent rate budgets;
- missing provenance requirements.

### Readiness states
Each selected observation is classified into exactly one state:

**`ready_for_future_explicit_read_only_capture`**
- source is scheduled;
- GET-only and credential-free;
- production environment is predeclared;
- requested evidence is demand/utilization-capable rather than only mechanics/observability documentation.

**`blocked_by_observability_or_environment_requirement`**
- production environment is not predeclared (for example an `unknown` environment that must be proven); and/or
- the source exposes only `public_observability_gate` / `monetization_mechanics`, which cannot close the real-demand gap by itself.

A readiness result is not authorization. Every row and the top-level packet retain:
- `authorization_state = explicit_read_only_network_authorization_required`;
- `authorization_granted = False`;
- `network_calls_performed = False`;
- `credentials_allowed = False`;
- `dry_run_only = True`;
- `action_enabled = False`.

### Provenance/rate controls
The packet copies the exact manifest provenance checklist and rate-limit contract. The rate budget remains a conservative project self-limit, not a claim about platform capacity or permission.

Missing evidence remains `unknown`, never zero or negative demand.

## Tests
Added `test_capture_readiness.py` covering:
- production demand-capable source classified ready;
- unknown environment classified blocked;
- observability-only source classified blocked;
- manifest/source identity mismatch fails closed;
- POST/non-GET capture forbidden;
- malformed rate budget rejected;
- duplicate selected item rejected;
- provenance and no-action invariants preserved.

## Verification
Eight deterministic tests passed in an isolated local harness (`8 passed`). The new module also syntax-compiled successfully.

Full repository CI was not run. GitHub Actions workflow was not changed; push-triggered CI remains disabled.

## Safety / external actions
No HTTP/network capture, login/account/KYC, API key, wallet, paid infrastructure, task acceptance, bid, service publication, transaction or settlement occurred.

## Outcome
The stack now has a reproducible bridge from "what evidence should be sampled next?" to "is that exact source technically ready for a future explicitly authorized read-only capture, and what must be preserved when doing it?"

This prevents an observability-only documentation page or unknown/test environment from being mistaken for production demand evidence.

The main economic gap remains unchanged: attributable production demand/utilization has not yet been captured.

## Next — I029
Add a deterministic capture-session planner over I028 that batches only readiness=`ready` items under a total request/time budget, groups them by host/rate limit, emits an exact chronological no-network session plan, and keeps blocked sources in a separate remediation queue. Still do not perform HTTP requests.
