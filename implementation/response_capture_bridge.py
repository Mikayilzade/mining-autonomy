"""Bridge synthetic I031 responses into receipt-gated sanitized evidence captures.

No network access lives here. Callers must provide already-received synthetic response
bytes plus explicit provenance timestamps and a platform-specific sanitizer/builder.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Callable, Mapping

from bundle_registry import index_bundle
from execution_gate import EXECUTION_MODE, RECEIPT_MODE, _validate_envelope
from sampling_receipt import (
    TransportResult,
    bind_capture_result,
    manifest_item_sha256,
    sha256_hex,
    verify_capture_receipt,
    verify_sampling_manifest_envelope,
)

BRIDGE_MODE = "synthetic_response_to_sanitized_capture"
ALLOWED_MEDIA_TYPES = frozenset({"application/json", "text/plain"})
DEFAULT_MAX_PARSE_BYTES = 1_048_576
DEFAULT_MAX_JSON_NODES = 20_000
DEFAULT_MAX_JSON_DEPTH = 32
DEFAULT_MAX_TEXT_CHARS = 200_000


@dataclass(frozen=True)
class SanitizedCapture:
    bundle: Any
    evidence_class: str
    source_timestamp: str


PayloadBuilder = Callable[[Any, Mapping[str, Any]], SanitizedCapture]


def _utc(value: Any, error: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(error) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(error)
    return parsed.astimezone(timezone.utc).isoformat()


def _verify_execution_receipt(receipt: Mapping[str, Any]) -> None:
    if not isinstance(receipt, Mapping) or receipt.get("mode") != EXECUTION_MODE:
        raise ValueError("bridge_execution_receipt_invalid")
    if receipt.get("synthetic_transport_only") is not True:
        raise ValueError("bridge_real_transport_forbidden")
    if receipt.get("real_network_calls_performed") is not False:
        raise ValueError("bridge_real_network_forbidden")
    if receipt.get("credentials_used") is not False or receipt.get("actions_performed") is not False:
        raise ValueError("bridge_execution_boundary_invalid")
    core = dict(receipt)
    supplied = core.pop("execution_receipt_sha256", None)
    if supplied != sha256_hex(core):
        raise ValueError("bridge_execution_receipt_hash_mismatch")
    responses = receipt.get("response_receipts")
    if not isinstance(responses, list) or len(responses) != receipt.get("executed_request_count"):
        raise ValueError("bridge_execution_response_count_invalid")


def _response_meta(receipt: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "request_binding_sha256": receipt.get("request_binding_sha256"),
        "source_url": receipt.get("source_url"),
        "status_code": receipt.get("status_code"),
        "resolved_global_addresses": receipt.get("resolved_global_addresses"),
        "content_type": receipt.get("content_type"),
        "response_bytes": receipt.get("response_bytes"),
        "body_sha256": receipt.get("body_sha256"),
    }


def _find_response(execution_receipt: Mapping[str, Any], response_receipt_sha256: str) -> Mapping[str, Any]:
    matches = [
        item for item in execution_receipt["response_receipts"]
        if isinstance(item, Mapping) and item.get("response_receipt_sha256") == response_receipt_sha256
    ]
    if len(matches) != 1:
        raise ValueError("bridge_response_receipt_not_unique")
    receipt = matches[0]
    if receipt.get("mode") != RECEIPT_MODE:
        raise ValueError("bridge_response_receipt_mode_invalid")
    if receipt.get("response_receipt_sha256") != sha256_hex(_response_meta(receipt)):
        raise ValueError("bridge_response_receipt_hash_mismatch")
    if receipt.get("synthetic_transport_only") is not True:
        raise ValueError("bridge_response_transport_invalid")
    if receipt.get("credentials_used") is not False or receipt.get("action_enabled") is not False:
        raise ValueError("bridge_response_boundary_invalid")
    if receipt.get("redirect_followed") is not False:
        raise ValueError("bridge_redirect_forbidden")
    return receipt


def _json_complexity(value: Any, *, max_nodes: int, max_depth: int) -> None:
    nodes = 0
    stack: list[tuple[Any, int]] = [(value, 0)]
    while stack:
        current, depth = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            raise ValueError("bridge_json_node_limit_exceeded")
        if depth > max_depth:
            raise ValueError("bridge_json_depth_limit_exceeded")
        if isinstance(current, Mapping):
            if any(not isinstance(key, str) for key in current):
                raise ValueError("bridge_json_object_key_invalid")
            stack.extend((child, depth + 1) for child in current.values())
        elif isinstance(current, list):
            stack.extend((child, depth + 1) for child in current)
        elif current is not None and not isinstance(current, (str, int, float, bool)):
            raise ValueError("bridge_json_value_invalid")


def _parse_body(
    body: bytes,
    media_type: str,
    *,
    max_parse_bytes: int,
    max_json_nodes: int,
    max_json_depth: int,
    max_text_chars: int,
) -> Any:
    if not isinstance(body, (bytes, bytearray)):
        raise ValueError("bridge_body_must_be_bytes")
    body = bytes(body)
    if len(body) > max_parse_bytes:
        raise ValueError("bridge_body_parse_limit_exceeded")
    try:
        text = body.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError("bridge_body_utf8_invalid") from exc

    if media_type == "application/json":
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("bridge_json_invalid") from exc
        _json_complexity(parsed, max_nodes=max_json_nodes, max_depth=max_json_depth)
        return parsed

    if media_type == "text/plain":
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        if "\x00" in normalized:
            raise ValueError("bridge_text_nul_forbidden")
        if len(normalized) > max_text_chars:
            raise ValueError("bridge_text_char_limit_exceeded")
        for char in normalized:
            if ord(char) < 32 and char not in "\n\t":
                raise ValueError("bridge_text_control_character_forbidden")
        return normalized

    raise ValueError("bridge_content_type_forbidden")


def _manifest_item_index(
    manifest_envelope: Mapping[str, Any],
    request_envelope: Mapping[str, Any],
) -> int:
    if request_envelope.get("manifest_sha256") != manifest_envelope.get("manifest_sha256"):
        raise ValueError("bridge_manifest_hash_mismatch")
    wanted = request_envelope.get("manifest_item_sha256")
    matches: list[int] = []
    for index, _ in enumerate(manifest_envelope["manifest"]["items"]):
        if manifest_item_sha256(manifest_envelope, index) == wanted:
            matches.append(index)
    if len(matches) != 1:
        raise ValueError("bridge_manifest_item_not_unique")
    return matches[0]


def bridge_response_to_verified_capture(
    preflight: Mapping[str, Any],
    execution_receipt: Mapping[str, Any],
    manifest_envelope: Mapping[str, Any],
    *,
    response_receipt_sha256: str,
    response_body: bytes,
    source_timestamp_utc: str,
    capture_started_at_utc: str,
    capture_finished_at_utc: str,
    payload_builder: PayloadBuilder,
    captured_environment: str = "production",
    environment_evidence_sha256: str | None = None,
    max_parse_bytes: int = DEFAULT_MAX_PARSE_BYTES,
    max_json_nodes: int = DEFAULT_MAX_JSON_NODES,
    max_json_depth: int = DEFAULT_MAX_JSON_DEPTH,
    max_text_chars: int = DEFAULT_MAX_TEXT_CHARS,
) -> dict[str, Any]:
    """Turn one synthetic response into an existing I024-compatible verified capture."""
    verify_sampling_manifest_envelope(manifest_envelope)
    _verify_execution_receipt(execution_receipt)
    response = _find_response(execution_receipt, response_receipt_sha256)

    envelopes = preflight.get("transport_envelopes") if isinstance(preflight, Mapping) else None
    if not isinstance(envelopes, list):
        raise ValueError("bridge_preflight_envelopes_invalid")
    request_matches = [
        item for item in envelopes
        if isinstance(item, Mapping)
        and item.get("request_binding_sha256") == response.get("request_binding_sha256")
    ]
    if len(request_matches) != 1:
        raise ValueError("bridge_request_binding_not_unique")
    request = request_matches[0]
    _validate_envelope(request)
    if response.get("source_url") != request.get("source_url"):
        raise ValueError("bridge_response_source_mismatch")

    item_index = _manifest_item_index(manifest_envelope, request)
    item = manifest_envelope["manifest"]["items"][item_index]
    if item.get("source_url") != request.get("source_url") or item.get("platform") != request.get("platform"):
        raise ValueError("bridge_manifest_source_identity_mismatch")
    if list(item.get("expected_evidence_classes", [])) != list(request.get("expected_evidence_classes", [])):
        raise ValueError("bridge_manifest_evidence_binding_mismatch")

    try:
        status = int(response.get("status_code"))
        declared_bytes = int(response.get("response_bytes"))
    except (TypeError, ValueError) as exc:
        raise ValueError("bridge_response_metadata_invalid") from exc
    if status < 200 or status >= 300:
        raise ValueError("bridge_non_success_response_forbidden")
    body = bytes(response_body)
    if declared_bytes != len(body):
        raise ValueError("bridge_response_byte_count_mismatch")
    if sha256(body).hexdigest() != response.get("body_sha256"):
        raise ValueError("bridge_response_body_hash_mismatch")
    media_type = str(response.get("content_type", "")).lower()
    if media_type not in ALLOWED_MEDIA_TYPES:
        raise ValueError("bridge_content_type_forbidden")

    started = _utc(capture_started_at_utc, "bridge_capture_started_at_invalid")
    finished = _utc(capture_finished_at_utc, "bridge_capture_finished_at_invalid")
    source_timestamp = _utc(source_timestamp_utc, "bridge_source_timestamp_invalid")
    if datetime.fromisoformat(finished) < datetime.fromisoformat(started):
        raise ValueError("bridge_capture_time_order_invalid")

    parsed = _parse_body(
        body, media_type,
        max_parse_bytes=max_parse_bytes,
        max_json_nodes=max_json_nodes,
        max_json_depth=max_json_depth,
        max_text_chars=max_text_chars,
    )
    context = {
        "platform": request["platform"],
        "source_url": request["source_url"],
        "source_timestamp": source_timestamp,
        "capture_started_at": started,
        "capture_finished_at": finished,
        "content_type": media_type,
        "response_receipt_sha256": response_receipt_sha256,
        "request_binding_sha256": request["request_binding_sha256"],
    }
    sanitized = payload_builder(parsed, context)
    if not isinstance(sanitized, SanitizedCapture):
        raise ValueError("bridge_payload_builder_result_invalid")
    if _utc(sanitized.source_timestamp, "bridge_builder_source_timestamp_invalid") != source_timestamp:
        raise ValueError("bridge_builder_source_timestamp_mismatch")
    expected_classes = list(item.get("expected_evidence_classes", []))
    if sanitized.evidence_class not in expected_classes:
        raise ValueError("bridge_evidence_class_not_expected")

    entry = index_bundle(sanitized.bundle)
    if entry.platform != request["platform"] or entry.source_url != request["source_url"]:
        raise ValueError("bridge_sanitized_bundle_source_identity_mismatch")
    if _utc(entry.source_timestamp, "bridge_bundle_source_timestamp_invalid") != source_timestamp:
        raise ValueError("bridge_sanitized_bundle_source_time_mismatch")
    if _utc(entry.captured_at, "bridge_bundle_captured_at_invalid") != finished:
        raise ValueError("bridge_sanitized_bundle_capture_time_mismatch")
    if entry.request_evidence_class != sanitized.evidence_class:
        raise ValueError("bridge_sanitized_bundle_evidence_class_mismatch")

    base_receipt = bind_capture_result(
        manifest_envelope,
        item_index=item_index,
        result=TransportResult(
            sanitized_bundle_sha256=entry.bundle_sha256,
            capture_started_at=started,
            capture_finished_at=finished,
            captured_environment=captured_environment,
            environment_evidence_sha256=environment_evidence_sha256,
            source_timestamp=source_timestamp,
            network_performed=False,
            credentials_used=False,
            action_performed=False,
        ),
        transport_name="i031-synthetic-response-bridge",
        transport_network_capable=False,
        network_explicitly_enabled=False,
    )
    receipt_core = dict(base_receipt)
    receipt_core.pop("receipt_sha256", None)
    receipt_core["execution_provenance"] = {
        "execution_receipt_sha256": execution_receipt["execution_receipt_sha256"],
        "request_binding_sha256": request["request_binding_sha256"],
        "response_receipt_sha256": response_receipt_sha256,
        "response_body_sha256": response["body_sha256"],
        "response_content_type": media_type,
        "response_status_code": status,
        "synthetic_transport_only": True,
        "real_network_calls_performed": False,
    }
    capture_receipt = {**receipt_core, "receipt_sha256": sha256_hex(receipt_core)}
    verify_capture_receipt(manifest_envelope, capture_receipt)

    return {
        "schema_version": 1,
        "mode": BRIDGE_MODE,
        "bundle": sanitized.bundle,
        "manifest_envelope": dict(manifest_envelope),
        "receipt": capture_receipt,
        "evidence_class": sanitized.evidence_class,
        "parsed_content_type": media_type,
        "request_binding_sha256": request["request_binding_sha256"],
        "response_receipt_sha256": response_receipt_sha256,
        "dry_run_only": True,
        "action_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
    }
