from datetime import datetime, timedelta, timezone
from hashlib import sha256

import pytest

from evidence_archive import EvidenceArchive, append_capture_report
from observation_bundle import build_payan_observation_bundle
from observation_capture import run_verified_capture_batch
from response_capture_bridge import SanitizedCapture, bridge_response_to_verified_capture
from sampling_receipt import manifest_item_sha256, seal_sampling_manifest, sha256_hex


SOURCE_URL = "https://payanagent.com/api/v1/discover"
SIGNING_KEY = b"offline-test-key-32-bytes-long!!"


def _fixture(body: bytes):
    capture_finished = datetime(2026, 8, 20, 2, 0, tzinfo=timezone.utc)
    source_timestamp = capture_finished - timedelta(minutes=2)
    manifest = {
        "schema_version": 1,
        "mode": "inert_read_only_sampling_contract",
        "network_calls_performed": False,
        "action_enabled": False,
        "credentials_allowed": False,
        "items": [{
            "platform": "payanagent",
            "source_url": SOURCE_URL,
            "method": "GET",
            "credentials_allowed": False,
            "action_enabled": False,
            "network_calls_performed": False,
            "scheduled": True,
            "environment": "production",
            "expected_evidence_classes": ["open_paid_request"],
        }],
    }
    sealed = seal_sampling_manifest(manifest)
    item_sha = manifest_item_sha256(sealed, 0)
    request_base = {
        "sequence": 1,
        "priority_index": 0,
        "platform": "payanagent",
        "item_index": 0,
        "source_url": SOURCE_URL,
        "host": "payanagent.com",
        "port": 443,
        "method": "GET",
        "scheduled_at_utc": capture_finished.isoformat(),
        "offset_seconds": 0,
        "manifest_item_sha256": item_sha,
        "manifest_sha256": sealed["manifest_sha256"],
        "expected_evidence_classes": ["open_paid_request"],
        "required_environment": "production",
        "provenance_checklist": ["source_url", "source_timestamp", "captured_at"],
        "rate_limit": {"max_requests": 1, "window_seconds": 60},
        "timeout_seconds": 10.0,
        "allowed_request_headers": ["accept", "user-agent"],
        "forbidden_request_headers": ["authorization", "cookie"],
        "redirect_policy": "forbid",
        "dns_policy": "global_only",
        "credentials_allowed": False,
        "action_enabled": False,
    }
    request = {
        **request_base,
        "request_binding_sha256": sha256_hex(request_base),
        "transport_enabled": False,
        "network_calls_performed": False,
        "dry_run_only": True,
    }
    preflight = {
        "transport_envelopes": [request],
        "planned_request_count": 1,
    }
    response_meta = {
        "request_binding_sha256": request["request_binding_sha256"],
        "source_url": SOURCE_URL,
        "status_code": 200,
        "resolved_global_addresses": ["93.184.216.34"],
        "content_type": "application/json",
        "response_bytes": len(body),
        "body_sha256": sha256(body).hexdigest(),
    }
    response = {
        "schema_version": 1,
        "mode": "synthetic_read_only_response_receipt",
        **response_meta,
        "response_receipt_sha256": sha256_hex(response_meta),
        "authorization_nonce_hash": "0" * 64,
        "credentials_used": False,
        "redirect_followed": False,
        "action_enabled": False,
        "synthetic_transport_only": True,
    }
    execution_core = {
        "schema_version": 1,
        "mode": "synthetic_authorized_read_only_execution",
        "session_plan_sha256": "1" * 64,
        "transport_envelope_set_sha256": "2" * 64,
        "authorization_validation_receipt_sha256": "3" * 64,
        "executed_request_count": 1,
        "response_receipts": [response],
        "credentials_used": False,
        "actions_performed": False,
        "synthetic_transport_only": True,
        "real_network_calls_performed": False,
    }
    execution = {**execution_core, "execution_receipt_sha256": sha256_hex(execution_core)}
    return sealed, preflight, execution, response, source_timestamp, capture_finished


def _builder(parsed, context):
    bundle = build_payan_observation_bundle(
        raw_requests=parsed["items"],
        request_source_url=context["source_url"],
        request_source_timestamp=context["source_timestamp"],
        captured_at=context["capture_finished_at"],
        signing_key=SIGNING_KEY,
        now=datetime.fromisoformat(context["capture_finished_at"]),
    )
    return SanitizedCapture(
        bundle=bundle,
        evidence_class="open_paid_request",
        source_timestamp=context["source_timestamp"],
    )


def _body():
    return (
        b'{"items":[{"id":"req-1","status":"open","bountyUsd":12.5,'
        b'"currency":"USDC","title":"Summarize text","skills":["text"]}]}'
    )


