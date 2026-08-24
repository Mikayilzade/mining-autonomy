# I191 — Resource Router semantic-domain hardening

Date: 2026-08-25
Status: **completed repository-side correctness checkpoint**

## Scope
Close the concrete I190 fail-open defect in `resource_router.py` without changing authorization/evidence boundaries or enabling execution/value movement.

## Changes
- probabilities now require finite real values in `[0,1]` instead of clamping;
- fractional `platform_fee_rate` is explicitly constrained to `[0,1]`;
- negative payout, fees, backend marginal costs, units, fixed cost, quota/capacity, latency and rate limits fail closed;
- positive allocation basis is required when non-sunk fixed cost must be allocated;
- valid dry-run routing remains available and execution stays globally disabled.

## Verification
Focused local regression suite: **29 passed in 0.18s**. This verification used the staged I191 module and focused tests only; no CI was dispatched.

## Safety
No network observation, credentials, spend, account creation, KYC/wallet action, hardware purchase, task acceptance/fulfillment, publication, settlement or value movement occurred.

## Next action
Re-audit the direct I123 -> conservative economics/readiness boundary against these stricter domains, especially source/evidence promotion and any remaining signed-threshold semantics. The genuine forward path still requires real owned-PC I181/I166/I179 evidence; do not estimate missing energy/accounting facts.