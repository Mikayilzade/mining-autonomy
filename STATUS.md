# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I092 — canonical exact HTTPS path/query binding contract**
Last updated: **2026-08-22**

## Latest durable files
- `implementation/RUN_I092_EXACT_HTTPS_TARGET_BINDING.md`
- `implementation/exact_https_target_binding.py`
- `implementation/test_exact_https_target_binding.py`
- `implementation/RUN_I091_CONCRETE_ATTESTED_TRANSPORT_BOUNDARY.md`
- `implementation/concrete_pinned_https_json_transport.py`

## I092 outcome
The I091 path/query gap now has a deterministic fail-closed contract. Only canonical origin-form HTTPS path/query is accepted; absolute URLs, authority/userinfo shapes, fragments, controls, whitespace and backslashes are rejected. The exact path/query is inserted into the exact production-GET scope before hashing, and validation requires it unchanged across review, authorization, execution-envelope, adapter-manifest and I089-shaped artifacts plus a final pre-I090 drift check.

Nine offline deterministic tests and syntax compilation passed. No network activity occurred.

Important: this is a safe binding-contract checkpoint, not a retroactive authorization repair. Existing I086–I091 artifacts remain inert. The actual fresh builders still need I092 fields integrated before any future decision/authorization can bind a real endpoint.

## Current ranking
1. PayanAgent
2. OKX.AI A2A ASP
3. agent2agent.market
4. MCPize
5. AgentGigs.io

## Durable rules
- Real demand/fill remains the dominant unknown.
- No irreversible/paid action without explicit user authorization.
- Resource routing never widens upstream policy/demand eligibility.
- Synthetic/default resources remain planning references; only current reproducible materialized resources are selectable.
- Exact scope remains one production GET, no credentials, no action.
- ChatGPT/Codex subscription is fixed/sunk limited support, not a free autonomous API.
- I086–I091 remain narrow short-lived authorization/invocation lineage, not general execution permission.
- I090 consumes a valid I089 attempt even on transport error/result rejection and blocks replay before any second callable invocation.
- I091 bundles no live connector or DNS resolver and requires a bound path.
- I092 forbids out-of-band endpoint components and requires path/query inside the exact-scope hash.
- Existing pre-I092 authorizations cannot be upgraded or reused; a fresh lineage is required after builder integration.
- No real DNS/HTTP request has yet been performed by this implementation chain.

## Immediate next run — I093
Integrate the I092 canonical `https_path_query` binding into the actual fresh I086 review packet, I087 decision/authorization, I088 execution envelope/receipt checks, adapter manifest, I089 request specification and I090 pre-transport validation. Update deterministic fixtures and tamper/replay regressions. Keep all tests offline/synthetic. Do not perform a real observation.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
