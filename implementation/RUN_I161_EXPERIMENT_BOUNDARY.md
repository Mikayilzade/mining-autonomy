# I161 — Experiment readiness boundary after I156–I160

Date: 2026-08-24
Status: **completed fail-closed readiness checkpoint**

## Scope
Advanced the existing I138 readiness/control chain using the already-established I156–I160 runtime and Resource / Execution Router outcomes. No discovery was reopened.

## Result
Added `i161_experiment_boundary.py`, which separates the current project boundary into five non-substitutable gates:

1. **User-PC measurement** — autonomous preparation is allowed, but production routing needs machine-bound hardware/interface, benchmark, availability, energy, explicit tariff and opportunity-cost measurements.
2. **External API materialization** — pricing/policy/rate-limit research and benchmark design are inertly preparable; real credentials and bounded live API measurement require explicit authorization.
3. **Future VPS materialization** — provider/spec/price and fixed-cost allocation planning are preparable; rental/materialization requires explicit spend/infrastructure authorization.
4. **PayanAgent provider geography** — repeated broad searches remain closed; only genuinely new first-party Azerbaijan/provider-country evidence or separately authorized local-access evidence can satisfy this boundary.
5. **Bounded read-only observation** — exact one-shot request manifest can be prepared, but the production observation remains disabled until exact explicit authorization.

The module verifies that I160 classifications have not drifted and preserves the I156 runtime result as a separate fact. Runtime evidence does not substitute for a measured positive execution route, geography evidence or observation authorization.

Current default state is `FAIL_CLOSED_EXTERNAL_BOUNDARIES`. No currently measured positive conservative execution route exists. The next inert packet is therefore the existing **I159 user-PC measurement packet**, because it is the only zero-new-spend production-resource fact that can materially advance routing without credentials or infrastructure rental.

## Safety
No network access, credentials, API call, CI dispatch, account creation, infrastructure rental, task acceptance, spend, settlement or value movement occurred.

## Next action
Prepare a concise portable user-PC measurement procedure around I159/I129 that can collect only the missing hardware/runtime/availability/energy/tariff/opportunity-cost evidence without installing paid software or using credentials. Do not claim measurements until they are actually produced on the user's machine. If such local evidence remains unavailable, keep the branch blocked and do not substitute synthetic economics.
