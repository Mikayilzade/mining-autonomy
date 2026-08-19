# Implementation Run I014 — PayanAgent sanitization boundary + utilization-history comparison

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Prepare the stack for future permitted raw PayanAgent request/receipt observations without trusting arbitrary platform fields, leaking buyer identities, or producing false utilization comparisons across mismatched observation windows.

## Changes
Added `implementation/payan_sanitizer.py`:
- fail-closed PayanAgent request parser/sanitizer;
- bounded alias normalization for ID/content/payout/currency/deadline/skills;
- explicit rejection of closed/non-open requests, conflicting aliases, unsupported currencies, malformed timestamps and invalid payouts;
- platform `metadata` is ignored for compliance authorization;
- ToS/rights/automation/source-data permission can enter only through a separate trusted policy mapping;
- trusted cost/effort estimates are similarly separate from raw market data;
- receipt parser accepts one value representation (USD amount or cents), normalizes UTC time, and hash-minimizes recognized buyer/wallet/customer/payer identity before persistence;
- raw buyer identity fields are never emitted.

Added `implementation/utilization_history.py`:
- consumes two or more already-imported paid-utilization observations;
- reuses strict I013 aggregation, so provenance/hash/freshness/paid-evidence checks remain mandatory;
- rejects duplicate snapshot hashes, mixed platforms and mixed evidence classes;
- orders windows by trusted snapshot source timestamp;
- emits raw count/value deltas only when coverage durations match within explicit tolerance;
- mismatched windows return no deltas and are never normalized/extrapolated.

Added deterministic tests:
- trusted-policy separation and platform-metadata non-authority;
- alias conflict/non-open request rejection;
- buyer hashing/raw-identity removal;
- ambiguous amount and naive-time rejection;
- equal-duration raw utilization deltas;
- mismatched-window no-extrapolation behavior.

## Fresh read-only observation
Primary-source PayanAgent material observed on 2026-08-19 still documents:
- public `GET /api/v1/discover`;
- public `GET /api/v1/receipts` as a live settled-transaction feed;
- API-key-gated request bidding/fulfillment;
- signed receipts after settlement;
- machine-native API-first operation.

The rendered PayanAgent Requests marketplace surface returned `0 open` in the retrieved page. The Receipts surface exposed a `live` loading shell but no attributable rows. Neither rendered result was converted into a raw evidence snapshot because no reliable raw payload plus source timestamp was available.

Current MCPize first-party monetization docs still describe subscriptions and x402 pay-per-call, Base Sepolia test-first flow, and the standard 80% developer share for new monetized servers. This proves seller mechanics, not utilization.

## Safety / external actions
No authentication, account creation, KYC, wallet creation/funding, bid, task acceptance, fulfillment, approval, paid call, service publication, paid server, API spend or settlement occurred.

## CI / git
Push-triggered CI remains disabled; no manual workflow dispatch was performed. The stage was prepared as one atomic Git commit so code, tests, documentation and checkpoints move together without notification spam.

## Outcome
The implementation is now ready to ingest real PayanAgent data when a permitted raw payload becomes observable, while keeping compliance authority and buyer identity outside untrusted payloads. Utilization histories can be compared without turning mismatched observation windows into misleading rate estimates.

## Next — I015
Build an offline observation-bundle pipeline joining sanitizer → snapshot → saved-observation import → task replay/orchestrator + receipt aggregation/history → audit export, with fixture-driven end-to-end tests. Continue public read-only observation and save a real sanitized snapshot only when source timestamp and attributable raw payload are available.

Project state: **IMPLEMENTATION IN PROGRESS**.
