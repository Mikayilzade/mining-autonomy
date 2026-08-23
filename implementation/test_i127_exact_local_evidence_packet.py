from dataclasses import asdict

import i127_exact_local_evidence_packet as m
from resource_profile_evidence import make_evidence, reference_backend_hash
from resource_router import default_backend_families


def fake_i124():
    return {
        "result_hash": "r" * 64,
        "python_local_probe": {
            "state": "MEASURED_LOCAL_PROBE_COMPLETE",
            "backend_id": "python_local",
            "observed_at": "2026-08-23T19:00:00Z",
            "repetitions": 20,
            "successful_runs": 20,
            "quality_passes": 20,
            "latency_p95_seconds": 0.01,
            "reliability_probability_observed": 1.0,
            "quality_probability_observed": 1.0,
            "max_parallelism_observed": 1,
            "rate_limit_per_minute_observed": None,
            "portable_transcript_digest": "a" * 64,
            "network_enabled": False,
            "credentials_used": False,
            "spend_performed": False,
            "value_movement_enabled": False,
        },
    }


def reference():
    return asdict(next(x for x in default_backend_families() if x.backend_id == "python_local"))


def extra(parameter, value, source_kind="measured_local"):
    ref = reference()
    return make_evidence(
        evidence_id=f"extra-{parameter}",
        backend_id="python_local",
        parameter=parameter,
        value=value,
        source_kind=source_kind,
        source_ref=f"fixture://{parameter}",
        observed_at="2026-08-23T19:00:00Z",
        max_age_seconds=3600,
        reference_hash=reference_backend_hash(ref),
        source_content_digest="b" * 64,
        notes="test fixture only",
    )


def test_default_packet_has_only_three_dynamic_gaps_after_i124_plus_i126():
    result = m.build_exact_packet(fake_i124())
    assert result["state"] == "PASS_BLOCKED"
    assert set(result["missing_parameters"]) == {
        "quota_units_remaining", "electricity_per_task_usd", "rate_limit_per_minute"
    }
    assert result["i066_materialization"] is None
    assert result["current_resource_route_created"] is False


def test_complete_additional_evidence_reaches_reproducible_i050_and_i066():
    result = m.build_exact_packet(fake_i124(), additional_records=(
        extra("quota_units_remaining", None, "system_probe"),
        extra("electricity_per_task_usd", 0.001, "measured_local"),
        extra("rate_limit_per_minute", None, "system_probe"),
    ))
    assert result["state"] == "RESOURCE_EVIDENCE_COMPLETE"
    assert result["missing_parameters"] == ()
    assert result["i050_attestation"]["state"] == "calibrated_reproducible"
    assert result["i066_materialization"]["state"] == "materialized_reproducible"
    assert result["i123_backend_evidence"]["provenance_class"] == "measured_reproducible"
    assert result["current_resource_route_created"] is False


def test_disallowed_additional_parameter_cannot_make_packet_complete():
    record = extra("latency_seconds", 1.0)
    result = m.build_exact_packet(fake_i124(), additional_records=(record,))
    assert result["state"] == "PASS_BLOCKED"
    assert "quota_units_remaining" in result["missing_parameters"]
    assert "electricity_per_task_usd" in result["missing_parameters"]
    assert "rate_limit_per_minute" in result["missing_parameters"]


def test_unverified_or_non_inert_probe_is_rejected():
    bad = fake_i124()
    bad["python_local_probe"]["network_enabled"] = True
    try:
        m.build_exact_packet(bad)
        assert False
    except ValueError as exc:
        assert "not_inert" in str(exc)


def test_probe_records_are_hash_bound_and_do_not_include_config_or_energy():
    records = m.build_probe_evidence(reference(), fake_i124()["python_local_probe"])
    params = {x.parameter for x in records}
    assert params == set(m.PROBE_PARAMETERS)
    assert "electricity_per_task_usd" not in params
    assert "fixed_monthly_cost_usd" not in params
