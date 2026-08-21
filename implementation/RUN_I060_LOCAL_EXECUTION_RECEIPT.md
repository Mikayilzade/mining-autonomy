# I060 — inert local execution plan / receipt boundary

Status: **completed** — 2026-08-21

Added `local_execution_receipt.py` as the first boundary after an I059-selected `python_local` route. The plan accepts only a provenance-verified `route_dry_run`, binds the exact task, I059 provenance hash, fixed fixture and expected output, and copies the selected router marginal-cost quote.

The executor can run only the caller-supplied deterministic local fixture function. Fixture drift fails before execution. The receipt records measured wall-clock runtime and only explicitly supplied energy/other incremental costs; unknown energy remains unknown rather than inferred. Output identity mismatch or observed incremental cost beyond the router quote tolerance produces `hold`.

All records remain `dry_run_only`; network, credentials, market submission and value movement are hard-disabled. This stage is local evidence generation only and is not authorization to accept or submit paid work.

Verification in this automation environment was limited to construction/review of the deterministic module; no repository checkout/runtime was available, so no pytest/green-CI claim is made and GitHub Actions was not dispatched.

Next: **I061 — add deterministic replay/verification for I060 receipts, including plan/provenance/fixture/output hashes, runtime envelope evidence and explicit unknown-energy handling; then bridge verified receipts back into resource calibration without allowing a benchmark to prove market demand or execution authorization.**
