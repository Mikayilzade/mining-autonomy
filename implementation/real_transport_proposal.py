"""Inert real-transport integration proposal contract (I044).

This module deliberately contains no DNS/HTTP client and cannot execute transport.
It only validates the exact I043 one-GET boundary and describes the evidence and
explicit authorization a later, separately reviewed integration would require.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

PROPOSAL_MODE = "inert_real_transport_integration_proposal"
EXECUTION_REQUEST_MODE = "dependency_injected_single_get_execution_request"
LEASE_MODE = "deterministic_single_use_read_only_authorization_lease"


def _hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def _parse_utc(value: str) -> datetime:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp_must_be_utc_z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("timestamp_invalid") from exc
    if parsed.tzinfo is None or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise ValueError("timestamp_must_be_utc_z")
    return parsed


def _validate_lease(lease: Mapping[str, Any]) -> str:
    if not isinstance(lease, Mapping) or lease.get("schema_version") != 1 or lease.get("mode") != LEASE_MODE:
        raise ValueError("authorization_lease_schema_or_mode_invalid")
    supplied = lease.get("authorization_lease_sha256")
    core = dict(lease)
    core.pop("authorization_lease_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("authorization_lease_hash_mismatch")
    if (
        lease.get("max_requests") != 1
        or lease.get("remaining_requests") != 1
        or lease.get("method") != "GET"
        or lease.get("required_environment") != "production"
        or lease.get("credentials_allowed") is not False
        or lease.get("action_enabled") is not False
        or lease.get("transport_enabled") is not False
        or lease.get("single_use") is not True
    ):
        raise ValueError("authorization_lease_scope_invalid")
    return supplied


def _validate_execution_request(lease: Mapping[str, Any], request: Mapping[str, Any]) -> str:
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
    if (
        request.get("method") != "GET"
        or request.get("required_environment") != "production"
        or request.get("request_count") != 1
    ):
        raise ValueError("execution_request_scope_widened")
    if request.get("credentials_used") is not False or request.get("action_enabled") is not False:
        raise ValueError("execution_request_unsafe")
    target = request.get("target_fingerprint")
    if not isinstance(target, str) or not target.strip():
        raise ValueError("execution_request_target_missing")
    return supplied


def build_real_transport_integration_proposal(
    lease: Mapping[str, Any],
    execution_request: Mapping[str, Any],
    *,
    proposed_at_utc: str,
) -> dict[str, Any]:
    """Return an inert, hash-bound proposal for a future one-GET integration.

    The result is intentionally non-authorizing and non-executable. It records
    the exact additional gates a later implementation must satisfy before any
    real DNS/HTTP integration may be considered.
    """
    lease_hash = _validate_lease(lease)
    request_hash = _validate_execution_request(lease, execution_request)
    proposed_at = _parse_utc(proposed_at_utc)
    issued_at = _parse_utc(lease.get("issued_at_utc"))
    expires_at = _parse_utc(lease.get("expires_at_utc"))
    if not issued_at <= proposed_at < expires_at:
        raise ValueError("proposal_outside_lease_validity_window")

    exact_scope = {
        "execution_request_sha256": request_hash,
        "authorization_lease_sha256": lease_hash,
        "execution_authorization_sha256": lease.get("execution_authorization_sha256"),
        "method": "GET",
        "required_environment": "production",
        "request_count": 1,
        "credentials_allowed": False,
        "action_enabled": False,
        "target_fingerprint": execution_request.get("target_fingerprint"),
    }
    exact_scope_hash = _hash(exact_scope)

    required_gates = [
        {
            "gate": "fresh_explicit_real_user_authorization",
            "required": True,
            "evidence": "decision explicitly authorizes this exact proposal/scope hash and is still inside the lease window",
            "synthetic_or_inferred_consent_accepted": False,
        },
        {
            "gate": "transport_implementation_review",
            "required": True,
            "evidence": "separately reviewed adapter exposes one GET only and consumes the single-use lease before network activity",
        },
        {
            "gate": "dns_and_destination_policy",
            "required": True,
            "evidence": "resolved destination is policy-allowed; loopback/private/link-local/metadata/internal targets fail closed",
        },
        {
            "gate": "redirect_policy",
            "required": True,
            "evidence": "redirect behavior is disabled or separately revalidated without widening the authorized destination scope",
        },
        {
            "gate": "response_resource_limits",
            "required": True,
            "evidence": "strict timeout, maximum body size and permitted content-type are enforced before evidence parsing",
        },
        {
            "gate": "current_source_compliance",
            "required": True,
            "evidence": "current first-party platform terms/public-access rules permit the exact anonymous read-only observation",
        },
        {
            "gate": "durable_receipt_binding",
            "required": True,
            "evidence": "request, lease consumption, destination, response metadata/body digest and timestamps are hash-bound for audit",
        },
    ]

    core = {
        "schema_version": 1,
        "mode": PROPOSAL_MODE,
        "proposal_state": "blocked_pending_separate_real_transport_review_and_explicit_user_authorization",
        "proposed_at_utc": proposed_at_utc,
        "expires_at_utc": lease.get("expires_at_utc"),
        "exact_scope": exact_scope,
        "exact_scope_sha256": exact_scope_hash,
        "required_gates": required_gates,
        "authorization_granted": False,
        "real_user_authorization_present": False,
        "transport_implementation_present": False,
        "transport_enabled": False,
        "network_capable": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "action_enabled": False,
        "money_or_value_movement_enabled": False,
        "executable_callback_present": False,
        "proposal_is_authorization": False,
        "proposal_is_execution_token": False,
    }
    return {**core, "real_transport_proposal_sha256": _hash(core)}
