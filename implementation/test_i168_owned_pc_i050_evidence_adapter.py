import copy

import i168_owned_pc_i050_evidence_adapter as i168


def _reference():
    # Minimal identity-bearing mapping is sufficient for I168's hash-binding tests;
    # production use passes the exact current owned_pc Router reference mapping.
    return {
        "backend_id": "owned_pc",
        "family": "owned_pc",
        "programmatic_access": True,
        "currently_available": True,
    }


def _i166():
    explicit = {
        "benchmark_id": "python-local-fixed-json-transform-v1",
        "benchmark_source_ref": "repo:i163-fixed-json-transform-session-v1:abc123",
        "quality_acceptance_probability": 1.0,
        "latency_seconds": 0.25,
        "reliability_probability": 1.0,
        "max_parallelism": 2,
        "measured_available_hours_per_day": 8.0,
        "availability_source_ref": "local-log:availability-2026-08-24",
        "energy_before_joules": 1000.0,
        "energy_after_joules": 4600.0,
        "energy_task_count": 10,
        "energy_source_ref": "local-meter:session-2026-08-24",
        "tariff_usd_per_kwh": 0.1,
        "tariff_source_ref": "utility-bill:applicable-tariff-2026-08",
        "opportunity_cost_usd_per_hour": 0.01,
        "opportunity_cost_source_ref": "user-declaration:pc-occupation-cost-2026-08-24",
    }
    observation = {
        **explicit,
        "deterministic_programmatic_access_verified": True,
        "measurement_environment_ref": "i163-session:environment-digest",
        "measurements_from_user_owned_pc": True,
    }
    packet = {
        "state": "USER_PC_PACKET_COMPLETE",
        "explicit_measurements": explicit,
        "derived_energy_kwh_per_task": 0.0001,
        "i159_evaluation": {
            "production_evidence_ready": True,
            "observation": observation,
        },
    }
    return {
        "schema": "mining-autonomy/i166-user-pc-real-evidence-gate/v1",
        "run": "I166",
        "gate": {
            "state": "REAL_EXTERNAL_EVIDENCE_ACCEPTED",
            "ownership_confirmation_supplied": True,
        },
        "i165_result": {
            "state": "USER_PC_MATERIALIZED",
            "i162_packet": packet,
        },
    }


def _i167(i166_result):
    return {
        "state": "ROUTER_RESOURCE_FACTS_READY",
        "backend_id": "owned_pc",
        "source_digest": i168._git_source_digest(i166_result),
        "router_backend_patch": {
            "backend_id": "owned_pc",
            "currently_available": True,
            "electricity_per_task_usd": 0.00001,
            "opportunity_cost_per_task_usd": 0.000000694444,
            "latency_seconds": 0.25,
            "reliability_probability": 1.0,
            "quality_probability": 1.0,
            "max_parallelism": 2,
        },
    }


def test_adapter_emits_only_seven_measured_i050_parameters():
    i166_result = _i166()
    result = i168.build_adapter(
        i166_result,
        _i167(i166_result),
        _reference(),
        observed_at="2026-08-24T07:30:00Z",
    )
    assert result.state == "PARTIAL_I050_EVIDENCE_READY"
    assert result.errors == ()
    assert result.i166_i167_source_binding_valid is True
    assert result.emitted_parameters == i168.MEASURED_PARAMETERS
    assert result.missing_control_parameters == i168.CONTROL_PARAMETERS
    assert len(result.emitted_records) == 7
    assert len(result.missing_control_parameters) == 7
    assert all(record.evidence_hash for record in result.emitted_records)
    assert all(record.backend_id == "owned_pc" for record in result.emitted_records)
    assert result.i050_attestation_executed is False
    assert result.i066_materialization_executed is False
    assert result.i123_promotion_performed is False


def test_i167_must_be_bound_to_exact_i166_packet():
    i166_result = _i166()
    i167_result = _i167(i166_result)
    changed = copy.deepcopy(i166_result)
    changed["i165_result"]["i162_packet"]["explicit_measurements"]["measured_available_hours_per_day"] = 9.0
    result = i168.build_adapter(
        changed,
        i167_result,
        _reference(),
        observed_at="2026-08-24T07:30:00Z",
    )
    assert result.state == "PASS_BLOCKED"
    assert "i166_i167_source_digest_mismatch" in result.errors
    assert result.emitted_records == ()


def test_unaccepted_or_unowned_evidence_fails_closed():
    i166_result = _i166()
    i166_result["gate"]["ownership_confirmation_supplied"] = False
    i167_result = _i167(i166_result)
    result = i168.build_adapter(
        i166_result,
        i167_result,
        _reference(),
        observed_at="2026-08-24T07:30:00Z",
    )
    assert result.state == "PASS_BLOCKED"
    assert "i166_ownership_confirmation_missing" in result.errors
    assert result.emitted_records == ()


def test_invalid_observed_at_or_reference_fails_closed():
    i166_result = _i166()
    result = i168.build_adapter(
        i166_result,
        _i167(i166_result),
        {"backend_id": "python_local", "family": "deterministic_python"},
        observed_at="2026-08-24T07:30:00",
    )
    assert result.state == "PASS_BLOCKED"
    assert "observed_at_must_be_utc" in result.errors
    assert "owned_pc_reference_required" in result.errors
    assert "owned_pc_reference_family_required" in result.errors


def test_record_hash_is_stable_and_tamper_evident():
    i166_result = _i166()
    result = i168.build_adapter(
        i166_result,
        _i167(i166_result),
        _reference(),
        observed_at="2026-08-24T07:30:00Z",
    )
    record = result.emitted_records[0]
    assert record.evidence_hash == i168._digest(record.hash_body())
    changed = {**record.hash_body(), "value": not bool(record.value)}
    assert i168._digest(changed) != record.evidence_hash
