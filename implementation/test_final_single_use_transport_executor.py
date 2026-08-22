from hashlib import sha256
import json
from final_single_use_transport_executor import execute_single_use_dependency_injected_transport as execute


def h(v):
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def rh(o, key):
    o[key] = h({a: b for a, b in o.items() if a != key})


def i089_fixture():
    request = {
        "adapter_id": "payan_readonly", "target_fingerprint": "target-1", "exact_scope_sha256": "1" * 64,
        "implementation_source_sha256": "2" * 64, "hostname": "example.com", "path": "/v1/tasks?state=open", "pinned_addresses": ["93.184.216.34"],
        "scheme": "https", "tls_required": True, "method": "GET", "max_network_requests": 1,
        "allow_redirects": False, "max_redirects": 0, "allowed_content_types": ["application/json"],
        "max_response_bytes": 1024, "credentials_allowed": False, "action_enabled": False,
    }
    gate_core = {
        "schema_version": 1, "mode": "single_attempt_dependency_injected_network_adapter_gate",
        "gate_state": "validated_ready_for_single_dependency_injected_network_invocation",
        "gated_at": "2026-08-22T08:00:00Z", "expires_at": "2026-08-22T08:01:00Z", "max_gate_age_seconds": 60,
        "i088_consumption_preflight_sha256": "3" * 64, "i088_execution_envelope_sha256": "4" * 64,
        "i088_consumption_receipt_sha256": "5" * 64, "final_real_observation_review_packet_sha256": "6" * 64,
        "final_real_observation_authorization_sha256": "7" * 64, "network_adapter_manifest_sha256": "8" * 64,
        "policy_evidence_sha256": "9" * 64, "dns_evidence_sha256": "a" * 64, "transport_contract_sha256": "b" * 64,
        "request_spec": request, "max_adapter_invocations": 1, "max_network_requests": 1,
        "dependency_injected_transport_boundary_required": True, "network_transport_invoked": False,
        "network_calls_performed": False, "credentials_used": False, "task_acceptance_enabled": False,
        "submission_enabled": False, "value_movement_enabled": False, "gate_is_execution_result": False,
        "gate_is_payment_or_task_permission": False,
    }
    gate = {**gate_core, "final_network_adapter_invocation_gate_sha256": h(gate_core)}
    core = {
        "schema_version": 1, "mode": "deterministic_final_network_adapter_invocation_gate",
        "gate_state": "final_network_adapter_invocation_gate_ready_no_call",
        "i088_consumption_preflight_sha256": "3" * 64, "i088_execution_envelope_sha256": "4" * 64,
        "i088_consumption_receipt_sha256": "5" * 64, "network_adapter_manifest_sha256": "8" * 64,
        "invocation_gate": gate, "blockers": [], "dependency_injected_transport_boundary_exposed": True,
        "network_transport_invoked": False, "network_calls_performed": False, "credentials_used": False,
        "task_acceptance_enabled": False, "submission_enabled": False, "execution_enabled": False,
        "value_movement_enabled": False, "gate_record_is_execution_token": False,
    }
    return {**core, "final_network_adapter_invocation_gate_builder_sha256": h(core)}


def ok_transport(_request):
    body = '{"opportunities":[]}'
    size = len(body.encode())
    return {
        "network_requests_performed": 1, "peer_ip": "93.184.216.34", "tls_verified": True,
        "tls_server_name": "example.com", "dns_reresolved_after_connect": False, "redirect_count": 0,
        "status_code": 200, "content_type": "application/json; charset=utf-8", "compressed_response_bytes": size,
        "decompressed_response_bytes": size, "body_utf8": body,
    }


def test_clean_synthetic_response_attested_and_consumed():
    out = execute(i089_fixture(), ok_transport, invoked_at="2026-08-22T08:00:30Z")
    assert out["execution_state"] == "invoked_once_response_attested"
    assert out["attempt_consumed"] is True
    assert out["invocation_receipt"]["invocation_state"] == "invoked_once"
    assert out["response_attestation"]["peer_ip"] == "93.184.216.34"
    assert out["response_attestation"]["content_type"] == "application/json"


