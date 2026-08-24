# I170 — owned-PC control evidence source policy

Date: 2026-08-24

## Goal
Resolve the source-class question exposed by I168/I169 for the seven I050 control/accounting/interface parameters without copying synthetic Router defaults or weakening I050/I123 implicitly.

## Result
I170 splits the seven unresolved controls into two groups.

### Exact-interface reproducible facts
These must be proven by the exact local production executor/interface using current reproducible source classes (`system_probe`, `measured_local`, or `provider_first_party`):

- `requires_credentials`
- `requires_paid_account`
- `requires_new_spend`
- `quota_units_remaining`
- `rate_limit_per_minute`

For local quota/rate semantics, `None` means no external provider primitive applies; it never means unlimited host capacity. Host throughput remains separately measured.

### Owner/accounting facts
These are accounting classifications and must not be relabelled as machine measurements:

- `fixed_monthly_cost_usd`
- `sunk_or_already_committed`

Accepted plan sources are explicit `user_declared` or genuine `provider_first_party` evidence. Zero fixed cost must be explicit; it is not inferred from ownership.

## Current strict-I123 consequence
If either accounting field is `user_declared`, current I050 semantics produce a declared rather than fully reproducible attestation. Current I123 therefore cannot treat that bundle as `measured_reproducible`.

I170 records this as `HYBRID_ACCOUNTING_POLICY_REVIEW_REQUIRED`; it does **not** modify I050, I123 or any production gate. Provider-first-party evidence for both accounting fields can fit the existing strict source classes without policy change.

## Exact local verification
Repository blob SHAs were matched before execution:

- `i170_owned_pc_control_evidence_policy.py`: `5ef672da91e00baacd6f9460b499a86b3b230106`
- `test_i170_owned_pc_control_evidence_policy.py`: `3de9b9d4e3a65368f1b7c913acb87df1a4e669fa`
- focused result: **6 passed**

Together with I168/I169 in this broad run, exact-local focused verification is **17 passed** (5 + 6 + 6).

## Safety / external effects
No production market/API request, credentials, CI dispatch, downloads/paid installs, account creation, infrastructure rental, task acceptance/submission, spend, settlement, payment or value movement occurred.

## Next action
Prepare a narrow, review-only hybrid evidence contract for the owned-PC path that would allow explicit owner/accounting declarations only for `fixed_monthly_cost_usd` and `sunk_or_already_committed`, while requiring every dynamic/resource/interface/authorization-sensitive fact to remain reproducibly evidenced. Do not change I123 acceptance yet; first prove the proposed boundary cannot widen other backend families or consume credentials/spend authorization.
