"""Deterministic authorization-to-execution gate for synthetic read-only transport tests."""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import ipaddress
import json
from typing import Any, Mapping, Protocol, Sequence

from transport_preflight import (
    PREFLIGHT_MODE,
    ReadOnlyGetTransport,
    validate_explicit_read_only_authorization,
)

EXECUTION_MODE = "synthetic_authorized_read_only_execution"
RECEIPT_MODE = "synthetic_read_only_response_receipt"
DEFAULT_ALLOWED_CONTENT_TYPES = ("application/json", "text/plain")
DEFAULT_MAX_RESPONSE_BYTES = 1_048_576


class ReadOnlyResolver(Protocol):
    def resolve(self, *, host: str, port: int | None) -> Sequence[str]: ...


def _hash(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return sha256(payload).hexdigest()


def _time(value: Any, error: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(error)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(error) from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(error)
    return parsed.astimezone(timezone.utc)


def _global_addresses(values: Any) -> list[str]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence) or not values:
        raise ValueError("execution_dns_resolution_missing")
    out: list[str] = []
    for raw in values:
        try:
            address = ipaddress.ip_address(str(raw))
        except ValueError as exc:
            raise ValueError("execution_dns_resolution_invalid") from exc
        if not address.is_global:
            raise ValueError("execution_dns_non_global_forbidden")
        out.append(str(address))
    return out


def _headers(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ValueError("execution_response_headers_invalid")
    result: dict[str, str] = {}
    for key, raw in value.items():
        name = str(key).strip()
        if not name:
            raise ValueError("execution_response_headers_invalid")
        result[name.lower()] = str(raw).strip()
    return result


def _content_type(headers: Mapping[str, str], allowed: tuple[str, ...]) -> str:
    raw = headers.get("content-type", "")
    media = raw.split(";", 1)[0].strip().lower()
    if not media or media not in allowed:
        raise ValueError("execution_content_type_forbidden")
    return media


def _validate_envelope(envelope: Mapping[str, Any]) -> None:
    if not isinstance(envelope, Mapping):
        raise ValueError("execution_envelope_invalid")
    if envelope.get("method") != "GET":
        raise ValueError("execution_non_get_forbidden")
    if envelope.get("credentials_allowed") is not False:
        raise ValueError("execution_credentials_forbidden")
    if envelope.get("action_enabled") is not False:
        raise ValueError("execution_action_forbidden")
    if envelope.get("transport_enabled") is not False:
        raise ValueError("execution_preflight_transport_flag_invalid")
    if envelope.get("network_calls_performed") is not False:
        raise ValueError("execution_preflight_network_flag_invalid")
    if envelope.get("dry_run_only") is not True:
        raise ValueError("execution_preflight_dry_run_flag_invalid")

    base = {
        "sequence": envelope["sequence"],
        "priority_index": envelope["priority_index"],
        "platform": envelope["platform"],
        "item_index": envelope["item_index"],
        "source_url": envelope["source_url"],
        "host": envelope["host"],
        "port": envelope.get("port"),
        "method": "GET",
        "scheduled_at_utc": envelope["scheduled_at_utc"],
        "offset_seconds": envelope["offset_seconds"],
        "manifest_item_sha256": envelope["manifest_item_sha256"],
        "manifest_sha256": envelope["manifest_sha256"],
        "expected_evidence_classes": envelope["expected_evidence_classes"],
        "required_environment": envelope["required_environment"],
        "provenance_checklist": envelope["provenance_checklist"],
        "rate_limit": envelope["rate_limit"],
        "timeout_seconds": envelope["timeout_seconds"],
        "allowed_request_headers": envelope["allowed_request_headers"],
        "forbidden_request_headers": envelope["forbidden_request_headers"],
        "redirect_policy": envelope["redirect_policy"],
        "dns_policy": envelope["dns_policy"],
        "credentials_allowed": False,
        "action_enabled": False,
    }
    if _hash(base) != envelope.get("request_binding_sha256"):
        raise ValueError("execution_request_binding_hash_mismatch")


def execute_synthetic_read_only(
    preflight: Mapping[str, Any],
    authorization: Mapping[str, Any] | None,
    *,
    resolver: ReadOnlyResolver,
    transport: ReadOnlyGetTransport,
    now_utc: str,
    max_response_bytes: int = DEFAULT_MAX_RESPONSE_BYTES,
    allowed_content_types: Sequence[str] = DEFAULT_ALLOWED_CONTENT_TYPES,
) -> dict[str, Any]:
    """Execute only through injected synthetic dependencies after exact authorization validation."""
    if not isinstance(preflight, Mapping) or preflight.get("mode") != PREFLIGHT_MODE:
        raise ValueError("execution_preflight_invalid")
    if authorization is None:
        raise ValueError("execution_authorization_missing")

    auth_receipt = validate_explicit_read_only_authorization(preflight, authorization)
    now = _time(now_utc, "execution_now_invalid")
    expires = _time(authorization.get("expires_at_utc"), "execution_authorization_expiry_invalid")
    if now > expires:
        raise ValueError("execution_authorization_expired")

    try:
        response_cap = int(max_response_bytes)
    except (TypeError, ValueError) as exc:
        raise ValueError("execution_response_size_limit_invalid") from exc
    if response_cap <= 0 or response_cap > 10_485_760:
        raise ValueError("execution_response_size_limit_invalid")

    if isinstance(allowed_content_types, (str, bytes)):
        raise ValueError("execution_allowed_content_types_invalid")
    allowed = tuple(str(v).strip().lower() for v in allowed_content_types)
    if not allowed or any(not v or "/" not in v for v in allowed):
        raise ValueError("execution_allowed_content_types_invalid")

    envelopes = preflight.get("transport_envelopes")
    if not isinstance(envelopes, list):
        raise ValueError("execution_envelopes_invalid")
    if len(envelopes) != preflight.get("planned_request_count"):
        raise ValueError("execution_request_count_mismatch")
    if len(envelopes) > auth_receipt["max_requests"]:
        raise ValueError("execution_authorized_request_cap_exceeded")

    receipts: list[dict[str, Any]] = []
    for envelope in envelopes:
        _validate_envelope(envelope)
        resolved = _global_addresses(
            resolver.resolve(host=str(envelope["host"]), port=envelope.get("port"))
        )

        raw = transport.get(
            url=str(envelope["source_url"]),
            headers={"Accept": ", ".join(allowed), "User-Agent": "mining-autonomy-readonly/1"},
            timeout_seconds=float(envelope["timeout_seconds"]),
        )
        if not isinstance(raw, Mapping):
            raise ValueError("execution_transport_response_invalid")

        try:
            status = int(raw["status_code"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("execution_status_invalid") from exc
        if status < 100 or status > 599:
            raise ValueError("execution_status_invalid")

        response_headers = _headers(raw.get("headers", {}))
        if 300 <= status < 400 or "location" in response_headers:
            raise ValueError("execution_redirect_forbidden")

        body = raw.get("body")
        if not isinstance(body, (bytes, bytearray)):
            raise ValueError("execution_response_body_invalid")
        body_bytes = bytes(body)
        declared = raw.get("declared_content_length", response_headers.get("content-length"))
        if declared is not None:
            try:
                declared_int = int(declared)
            except (TypeError, ValueError) as exc:
                raise ValueError("execution_declared_content_length_invalid") from exc
            if declared_int < 0 or declared_int > response_cap:
                raise ValueError("execution_response_too_large")
        if len(body_bytes) > response_cap:
            raise ValueError("execution_response_too_large")

        media_type = _content_type(response_headers, allowed)
        body_sha = sha256(body_bytes).hexdigest()
        response_meta = {
            "request_binding_sha256": envelope["request_binding_sha256"],
            "source_url": envelope["source_url"],
            "status_code": status,
            "resolved_global_addresses": resolved,
            "content_type": media_type,
            "response_bytes": len(body_bytes),
            "body_sha256": body_sha,
        }
        receipts.append(
            {
                "schema_version": 1,
                "mode": RECEIPT_MODE,
                **response_meta,
                "response_receipt_sha256": _hash(response_meta),
                "authorization_nonce_hash": sha256(
                    str(authorization["authorization_nonce"]).encode()
                ).hexdigest(),
                "credentials_used": False,
                "redirect_followed": False,
                "action_enabled": False,
                "synthetic_transport_only": True,
            }
        )

    execution_core = {
        "schema_version": 1,
        "mode": EXECUTION_MODE,
        "session_plan_sha256": preflight["session_plan_sha256"],
        "transport_envelope_set_sha256": preflight["transport_envelope_set_sha256"],
        "authorization_validation_receipt_sha256": _hash(auth_receipt),
        "executed_request_count": len(receipts),
        "response_receipts": receipts,
        "credentials_used": False,
        "actions_performed": False,
        "synthetic_transport_only": True,
        "real_network_calls_performed": False,
    }
    return {**execution_core, "execution_receipt_sha256": _hash(execution_core)}
