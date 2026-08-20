"""Dependency-injected, synthetic-only execution wrapper over I042 (I043)."""
from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Protocol

from authorization_lease import consume_single_use_authorization_lease

EXECUTION_REQUEST_MODE = "dependency_injected_single_get_execution_request"
EXECUTION_RESULT_MODE = "deterministic_dependency_injected_execution_result"
SYNTHETIC_TRANSPORT_KIND = "synthetic_stub"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class SyntheticTransport(Protocol):
    transport_kind: str
    network_capable: bool

    def execute(self, request: Mapping[str, Any]) -> Mapping[str, Any]: ...


class DeterministicSyntheticTransport:
    """Pure deterministic transport stub. It cannot perform DNS/HTTP."""

    transport_kind = SYNTHETIC_TRANSPORT_KIND
    network_capable = False

    def execute(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        return {
            "status_code": 200,
            "content_type": "application/json",
            "body": {"synthetic": True, "target_fingerprint": request["target_fingerprint"]},
            "network_calls_performed": False,
        }


def _validate_execution_request(lease: Mapping[str, Any], request: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    if not isinstance(request, Mapping) or request.get("schema_version") != 1 or request.get("mode") != EXECUTION_REQUEST_MODE:
        raise ValueError("execution_request_schema_or_mode_invalid")
    supplied = request.get("execution_request_sha256")
    core = dict(request)
    core.pop("execution_request_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("execution_request_hash_mismatch")
    if request.get("authorization_lease_sha256") != lease.get("authorization_lease_sha256"):
        raise ValueError("execution_request_lease_binding_mismatch")
    if request.get("execution_authorization_sha256") != lease.get("execution_authorization_sha256"):
        raise ValueError("execution_request_authorization_binding_mismatch")
    if request.get("method") != "GET" or request.get("required_environment") != "production" or request.get("request_count") != 1:
        raise ValueError("execution_request_scope_widened")
    if request.get("credentials_used") is not False or request.get("action_enabled") is not False:
        raise ValueError("execution_request_unsafe")
    target = request.get("target_fingerprint")
    if not isinstance(target, str) or not target:
        raise ValueError("execution_request_target_missing")
    return core, supplied


def execute_with_single_use_lease(
    lease: Mapping[str, Any],
    execution_request: Mapping[str, Any],
    *,
    attempted_at_utc: str,
    prior_consumption_receipts: Iterable[Mapping[str, Any]] = (),
    transport: SyntheticTransport | None = None,
    allow_real_transport: bool = False,
) -> dict[str, Any]:
    """Consume one I042 lease before invoking exactly one synthetic transport stub.

    I043 intentionally has no real-network integration. ``allow_real_transport=True``
    fails closed so a later run must add a separately reviewed integration boundary.
    """
    if allow_real_transport is not False:
        raise ValueError("real_transport_not_supported_in_i043")

    _, request_hash = _validate_execution_request(lease, execution_request)
    selected = transport if transport is not None else DeterministicSyntheticTransport()
    if getattr(selected, "transport_kind", None) != SYNTHETIC_TRANSPORT_KIND or getattr(selected, "network_capable", None) is not False:
        raise ValueError("non_synthetic_transport_rejected")
    execute = getattr(selected, "execute", None)
    if not callable(execute):
        raise ValueError("synthetic_transport_invalid")

    attempt_core = {
        "schema_version": 1,
        "mode": "offline_single_request_execution_attempt",
        "authorization_lease_sha256": lease.get("authorization_lease_sha256"),
        "execution_authorization_sha256": lease.get("execution_authorization_sha256"),
        "method": "GET",
        "required_environment": "production",
        "request_count": 1,
        "credentials_used": False,
        "action_enabled": False,
        "transport_requested": False,
        "target_fingerprint": execution_request["target_fingerprint"],
    }
    offline_attempt = {**attempt_core, "attempt_sha256": _hash(attempt_core)}
    consumption = consume_single_use_authorization_lease(
        lease,
        offline_attempt,
        attempted_at_utc=attempted_at_utc,
        prior_consumption_receipts=prior_consumption_receipts,
    )

    response = selected.execute(execution_request)
    if not isinstance(response, Mapping):
        raise ValueError("synthetic_transport_response_invalid")
    if response.get("network_calls_performed") is not False:
        raise ValueError("synthetic_transport_claimed_network_activity")
    response_core = dict(response)
    response_hash = _hash(response_core)

    core = {
        "schema_version": 1,
        "mode": EXECUTION_RESULT_MODE,
        "execution_request_sha256": request_hash,
        "authorization_lease_sha256": lease["authorization_lease_sha256"],
        "execution_authorization_sha256": lease["execution_authorization_sha256"],
        "lease_consumption_sha256": consumption["lease_consumption_sha256"],
        "lease_consumed_before_transport": True,
        "remaining_requests": 0,
        "transport_kind": SYNTHETIC_TRANSPORT_KIND,
        "allow_real_transport": False,
        "real_transport_supported": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "action_enabled": False,
        "synthetic_response_sha256": response_hash,
        "synthetic_response": response_core,
    }
    return {**core, "execution_result_sha256": _hash(core)}
