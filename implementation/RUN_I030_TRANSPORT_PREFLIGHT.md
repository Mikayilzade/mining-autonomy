# Implementation Run I030 — deterministic read-only transport preflight

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a deterministic transport-preflight layer over the I029 capture-session plan while keeping all real network activity disabled.

## Changes
Added `implementation/transport_preflight.py`:
- binds every scheduled I029 GET step to the exact I028 readiness row through `manifest_item_sha256`;
- revalidates exact platform, item index, source URL, host, method, production environment, expected evidence class and provenance checklist;
- carries the original conservative per-source rate contract into each transport envelope;
- hashes the full session plan, readiness packet, envelope set and each individual request binding;
- rejects source/manifest/host/schedule tampering, duplicate planned items and any non-GET, credentialed, action-enabled or non-production step;
- rejects localhost/private/non-global literal IP endpoints before any transport could exist;
- records a future DNS policy requiring execution-time resolution and rejection of non-global addresses to reduce SSRF/DNS-rebinding risk;
- declares a dependency-injected `ReadOnlyGetTransport` protocol but does not instantiate or call it;
- keeps redirects disabled until a separately authorized transport phase;
- defines a separate hash-bound explicit read-only authorization-envelope validator. Validation only produces an inert receipt; it still does not enable transport or perform HTTP.

Added `implementation/test_transport_preflight.py` with deterministic failure-mode coverage for exact binding, deterministic replay, manifest/source/host/schedule tampering, POST/credentials/action attempts, localhost/private endpoints, duplicate planned items, authorization-plan hash mismatch and synthetic authorization validation.

## Verification
Ten deterministic tests passed in an isolated local harness (`10 passed`). The test transport path remained fully synthetic and no network client was invoked.

## Safety / external actions
No HTTP request, login, KYC, API key, wallet, payment, task acceptance, bid, service publication, paid API, server rental or settlement occurred. The new preflight remains `transport_enabled=false`, `authorization_granted=false`, `network_calls_performed=false`, `credentials_allowed=false`, `dry_run_only=true`, and `action_enabled=false`.

## Outcome
The capture pipeline now reaches an exact request-envelope boundary that is integrity-bound to the previously sealed evidence plan and original conservative rate contracts. A later real read-only capture can be made auditable without letting a session plan self-authorize network access.

## Next run — I031
Build a deterministic authorization-to-execution gate around `ReadOnlyGetTransport` using a fake/in-memory transport only. Add execution receipts that bind response metadata to request hashes, enforce redirect/DNS/size/content-type limits at the adapter boundary, and prove that absent/expired/mismatched authorization cannot invoke the transport. Still perform no real HTTP request.

Project state: **IMPLEMENTATION IN PROGRESS**.
