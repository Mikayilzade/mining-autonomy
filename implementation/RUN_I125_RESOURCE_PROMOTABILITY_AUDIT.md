# I125 — Resource promotability audit

Status: **completed scoped model-consistency checkpoint**

I125 audited the current I053/I050 source-class contract against I123's strict production requirement that a backend become `measured_reproducible` before selection.

## Finding

The current model contains a structural promotion contradiction for `python_local`: `sunk_or_already_committed` is accepted only as `user_declared`, while I050 marks any bundle containing `user_declared` evidence as `calibrated_declared` and not `all_current_evidence_reproducible`. I123, however, requires strict `measured_reproducible` evidence.

Therefore even a perfect I113 runtime receipt, successful local probe, measured latency/reliability/quality/parallelism, and measured electricity cannot by themselves produce the strict I123 evidence class under the current source taxonomy.

This is a real model defect rather than an environment/runtime blocker. Repeated runtime attempts cannot solve it.

## Safe resolution direction

Do **not** weaken I123 to accept arbitrary declarations. The next broad implementation stage should add a narrowly scoped, hash-bound reproducible backend-configuration invariant for model-defined `python_local` accounting facts where that is semantically valid, especially zero fixed software cost / zero-cost sunk normalization. Host electricity and any nonzero external cost must remain measured or first-party evidenced.

The invariant must be backend-specific, exact-source-bound and non-synthetic. It must not allow owned-PC/VPS/subscription costs to be silently normalized to zero.

## Safety

No network access, credentials, workflow dispatch, paid infrastructure, task acceptance, authorization creation, production observation, spend or value movement occurred. Production selection was not widened.

## Files

- `implementation/i125_resource_promotability_audit.py`
- `implementation/test_i125_resource_promotability_audit.py`
- `implementation/RUN_I125_RESOURCE_PROMOTABILITY_AUDIT.md`

## Next

Implement the narrow reproducible `python_local` backend-configuration evidence path, add negative tests proving it cannot be reused for `owned_pc`, CI, subscription, external API or VPS backends, then reconnect I124 -> I050/I066 -> I123. Keep electricity and exact runtime evidence independently fail-closed until genuinely measured.
