# Status

Project state: **IMPLEMENTATION IN PROGRESS**

Discovery phase: **COMPLETE (Runs 001–062)**
Last completed implementation run: **I091 — concrete attested pinned HTTPS/JSON transport boundary**
Last updated: **2026-08-22**

## Latest durable files
- `implementation/RUN_I091_CONCRETE_ATTESTED_TRANSPORT_BOUNDARY.md`
- `implementation/concrete_pinned_https_json_transport.py`
- `implementation/test_concrete_pinned_https_json_transport.py`
- `implementation/RUN_I090_SINGLE_USE_TRANSPORT_EXECUTOR.md`
- `implementation/final_single_use_transport_executor.py`

## I091 outcome
The I090 transport boundary is now concrete rather than self-attested. It dials only an already-pinned public address through an injected connector, checks the actual raw/TLS peer, requires hostname-verifying `CERT_REQUIRED` TLS with the original hostname as SNI, sends one GET, follows no redirects, bounds headers/wire bytes/decompressed bytes while reading, accepts only UTF-8 JSON, and derives its result metadata from adapter operations/state. No live connector/resolver is bundled.

Nine deterministic in-memory socket/TLS/HTTP tests and syntax compilation passed. No live DNS/HTTP occurred.

A new fail-closed gap was exposed: the current I089-produced request specification binds hostname/pins/transport limits but does not cryptographically carry an exact HTTP path/query. I091 therefore refuses to run without a bound `path`; the endpoint may not be supplied out-of-band.

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
- I086–I089 remain narrow short-lived authorization/invocation lineage, not general execution permission.
- I090 consumes a valid I089 attempt even on transport error/result rejection and blocks replay before any second callable invocation.
- **I091 contains concrete pinned-address/TLS/HTTP/byte-bound mechanics but intentionally bundles no live connector or DNS resolver.**
- **I091 derives peer/SNI/request-count/redirect/size metadata from adapter state and rejects 3xx rather than following it.**
- **An exact path/query must be hash-bound upstream before any real observation; no target component may be injected after review.**
- No real DNS/HTTP request has yet been performed by this implementation chain.

## Immediate next run — I092
Repair the upstream target-binding gap: carry a canonical HTTPS path/query through the reviewed/authorized target lineage and adapter manifest into the I089 request specification, require I090 to validate it unchanged, and add tamper/replay tests. Keep all tests offline/synthetic. Do not perform a real observation until a separate fresh explicit authorization/safety chain permits exactly one read-only request using the fully bound target.

## Completion gate
Implementation completes only with confirmed positive economics on real permitted tests or exhaustion of reasonable candidates by control passes.
