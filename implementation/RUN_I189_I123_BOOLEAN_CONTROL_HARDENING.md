# I189 — I123 boolean/control-plane hardening

Date: 2026-08-25
Status: **completed repository-side correctness/safety checkpoint; focused tests authored**

## Scope
Audit the direct downstream Resource / Execution Router consumer `i123_execution_backend_portfolio.py` for fail-open behavior after I188 numeric hardening. This is a concrete control-plane audit, not a new wrapper and not a return to discovery.

## Defect found
Python dataclass annotations do not enforce runtime boolean types. I123 previously used truthiness for backend control fields and evidence/authorization fields. Strings and integers such as `"false"`, `"true"`, `0`, and `1` could therefore be interpreted as control decisions rather than rejected.

The highest-risk paths were:
- `policy_allowed="false"` or `programmatic_access="false"` being truthy and potentially bypassing a production blocker;
- `currently_available=1` being accepted as availability;
- `sunk_or_already_committed="false"` being truthy and potentially converting a fixed monthly cost into zero allocated task cost;
- evidence flags such as `current_reproducible`, `non_synthetic`, `capacity_verified`, and `policy_evidence_current` accepting truthy non-booleans;
- authorization flags accepting non-boolean values;
- `ai_allowed="false"` being truthy and enabling AI escalation;
- duplicate backend identifiers creating ambiguous portfolio selection input.

## Changes
`implementation/i123_execution_backend_portfolio.py` now:
- requires exact `bool` values for backend control fields before I123 quoting/selection;
- requires exact `bool` values for all evidence and authorization flags;
- validates non-empty evidence/backend identifiers;
- rejects duplicate backend identifiers as well as duplicate evidence identifiers;
- requires `ai_allowed` and internal AI-selection flags to be exact booleans;
- validates the same controls when `production_blockers()` is called directly;
- preserves deterministic-first routing, conservative economics, evidence requirements, and the default `production_execution_enabled=False` / `value_movement_enabled=False` boundary.

## Regression coverage
Added `implementation/test_i189_i123_boolean_control_hardening.py` covering:
- valid strict-boolean deterministic route construction;
- malformed backend policy/programmatic/availability/spend/fixed-cost control flags;
- malformed evidence and authorization flags;
- string `ai_allowed` escalation attempts;
- duplicate backend/evidence identities;
- empty evidence identity.

Focused tests are authored but this run does not claim a byte-identical full pytest PASS because raw GitHub/DNS materialization remains unavailable in the execution host and CI was not dispatched merely to obtain status.

## Source bindings
- hardened I123 blob: `fa7de3bdc814adec81496d938ebd8814bff504ad`
- I189 regression blob: `f91bfb1ca6004c3a987d06e2719d482f5453ba65`

## Safety / external actions
No market/API observation, credentials, account creation, paid infrastructure, KYC/wallet action, hardware purchase, task acceptance/fulfillment, publication, settlement, spend or value movement occurred. No CI workflow was dispatched.

## Outcome
The direct production-portfolio Router path no longer accepts truthy non-boolean control/evidence values as production facts or authorization. This closes a distinct fail-open class downstream of I188 numeric hardening.

## Remaining blockers
Real forward progress still requires actual owned-PC evidence: run I181 on the owned PC, use a validated local cumulative counter or the hardened I182 external-meter path if already available, supply genuine tariff/availability/opportunity-cost/accounting provenance, and run exact I178/I179. Exact I050/I066 and later real task economics remain subsequent gates.

## Next action
Continue only with direct downstream Router/economics correctness audits if a distinct fail-open defect is found. Do not add another packaging layer around missing real evidence. A useful next audit target is the conservative economics/readiness consumer immediately after I123, checking runtime type/finite handling and source-class promotion without changing real-world authorization boundaries.
