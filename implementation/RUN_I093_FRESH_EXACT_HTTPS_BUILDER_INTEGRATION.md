# Implementation Run I093 — fresh exact HTTPS builder-lineage integration

Date: 2026-08-22
Status: **completed safe checkpoint; offline only**

## Goal
Connect the I092 canonical `https_path_query` contract to the actual fresh I086→I090 artifact lineage without retroactively modifying any existing authorization and without performing a network request.

## Added
- `fresh_exact_https_builder_integration.py`
- `test_fresh_exact_https_builder_integration.py`

## Result
The new integration layer uses the exact production artifact/hash field names from I086–I090. It:
1. reseals a fresh I086 review packet with the canonical bound exact scope and `path_query` **before** any human decision;
2. reseals I087 authorization with the identical scope/path binding;
3. propagates the binding into I088 execution envelope and consumption receipt while preserving single-use lineage;
4. binds adapter manifest path/query and exact-scope hash;
5. inserts the canonical path into I089 `request_spec`;
6. provides a final pre-I090 fail-closed validator for path, hostname, target, adapter and exact-scope drift.

The module does not perform DNS, TLS, HTTP, task acceptance, submission, settlement or value movement. Existing pre-I092 authorization artifacts are not upgraded and remain inert.

## Validation
The new module and regression file compile cleanly offline. Regression cases cover review packet resealing before decision, I089 path insertion, pre-I090 path drift rejection, adapter-manifest path hash binding and out-of-band hostname rejection. No live target was contacted.

## Risks / limitation
I093 deliberately uses a narrow integration adapter around the existing builder artifact schemas rather than rewriting several mature builders at once. This minimizes regression risk but means the native builders still accept legacy unbound fixtures unless the adapter is used.

## Next action
I094: inline the I093 invariants into the native I086/I087/I089/I090 builders, migrate native and downstream fixtures to bound `https_path_query`, and run the complete implementation suite offline/synthetic. Only after that may a separately fresh explicit authorization chain be considered for one anonymous read-only real observation.
