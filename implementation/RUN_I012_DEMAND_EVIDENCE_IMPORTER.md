# Implementation Run I012 — demand-evidence scoring + saved-observation importer

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Prevent supply/listing/marketing signals from being confused with actual buyer demand, and add an offline import boundary for previously saved observation snapshots without adding network, credential, publication, execution or settlement capability.

## Changes
Added `implementation/demand_evidence.py` with fail-closed classes: `settled_receipt` (strength 4, paid utilization), `paid_invocation` (4, paid utilization), `open_paid_request` (3, current paid demand), `listing_only` (1, supply only), `marketing_claim` (0), and `unknown` (0). Unknown custom labels are rejected.

Added `implementation/observation_importer.py`. It accepts already-saved JSON/path/mapping envelopes, reconstructs `EvidenceSnapshot`, re-runs provenance/hash/freshness checks, validates the exact snapshot schema and performs no network calls. Replay into task adapters is allowed only for evidence classified as `open_paid_request`.

Extended `implementation/orchestrator.py` so every observation carries evidence class/strength plus `paid_utilization_proven` and `open_paid_demand_proven`. Positive-margin task payloads are held unless backed by `open_paid_request`; passive projected economics are held unless backed by attributable paid-utilization evidence. Audit export now reports evidence-class counts separately from acceptance/hold/reject counts.

Tests cover evidence ordering, invalid classes, importer hash validation, replay gating, trusted timestamps, listing-vs-open-request handling, passive utilization gating and evidence-aware audit output. Existing orchestrator tests now state evidence assumptions explicitly.

## Public read-only refresh
Evidence date: 2026-08-19.

PayanAgent first-party material still documents anonymous discovery/offers/receipts endpoints plus request/bid/fulfill/approve and signed receipt issuance. The 24,000+ offer count is classified as supply/listing evidence, not worker demand. No attributable raw request/receipt snapshot was captured.

MCPize first-party developer/hosting/monetization material still documents 80% creator share for new monetized servers, x402 USDC pay-per-call, Stripe Connect subscription payouts and a free hosting tier with 250K requests/month. These prove seller mechanics/low fixed-cost feasibility, not attributable paid utilization. No real paid-utilization snapshot was captured.

## CI / notification hygiene
No workflow change and no manual CI dispatch. Push-triggered CI remains disabled. This stage is committed as one final repository commit. Local syntax compilation of changed Python files succeeded; green GitHub CI is not claimed.

## Safety / external actions
No account creation/login, KYC, wallet, paid API/server, task acceptance, bid, service publication, transaction, settlement or money movement occurred.

## Outcome
The control plane now separates: seller/listing existence, current open paid demand, and actual settled/paid utilization. These can no longer be silently collapsed into one "demand" signal.

## Next run — I013
1. Add an evidence-aware replay-to-orchestrator bridge for imported `open_paid_request` snapshots.
2. Add saved receipt/utilization aggregation (count, value, recurrence, buyer concentration) while keeping identities sanitized.
3. Continue read-only PayanAgent receipt/request and MCPize utilization checks; save real sanitized snapshots only when raw permitted data is actually observable.
4. Keep one-stage/one-final-commit and push-CI-disabled hygiene.

Project state: **IMPLEMENTATION IN PROGRESS**.