def test_bridge_enters_existing_receipt_gated_archive():
    body = _body()
    sealed, preflight, execution, response, source_ts, finished = _fixture(body)
    bridged = bridge_response_to_verified_capture(
        preflight,
        execution,
        sealed,
        response_receipt_sha256=response["response_receipt_sha256"],
        response_body=body,
        source_timestamp_utc=source_ts.isoformat(),
        capture_started_at_utc=(finished - timedelta(seconds=1)).isoformat(),
        capture_finished_at_utc=finished.isoformat(),
        payload_builder=_builder,
    )
    assert bridged["dry_run_only"] is True
    assert bridged["receipt"]["execution_provenance"]["response_receipt_sha256"] == response["response_receipt_sha256"]
    report = run_verified_capture_batch([bridged])
    archive = append_capture_report(EvidenceArchive(), report)
    assert len(archive.entries) == 1
    assert archive.entries[0].environment == "production"
    assert archive.entries[0].demand_state == "positive_open_demand"


def test_body_hash_mismatch_fails_before_builder():
    body = _body()
    sealed, preflight, execution, response, source_ts, finished = _fixture(body)
    with pytest.raises(ValueError, match="bridge_response_body_hash_mismatch"):
        bridge_response_to_verified_capture(
            preflight, execution, sealed,
            response_receipt_sha256=response["response_receipt_sha256"],
            response_body=body + b" ",
            source_timestamp_utc=source_ts.isoformat(),
            capture_started_at_utc=finished.isoformat(),
            capture_finished_at_utc=finished.isoformat(),
            payload_builder=_builder,
        )


def test_response_receipt_tamper_is_rejected():
    body = _body()
    sealed, preflight, execution, response, source_ts, finished = _fixture(body)
    execution["response_receipts"][0]["status_code"] = 201
    execution_core = dict(execution)
    execution_core.pop("execution_receipt_sha256")
    execution["execution_receipt_sha256"] = sha256_hex(execution_core)
    with pytest.raises(ValueError, match="bridge_response_receipt_hash_mismatch"):
        bridge_response_to_verified_capture(
            preflight, execution, sealed,
            response_receipt_sha256=response["response_receipt_sha256"],
            response_body=body,
            source_timestamp_utc=source_ts.isoformat(),
            capture_started_at_utc=finished.isoformat(),
            capture_finished_at_utc=finished.isoformat(),
            payload_builder=_builder,
        )


def test_unexpected_evidence_class_is_rejected():
    body = _body()
    sealed, preflight, execution, response, source_ts, finished = _fixture(body)

    def wrong_builder(parsed, context):
        result = _builder(parsed, context)
        return SanitizedCapture(result.bundle, "settled_receipt", result.source_timestamp)

    with pytest.raises(ValueError, match="bridge_evidence_class_not_expected"):
        bridge_response_to_verified_capture(
            preflight, execution, sealed,
            response_receipt_sha256=response["response_receipt_sha256"],
            response_body=body,
            source_timestamp_utc=source_ts.isoformat(),
            capture_started_at_utc=finished.isoformat(),
            capture_finished_at_utc=finished.isoformat(),
            payload_builder=wrong_builder,
        )


def test_malformed_json_never_reaches_builder():
    body = b'{"items":['
    sealed, preflight, execution, response, source_ts, finished = _fixture(body)
    touched = {"value": False}

    def builder(parsed, context):
        touched["value"] = True
        return _builder(parsed, context)

    with pytest.raises(ValueError, match="bridge_json_invalid"):
        bridge_response_to_verified_capture(
            preflight, execution, sealed,
            response_receipt_sha256=response["response_receipt_sha256"],
            response_body=body,
            source_timestamp_utc=source_ts.isoformat(),
            capture_started_at_utc=finished.isoformat(),
            capture_finished_at_utc=finished.isoformat(),
            payload_builder=builder,
        )
    assert touched["value"] is False


def test_parse_byte_limit_fails_closed():
    body = _body()
    sealed, preflight, execution, response, source_ts, finished = _fixture(body)
    with pytest.raises(ValueError, match="bridge_body_parse_limit_exceeded"):
        bridge_response_to_verified_capture(
            preflight, execution, sealed,
            response_receipt_sha256=response["response_receipt_sha256"],
            response_body=body,
            source_timestamp_utc=source_ts.isoformat(),
            capture_started_at_utc=finished.isoformat(),
            capture_finished_at_utc=finished.isoformat(),
            payload_builder=_builder,
            max_parse_bytes=8,
        )
