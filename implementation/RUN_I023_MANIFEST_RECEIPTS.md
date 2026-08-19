# Implementation Run I023 — sealed sampling manifests + capture receipts

Date: 2026-08-19
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add deterministic integrity sealing for inert sampling manifests and a capture-result receipt contract that proves exactly which manifest item produced a sanitized bundle, while keeping all built-in network access disabled.

## Changes
Added `implementation/sampling_receipt.py`.

The new integrity layer provides:
- canonical UTF-8 JSON serialization with sorted keys and no NaN values;
- SHA-256 hash envelopes for complete sampling manifests;
- optional HMAC-SHA256 authentication with explicit `key_id`;
- fail-closed manifest verification that rechecks GET-only, no-credentials, no-action and no-network flags;
- per-item hashes bound to both the manifest hash and item index;
- deterministic capture receipts binding source URL, method, platform, expected evidence class, environment, timestamps and sanitized bundle SHA-256 to the sealed manifest item;
- receipt self-hashing and replay verification;
- explicit prohibition on receipt-derived execution authority.

Added an injected transport scaffold only. There is no built-in HTTP client. A network-capable injected transport is rejected unless the caller explicitly sets `allow_network=True`; missing transport fails closed. Results that report credentials or action execution are rejected.

Environment handling remains conservative: an item declared `unknown` cannot be recorded as `production` unless a separate environment-evidence SHA-256 is supplied. This records evidence provenance but still does not authorize execution.

Added `implementation/test_sampling_receipt.py` with eight deterministic tests covering canonical/HMAC verification, tamper detection, manifest-item binding, default network denial, offline mock receipt creation, receipt tampering, unknown→production evidence requirement, and credential/action/unscheduled rejection.

## Verification
Local isolated test run: **8 passed**.

Push-triggered CI remains disabled and the workflow is unchanged, so this run does not create GitHub notification spam.

## Safety / external actions
No network capture, login, account, KYC, API key, wallet, paid server/API, bid, task acceptance, service publication, transaction or settlement occurred. No raw buyer identity or raw platform payload was persisted.

## Outcome
The stack now has a cryptographically bound chain from `sampling plan -> manifest -> exact manifest item -> sanitized capture bundle -> receipt`, with network/action authority still absent by default.

## Next — I024
Integrate verified capture receipts into `observation_capture` / `evidence_archive` ingestion so a sanitized bundle cannot enter the durable archive unless its receipt verifies against the sealed manifest. Add replay fixtures for mismatch/tamper/environment cases and keep live transport disabled.