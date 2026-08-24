# I180 — inert user-PC handoff package

Date: 2026-08-24

## Goal
Make the existing I178/I179 user-PC path easier to copy and run without creating or fabricating any evidence.

## Added
- `implementation/i180_user_pc_handoff_package.py`
- `implementation/test_i180_user_pc_handoff_package.py`
- `implementation/user_pc_handoff/measurement.NON_EVIDENCE.json`
- `implementation/user_pc_handoff/accounting.NON_EVIDENCE.json`
- `implementation/user_pc_handoff/README.md`

## Behaviour
I180 is self-contained and bound to the current runtime entry points:
- I178 blob: `9f227af6402e973b4a3b898b0bd9929cb61393cd`
- I179 blob: `e0dac00cba1acbd9d5dbda6362867af298f50a0a`

The checked-in measurement and accounting templates contain only null promotable values. They are deliberately NON_EVIDENCE and are required to fail the bound I178 structural contract until replaced with genuine owned-PC facts and provenance.

I180 performs only package generation/checking and Git-blob source-drift detection. It does not import or execute I178/I179, measure hardware, infer values, use network/credentials, dispatch CI, contact a market, accept/submit a task, create infrastructure, spend, settle, pay, move value, execute I050/I066/I123, or apply I176.

## Exact-local verification
The focused I180 closure was materialized locally from the exact authored bytes and compared to the current Git blob identities:
- `i180_user_pc_handoff_package.py` Git blob: `33e32b70ce9c5495111e5e5745c4439431889d8b`
- `test_i180_user_pc_handoff_package.py` Git blob: `9f427c505818c357542b03932cc29e1f64f62551`

Both local Git-blob hashes matched the repository blobs exactly.

Focused test result with network/proxy disabled:

`6 passed in 0.11s`

The tests cover blank/non-evidence invariants, deterministic package generation, exact-byte binding logic, source-drift fail-closed behaviour, and proof that I180 itself never fills a structurally complete real evidence packet.

## Checked-in package blobs
- measurement template: `e79aa961db042a94e66b60cdc95224841a00f0e9`
- accounting template: `ce3e89190192b3607874894b8a32986cb8326a3f`
- handoff README: `29dd08ee950c4acc9c0583cd79164a7b2fec38c9`

## Result
Repository-side user-PC handoff packaging is complete. The next genuine progress requires running exact I178/I179 on the actual owned PC with truthful measurement/accounting inputs. If trustworthy energy measurement is unavailable, the route remains blocked rather than estimated.
