# I163 — User-PC deterministic benchmark/session wrapper

Date: 2026-08-24
Status: **completed preparation checkpoint; focused tests authored, execution pending exact local checkout**

## Scope
Implemented the immediate next action from I162 without reopening discovery: a portable local-only deterministic benchmark/session wrapper for the existing `owned_pc` Resource / Execution Router branch.

## Implementation
Added `i163_user_pc_benchmark_session.py` and focused tests.

The wrapper reuses the existing fixed JSON-transform benchmark and measures only facts produced by the local run:
- benchmark quality acceptance probability;
- per-work-unit latency;
- reliability across repeated attempts;
- safe parallelism actually exercised at candidate concurrency levels.

Candidate parallelism is bounded by the Python-visible logical CPU count and an explicit cap, but CPU count itself is **not** accepted as measured parallelism. A parallelism level is promoted only when every attempted work unit at that level succeeds and matches the exact expected output. The session emits a hash-bound measurement-environment reference and an I162-compatible benchmark projection.

## Explicitly retained external blockers
I163 does not infer or fabricate:
- available hours/day;
- energy/joule readings;
- electricity tariff;
- opportunity cost.

Those remain explicit provenance-bound facts for I162/I159. Even with `--confirm-user-owned-pc`, benchmark completion cannot create a production route while those facts are absent.

## Verification status
Focused tests were added for:
1. bounded candidate parallelism with level 1 always present;
2. benchmark/session completion while availability, energy/tariff and opportunity cost remain blocked;
3. ownership confirmation making identity/benchmark ready without completing economics;
4. invalid repetition/iteration/parallelism inputs failing closed.

A direct fresh `git clone` into the execution container was attempted only to run these local tests, but the container could not resolve `github.com`. No GitHub Actions workflow was dispatched. Therefore this run does **not** claim that the new I163 focused tests executed in the current container; execution remains pending an exact local checkout/source-bound materialization.

## Safety / external effects
No production market/API request, credentials, account creation, downloads/paid installs, CI dispatch, paid infrastructure, task acceptance/submission, spend, settlement or value movement occurred.

## Risks / blockers
- I163 must ultimately run on the user-owned PC to produce real owned-PC benchmark evidence.
- A trustworthy local joule counter may still be unavailable; if so energy remains blocked.
- Availability, electricity tariff and opportunity cost still require explicit provenance.
- PayanAgent provider geography/access and exact bounded-observation authorization remain independent blockers.

## Next action
Materialize/run I163 on the user-owned PC (or first run its focused tests in an exact source-bound local checkout). Then extend the user-PC session packet with separately observed availability and, only if genuinely available, trustworthy energy-counter readings plus explicit tariff and opportunity-cost provenance. Do not estimate missing energy/economic facts and do not reopen discovery.
