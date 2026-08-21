# Implementation Run I069 — exact human-decision request

Date: 2026-08-21
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Build the next inert boundary over I068: a short-lived human-decision request bound to the exact market-readiness packet and exact single anonymous production GET scope, without granting authorization or enabling any transport/action path.

## Changes
Added `human_decision_request.py` with `build_human_decision_request()`.

The request builder:
- independently revalidates the I068 `market_side_readiness_sha256`;
- accepts only `ready_for_human_review_only` checkpoints;
- independently enforces exactly one production `GET`, no credentials and no action;
- requires a current selected resource-route backend for decision context;
- fails closed if any I068 inert safety flag has been widened or omitted;
- binds the future decision target to the exact I068 readiness hash and `exact_scope_sha256`;
- inherits the exact upstream review-scope expiry verbatim and cannot extend it;
- exposes only two decision values: `authorize_one_read_only_observation` or `deny`;
- explicitly excludes credentials/login, task acceptance, task submission, payment/purchase, wallet/settlement, value movement, additional requests and non-GET methods;
- always emits `authorization_granted=false`, `network_enabled=false`, `execution_enabled=false` and no execution token.

## Verification
Added `test_human_decision_request.py` with seven deterministic tests covering exact ready-state construction, I068 hash tampering, expired upstream scope, scope widening after re-hash, blocked readiness, unsafe flag widening and missing current-resource route.

Isolated local verification: **7 passed**. GitHub Actions was not dispatched.

## Safety / external actions
No DNS/HTTP, credentials, login, KYC, wallet, payment, task acceptance, submission, publication, settlement or value movement occurred. This run only creates an offline request object; it does not record a human decision and cannot infer authorization from chat history.

## Outcome
The project now has a deterministic object suitable for asking a human one exact question at the market-side boundary without widening any earlier safety/resource/compliance contract. Approval of this request, if separately provided in a future run, can only concern one anonymous read-only observation and must still pass a new consent verifier plus the existing real-transport gates before any network call.

## Next run — I070
Build a deterministic decision-record verifier over I069. Accept only an explicit `authorize_one_read_only_observation` or `deny` decision bound to the exact I069 request hash, exact I068 readiness hash, exact scope hash and unexpired request window. Do not infer consent from chat history, do not enable transport, and do not perform network access.

Project state: **IMPLEMENTATION IN PROGRESS**.
