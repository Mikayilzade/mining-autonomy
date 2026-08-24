import i173_structured_json_transform_executor as i173


def _sample():
    return {
        "schema_version": 1,
        "records": [
            {"id": "gamma", "value": 5, "ignored": "x"},
            {"id": "alpha", "value": 2},
            {"id": "beta", "value": 3},
        ],
    }


def test_valid_payload_is_deterministically_accepted():
    first = i173.execute(_sample())
    second = i173.execute(_sample())
    assert first.state == "DRY_RUN_ARTIFACT_ACCEPTED"
    assert first.accepted is True
    assert first.artifact == second.artifact
    assert first.artifact_digest == second.artifact_digest
    assert [row["id"] for row in first.artifact["records"]] == ["alpha", "beta", "gamma"]
    assert first.artifact["count"] == 3
    assert first.artifact["sum"] == 10


def test_acceptance_validator_recomputes_expected_artifact():
    result = i173.execute(_sample())
    assert i173.validate_artifact(_sample(), result.artifact) is True
    tampered = dict(result.artifact)
    tampered["sum"] = 999
    assert i173.validate_artifact(_sample(), tampered) is False


def test_invalid_inputs_fail_closed():
    bad_payloads = (
        {"schema_version": 2, "records": [{"id": "a", "value": 1}]},
        {"schema_version": 1, "records": []},
        {"schema_version": 1, "records": [{"id": "", "value": 1}]},
        {"schema_version": 1, "records": [{"id": "a", "value": True}]},
        {"schema_version": 1, "records": [{"id": "a", "value": 1}, {"id": "a", "value": 2}]},
    )
    for raw in bad_payloads:
        result = i173.execute(raw)
        assert result.state == "REJECTED"
        assert result.accepted is False
        assert result.artifact is None
        assert result.production_execution_enabled is False


def test_executor_contract_is_transform_only_and_inert():
    result = i173.execute(_sample())
    assert i173.ROUTER_CAPABILITY == "transform"
    assert i173.TASK_FAMILY == "structured_json_normalization_v1"
    assert i173.ACCEPTANCE_CONTRACT_ID == "structured-json-normalization-acceptance-v1"
    assert len(i173.acceptance_contract_digest()) == 64
    assert result.dry_run_only is True
    assert result.network_enabled is False
    assert result.credentials_used is False
    assert result.provider_account_used is False
    assert result.paid_service_used is False
    assert result.external_quota_used is False
    assert result.external_rate_limit_used is False
    assert result.task_acceptance_or_submission is False
    assert result.spend_or_value_movement is False
