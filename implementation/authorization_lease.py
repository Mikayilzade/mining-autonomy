"""Deterministic offline single-use authorization lease and consumption gate (I042)."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

CONSENT_MODE = "deterministic_offline_authorization_consent_verification"
EXECUTION_AUTH_MODE = "verified_exact_read_only_execution_authorization"
LEASE_MODE = "deterministic_single_use_read_only_authorization_lease"
ATTEMPT_MODE = "offline_single_request_execution_attempt"
RECEIPT_MODE = "deterministic_offline_authorization_lease_consumption"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _utc(value: Any, code: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(code)
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(code) from exc
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError(code + "_not_utc")
    return dt.astimezone(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _validate_consent(consent: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    if not isinstance(consent, Mapping) or consent.get("schema_version") != 1 or consent.get("mode") != CONSENT_MODE:
        raise ValueError("lease_consent_schema_or_mode_invalid")
    supplied = consent.get("consent_verification_sha256")
    core = dict(consent)
    core.pop("consent_verification_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("lease_consent_hash_mismatch")
    if consent.get("authorization_valid") is not True or consent.get("decision") != "authorize":
        raise ValueError("lease_authorization_not_valid")
    for key, wanted in {
        "transport_enabled": False,
        "network_calls_performed": False,
        "credentials_allowed": False,
        "action_enabled": False,
        "offline_only": True,
        "real_user_consent_inferred": False,
        "scope_widened": False,
    }.items():
        if consent.get(key) is not wanted:
            raise ValueError("lease_consent_" + key + "_invalid")
    auth = consent.get("execution_authorization")
    if not isinstance(auth, Mapping) or auth.get("schema_version") != 1 or auth.get("mode") != EXECUTION_AUTH_MODE:
        raise ValueError("lease_execution_authorization_invalid")
    auth_hash = auth.get("execution_authorization_sha256")
    auth_core = dict(auth)
    auth_core.pop("execution_authorization_sha256", None)
    if not isinstance(auth_hash, str) or len(auth_hash) != 64 or _hash(auth_core) != auth_hash:
        raise ValueError("lease_execution_authorization_hash_mismatch")
    if auth.get("authorization_granted") is not True:
        raise ValueError("lease_execution_authorization_not_granted")
    if auth.get("max_requests") != 1 or auth.get("method") != "GET" or auth.get("required_environment") != "production":
        raise ValueError("lease_execution_scope_not_single_production_get")
    if auth.get("credentials_allowed") is not False or auth.get("action_enabled") is not False:
        raise ValueError("lease_execution_scope_unsafe")
    if auth.get("transport_enabled") is not False or auth.get("network_calls_performed") is not False or auth.get("offline_verification_only") is not True:
        raise ValueError("lease_execution_authorization_not_inert")
    return dict(auth), supplied


def issue_single_use_authorization_lease(consent_verification: Mapping[str, Any], *, issued_at_utc: str) -> dict[str, Any]:
    """Issue an inert one-request lease over an exact I041 execution authorization."""
    auth, consent_hash = _validate_consent(consent_verification)
    issued = _utc(issued_at_utc, "lease_issued_at_invalid")
    verified = _utc(auth.get("verified_at_utc"), "lease_auth_verified_at_invalid")
    expires = _utc(auth.get("expires_at_utc"), "lease_auth_expiry_invalid")
    if issued < verified or issued >= expires:
        raise ValueError("lease_issue_time_outside_authorization_window")
    core = {
        "schema_version": 1, "mode": LEASE_MODE,
        "consent_verification_sha256": consent_hash,
        "execution_authorization_sha256": auth["execution_authorization_sha256"],
        "authorization_request_sha256": auth["authorization_request_sha256"],
        "scope_sha256": auth["scope_sha256"], "decision_sha256": auth["decision_sha256"],
        "issued_at_utc": _iso(issued), "expires_at_utc": _iso(expires),
        "max_requests": 1, "remaining_requests": 1, "method": "GET", "required_environment": "production",
        "credentials_allowed": False, "action_enabled": False, "transport_enabled": False,
        "network_calls_performed": False, "offline_consumption_only": True, "single_use": True,
        "synthetic_fixture_not_real_consent": bool(auth.get("synthetic_fixture_not_real_consent", False)),
    }
    return {**core, "authorization_lease_sha256": _hash(core)}


def _validate_lease(lease: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    if not isinstance(lease, Mapping) or lease.get("schema_version") != 1 or lease.get("mode") != LEASE_MODE:
        raise ValueError("lease_schema_or_mode_invalid")
    supplied = lease.get("authorization_lease_sha256")
    core = dict(lease); core.pop("authorization_lease_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("lease_hash_mismatch")
    if lease.get("single_use") is not True or lease.get("max_requests") != 1 or lease.get("remaining_requests") != 1:
        raise ValueError("lease_budget_invalid")
    if lease.get("method") != "GET" or lease.get("required_environment") != "production":
        raise ValueError("lease_scope_invalid")
    for key, wanted in {"credentials_allowed": False, "action_enabled": False, "transport_enabled": False,
                        "network_calls_performed": False, "offline_consumption_only": True}.items():
        if lease.get(key) is not wanted:
            raise ValueError("lease_" + key + "_invalid")
    return core, supplied


def _validate_prior_receipts(receipts: Iterable[Mapping[str, Any]], lease_hash: str) -> None:
    for receipt in receipts:
        if not isinstance(receipt, Mapping) or receipt.get("schema_version") != 1 or receipt.get("mode") != RECEIPT_MODE:
            raise ValueError("lease_prior_receipt_invalid")
        supplied = receipt.get("lease_consumption_sha256")
        core = dict(receipt); core.pop("lease_consumption_sha256", None)
        if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
            raise ValueError("lease_prior_receipt_hash_mismatch")
        if receipt.get("authorization_lease_sha256") == lease_hash and receipt.get("consumed") is True:
            raise ValueError("lease_replay_or_double_consumption")


def consume_single_use_authorization_lease(lease: Mapping[str, Any], attempt: Mapping[str, Any], *, attempted_at_utc: str,
                                            prior_consumption_receipts: Iterable[Mapping[str, Any]] = ()) -> dict[str, Any]:
    """Consume the lease exactly once in an offline gate; never performs transport."""
    _, lease_hash = _validate_lease(lease)
    _validate_prior_receipts(prior_consumption_receipts, lease_hash)
    now = _utc(attempted_at_utc, "lease_attempt_time_invalid")
    issued = _utc(lease.get("issued_at_utc"), "lease_issue_time_invalid")
    expires = _utc(lease.get("expires_at_utc"), "lease_expiry_invalid")
    if now < issued or now >= expires:
        raise ValueError("lease_attempt_outside_validity_window")
    if not isinstance(attempt, Mapping) or attempt.get("schema_version") != 1 or attempt.get("mode") != ATTEMPT_MODE:
        raise ValueError("lease_attempt_schema_or_mode_invalid")
    supplied_attempt = attempt.get("attempt_sha256")
    attempt_core = dict(attempt); attempt_core.pop("attempt_sha256", None)
    if not isinstance(supplied_attempt, str) or len(supplied_attempt) != 64 or _hash(attempt_core) != supplied_attempt:
        raise ValueError("lease_attempt_hash_mismatch")
    if attempt.get("authorization_lease_sha256") != lease_hash:
        raise ValueError("lease_attempt_binding_mismatch")
    if attempt.get("execution_authorization_sha256") != lease.get("execution_authorization_sha256"):
        raise ValueError("lease_execution_authorization_binding_mismatch")
    if attempt.get("method") != "GET" or attempt.get("required_environment") != "production" or attempt.get("request_count") != 1:
        raise ValueError("lease_attempt_scope_widened")
    if attempt.get("credentials_used") is not False or attempt.get("action_enabled") is not False:
        raise ValueError("lease_attempt_unsafe")
    if attempt.get("transport_requested") is not False:
        raise ValueError("lease_transport_must_remain_disabled_in_i042")
    core = {
        "schema_version": 1, "mode": RECEIPT_MODE,
        "authorization_lease_sha256": lease_hash,
        "execution_authorization_sha256": lease["execution_authorization_sha256"],
        "attempt_sha256": supplied_attempt, "consumed_at_utc": _iso(now),
        "consumed": True, "requests_consumed": 1, "remaining_requests": 0, "replay_allowed": False,
        "transport_enabled": False, "network_calls_performed": False, "credentials_used": False,
        "action_enabled": False, "offline_consumption_only": True,
        "synthetic_fixture_not_real_consent": bool(lease.get("synthetic_fixture_not_real_consent", False)),
    }
    return {**core, "lease_consumption_sha256": _hash(core)}
