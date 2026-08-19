# Implementation Run I025 — receipt-aware replay provenance + deterministic sampling audit

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Make the evidence audit path explain exactly what happened to each scheduled read-only sampling item after I024 receipt-gated ingestion, and make replay output reference the verified sealed-manifest/capture receipt when such provenance is supplied.

No live transport was enabled.

## Changes

### `sampling_audit.py`
Added a deterministic audit for sealed sampling manifests.

Every scheduled item is classified into exactly one of:
- `scheduled_but_uncaptured`;
- `receipt_invalid`;
- `receipt_valid_non_production`;
- `receipt_valid_production`.

Important fail-closed rules:
- duplicate receipts for one manifest item are invalid;
- structurally unmatched receipts cannot close any scheduled gap;
- tampered receipts fail receipt verification;
- valid `testnet` and `unknown` captures stay non-production;
- only a valid receipt whose authoritative captured environment is `production` enters the production-valid bucket;
- receipt evidence cannot authorize execution.

Added `receipt_provenance_index()`:
- accepts only a full receipt-gated capture report;
- reuses the durable-ingestion validator before returning anything;
- exposes exact `manifest_sha256`, `manifest_item_sha256`, `receipt_sha256`, authoritative captured environment, environment-evidence hash, source URL and capture finish time;
- remains keyed by sanitized bundle hash for deterministic replay matching.

### `archive_replay.py`
Added optional receipt-gated provenance input to `archive_replay_report()`.

Replay now:
- revalidates every supplied receipt-gated report;
- attaches receipt/manifest hash references only to the matching bundle;
- reports verified and missing receipt-provenance counts;
- rejects conflicting provenance for the same bundle;
- keeps all archive replay items HOLD-only;
- explicitly states that receipt provenance cannot authorize action.

The durable archive schema was deliberately left unchanged: receipt provenance is attached only when the source receipt-gated report is supplied and reverified, instead of pretending the archive stored receipt fields it does not currently persist.

### Tests
- Added `test_sampling_audit.py` covering all four required states, duplicate-receipt failure and unmatched-receipt handling.
- Reworked `test_archive_replay.py` to use I024 receipt-gated reports. The old fixture created unverified capture reports and was obsolete after I024.
- Added assertions for verified receipt provenance, missing provenance, and no-action invariants.

## Verification
New/modified Python modules and tests were syntax-checked locally.

Push-triggered CI remains disabled and the workflow was not modified, preventing a return of per-commit failure-email spam.

## Safety / external actions
No live HTTP capture, account/login/KYC, API key, wallet, paid infrastructure, bid, task acceptance, service publication, transaction or settlement occurred.

## Outcome
The audit chain can now distinguish a source that was merely scheduled from one that produced a valid non-production or production receipt, and replay can point back to the exact receipt/manifest hashes when the verified capture report is available.

This reduces a key ambiguity before any future real public observation experiment:
`scheduled != captured != receipt-valid != production-valid`.

## Next — I026
Build one deterministic end-to-end evidence audit export joining:
1. sealed sampling schedule;
2. receipt audit state;
3. durable archive membership;
4. replay receipt provenance;
5. unresolved production evidence gaps per platform/source.

Keep live transport disabled and do not infer demand from an uncaptured source.
