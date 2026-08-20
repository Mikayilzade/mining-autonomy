# Implementation Run I046 — deterministic offline source-compliance attestation/replay

Date: 2026-08-20
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Add a deterministic offline provenance layer over I045 source-compliance metadata so manually supplied assertions are distinguishable from reproducible captured first-party evidence. Bind exact source URL, checked/retrieved/attested timestamps, source-content digest and policy conclusion without adding any transport capability.

## Changes
Added `implementation/source_compliance_attestation.py` with:
- `attest_source_compliance_evidence()`;
- `replay_source_compliance_attestation()`.

The attestation layer:
- independently revalidates the I045-compatible evidence hash and first-party HTTPS evidence class;
- binds platform, exact source URL, checked time, optional retrieval time, attestation time and exact source-content SHA-256;
- copies the policy conclusion (`anonymous_read_only_observation_permitted`, `credentials_required`, `human_only_access_required`) into the attested hash domain;
- distinguishes `manual_metadata_only` from `reproducible_captured_content`;
- never embeds source content and contains no network client or callback;
- marks all transport/network/authorization flags false.

The replay layer:
- revalidates the attestation hash and the nested I045 evidence hash;
- rejects source/platform/policy rebinding;
- rechecks evidence freshness and policy conclusions;
- requires the exact captured bytes to reproduce the stored content digest before classifying evidence as `reproducible_evidence_verified`;
- leaves manual-only metadata or missing/mismatched captured bytes blocked and does not expose them as usable `i045_evidence`;
- emits a deterministic replay hash while keeping transport and authorization disabled.

## Verification
Added `implementation/test_source_compliance_attestation.py` with eight deterministic tests covering:
1. matching captured content -> reproducible verified evidence;
2. manual metadata remains explicitly non-reproducible and is not promoted;
3. missing or changed captured bytes block replay;
4. stale/non-permitted policy blocks despite matching capture;
5. outer attestation tamper rejection;
6. rehashed nested evidence tamper still breaks the original binding;
7. retrieval/attestation chronology and UTC-only timestamps fail closed;
8. deterministic replay hash and bounded freshness window.

Isolated local verification: **8 passed** (`python -m pytest -q`). GitHub Actions was not dispatched and push-triggered CI remains disabled.

## Safety / external actions
All evidence and source bytes used in tests are synthetic. No DNS/HTTP, login, KYC, credentials, wallet, payment, bid, task acceptance, publication, paid API/server, settlement or other external/value-moving action occurred. No real platform permission is inferred.

## Outcome
The compliance boundary can now prove whether an I045-compatible first-party policy claim is merely manually supplied metadata or is reproducibly bound to exact captured source bytes. Only the latter can be replayed into an I045 evidence object; the former stays blocked/manual-only.

The economic gap remains unchanged: no real production demand/utilization sample has been taken.

## Next run — I047
Build an offline deterministic bridge that combines I046 replay output with the I045 human-review packet and requires `reproducible_evidence_verified` before `ready_for_human_decision`. Preserve exact I044 proposal/scope hashes, keep all fixtures synthetic, and remain transport-free. Add explicit proof that manual-only compliance metadata cannot reach the human-decision-ready state through the new bridge.

Project state: **IMPLEMENTATION IN PROGRESS**.
