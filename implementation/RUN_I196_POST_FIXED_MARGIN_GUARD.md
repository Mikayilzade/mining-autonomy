# I196 — post-fixed conservative margin guard

Date: 2026-08-25
Status: **completed repository-side safety/economics hardening**

## Scope
Followed the current I195 boundary rule: do not add packaging-only wrappers. Audited the existing I123 Resource / Execution Router production-selection path for a distinct economic fail-open before any real monetization test.

## Finding
A real boundary was found. `quote_backend()` calculated both pre-allocation and post-allocation expected margin, but I123 production eligibility only required the pre-allocation planning reasons to clear. If a backend had a known, non-sunk monthly fixed cost with an allocation basis, it could therefore remain production-eligible even when its conservative per-task margin became non-positive or fell below the configured absolute/ratio thresholds after fixed-cost allocation.

This matters specifically for future paid infrastructure or any non-sunk backend: fixed and sunk costs must remain separate, but a real incremental allocation of a non-sunk fixed commitment cannot be ignored when deciding whether a task is economically acceptable.

## Change
`implementation/i123_execution_backend_portfolio.py` now:
- adds a production-only post-fixed economics gate;
- blocks `nonpositive_margin_after_fixed_allocation`;
- blocks `insufficient_conservative_margin_after_fixed_allocation` when either configured absolute or ratio threshold is missed;
- preserves the existing fail-closed blocker when allocation basis is unknown;
- ranks otherwise eligible production routes using post-fixed expected margin as the secondary economic tie-breaker;
- updates the snapshot schema/routing statement to make the post-fixed requirement explicit.

Added `implementation/test_i196_i123_fixed_cost_margin.py` with two synthetic, no-network regression cases:
1. a non-sunk backend that looks profitable before allocation but loses money after allocation must remain `hold`;
2. a small allocated fixed cost that still clears the conservative thresholds may remain production-route eligible when all synthetic evidence gates are intentionally satisfied.

## Safety
No network observation, credentials, registration, KYC, wallet, paid account, paid infrastructure, hardware purchase, task acceptance, spend, settlement or value movement occurred. Test evidence is synthetic and exists only to exercise the gate; it does not authorize or materialize any real backend.

## Risks / limitations
- The lower-level `resource_router.route_task()` remains a dry-run/planning helper; the hardened production boundary is I123. Any future direct production consumer of the lower-level helper must either inherit this post-fixed rule or be separately audited before use.
- The actual owned-PC evidence chain is still blocked on genuine energy/availability/opportunity-cost/accounting measurements.
- No claim of real profitability is made.

## Files
- `implementation/i123_execution_backend_portfolio.py`
- `implementation/test_i196_i123_fixed_cost_margin.py`
- `implementation/RUN_I196_POST_FIXED_MARGIN_GUARD.md`
- `STATUS.md`
- `HANDOFF.md`
- `implementation/IMPLEMENTATION_RUN_LOG.md`

## Next action
Return to the genuine owned-PC chain rather than further repository-only packaging: run I181 on the actual owned PC; use a validated built-in cumulative counter or, only if already available, the hardened I182 whole-system external-meter route; then materialize genuine tariff, availability, opportunity-cost and accounting provenance and run exact I178/I179. If a future code path directly promotes `resource_router.route_task()` to production, audit/port the I196 post-fixed guard first.
