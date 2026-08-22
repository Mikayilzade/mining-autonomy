# Implementation Run I092 — exact HTTPS path/query binding contract

Date: 2026-08-22
Status: **completed safe checkpoint; builder integration still required before any live observation**

## Goal
Repair the I091 fail-closed finding without performing network activity: define one canonical origin-form HTTPS path/query, bind it into the exact scope hash, and prove that review/authorization/execution/adapter/I089/I090-shaped artifacts cannot drift to another endpoint.

## Added
- `exact_https_target_binding.py`
- `test_exact_https_target_binding.py`

## Result
The new binding contract rejects absolute URLs, authority/userinfo shapes, fragments, backslashes, whitespace and controls. Query ordering is preserved exactly and empty path canonicalizes to `/`.

`build_exact_https_target_binding()` inserts `https_path_query` into the exact production GET scope before hashing. `propagate_binding()` then requires the same hostname/path/query/target/adapter/scope hash across I086/I087/I088/I089-shaped artifacts and the adapter manifest. `validate_i090_request_unchanged()` is the final fail-closed pre-I090 check and rejects any out-of-band path/query, hostname or exact-scope drift.

Nine deterministic offline tests passed, including packet tamper, authorization scope tamper, manifest drift, I089 request-path drift, pre-I090 path change and idempotent replay. Python compilation passed. No DNS/HTTP, credentials, spend, KYC, paid action or value movement occurred.

## Important boundary
This run deliberately does **not** retroactively alter an already hash-bound/authorized artifact. The contract must be integrated into the fresh I086→I090 builders before any future authorization is requested. Existing I086–I091 artifacts therefore remain inert and insufficient for a live request.

## Risk / next
I093: integrate this binding into the actual fresh review/decision/consumption/adapter/gate/executor builders and their fixtures, so `path_query` is present before human decision hashing and `path` reaches I091 directly from I089. Keep the whole run offline. Only after that may a separately fresh explicit authorization chain be considered for one real anonymous read-only observation.
