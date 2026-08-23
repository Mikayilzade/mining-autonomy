#!/usr/bin/env python3
"""I110 adversarial self-test for I109 lineage/preauthorization bridge; network-inert."""
from __future__ import annotations
import copy
import i109_lineage_preauthorization_consistency_validator as i109


def blocker(value: bool) -> dict:
    return {"satisfied": value}


def base_i104() -> dict:
    return {
        "non_substitutable_blockers": {
            "fresh_real_execution_evidence": blocker(False),
            "current_materialized_non_synthetic_resource_route": blocker(False),
            "exact_explicit_user_authorization": blocker(False),
            "runtime_regression_verification": blocker(False),
        },
        "production_observation_allowed": False,
        "external_effects": {"production_dns_http_socket_tls": False},
    }


def base_i100() -> dict:
    return {
        "readiness_inputs": {
            "fresh_real_execution_evidence_not_synthetic": False,
            "fresh_real_execution_evidence_valid": False,
            "current_materialized_route_supplied": False,
            "resource_route_not_synthetic": False,
            "resource_route_eligible": False,
            "explicit_exact_authorization_present": False,
        },
        "ready_for_network_invocation": False,
        "execution_token": False,
        "network_capable": False,
    }


def valid_i108() -> dict:
    return {
        "result": "PASS",
        "receipt_present": True,
        "exact_source_lineage_valid": True,
        "derived_blockers": {"runtime_regression_verification": True},
    }


def main() -> int:
    cases = []
    a = i109.validate(base_i104(), base_i100(), None)
    cases.append(a["result"] == "PASS" and a["runtime_lineage_projected"] is False and a["four_gate_and"] is False)

    b = i109.validate(base_i104(), base_i100(), valid_i108())
    cases.append(b["result"] == "PASS" and b["runtime_lineage_projected"] is True and b["four_gate_and"] is False)
    cases.append(b["derived_blockers"]["fresh_real_execution_evidence"] is False)
    cases.append(b["derived_blockers"]["current_materialized_non_synthetic_resource_route"] is False)
    cases.append(b["derived_blockers"]["exact_explicit_user_authorization"] is False)

    forged = valid_i108(); forged["exact_source_lineage_valid"] = False
    c = i109.validate(base_i104(), base_i100(), forged)
    cases.append(c["runtime_lineage_projected"] is False and c["four_gate_and"] is False)

    stale104 = base_i104(); stale104["non_substitutable_blockers"]["runtime_regression_verification"] = blocker(True)
    d = i109.validate(stale104, base_i100(), None)
    cases.append(d["result"] == "FAIL_CLOSED")

    permissive = base_i104(); permissive["production_observation_allowed"] = True
    e = i109.validate(permissive, base_i100(), valid_i108())
    cases.append(e["result"] == "FAIL_CLOSED" and e["four_gate_and"] is False)

    print(f"I110 adversarial bridge self-test: {'PASS' if all(cases) else 'FAIL'} ({sum(cases)}/{len(cases)})")
    return 0 if all(cases) else 2

if __name__ == "__main__":
    raise SystemExit(main())
