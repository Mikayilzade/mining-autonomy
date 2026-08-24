# I159 — owned_pc portable evidence packet

Date: 2026-08-24

## Scope
Advance the existing I134/I137 `owned_pc` Resource / Execution Router branch without pretending the current execution container is the user's physical computer and without downloads, credentials, network use, paid infrastructure or spend.

## Work performed
Added `i159_owned_pc_evidence_packet.py`, a portable fail-closed evidence gate for measurements produced on a user-owned computer. The packet requires explicit provenance for hardware/OS/interface identity, deterministic programmatic access, benchmark identity, measured acceptance quality, latency, reliability, parallelism, measured availability, per-task energy, electricity tariff, and opportunity cost.

The gate deliberately distinguishes evidence completion from execution permission: even a complete packet only makes the backend evidence-eligible; `execution_enabled` remains false and downstream economics/authorization gates still apply.

## Current autonomous boundary
The repository automation has no direct, trustworthy measurement channel to the user's physical PC in this environment. Therefore the current state is **LOCAL_MATERIALIZATION_REQUIRED** rather than a fabricated pass/fail hardware judgment. The execution container must not be treated as owned-PC evidence.

This closes the autonomous no-new-spend evidence work available for `owned_pc` until a locally generated packet exists. Per I137, the next control-pass branch is the separately authorized external-backend family. Evidence/planning may continue offline, but no credentials, account creation, API calls carrying spend, VPS rental or production task execution may occur without separate explicit authorization.

## Verification
Focused local tests: **4 passed**. Covered empty/local-materialization state, rejection of unbound measurements, a complete synthetic packet that promotes evidence only, and fail-closed handling of forbidden probe effects.

## Safety / external effects
No production market request, model download, credential use, CI dispatch, task acceptance, paid account, infrastructure rental, spend, payment or value movement occurred.

## Next action
Run a control pass over the remaining existing backend families (`subscription_assistant`, `cheap_external_api`, `strong_external_api`, `future_paid_vps`) and classify which are support-only, authorization-gated or evidence-preparable without credentials/spend. Preserve sunk-vs-marginal cost semantics and do not reopen discovery.
