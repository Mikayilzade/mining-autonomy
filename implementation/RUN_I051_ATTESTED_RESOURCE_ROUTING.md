# Implementation Run I051 — attested resource routing

Date: 2026-08-21
Status: **COMPLETED**
Phase: Implementation / Experiment

## Objective
Integrate I050 resource-profile attestations into the I048/I049 Resource / Execution Router so illustrative default backends remain planning references and only complete current evidence can enter the calibrated route set.

## Changes
Added `implementation/resource_routing_attestation.py` and `implementation/test_resource_routing_attestation.py`.

The integration now:
- always keeps synthetic/default backend quotes visible as reference planning information;
- never allows an unattested reference backend to become selectable merely because its synthetic cost is low;
- accepts only I050 `calibrated_declared` or `calibrated_reproducible` attestations bound to the exact reference backend;
- materializes calibrated router fields only through the I050 evidence boundary;
- reports explicit route states: `resource_evidence_missing`, `calibrated_declared_route`, and `calibrated_reproducible_route`;
- preserves the underlying router's capability, quota, policy, success-probability and conservative-margin gates after calibration;
- rejects attestations for unknown reference backends and duplicate reference/attestation IDs;
- keeps `dry_run_only=true`, `execution_enabled=false`, `network_enabled=false`, and `value_movement_enabled=false`.

## Verification
Added seven deterministic tests covering reference-only fail-closed routing, reproducible calibration, declared calibration labeling, planning-only evidence, cheaper-but-unproven reference exclusion, post-calibration quality gating and unknown-attestation rejection. Module and test syntax compiled successfully in the run environment. GitHub Actions was not dispatched.

## Outcome
Synthetic resource assumptions can no longer win an execution-route decision. The routing layer now distinguishes planning economics from evidence-backed current resource economics while preserving the ability to compare both for planning.

The next gap is to connect this attested router to the full I049 observation bridge so upstream policy/demand evidence remains authoritative and route records expose both upstream evidence state and resource-calibration provenance in one deterministic object.

## Next run — I052
Build the end-to-end `observe -> demand/policy gate -> TaskEconomics -> attested resource route` bridge. Require I049 upstream acceptance before any attested resource routing, carry I050 evidence bundle/calibration state into the combined record, and ensure reference-only resources can never convert an upstream candidate into a routable state. Keep all execution/network/value movement disabled.

Project state: **IMPLEMENTATION IN PROGRESS**.
