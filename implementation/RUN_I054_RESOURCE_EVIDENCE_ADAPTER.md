# I054 — I053 probe/declaration to I050 ResourceEvidence adapter

Status: **completed**
Date: 2026-08-21

Built `resource_evidence_adapter.py`, a deterministic bridge from the I053 local/no-new-spend calibration acquisition outputs into the I050 `ResourceEvidence` contract.

The adapter preserves provenance classes rather than flattening them. I053 offline probe facts become `system_probe` records bound to the exact transcript digest and reference-backend hash. Explicit accounting/interface facts remain `user_declared`. Electricity-per-task can become `measured_local` only when explicit energy-per-task and tariff values are supplied together with a source digest.

The adapter refuses to fill gaps from the synthetic backend reference. Missing fields remain explicit in `missing_parameters`; `complete_for_attestation` is false until every I050 critical field is actually supplied. Duplicate parameter inputs across probe/declaration/energy paths fail closed rather than silently choosing a winner.

Probe summaries must stay inert, match the exact backend and benchmark, carry a transcript digest and a collector-supplied UTC observation timestamp, and remain internally consistent with their top-level reliability/quality/latency/parallelism/rate-limit summary values. The adapter does not substitute current time, commit time or file time for measurement time.

Added `test_resource_evidence_adapter.py` with 10 deterministic tests covering partial probe evidence, no timestamp inference, declaration source-kind preservation, measured-energy derivation, duplicate-source rejection, no synthetic backfill, complete declared attestation, non-inert probe rejection, backend-binding mismatch and invalid energy inputs.

The current automation environment exposed GitHub through the connector but no local repository checkout/network path for executing pytest. Therefore the tests were added but **not claimed as executed in this run**. GitHub Actions was deliberately not dispatched to preserve the anti-spam CI policy.

No real hardware inspection, DNS/HTTP, credentials, subscription API assumption, paid service, task acceptance, publication, settlement, spend or value movement occurred.

Next: **I055 — build a deterministic end-to-end calibration packet that composes I053 acquisition summary -> I054 evidence -> I050 attestation -> I051/I052 attested dry-run routing, and prove that any missing/stale resource evidence narrows the route to hold while complete synthetic fixtures preserve calibration class/evidence bundle hashes. Keep execution/network/value movement disabled.**
