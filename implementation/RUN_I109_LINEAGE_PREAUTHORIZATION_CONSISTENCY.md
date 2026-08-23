# I109 — Lineage-aware preauthorization consistency

Date: 2026-08-23
Status: **COMPLETED SCOPED NETWORK-INERT HARDENING CHECKPOINT**

## Goal
Continue the exact safety step from I108 without broad discovery: bind I108 exact-current-source runtime receipt lineage into the I104/I105 preauthorization consistency view, while preserving the four independent blockers and performing no production observation.

## Work completed
Added `implementation/i109_lineage_preauthorization_consistency.py`.

The validator:
- reuses I105 to validate the historical I104 blocker report against current I100 readiness inputs;
- runs the I108 lineage projection over an optional I106 receipt;
- requires all three non-runtime blockers in I108 to remain exactly equal to independently derived I100 state;
- permits `runtime_regression_verification=true` only when a receipt is present and I108 reports exact-current-source lineage PASS;
- fails closed if the runtime blocker becomes true without a receipt, if I108 widens any non-runtime blocker, or if any network/execution capability appears;
- records SHA-256 bindings for I105/I106/I107/I108 source modules so the consistency layer itself is diagnosable against source drift;
- remains evidence-only: it never authorizes or performs the production GET.

## Runtime status
This automation environment has GitHub source access but no repository-mounted executable checkout exposed through the connector, so I106 -> I107 -> I108 -> I109 was **not executed** here and no PASS receipt/result was fabricated.

`I106_LOCAL_RUNTIME_RECEIPT.json` remains absent in the durable repository state. Therefore runtime regression verification remains unsatisfied. The other three blockers also remain independently unsatisfied: fresh-real execution evidence, current eligible non-synthetic Resource / Execution Router route, and exact explicit user authorization.

## Resource / Execution Router status
The existing I048-I067 router remains the execution-selection foundation, with I101 requiring current materialization, non-synthetic provenance, policy eligibility, capacity/reliability/quality, full marginal-cost accounting and positive conservative margin. I109 does not weaken or bypass that route requirement and does not treat ChatGPT/Codex subscription access as a free autonomous API.

## Safety / external effects
- production DNS/HTTP/socket/TLS: **NO**
- credentials: **NO**
- user authorization created/consumed: **NO**
- task acceptance/submission: **NO**
- paid infrastructure/API/account: **NO**
- spend/payment/value movement: **NO**
- GitHub Actions dispatch: **NO**

## Risks closed
I108 had exact-source anti-replay protection, but its runtime projection was not yet explicitly cross-checked against the I105 preauthorization consistency view. I109 closes that integration gap: runtime lineage may affect only the runtime blocker and cannot mutate or substitute for market evidence, route materialization, or authorization.

## Remaining blockers
1. Fresh real execution/policy/DNS/TLS/rebinding evidence — false.
2. Current materialized eligible non-synthetic Resource Router route — false.
3. Exact explicit user authorization for one read-only production GET — false.
4. Current exact-source runtime-regression receipt verified through I106/I107/I108/I109 — false because no receipt has been executed.

## Next action — I110
At the first repository-local Python runtime, execute in order:

`python3 implementation/i106_local_runtime_receipt.py`

If and only if it produces PASS, then run:

`python3 implementation/i107_runtime_receipt_binding_validator.py`

`python3 implementation/i108_runtime_receipt_lineage_validator.py`

`python3 implementation/i109_lineage_preauthorization_consistency.py`

Accept runtime regression verification only if all agree and I109 shows that the three non-runtime blockers were not widened. Do **not** perform the production GET, dispatch repeated failing PR CI, spend money, use credentials, or move value.

If repository-local runtime is still unavailable, the next safe hardening target is deterministic receipt/result chaining for I109 itself (including source hashes and blocker projection), without reopening discovery or weakening any blocker.