def test_transport_exception_consumes_attempt():
    def boom(_request):
        raise TimeoutError("synthetic timeout")
    out = execute(i089_fixture(), boom, invoked_at="2026-08-22T08:00:30Z")
    assert out["execution_state"] == "attempted_once_transport_error"
    assert out["attempt_consumed"] is True
    assert out["invocation_receipt"]["one_shot_consumed"] is True
    assert out["response_attestation"] is None


def test_bad_peer_or_redirect_rejected_after_consumption():
    def bad(req):
        result = ok_transport(req)
        result["peer_ip"] = "8.8.8.8"
        result["redirect_count"] = 1
        return result
    out = execute(i089_fixture(), bad, invoked_at="2026-08-22T08:00:30Z")
    assert out["execution_state"] == "attempted_once_result_rejected"
    assert out["attempt_consumed"] is True
    assert "transport_peer_ip_not_pinned_public_address" in out["blockers"]
    assert "transport_redirect_detected" in out["blockers"]


def test_replay_receipt_blocks_before_transport():
    first = execute(i089_fixture(), ok_transport, invoked_at="2026-08-22T08:00:30Z")
    calls = []
    def tracked(req):
        calls.append(req)
        return ok_transport(req)
    second = execute(i089_fixture(), tracked, invoked_at="2026-08-22T08:00:31Z", prior_invocation_receipts=[first["invocation_receipt"]])
    assert second["execution_state"] == "rejected_before_transport"
    assert "final_network_adapter_invocation_replay_detected" in second["blockers"]
    assert calls == []


def test_expired_gate_blocks_before_transport():
    calls = []
    out = execute(i089_fixture(), lambda req: calls.append(req) or ok_transport(req), invoked_at="2026-08-22T08:01:01Z")
    assert out["execution_state"] == "rejected_before_transport"
    assert "invocation_gate_expired" in out["blockers"]
    assert calls == []


def test_oversized_decompressed_body_rejected():
    def oversized(req):
        result = ok_transport(req)
        body = "{" + '"x":"' + ("a" * 1100) + '"}'
        result["body_utf8"] = body
        result["decompressed_response_bytes"] = len(body.encode())
        return result
    out = execute(i089_fixture(), oversized, invoked_at="2026-08-22T08:00:30Z")
    assert "transport_decompressed_response_size_invalid_or_over_limit" in out["blockers"]
    assert out["attempt_consumed"] is True


def test_non_json_response_rejected():
    def bad_json(req):
        result = ok_transport(req)
        result["content_type"] = "text/html"
        result["body_utf8"] = "not json"
        result["decompressed_response_bytes"] = len(result["body_utf8"].encode())
        return result
    out = execute(i089_fixture(), bad_json, invoked_at="2026-08-22T08:00:30Z")
    assert "transport_content_type_not_json" in out["blockers"]
    assert "transport_body_invalid_json" in out["blockers"]


def test_tampered_i089_hash_blocks_before_transport():
    gate = i089_fixture()
    gate["network_calls_performed"] = True
    rh(gate, "final_network_adapter_invocation_gate_builder_sha256")
    calls = []
    out = execute(gate, lambda req: calls.append(req) or ok_transport(req), invoked_at="2026-08-22T08:00:30Z")
    assert "i089_network_calls_performed_must_be_false" in out["blockers"]
    assert calls == []


def test_missing_or_noncanonical_path_blocks_before_transport():
    for bad in (None, "https://example.com/v1/tasks", "//example.com/v1/tasks", "/v1/tasks#frag"):
        gate = i089_fixture()
        req = gate["invocation_gate"]["request_spec"]
        if bad is None:
            req.pop("path")
        else:
            req["path"] = bad
        rh(gate["invocation_gate"], "final_network_adapter_invocation_gate_sha256")
        rh(gate, "final_network_adapter_invocation_gate_builder_sha256")
        calls = []
        out = execute(gate, lambda req: calls.append(req) or ok_transport(req), invoked_at="2026-08-22T08:00:30Z")
        assert out["execution_state"] == "rejected_before_transport"
        assert out["attempt_consumed"] is False
        assert calls == []
        assert any(x.startswith("native_https_path_query_") for x in out["blockers"])
