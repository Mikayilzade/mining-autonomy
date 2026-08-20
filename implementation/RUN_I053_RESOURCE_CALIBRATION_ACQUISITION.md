# I053 — Local no-new-spend resource calibration acquisition plan

Status: **completed**
Date: 2026-08-21

Built `resource_calibration_acquisition.py`, defining the first concrete acquisition path for a real resource profile without assuming hardware, electricity price, quotas, subscription API access, credentials, or new spend.

The plan prioritizes the existing `deterministic_python` / `owned_pc` backend families and covers all 14 I050 critical resource parameters. It explicitly separates reproducibly observable local facts from facts that require declaration/provider evidence.

Offline probe facts that may be measured from a fixed benchmark transcript include local availability, demonstrated programmatic access, p95 latency, reliability, quality and bounded concurrency. Optional observed rate limits can be recorded when they are actually tested. The probe contract forbids network access, credentials, paid services and value movement.

Fields such as fixed/sunk cost classification, quotas, credential/paid-account/new-spend constraints, electricity cost and intentional no-rate-limit/no-quota states are never inferred from hardware or successful execution. Electricity-per-task may become measured evidence only from actual energy measurement plus an explicit tariff; otherwise it remains declared.

The transcript reducer is deterministic, requires at least 10 uniquely identified observations, rejects impossible quality-pass claims, separates reliability from conditional quality, emits an order-invariant transcript digest and does not manufacture non-observed accounting/interface fields.

Added 10 deterministic tests covering exact I050 field coverage, local-family restriction, inert probe flags, observable-field boundary, reliability/quality separation, repetition floor, duplicate IDs, invalid quality claims, non-inert contracts and transcript digest stability. GitHub Actions was not dispatched; no external action, credentials, spend or value movement occurred.

Next: **I054 — add a deterministic adapter that converts an I053 probe summary plus explicit declarations/energy evidence into I050 `ResourceEvidence` records, while preserving source-kind distinctions and refusing to fabricate missing fields. Use synthetic fixtures only.**
