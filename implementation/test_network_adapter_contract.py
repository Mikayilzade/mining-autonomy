from copy import deepcopy
from network_adapter_contract import validate_network_capable_adapter_contract, _hash, _required_transport_gates


def consumption_fixture():
    scope = {
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": "payanagent:public-task-feed:v1",
        "credentials_allowed": False,
        "action_enabled": False,
    }
    env_core = {
        "schema_version": 1,
        "mode": "single_use_real_transport_authorized_attempt_envelope",
        "attempt_state": "authorized_attempt_preflight_ready_no_network",
        "consumed_at_utc": "2026-08-21T20:02:00Z",
        "authorization_expires_at_utc": "2026-08-21T20:03:00Z",
        "real_transport_authorization_verification_sha256": "v" * 64,
        "real_transport_authorization_sha256": "a" * 64,
        "pre_real_transport_review_sha256": "r" * 64,
        "real_transport_decision_sha256": "d" * 64,
        "exact_scope_sha256": "s" * 64,
        "exact_scope": scope,
        "mandatory_transport_gates": _required_transport_gates(),
        "max_network_requests": 1,
        "authorization_consumed": True,
        "authorization_reusable": False,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "transport_adapter_present": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "envelope_is_network_result": False,
    }
    env = {**env_core, "authorized_attempt_envelope_sha256": _hash(env_core)}
    core = {
        "schema_version": 1,
        "mode": "deterministic_real_transport_authorization_consumption_preflight",
        "consumption_state": "authorization_consumed_preflight_ready_no_network",
        "consumed_at_utc": "2026-08-21T20:02:00Z",
        "real_transport_authorization_verification_sha256": "v" * 64,
        "real_transport_authorization_sha256": "a" * 64,
        "pre_real_transport_review_sha256": "r" * 64,
        "real_transport_decision_sha256": "d" * 64,
        "exact_scope_sha256": "s" * 64,
        "authorization_consumed": True,
        "authorization_reusable": False,
        "authorized_attempt_envelope": env,
        "blockers": [],
        "transport_adapter_present": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "consumption_record_is_network_token": False,
    }
    return {**core, "real_transport_authorization_consumption_sha256": _hash(core)}


def declaration_fixture(consumption=None):
    c = consumption or consumption_fixture()
    env = c["authorized_attempt_envelope"]
    scope = env["exact_scope"]
    core = {
        "schema_version": 1,
        "mode": "network_capable_adapter_contract_declaration",
        "adapter_id": "future-safe-https-json-v1",
        "network_capable": True,
        "bound_authorized_attempt_envelope_sha256": env["authorized_attempt_envelope_sha256"],
        "bound_exact_scope_sha256": env["exact_scope_sha256"],
        "request_contract": {
            "method": "GET",
            "max_network_requests": 1,
            "required_environment": "production",
            "target_fingerprint": scope["target_fingerprint"],
            "credentials_allowed": False,
            "action_enabled": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "value_movement_enabled": False,
        },
        "enforced_transport_gates": _required_transport_gates(),
        "execution_entrypoint_present": False,
        "execution_entrypoint_reachable": False,
        "transport_callable_attached": False,
        "execution_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_embedded": False,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "value_movement_enabled": False,
    }
    return {**core, "adapter_contract_sha256": _hash(core)}


def rehash(obj, field):
    core = deepcopy(obj)
    core.pop(field, None)
    return {**core, field: _hash(core)}


def rehash_envelope_and_consumption(c):
    c["authorized_attempt_envelope"] = rehash(c["authorized_attempt_envelope"], "authorized_attempt_envelope_sha256")
    return rehash(c, "real_transport_authorization_consumption_sha256")


def test_exact_contract_produces_review_only_readiness():
    c = consumption_fixture()
    d = declaration_fixture(c)
    out = validate_network_capable_adapter_contract(c, d)
    assert out["validation_state"] == "adapter_contract_ready_for_separate_review_no_execution"
    assert out["blockers"] == []
    art = out["adapter_readiness_artifact"]
    assert art["ready_for_real_network_execution"] is False
    assert art["separate_human_review_required"] is True
    assert art["execution_entrypoint_reachable"] is False
    assert out["network_enabled"] is False


def test_consumption_hash_tamper_fails_closed():
    c = consumption_fixture()
    c["network_enabled"] = True
    out = validate_network_capable_adapter_contract(c, declaration_fixture())
    assert "i075_consumption_hash_invalid" in out["blockers"]
    assert out["adapter_readiness_artifact"] is None


def test_envelope_hash_tamper_fails_closed_even_if_consumption_rehashed():
    c = consumption_fixture()
    c["authorized_attempt_envelope"]["max_network_requests"] = 2
    c = rehash(c, "real_transport_authorization_consumption_sha256")
    out = validate_network_capable_adapter_contract(c, declaration_fixture())
    assert "authorized_attempt_envelope_hash_invalid" in out["blockers"]


def test_rehashed_scope_widening_fails_closed():
    c = consumption_fixture()
    c["authorized_attempt_envelope"]["exact_scope"]["request_count"] = 2
    c = rehash_envelope_and_consumption(c)
    d = declaration_fixture(c)
    out = validate_network_capable_adapter_contract(c, d)
    assert "authorized_attempt_scope_not_exact_anonymous_get" in out["blockers"]


def test_missing_dns_enforcement_is_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["enforced_transport_gates"]["dns_policy"]["destination_pinning_required"] = False
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_transport_gates_not_exact" in out["blockers"]


def test_redirect_widening_is_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["enforced_transport_gates"]["redirect_policy"]["max_redirects"] = 1
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_transport_gates_not_exact" in out["blockers"]


def test_response_policy_widening_is_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["enforced_transport_gates"]["response_policy"]["allowed_content_types"] = ["application/json", "text/html"]
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_transport_gates_not_exact" in out["blockers"]


def test_source_policy_credentials_widening_is_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["enforced_transport_gates"]["source_policy"]["credentials_allowed"] = True
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_transport_gates_not_exact" in out["blockers"]


def test_reachable_entrypoint_is_rejected_even_when_hash_valid():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["execution_entrypoint_present"] = True
    d["execution_entrypoint_reachable"] = True
    d["transport_callable_attached"] = True
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "unsafe_or_missing_adapter_execution_entrypoint_present" in out["blockers"]
    assert "unsafe_or_missing_adapter_transport_callable_attached" in out["blockers"]
    assert out["network_calls_performed"] is False


def test_adapter_declaration_hash_tamper_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["adapter_id"] = "tampered"
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_declaration_hash_invalid" in out["blockers"]


def test_envelope_binding_mismatch_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["bound_authorized_attempt_envelope_sha256"] = "x" * 64
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_envelope_hash_binding_invalid" in out["blockers"]


def test_request_contract_widening_rejected():
    c = consumption_fixture()
    d = declaration_fixture(c)
    d["request_contract"]["credentials_allowed"] = True
    d = rehash(d, "adapter_contract_sha256")
    out = validate_network_capable_adapter_contract(c, d)
    assert "adapter_request_contract_not_exact" in out["blockers"]
