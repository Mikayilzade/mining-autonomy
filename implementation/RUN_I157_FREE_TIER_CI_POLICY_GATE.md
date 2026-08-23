# I157 — free-tier CI policy gate

Date: 2026-08-24

## Scope
Advance the existing `free_tier_ci` Resource / Execution Router evidence branch without dispatching CI, using credentials, creating spend, or widening any production authorization.

Provider checked: GitHub Actions standard GitHub-hosted runners for repository `Mikayilzade/mining-autonomy`.
Repository metadata observed through the connected GitHub API: visibility **public**.

## Current first-party evidence
1. GitHub Actions billing/usage docs state that standard GitHub-hosted runners are free for public repositories.
2. GitHub-hosted runner docs describe standard public-repository runners and their resource classes.
3. GitHub Actions limits remain applicable; public-repository pricing language is not an infinite-capacity guarantee.
4. GitHub Additional Product Terms state that Actions may not be used for cryptomining, disproportionate server burden, commercial resale of Actions, and — for GitHub-hosted runners — activity unrelated to production, testing, deployment, or publication of the software project associated with the repository.

Primary sources revalidated 2026-08-24:
- https://docs.github.com/en/actions/concepts/billing-and-usage
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
- https://docs.github.com/en/actions/reference/limits
- https://docs.github.com/en/site-policy/github-terms/github-terms-for-additional-products-and-features

## Decision
For this project's generic external paid-task execution use case, GitHub-hosted Actions is **not an eligible production earning backend**. It remains useful only as development/testing/support infrastructure for this repository, where separately enabled and within GitHub policy.

This distinction prevents a pricing fact (`$0` incremental standard hosted-runner price for public repositories) from being incorrectly promoted into a permission/capacity fact. `free_tier_ci` therefore does not become a production route merely because the repository is public.

State: **SUPPORT_TESTING_ONLY**.

Production paid-task eligibility: **false**.
Development/testing eligibility: **true**, subject to repository workflow policy and service limits.
Capacity claim verified: **false**; no workflow was dispatched and no concurrency/runtime capacity was measured.

## Implementation
Added `i157_free_tier_ci_policy_gate.py` with fail-closed policy semantics and `test_i157_free_tier_ci_policy_gate.py`.

Focused local verification before repository write: **3 tests passed**.
Coverage includes:
- current public-repository evidence -> `SUPPORT_TESTING_ONLY`;
- any attempted widening to generic external paid-task permission -> `FAIL_CLOSED`;
- private-repository substitution rejected because this checkpoint is bound to the observed public repository state.

## Safety / external effects
No GitHub Actions workflow was dispatched.
No production market observation was performed.
No credentials, registration, paid account, wallet, task acceptance, fulfillment, spend, payment or value movement occurred.
Automatic push/PR runtime CI remains disabled.

## Router consequence
Treat `python_local` as exhausted in the current execution environment on genuine energy measurement, and `free_tier_ci` as exhausted as a production earning backend on policy grounds. Per the existing I134/I137 ordering, the next no-new-spend evidence branch is `local_model`.

The next stage should test whether a genuinely available local CPU/GPU/model interface exists and can provide current quality/capacity/energy/opportunity-cost evidence without assuming hardware or model availability. If not, continue I137 to `owned_pc`; do not reopen broad discovery.
