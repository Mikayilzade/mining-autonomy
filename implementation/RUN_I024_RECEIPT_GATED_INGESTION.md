# Implementation Run I024 — receipt-gated durable evidence ingestion

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Close the integrity gap between sealed sampling manifests/capture receipts and durable evidence history. A sanitized bundle must not enter `evidence_archive` unless a receipt verifies against the exact sealed manifest item that produced it.

## Changes
### `observation_capture.py`
- retained `apply_captured_bundle()` / `run_capture_batch()` as transient offline helpers only;
- marked ordinary batch reports as **not eligible for durable ingestion**;
- added `run_verified_capture_batch()` accepting only `{bundle, manifest_envelope, receipt}` triplets;
- verifies each receipt against the sealed manifest;
- binds receipt bundle hash, platform, source URL, capture time and optional source timestamp to the normalized bundle;
- rejects non-GET receipts and invalid receipt environments;
- emits exact capture attestations only after verification.

### `evidence_archive.py`
- durable `append_capture_report()` now fails closed unless `receipt_required_for_durable_ingestion=True`;
- requires one verified attestation for every delta and rejects missing, duplicate or unmatched attestations;
- re-verifies each sealed manifest + receipt at the archive boundary instead of trusting the capture layer;
- requires receipt bundle/source/platform/capture-time/source-time consistency;
- receipt `captured_environment` is authoritative;
- caller-supplied environment mappings may confirm but cannot promote/relabel receipt evidence;
- serialized archives now declare `verified_capture_receipt_required: true` and `environment_policy: receipt_verified_explicit_only`.

### Tests
Updated archive tests cover unverified-report rejection, testnet isolation, production paid evidence, receipt tampering, bundle mismatch, environment override rejection, deterministic roundtrip and append-only/duplicate guards.

## Verification
Source files and tests were syntax-checked locally. Push-triggered CI remains disabled; workflow unchanged, so this stage does not generate GitHub notification spam.

## Safety / external actions
No network capture, account/login/KYC, API key, wallet, paid infrastructure, bid, task acceptance, service publication, transaction or settlement occurred.

## Outcome
The durable chain is now fail-closed at both sides:

`sealed manifest -> exact item -> sanitized bundle -> verified receipt -> verified capture report -> append-only evidence archive`

A sanitized bundle that lacks the correct sealed-manifest receipt can still be inspected transiently offline, but cannot become durable evidence.

## Next — I025
Add receipt-derived provenance references to replay/audit output and a sampling audit summary distinguishing scheduled-but-uncaptured, receipt-invalid, receipt-valid non-production and receipt-valid production evidence. Keep live transport disabled.
