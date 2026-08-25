# I193 — I123 evidence-origin / authorization-promotion audit

Date: 2026-08-25
Status: **completed audit; concrete fail-open boundary identified; no production action enabled**

## Scope
Narrow post-I192 audit of the direct `I123 -> conservative economics/readiness` boundary requested by `STATUS.md`. This run did not reopen discovery and did not perform network observation, use credentials, spend funds, dispatch CI, accept/fulfil a task, or move value.

## Concrete finding
`BackendEvidence` currently treats `provenance_class="measured_reproducible"` plus boolean evidence flags as sufficient production-grade evidence, but I123 does not bind that claim to any source artifact identity, digest, observation timestamp, or source class.

Consequently, a caller can construct a source-less `BackendEvidence` object with:
- `provenance_class="measured_reproducible"`;
- `current_reproducible=True`;
- `non_synthetic=True`;
- `capacity_verified=True`;
- `policy_evidence_current=True`;

and I123 can classify an otherwise economically eligible backend as `production_route_ready`. I189 correctly hardened boolean typing, but did not establish where those asserted facts came from.

The same structural gap applies more strongly to authorization flags. `credentials_authorized`, `spend_authorized`, and `infrastructure_authorized` are exact booleans after I189, but I123 has no independent authorization-reference/origin field. A bare `True` is therefore structurally indistinguishable from a provenance-bound explicit authorization fact.

## Why this is fail-open
The repository's retained chain explicitly says declarations must not be relabelled reproducible and that spend/credentials/infrastructure require separate explicit authorization. At the direct I123 boundary, however, the object schema can currently promote declarations into measured evidence or authorization without a source binding.

This does **not** mean arbitrary untrusted network input reaches I123 today; the current project remains dry-run and no real route is materialized. It is nevertheless a concrete correctness defect before a real economics/readiness consumer is allowed to depend on I123.

## Required hardening contract
The next repository-side patch should remain narrow and fail closed:

1. Separate evidence truth from evidence origin. A `measured_reproducible` claim must carry a non-empty source binding that is machine-checkable (at minimum source artifact identity/digest and explicit observation time/class), rather than being promotable from booleans alone.
2. Planning/declaration/synthetic source classes must never be promotable to `measured_reproducible` merely by setting flags.
3. Authorization facts (`credentials`, `new spend`, paid infrastructure) must remain false unless accompanied by a separate explicit authorization-origin/reference accepted by a narrow allowlist/contract; measurement evidence must not itself create authorization.
4. Malformed/unknown source classes, blank origin IDs, invalid digests/timestamps, and authorization-without-origin must fail closed before portfolio selection.
5. Current `current_backend_evidence()` planning fixtures must remain non-promotable and the public dry-run snapshot must remain blocked.
6. Existing I191/I192 economics invariants, deterministic-first routing, cheapest-qualified selection, and strict-positive conservative margin must remain unchanged.
7. Do not invent a genuine source artifact. Real owned-PC evidence is still absent; this patch is schema/boundary hardening only.

## Safety impact
Until this origin binding is implemented, I123 `production_route_ready` must not be interpreted as proof that evidence provenance or external authorization is genuine. The actual real-test chain therefore remains blocked exactly as before.

## Next action
Patch `implementation/i123_execution_backend_portfolio.py` with explicit evidence-origin and authorization-origin contracts plus focused adversarial regressions. Re-run the I189/I191/I192 focused suite together with the new tests. Do not proceed to bounded real observation merely because an in-memory object claims `measured_reproducible`.
