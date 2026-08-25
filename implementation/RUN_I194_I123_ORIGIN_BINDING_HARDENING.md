# I194 — I123 source / authorization origin binding hardening

Date: 2026-08-25
Status: **completed repository-side hardening; no real evidence or authorization created**

## Work performed
Patched the direct I123 Resource / Execution Router boundary identified by I193.

- `measured_reproducible` evidence now requires a promotable source class plus nonblank artifact identity, lowercase SHA-256 digest and explicit UTC observation timestamp.
- `planning_reference`, `declaration` and `synthetic_fixture` origins cannot promote to production readiness even if all truth flags are set.
- unknown source classes and malformed artifact/digest/time metadata fail closed before selection.
- credentials, new-spend and paid-infrastructure authorization booleans now require an independent `explicit_user_authorization` origin and nonblank reference; measurement evidence cannot manufacture authorization.
- current planning fixtures remain non-promotable.
- deterministic-first routing, cheapest-qualified selection and existing conservative economics are unchanged.

Focused adversarial regressions were added in `test_i194_i123_origin_binding.py`. This run does not claim an executed pytest result; no CI workflow was dispatched merely to obtain a green status.

## Safety / economics result
No genuine source artifact, authorization, market observation, credentials, paid infrastructure, task acceptance, spend, settlement or value movement was created. The real chain remains blocked on actual owned-PC evidence and later separately authorized bounded observation.

## Next action
Audit direct consumers of I123 for any code path that interprets `production_route_ready` without preserving the new origin-bound evidence object. If none fail open, stop repository-only hardening and wait for the genuine owned-PC I181 -> I178/I179 evidence path rather than adding packaging layers.
