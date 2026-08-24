# I162 — Portable user-PC measurement procedure

Date: 2026-08-24
Status: **completed fail-closed preparation checkpoint**

## Scope
Implemented the next inert packet selected by I161 without reopening discovery: a portable local-only procedure for materializing the existing I159 `owned_pc` Resource / Execution Router evidence branch.

## Implementation
Added `i162_user_pc_measurement_procedure.py` and focused tests. The harness may collect only Python-visible machine/runtime identity locally. It does **not** treat that identity as proof of ownership until the caller explicitly confirms execution on the user-owned PC and supplies a measurement-environment reference.

All economically material facts remain explicit measurements with provenance:
- benchmark identity/source, quality acceptance probability, latency, reliability and measured safe parallelism;
- measured available hours/day and source;
- before/after joule counter readings, task count and counter source;
- explicit electricity tariff and source;
- explicit opportunity-cost estimate and source.

Energy per task is derived only from explicit before/after joule readings. Missing/partial counters, negative/reset counters, missing provenance or absent ownership binding remain blocked. The harness explicitly forbids substituting `os.cpu_count` for measured parallelism, one successful run for reliability=1, reachability for 24/7 availability, synthetic energy/tariff, or sunk ownership/subscription cost for zero opportunity cost.

The resulting packet is evaluated by the existing I159 gate. `USER_PC_PACKET_COMPLETE` is possible only when I159 reports `production_evidence_ready=true`; even then it creates no production route by itself and still must pass conservative economics/routing plus separate market/geography/observation authorization gates.

## Verification
Focused local verification: **4 tests passed**.

Coverage:
1. inert procedure manifest requires local user-PC execution;
2. empty measurements fail closed;
3. partial energy-counter inputs fail closed;
4. a fully explicit provenance-bound fixture can satisfy I159 semantics without enabling any external action.

The complete fixture is test data only and is **not** evidence about the user's machine or electricity tariff.

## External effects / safety
No network request, credentials, downloads, paid software, CI dispatch, account creation, paid infrastructure, task acceptance, spend, settlement or value movement occurred. No user-PC measurement is claimed to have occurred.

## Risks / blockers
- I162 must actually be run on the user-owned PC to materialize identity/benchmark evidence.
- A trustworthy local joule counter/meter may not be available; if absent, energy remains blocked rather than inferred.
- Electricity tariff, availability and opportunity cost require explicit provenance.
- PayanAgent geography/provider access and exact bounded-observation authorization remain independent blockers.

## Next action
Prepare a minimal deterministic benchmark runner/measurement session wrapper that can feed I162 on the user-owned PC without network access or paid installs, while keeping energy/tariff/availability/opportunity-cost fields explicitly external when the OS cannot measure them. Do not claim real measurements until user-PC execution occurs and do not reopen discovery.
