# Implementation Run I027 — deterministic production-gap prioritizer

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Turn the I026 source-level evidence audit into one deterministic next-observation priority plan without performing a network request.

The plan must:
1. preserve sealed-manifest/source identity;
2. prioritize unresolved production evidence;
3. account for platform importance, evidence value, freshness urgency and conservative source rate budget;
4. separate read-only recapture needs from offline archive/provenance repair;
5. never interpret missing evidence as zero or negative demand;
6. remain credentials-free, plan-only and action-disabled.

## Changes

### `gap_prioritizer.py`
Added `prioritize_production_gaps(audit, manifest_envelope, ...)`.

The prioritizer fails closed unless:
- audit schema/action/network invariants are intact;
- the audit and sealed manifest hashes match;
- each source row maps to the exact scheduled manifest item;
- source URL/platform/item hash match;
- the manifest item remains GET-only, no-credentials and no-action;
- rate-limit fields are structurally valid.

### Priority model
Each unresolved source receives deterministic components:
- platform priority (dominant tier);
- evidence-gap value;
- freshness urgency;
- conservative source request-budget score.

Known gap types are normalized into two important paths:

**Read-only observation needed**
- missing production capture;
- invalid/missing valid receipt requiring a new observation;
- valid non-production receipt when production evidence is required;
- stale production evidence;
- future-invalid production evidence.

**Offline integrity repair**
- production capture exists but is not in the durable archive;
- archived capture is not represented by the current replay state;
- replay receipt provenance is missing.

Offline repair does not consume the future observation request budget.

Unknown gap types fail into a manual-review queue rather than silently becoming executable.

### Global observation cap
`max_observations` bounds how many read-only observations may be selected by one plan. Lower-ranked candidates remain explicit in `deferred_read_only_observations`.

This is a planning cap only. The module does not perform those requests.

### Demand semantics
Every priority item carries:
`missing_evidence_interpretation = "unknown_not_negative_demand"`

The report also asserts:
`missing_evidence_is_negative_demand = False`

Thus prioritizing an absent capture cannot be confused with evidence that buyer demand is zero.

### Tests
Added `test_gap_prioritizer.py` covering:
- primary-platform priority ordering;
- stale evidence recapture;
- offline repair separation from request budget;
- non-production receipt requiring a new production observation;
- global observation cap/deferred queue;
- audit/manifest hash mismatch fail-closed;
- source identity mismatch fail-closed;
- zero-observation budget preserving a no-network plan.

## Verification
The new module and tests compile. Eight deterministic unit tests passed in an isolated local harness using compatible canonical manifest sealing and manifest-item hashing semantics. Full repository CI was not run.

The GitHub Actions workflow was not changed. Push-triggered CI remains disabled.

## Safety / external actions
No live HTTP capture, account/login/KYC, API key, wallet, paid infrastructure, task acceptance, bid, service publication, transaction or settlement occurred.

`network_calls_performed=False`, `credentials_allowed=False`, `dry_run_only=True`, and `action_enabled=False` remain hard output invariants.

## Outcome
The evidence stack can now answer not only "what is missing?" but also "what should be observed next, and what can be repaired offline first?" reproducibly.

The central economics gap remains unchanged: real attributable production demand/utilization still needs a future permitted observation or legitimate onboarding where public observability is unavailable.

## Next — I028
Create a deterministic capture-readiness packet from the selected I027 observation queue. Emit the exact GET intent, evidence class, environment requirement, provenance checklist, rate budget and explicit blocked/ready state for a future separately authorized read-only capture. Do not perform the request.
