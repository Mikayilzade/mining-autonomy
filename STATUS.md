# Status

Project state: **IMPLEMENTATION IN PROGRESS**
Discovery phase: **COMPLETE (Runs 001–062)**. Do not reopen broad discovery without a genuinely missing mechanism.
Last completed implementation run: **I196 — post-fixed conservative margin guard**
Last updated: **2026-08-25**

## Latest durable files
- `implementation/RUN_I196_POST_FIXED_MARGIN_GUARD.md`
- `implementation/test_i196_i123_fixed_cost_margin.py`
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/RUN_I195_I123_DOWNSTREAM_CONSUMER_AUDIT.md`
- `implementation/resource_router.py`

## I196 outcome
Found and closed a distinct economics fail-open in the I123 production Router: a backend with known non-sunk fixed cost could previously clear production eligibility using pre-allocation margin even when allocated fixed cost made the conservative per-task margin non-positive or below configured absolute/ratio thresholds. I123 now blocks that condition and uses post-fixed expected margin for production-route economic tie-breaking. Synthetic regression fixtures cover both blocked-loss and still-profitable allocated-fixed-cost cases.

No real evidence or authorization was invented; current dry-run/planning fixtures remain blocked from real execution. Deterministic-first routing, AI-only-if-needed escalation, fixed/sunk-vs-marginal separation and positive conservative margin remain mandatory.

## Current blockers
1. I181 has not run on the actual owned PC; built-in cumulative-counter availability is unknown.
2. No genuine I166 packet exists; availability, energy, applicable tariff and opportunity-cost provenance are not materialized.
3. If no local counter exists, I182 requires a genuine already-available whole-system cumulative external meter; no hardware purchase is authorized.
4. Exact I050/I066 for `owned_pc` is not yet evidence-permitted/materialized.
5. Real task payout, retries/failures, maintenance, platform/payment fees and acceptance/dispute/nonpayment economics remain unknown.
6. Current measured non-synthetic production route surviving conservative economics + watcher overhead: **false**.
7. Authorization for bounded read-only production observation: **false**.

## Immediate next broad run
The next genuine step is on the actual owned PC — run I181; use a validated built-in cumulative counter if present, otherwise hardened I182 only with an already-available trustworthy whole-system cumulative external meter; supply genuine tariff, availability, opportunity-cost and accounting provenance; then run exact I178/I179 with explicit ownership confirmation and explicit UTC `observed_at`.

If neither energy measurement route exists, keep energy blocked. Do not estimate energy and do not purchase hardware without separate authorization. Do not resume repository-only hardening unless new code/evidence creates a distinct boundary to audit. If any future production consumer bypasses I123 and directly promotes lower-level `resource_router.route_task()`, port/audit the I196 post-fixed guard before use.

## Hard boundary
No spend, credentials, registration, wallet/KYC, paid infrastructure, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement without separate explicit authorization. No CAPTCHA/rate-limit/KYC/geofence/product-limit bypass.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
