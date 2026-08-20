# Implementation Run I038 — deterministic authorization-readiness decision packet

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Combine I037 capture-integrity quality output with the exact I036 history and I028–I030 readiness/session/preflight contracts, then decide whether the smallest future read-only capture is warranted. Preserve exact hash binding, GET-only/no-credentials/no-action boundaries, and perform no real network request.

## Changes
Added `implementation/authorization_readiness.py` with `build_authorization_readiness_packet()`.

The module:
- independently revalidates the I037 `quality_gate_sha256` and I036 `history_sha256`;
- requires I036 history to bind to the exact I029 session-plan hash and I030 transport-envelope-set hash;
- independently recomputes I028 readiness-packet, I029 session-plan and I030 envelope-set hashes;
- revalidates every candidate request binding before selection;
- interprets I037 only as capture/infrastructure integrity, never economic demand;
- selects at most **one** exact production `GET` using upstream priority then session sequence;
- emits `no_capture_needed_for_integrity_only` when I037 does not recommend another integrity observation;
- emits a blocked state when repeat is recommended but no exact I030 request is available;
- when the existing I030 plan has multiple requests, emits `minimal_single_request_replan_required_before_user_authorization` rather than widening authorization to the full plan;
- when the existing plan already contains exactly one request, emits an inert authorization draft bound to that exact plan, but with `authorization_granted = false` and no nonce;
- constrains proposed authorization TTL to 60–3600 seconds;
- preserves `network_calls_performed = false`, `credentials_allowed = false`, `dry_run_only = true`, `action_enabled = false`.

## Verification
Added `implementation/test_authorization_readiness.py` with eight deterministic tests covering:
1. exact single-GET readiness while remaining inert;
2. no-repeat/no-capture decision;
3. multi-request plan narrowed to one target and forced replan before authorization;
4. repeat recommendation with no ready request;
5. I037 quality-hash tampering;
6. I036→I029 plan-binding mismatch;
7. transport-envelope/request-binding tampering;
8. TTL boundary enforcement.

Isolated local verification: **8 passed** plus syntax compilation. GitHub Actions was not dispatched and push-triggered CI remains disabled.

## Safety / external actions
No DNS/HTTP, login, KYC, API key, wallet, payment, bid, task acceptance, publication, paid API/server, or settlement occurred.

## Outcome
The stack can now answer a narrower question than I037 alone: not merely whether another observation might help, but **what exact smallest read-only request would be worth asking the user to authorize**, while refusing to broaden authorization to unrelated requests.

The main economic gap remains unchanged: attributable production demand/utilization has still not been captured.

## Next run — I039
Build a deterministic minimal-plan reducer that consumes an I038 `minimal_single_request_replan_required_before_user_authorization` decision and reconstructs an exact one-request I029/I030-compatible session/preflight pair without changing source/evidence/provenance/rate semantics. It must preserve all safety checks and still perform no network request. If I038 says no capture is needed, emit a no-op reducer result.

Project state: **IMPLEMENTATION IN PROGRESS**.
