# Sources — Implementation Run I023

Evidence date: 2026-08-19

## Internal implementation sources
- `implementation/sampling_manifest.py`
- `implementation/test_sampling_manifest.py`
- `implementation/observation_capture.py`
- `implementation/evidence_archive.py`
- `implementation/archive_replay.py`
- `implementation/sampling_planner.py`

## Standard-library primitives used
- Python `json` canonicalized with sorted keys / compact separators and `allow_nan=False`.
- Python `hashlib.sha256` for content addressing.
- Python `hmac` with SHA-256 for optional local manifest authentication.

## External-evidence note
I023 adds an offline integrity/receipt layer only. It makes no new platform-demand, payout, ToS, KYC or geography claim and therefore did not require a new external platform-validation pass.

## Evidence rule
A valid hash/signature/receipt proves integrity and provenance only. It does not prove buyer demand, profitability, production environment, platform permission, identity eligibility, or authority to execute paid work.