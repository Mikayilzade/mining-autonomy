"""Integrity contracts for inert sampling manifests and sanitized capture receipts."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import hmac
import json
from typing import Any, Callable, Mapping

HEX64 = frozenset("0123456789abcdef")
ALLOWED_ENVIRONMENTS = frozenset({"production", "testnet", "unknown"})


def canonical_json_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise ValueError("canonical_json_invalid") from exc
    return text.encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _valid_sha256(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and set(value.lower()) <= HEX64


def _validate_manifest(manifest: Mapping[str, Any]) -> None:
    if manifest.get("schema_version") != 1:
        raise ValueError("sealed_manifest_schema_invalid")
    if manifest.get("mode") != "inert_read_only_sampling_contract":
        raise ValueError("sealed_manifest_mode_invalid")
    if manifest.get("network_calls_performed") is not False:
        raise ValueError("sealed_manifest_network_flag_invalid")
    if manifest.get("action_enabled") is not False:
        raise ValueError("sealed_manifest_action_flag_invalid")
    if manifest.get("credentials_allowed") is not False:
        raise ValueError("sealed_manifest_credentials_flag_invalid")
    items = manifest.get("items")
    if not isinstance(items, list):
        raise ValueError("sealed_manifest_items_invalid")
    for item in items:
        if not isinstance(item, Mapping):
            raise ValueError("sealed_manifest_item_invalid")
        if item.get("method") != "GET":
            raise ValueError("sealed_manifest_non_get_item")
        if item.get("credentials_allowed") is not False:
            raise ValueError("sealed_manifest_item_credentials_invalid")
        if item.get("action_enabled") is not False:
            raise ValueError("sealed_manifest_item_action_invalid")
        if item.get("network_calls_performed") is not False:
            raise ValueError("sealed_manifest_item_network_flag_invalid")


def seal_sampling_manifest(manifest: Mapping[str, Any], *, signing_key: bytes | None = None, key_id: str | None = None) -> dict[str, Any]:
    _validate_manifest(manifest)
    payload = dict(manifest)
    digest = sha256_hex(payload)
    signature = None
    if signing_key is not None:
        if not isinstance(signing_key, bytes) or not signing_key:
            raise ValueError("sealed_manifest_signing_key_invalid")
        if not isinstance(key_id, str) or not key_id.strip():
            raise ValueError("sealed_manifest_key_id_required")
        signature = {
            "algorithm": "hmac-sha256",
            "key_id": key_id.strip(),
            "value": hmac.new(signing_key, digest.encode("ascii"), hashlib.sha256).hexdigest(),
        }
    elif key_id is not None:
        raise ValueError("sealed_manifest_key_without_signature")
    return {"envelope_schema_version": 1, "manifest_sha256": digest, "signature": signature, "manifest": payload}


def verify_sampling_manifest_envelope(envelope: Mapping[str, Any], *, signing_key: bytes | None = None, require_signature: bool = False) -> bool:
    if envelope.get("envelope_schema_version") != 1:
        raise ValueError("sealed_manifest_envelope_schema_invalid")
    manifest = envelope.get("manifest")
    if not isinstance(manifest, Mapping):
        raise ValueError("sealed_manifest_payload_missing")
    _validate_manifest(manifest)
    expected = sha256_hex(manifest)
    if envelope.get("manifest_sha256") != expected:
        raise ValueError("sealed_manifest_hash_mismatch")
    signature = envelope.get("signature")
    if signature is None:
        if require_signature:
            raise ValueError("sealed_manifest_signature_required")
        return True
    if not isinstance(signature, Mapping) or signature.get("algorithm") != "hmac-sha256":
        raise ValueError("sealed_manifest_signature_invalid")
    if signing_key is None:
        if require_signature:
            raise ValueError("sealed_manifest_verification_key_required")
        return True
    expected_sig = hmac.new(signing_key, expected.encode("ascii"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(str(signature.get("value", "")), expected_sig):
        raise ValueError("sealed_manifest_signature_mismatch")
    return True


def manifest_item_sha256(envelope: Mapping[str, Any], item_index: int) -> str:
    verify_sampling_manifest_envelope(envelope)
    items = envelope["manifest"]["items"]
    if not isinstance(item_index, int) or isinstance(item_index, bool) or not 0 <= item_index < len(items):
        raise ValueError("capture_manifest_item_index_invalid")
    return sha256_hex({"manifest_sha256": envelope["manifest_sha256"], "item_index": item_index, "item": items[item_index]})


@dataclass(frozen=True)
class TransportResult:
    sanitized_bundle_sha256: str
    capture_started_at: str
    capture_finished_at: str
    captured_environment: str = "unknown"
    environment_evidence_sha256: str | None = None
    source_timestamp: str | None = None
    network_performed: bool = False
    credentials_used: bool = False
    action_performed: bool = False


@dataclass(frozen=True)
class InjectedTransport:
    name: str
    handler: Callable[[Mapping[str, Any]], TransportResult]
    network_capable: bool = False

    def capture(self, item: Mapping[str, Any]) -> TransportResult:
        return self.handler(item)


def _parse_utc(value: str, error: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(error)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(error) from exc
    if parsed.tzinfo is None:
        raise ValueError(error)
    return parsed.astimezone(timezone.utc)


def bind_capture_result(envelope: Mapping[str, Any], *, item_index: int, result: TransportResult, transport_name: str, transport_network_capable: bool, network_explicitly_enabled: bool = False) -> dict[str, Any]:
    verify_sampling_manifest_envelope(envelope)
    items = envelope["manifest"]["items"]
    if not isinstance(item_index, int) or isinstance(item_index, bool) or not 0 <= item_index < len(items):
        raise ValueError("capture_manifest_item_index_invalid")
    item = items[item_index]
    if not _valid_sha256(result.sanitized_bundle_sha256):
        raise ValueError("capture_bundle_sha256_invalid")
    if result.captured_environment not in ALLOWED_ENVIRONMENTS:
        raise ValueError("capture_environment_invalid")
    if result.credentials_used:
        raise ValueError("capture_credentials_forbidden")
    if result.action_performed:
        raise ValueError("capture_action_forbidden")
    if result.network_performed and not (transport_network_capable and network_explicitly_enabled):
        raise ValueError("capture_network_not_explicitly_enabled")
    if item.get("method") != "GET" or item.get("credentials_allowed") is not False:
        raise ValueError("capture_manifest_item_not_read_only")
    started = _parse_utc(result.capture_started_at, "capture_started_at_invalid")
    finished = _parse_utc(result.capture_finished_at, "capture_finished_at_invalid")
    if finished < started:
        raise ValueError("capture_time_order_invalid")
    declared_env = item.get("environment", "unknown")
    env_evidence = result.environment_evidence_sha256
    if env_evidence is not None and not _valid_sha256(env_evidence):
        raise ValueError("capture_environment_evidence_sha256_invalid")
    if result.captured_environment == "production" and declared_env != "production" and env_evidence is None:
        raise ValueError("capture_production_promotion_requires_evidence")
    body = {
        "receipt_schema_version": 1,
        "manifest_sha256": envelope["manifest_sha256"],
        "manifest_item_sha256": manifest_item_sha256(envelope, item_index),
        "item_index": item_index,
        "platform": item["platform"],
        "source_url": item["source_url"],
        "method": item["method"],
        "expected_evidence_classes": list(item.get("expected_evidence_classes", [])),
        "declared_environment": declared_env,
        "captured_environment": result.captured_environment,
        "environment_evidence_sha256": env_evidence.lower() if env_evidence else None,
        "source_timestamp": result.source_timestamp,
        "capture_started_at": started.isoformat(),
        "capture_finished_at": finished.isoformat(),
        "sanitized_bundle_sha256": result.sanitized_bundle_sha256.lower(),
        "transport": {
            "name": transport_name,
            "network_capable": bool(transport_network_capable),
            "network_performed": bool(result.network_performed),
            "network_explicitly_enabled": bool(network_explicitly_enabled),
            "credentials_used": False,
            "action_performed": False,
        },
        "execution_authority_granted": False,
    }
    return {**body, "receipt_sha256": sha256_hex(body)}


def verify_capture_receipt(envelope: Mapping[str, Any], receipt: Mapping[str, Any]) -> bool:
    verify_sampling_manifest_envelope(envelope)
    if receipt.get("receipt_schema_version") != 1:
        raise ValueError("capture_receipt_schema_invalid")
    if receipt.get("manifest_sha256") != envelope.get("manifest_sha256"):
        raise ValueError("capture_receipt_manifest_mismatch")
    index = receipt.get("item_index")
    if receipt.get("manifest_item_sha256") != manifest_item_sha256(envelope, index):
        raise ValueError("capture_receipt_item_mismatch")
    item = envelope["manifest"]["items"][index]
    for field in ("platform", "source_url", "method"):
        if receipt.get(field) != item.get(field):
            raise ValueError(f"capture_receipt_{field}_mismatch")
    body = dict(receipt)
    actual = body.pop("receipt_sha256", None)
    if actual != sha256_hex(body):
        raise ValueError("capture_receipt_hash_mismatch")
    if receipt.get("execution_authority_granted") is not False:
        raise ValueError("capture_receipt_execution_authority_invalid")
    transport = receipt.get("transport")
    if not isinstance(transport, Mapping) or transport.get("credentials_used") is not False or transport.get("action_performed") is not False:
        raise ValueError("capture_receipt_transport_boundary_invalid")
    return True


def capture_with_injected_transport(envelope: Mapping[str, Any], *, item_index: int, transport: InjectedTransport | None = None, allow_network: bool = False) -> dict[str, Any]:
    verify_sampling_manifest_envelope(envelope)
    if transport is None:
        raise RuntimeError("capture_transport_not_injected")
    if transport.network_capable and not allow_network:
        raise RuntimeError("capture_network_transport_disabled")
    items = envelope["manifest"]["items"]
    if not isinstance(item_index, int) or isinstance(item_index, bool) or not 0 <= item_index < len(items):
        raise ValueError("capture_manifest_item_index_invalid")
    item = items[item_index]
    if item.get("scheduled") is not True:
        raise ValueError("capture_manifest_item_not_scheduled")
    result = transport.capture(item)
    if not isinstance(result, TransportResult):
        raise ValueError("capture_transport_result_invalid")
    return bind_capture_result(
        envelope,
        item_index=item_index,
        result=result,
        transport_name=transport.name,
        transport_network_capable=transport.network_capable,
        network_explicitly_enabled=allow_network,
    )
