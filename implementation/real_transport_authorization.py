"""I074 deterministic explicit real-transport authorization verifier over I073.

Offline only. Verifies a fresh explicit human decision bound to the exact I073
review packet and exact anonymous one-production-GET scope. It can emit a
short-lived single-use authorization record, but never performs DNS/HTTP,
enables transport, uses credentials, or permits any value-moving action.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from hashlib import sha256
import json
from typing import Any, Collection, Mapping

MODE = "deterministic_real_transport_authorization_verifier"
DECISION_MODE = "explicit_human_real_transport_authorization_decision"
_ALLOWED_DECISIONS = {"authorize_exact_read_only_transport", "deny"}
_EXPECTED_REVIEW_MODE = "deterministic_pre_real_transport_review"


def _hash(value: Any) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def _utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timezone.utc.utcoffset(dt):
        raise ValueError("timestamp_must_be_utc")
    return dt


def _iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _exact_scope(scope: Mapping[str, Any]) -> bool:
    return (
        scope.get("method") == "GET"
        and scope.get("request_count") == 1
        and scope.get("required_environment") == "production"
        and isinstance(scope.get("target_fingerprint"), str)
        and bool(scope.get("target_fingerprint"))
        and scope.get("credentials_allowed") is False
        and scope.get("action_enabled") is False
    )


def verify_real_transport_authorization(
    review: Mapping[str, Any],
    decision: Mapping[str, Any],
    *,
    verified_at_utc: str,
    authorization_ttl_seconds: int = 120,
    max_decision_age_seconds: int = 300,
    seen_decision_sha256: Collection[str] = (),
) -> dict[str, Any]:
    """Verify one explicit decision without enabling any real transport."""
    blockers: list[str] = []

    review_hash = review.get("pre_real_transport_review_sha256")
    review_core = dict(review)
    review_core.pop("pre_real_transport_review_sha256", None)
    if not isinstance(review_hash, str) or review_hash != _hash(review_core):
        blockers.append("pre_real_transport_review_hash_invalid")
    if review.get("mode") != _EXPECTED_REVIEW_MODE:
        blockers.append("pre_real_transport_review_mode_invalid")
    if (
        review.get("review_state") != "ready_for_explicit_real_transport_decision"
        or review.get("unresolved_blockers")
    ):
        blockers.append("pre_real_transport_review_not_ready")

    scope = review.get("exact_scope")
    if not isinstance(scope, Mapping):
        scope = {}
        blockers.append("review_exact_scope_missing")
    if not _exact_scope(scope):
        blockers.append("review_scope_not_exact_anonymous_get")

    inert_review_flags = {
        "authorization_granted": False,
        "real_user_authorization_inferred": False,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "review_packet_is_execution_token": False,
    }
    for key, required in inert_review_flags.items():
        if review.get(key) is not required:
            blockers.append(f"unsafe_or_missing_review_{key}")

    if (
        not isinstance(authorization_ttl_seconds, int)
        or isinstance(authorization_ttl_seconds, bool)
        or not 30 <= authorization_ttl_seconds <= 300
    ):
        blockers.append("authorization_ttl_out_of_bounds")
        authorization_ttl_seconds = 120
    if (
        not isinstance(max_decision_age_seconds, int)
        or isinstance(max_decision_age_seconds, bool)
        or not 30 <= max_decision_age_seconds <= 600
    ):
        blockers.append("max_decision_age_out_of_bounds")
        max_decision_age_seconds = 300

    choice = decision.get("decision")
    if decision.get("mode") != DECISION_MODE:
        blockers.append("explicit_real_transport_decision_mode_required")
    if choice not in _ALLOWED_DECISIONS:
        blockers.append("real_transport_decision_value_invalid")
    if decision.get("human_scope_acknowledged") is not True:
        blockers.append("human_scope_acknowledgement_required")
    if decision.get("pre_real_transport_review_sha256") != review_hash:
        blockers.append("decision_review_hash_binding_invalid")
    if decision.get("exact_scope_sha256") != review.get("exact_scope_sha256"):
        blockers.append("decision_exact_scope_hash_binding_invalid")

    decided_scope = decision.get("authorized_scope")
    if choice == "authorize_exact_read_only_transport":
        if not isinstance(decided_scope, Mapping):
            blockers.append("authorized_scope_missing")
        elif dict(decided_scope) != dict(scope) or not _exact_scope(decided_scope):
            blockers.append("authorized_scope_widened_or_changed")
    elif decided_scope not in (None, {}):
        blockers.append("deny_must_not_include_authorized_scope")

    decision_hash = decision.get("real_transport_decision_sha256")
    decision_core = dict(decision)
    decision_core.pop("real_transport_decision_sha256", None)
    if not isinstance(decision_hash, str) or decision_hash != _hash(decision_core):
        blockers.append("real_transport_decision_hash_invalid")
    elif decision_hash in set(seen_decision_sha256):
        blockers.append("real_transport_decision_replay_detected")

    try:
        reviewed_at = _utc(str(review.get("reviewed_at_utc")))
        decided_at = _utc(str(decision.get("decided_at_utc")))
        verified_at = _utc(verified_at_utc)
        if decided_at < reviewed_at:
            blockers.append("decision_precedes_review")
        if decided_at > verified_at:
            blockers.append("decision_timestamp_in_future")
        age = (verified_at - decided_at).total_seconds()
        if age < 0:
            blockers.append("decision_timestamp_in_future")
        elif age > max_decision_age_seconds:
            blockers.append("real_transport_decision_stale")
    except Exception:
        blockers.append("invalid_review_decision_or_verification_timestamp")
        verified_at = datetime.now(timezone.utc)

    blockers = list(dict.fromkeys(blockers))
    accepted = not blockers
    authorized = accepted and choice == "authorize_exact_read_only_transport"
    denied = accepted and choice == "deny"

    authorization_record = None
    if authorized:
        issued_at = verified_at
        expires_at = issued_at + timedelta(seconds=authorization_ttl_seconds)
        auth_core = {
            "schema_version": 1,
            "mode": "single_use_real_transport_authorization_record",
            "authorization_state": "authorized_exact_single_read_only_transport",
            "issued_at_utc": _iso_z(issued_at),
            "expires_at_utc": _iso_z(expires_at),
            "pre_real_transport_review_sha256": review_hash,
            "real_transport_decision_sha256": decision_hash,
            "exact_scope_sha256": review.get("exact_scope_sha256"),
            "authorization_scope": dict(scope),
            "max_consumptions": 1,
            "authorization_is_single_use": True,
            "credentials_allowed": False,
            "task_acceptance_enabled": False,
            "submission_enabled": False,
            "value_movement_enabled": False,
            "network_enabled": False,
            "network_calls_performed": False,
            "transport_enabled": False,
            "record_is_execution_token": False,
        }
        authorization_record = {
            **auth_core,
            "real_transport_authorization_sha256": _hash(auth_core),
        }

    core = {
        "schema_version": 1,
        "mode": MODE,
        "verification_state": (
            "explicit_real_transport_authorization_verified"
            if authorized
            else "explicit_real_transport_deny_verified"
            if denied
            else "real_transport_decision_rejected"
        ),
        "verified_at_utc": verified_at_utc,
        "decision": choice if accepted else None,
        "pre_real_transport_review_sha256": review_hash,
        "real_transport_decision_sha256": decision_hash if isinstance(decision_hash, str) else None,
        "exact_scope_sha256": review.get("exact_scope_sha256"),
        "authorization_record": authorization_record,
        "blockers": blockers,
        "human_decision_recorded": accepted,
        "explicit_real_transport_authorization_verified": authorized,
        "explicit_real_transport_deny_verified": denied,
        "real_user_authorization_inferred_from_chat_history": False,
        "authorization_is_short_lived": authorization_record is not None,
        "authorization_is_single_use": authorization_record is not None,
        "transport_enabled": False,
        "network_enabled": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "task_acceptance_enabled": False,
        "submission_enabled": False,
        "execution_enabled": False,
        "value_movement_enabled": False,
        "verification_record_is_execution_token": False,
    }
    return {**core, "real_transport_authorization_verification_sha256": _hash(core)}
