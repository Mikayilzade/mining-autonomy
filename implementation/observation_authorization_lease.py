"""I071 deterministic single-use observation authorization lease.

Offline only. Converts one verified I070 read-only authorization record into a
short-lived, single-use lease bound to the exact I069 request/scope. Consumption
is modeled with synthetic attempts and prior receipts; no transport exists here.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

LEASE_MODE = "deterministic_single_use_observation_authorization_lease"
CONSUME_MODE = "deterministic_observation_lease_consumption"
ATTEMPT_MODE = "synthetic_read_only_transport_attempt"
_EXACT_METHOD = "GET"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _verify_request(request: Mapping[str, Any]) -> tuple[list[str], str | None, Mapping[str, Any]]:
    blockers: list[str] = []
    request_hash = request.get("human_decision_request_sha256")
    core = dict(request)
    core.pop("human_decision_request_sha256", None)
    if not isinstance(request_hash, str) or request_hash != _hash(core):
        blockers.append("human_decision_request_hash_invalid")
    if request.get("request_state") != "decision_requested" or request.get("blockers"):
        blockers.append("human_decision_request_not_open")
    target = request.get("decision_scope", {}).get("authorization_target", {})
    if not isinstance(target, Mapping):
        target = {}
    if not (
        target.get("method") == _EXACT_METHOD
        and target.get("request_count") == 1
        and target.get("required_environment") == "production"
        and target.get("credentials_allowed") is False
        and target.get("action_enabled") is False
        and isinstance(target.get("target_fingerprint"), str)
        and target.get("target_fingerprint")
    ):
        blockers.append("request_scope_not_exact_anonymous_get")
    return blockers, request_hash if isinstance(request_hash, str) else None, target


def build_observation_authorization_lease(
    verification: Mapping[str, Any],
    request: Mapping[str, Any],
    *,
    issued_at_utc: str,
    lease_ttl_seconds: int = 120,
) -> dict[str, Any]:
    blockers: list[str] = []
    verification_hash = verification.get("human_decision_verification_sha256")
    verification_core = dict(verification)
    verification_core.pop("human_decision_verification_sha256", None)
    if not isinstance(verification_hash, str) or verification_hash != _hash(verification_core):
        blockers.append("human_decision_verification_hash_invalid")
    if verification.get("verification_state") != "explicit_read_only_authorization_verified":
        blockers.append("explicit_read_only_authorization_not_verified")
    if verification.get("explicit_authorization_verified") is not True:
        blockers.append("explicit_authorization_flag_missing")
    if verification.get("blockers"):
        blockers.append("verification_has_blockers")
    if verification.get("record_is_execution_token") is not False or verification.get("record_is_transport_lease") is not False:
        blockers.append("verification_record_type_unsafe")

    request_blockers, request_hash, target = _verify_request(request)
    blockers.extend(request_blockers)
    if verification.get("human_decision_request_sha256") != request_hash:
        blockers.append("verification_request_hash_binding_invalid")
    if verification.get("market_side_readiness_sha256") != request.get("market_side_readiness_sha256"):
        blockers.append("verification_readiness_hash_binding_invalid")
    if verification.get("exact_scope_sha256") != request.get("exact_scope_sha256"):
        blockers.append("verification_scope_hash_binding_invalid")

    auth_scope = verification.get("authorization_scope")
    if not isinstance(auth_scope, Mapping):
        auth_scope = {}
        blockers.append("verified_authorization_scope_missing")
    expected_scope = {
        "method": _EXACT_METHOD,
        "request_count": 1,
        "required_environment": "production",
        "target_fingerprint": target.get("target_fingerprint"),
        "credentials_allowed": False,
        "action_enabled": False,
    }
    if dict(auth_scope) != expected_scope:
        blockers.append("verified_authorization_scope_not_exact")

    if not isinstance(lease_ttl_seconds, int) or isinstance(lease_ttl_seconds, bool) or not 1 <= lease_ttl_seconds <= 300:
        blockers.append("lease_ttl_out_of_range")

    issued = expires = None
    try:
        issued = _utc(issued_at_utc)
        verified_at = _utc(str(verification.get("verified_at_utc")))
        request_expires = _utc(str(request.get("expires_at_utc")))
        if issued < verified_at:
            blockers.append("lease_issued_before_verification")
        if issued >= request_expires:
            blockers.append("request_expired_before_lease_issue")
        ttl = lease_ttl_seconds if isinstance(lease_ttl_seconds, int) and not isinstance(lease_ttl_seconds, bool) else 1
        ttl = max(1, min(ttl, 300))
        expires = min(issued + timedelta(seconds=ttl), request_expires)
        if expires <= issued:
            blockers.append("lease_has_no_valid_window")
    except Exception:
        blockers.append("invalid_lease_or_request_timestamp")

    inert_flags = (
        "transport_enabled", "network_enabled", "network_calls_performed",
        "credentials_used", "task_acceptance_enabled", "submission_enabled",
        "execution_enabled", "value_movement_enabled",
    )
    for key in inert_flags:
        if verification.get(key) is not False:
            blockers.append(f"unsafe_or_missing_verification_{key}")

    blockers = list(dict.fromkeys(blockers))
    lease_ready = not blockers
    lease_core = {
        "schema_version": 1,
        "mode": LEASE_MODE,
        "lease_state": "single_use_observation_lease_ready" if lease_ready else "lease_rejected",
        "issued_at_utc": issued_at_utc,
        "expires_at_utc": _iso(expires) if lease_ready and expires else None,
        "human_decision_verification_sha256": verification_hash,
        "human_decision_request_sha256": request_hash,
        "market_side_readiness_sha256": verification.get("market_side_readiness_sha256"),
        "exact_scope_sha256": verification.get("exact_scope_sha256"),
        "current_resource_backend_id": verification.get("current_resource_backend_id"),
        "lease_scope": expected_scope if lease_ready else None,
        "max_consumptions": 1,
        "blockers": blockers,
        "authorization_verified": lease_ready,
        "lease_is_single_use": True,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "lease_is_execution_token": False,
    }
    return {**lease_core, "observation_authorization_lease_sha256": _hash(lease_core)}


def _validated_consumed_hashes(receipts: Iterable[Mapping[str, Any]]) -> tuple[set[str], list[str]]:
    consumed: set[str] = set()
    blockers: list[str] = []
    for receipt in receipts:
        receipt_hash = receipt.get("observation_lease_consumption_sha256")
        core = dict(receipt)
        core.pop("observation_lease_consumption_sha256", None)
        if not isinstance(receipt_hash, str) or receipt_hash != _hash(core):
            blockers.append("prior_consumption_receipt_hash_invalid")
            continue
        if receipt.get("mode") != CONSUME_MODE:
            blockers.append("prior_consumption_receipt_mode_invalid")
            continue
        if receipt.get("consumption_state") == "lease_consumed":
            consumed_lease_hash = receipt.get("observation_authorization_lease_sha256")
            if isinstance(consumed_lease_hash, str):
                consumed.add(consumed_lease_hash)
    return consumed, blockers


def consume_observation_authorization_lease(
    lease: Mapping[str, Any],
    attempt: Mapping[str, Any],
    *,
    consumed_at_utc: str,
    prior_consumption_receipts: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    blockers: list[str] = []
    lease_hash = lease.get("observation_authorization_lease_sha256")
    lease_core = dict(lease)
    lease_core.pop("observation_authorization_lease_sha256", None)
    if not isinstance(lease_hash, str) or lease_hash != _hash(lease_core):
        blockers.append("observation_authorization_lease_hash_invalid")
    if lease.get("lease_state") != "single_use_observation_lease_ready" or lease.get("blockers"):
        blockers.append("lease_not_ready")
    if lease.get("max_consumptions") != 1 or lease.get("lease_is_single_use") is not True:
        blockers.append("lease_not_single_use")

    scope = lease.get("lease_scope")
    if not isinstance(scope, Mapping):
        scope = {}
        blockers.append("lease_scope_missing")
    if not (
        scope.get("method") == _EXACT_METHOD
        and scope.get("request_count") == 1
        and scope.get("required_environment") == "production"
        and scope.get("credentials_allowed") is False
        and scope.get("action_enabled") is False
        and scope.get("target_fingerprint")
    ):
        blockers.append("lease_scope_not_exact_anonymous_get")

    if attempt.get("mode") != ATTEMPT_MODE:
        blockers.append("synthetic_attempt_mode_required")
    if attempt.get("method") != _EXACT_METHOD:
        blockers.append("attempt_method_not_allowed")
    if attempt.get("request_count") != 1:
        blockers.append("attempt_request_count_not_one")
    if attempt.get("required_environment") != "production":
        blockers.append("attempt_environment_invalid")
    if attempt.get("target_fingerprint") != scope.get("target_fingerprint"):
        blockers.append("attempt_target_fingerprint_mismatch")
    if attempt.get("credentials_used") is not False:
        blockers.append("attempt_credentials_forbidden")
    if attempt.get("action_enabled") is not False:
        blockers.append("attempt_action_forbidden")
    if attempt.get("network_transport_callback_present") is not False:
        blockers.append("network_transport_callback_forbidden_in_i071")

    try:
        consumed_at = _utc(consumed_at_utc)
        issued_at = _utc(str(lease.get("issued_at_utc")))
        expires_at = _utc(str(lease.get("expires_at_utc")))
        if not (issued_at <= consumed_at < expires_at):
            blockers.append("lease_expired_or_not_yet_valid")
    except Exception:
        blockers.append("invalid_consumption_or_lease_timestamp")

    consumed_hashes, receipt_blockers = _validated_consumed_hashes(prior_consumption_receipts)
    blockers.extend(receipt_blockers)
    if isinstance(lease_hash, str) and lease_hash in consumed_hashes:
        blockers.append("lease_replay_or_double_consumption")

    blockers = list(dict.fromkeys(blockers))
    consumed = not blockers
    receipt_core = {
        "schema_version": 1,
        "mode": CONSUME_MODE,
        "consumption_state": "lease_consumed" if consumed else "consumption_rejected",
        "consumed_at_utc": consumed_at_utc,
        "observation_authorization_lease_sha256": lease_hash,
        "human_decision_verification_sha256": lease.get("human_decision_verification_sha256"),
        "human_decision_request_sha256": lease.get("human_decision_request_sha256"),
        "exact_scope_sha256": lease.get("exact_scope_sha256"),
        "attempt_fingerprint_sha256": _hash(dict(attempt)),
        "blockers": blockers,
        "lease_consumed": consumed,
        "remaining_consumptions": 0 if consumed else 1,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "receipt_is_execution_token": False,
    }
    return {**receipt_core, "observation_lease_consumption_sha256": _hash(receipt_core)}
