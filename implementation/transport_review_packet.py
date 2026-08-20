"""Deterministic offline human-review packet for I044 transport proposals (I045).

The packet never grants authorization and contains no transport capability. It
only proves that the exact inert proposal is internally valid, evaluates a
caller-supplied first-party source-compliance evidence record for freshness and
scope, and presents the remaining gates for an explicit human decision.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping
from urllib.parse import urlparse

PROPOSAL_MODE = "inert_real_transport_integration_proposal"
REVIEW_MODE = "deterministic_offline_real_transport_human_review_packet"
REQUIRED_GATES = (
    "fresh_explicit_real_user_authorization",
    "transport_implementation_review",
    "dns_and_destination_policy",
    "redirect_policy",
    "response_resource_limits",
    "current_source_compliance",
    "durable_receipt_binding",
)
ALLOWED_EVIDENCE_CLASSES = {"first_party_terms", "first_party_docs", "first_party_public_access_policy"}


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


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


def _validate_proposal(proposal: Mapping[str, Any]) -> tuple[str, Mapping[str, Any]]:
    if not isinstance(proposal, Mapping) or proposal.get("schema_version") != 1 or proposal.get("mode") != PROPOSAL_MODE:
        raise ValueError("proposal_schema_or_mode_invalid")
    supplied = proposal.get("real_transport_proposal_sha256")
    core = dict(proposal)
    core.pop("real_transport_proposal_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("proposal_hash_mismatch")
    scope = proposal.get("exact_scope")
    if not isinstance(scope, Mapping) or proposal.get("exact_scope_sha256") != _hash(scope):
        raise ValueError("proposal_exact_scope_hash_mismatch")
    if (
        scope.get("method") != "GET"
        or scope.get("required_environment") != "production"
        or scope.get("request_count") != 1
        or scope.get("credentials_allowed") is not False
        or scope.get("action_enabled") is not False
    ):
        raise ValueError("proposal_scope_invalid")
    gate_names = [g.get("gate") for g in proposal.get("required_gates", []) if isinstance(g, Mapping) and g.get("required") is True]
    if set(gate_names) != set(REQUIRED_GATES) or len(gate_names) != len(REQUIRED_GATES):
        raise ValueError("proposal_required_gates_invalid")
    inert_false = (
        "authorization_granted", "real_user_authorization_present", "transport_implementation_present",
        "transport_enabled", "network_capable", "network_calls_performed", "credentials_used",
        "action_enabled", "money_or_value_movement_enabled", "executable_callback_present",
        "proposal_is_authorization", "proposal_is_execution_token",
    )
    if any(proposal.get(k) is not False for k in inert_false):
        raise ValueError("proposal_not_inert")
    return supplied, scope


def _evaluate_source_compliance(evidence: Mapping[str, Any] | None, *, reviewed_at: datetime, max_age_hours: int) -> tuple[bool, list[str], dict[str, Any] | None]:
    reasons: list[str] = []
    if not isinstance(evidence, Mapping):
        return False, ["source_compliance_evidence_missing"], None
    required = ("platform", "source_url", "evidence_class", "checked_at_utc", "anonymous_read_only_observation_permitted", "credentials_required", "human_only_access_required", "evidence_sha256")
    if any(k not in evidence for k in required):
        return False, ["source_compliance_evidence_fields_missing"], None
    supplied_hash = evidence.get("evidence_sha256")
    core = dict(evidence)
    core.pop("evidence_sha256", None)
    if not isinstance(supplied_hash, str) or len(supplied_hash) != 64 or _hash(core) != supplied_hash:
        return False, ["source_compliance_evidence_hash_mismatch"], None
    parsed = urlparse(str(evidence.get("source_url")))
    if parsed.scheme != "https" or not parsed.netloc:
        reasons.append("source_compliance_source_url_not_https")
    if evidence.get("evidence_class") not in ALLOWED_EVIDENCE_CLASSES:
        reasons.append("source_compliance_evidence_class_not_first_party")
    try:
        checked_at = _parse_utc(evidence.get("checked_at_utc"))
    except (ValueError, TypeError):
        reasons.append("source_compliance_checked_at_invalid")
        checked_at = None
    if checked_at is not None:
        age_seconds = (reviewed_at - checked_at).total_seconds()
        if age_seconds < 0:
            reasons.append("source_compliance_checked_at_in_future")
        elif age_seconds > max_age_hours * 3600:
            reasons.append("source_compliance_evidence_stale")
    if evidence.get("anonymous_read_only_observation_permitted") is not True:
        reasons.append("anonymous_read_only_observation_not_confirmed")
    if evidence.get("credentials_required") is not False:
        reasons.append("credentials_free_access_not_confirmed")
    if evidence.get("human_only_access_required") is not False:
        reasons.append("machine_read_only_access_not_confirmed")
    normalized = {
        "platform": evidence.get("platform"),
        "source_url": evidence.get("source_url"),
        "evidence_class": evidence.get("evidence_class"),
        "checked_at_utc": evidence.get("checked_at_utc"),
        "evidence_sha256": supplied_hash,
        "anonymous_read_only_observation_permitted": evidence.get("anonymous_read_only_observation_permitted"),
        "credentials_required": evidence.get("credentials_required"),
        "human_only_access_required": evidence.get("human_only_access_required"),
    }
    return not reasons, reasons, normalized


def build_real_transport_human_review_packet(
    proposal: Mapping[str, Any],
    source_compliance_evidence: Mapping[str, Any] | None,
    *,
    reviewed_at_utc: str,
    max_source_evidence_age_hours: int = 168,
) -> dict[str, Any]:
    """Build an inert review packet; never create authorization or transport."""
    if not isinstance(max_source_evidence_age_hours, int) or not 1 <= max_source_evidence_age_hours <= 720:
        raise ValueError("source_evidence_max_age_invalid")
    proposal_hash, scope = _validate_proposal(proposal)
    reviewed_at = _parse_utc(reviewed_at_utc)
    expires_at = _parse_utc(proposal.get("expires_at_utc"))
    if reviewed_at >= expires_at:
        raise ValueError("review_after_proposal_expiry")
    compliance_ok, blockers, normalized_evidence = _evaluate_source_compliance(
        source_compliance_evidence, reviewed_at=reviewed_at, max_age_hours=max_source_evidence_age_hours
    )
    state = "ready_for_human_decision" if compliance_ok else "blocked_by_missing_evidence"
    checklist = []
    for gate in REQUIRED_GATES:
        if gate == "current_source_compliance":
            status = "evidence_ready" if compliance_ok else "blocked"
            detail = "current first-party evidence supports exact anonymous read-only observation" if compliance_ok else ";".join(blockers)
        elif gate == "fresh_explicit_real_user_authorization":
            status = "awaiting_human_decision" if compliance_ok else "not_reachable_until_evidence_ready"
            detail = "must be separately explicit and bound to this exact packet/scope; this packet is not authorization"
        else:
            status = "future_execution_gate_unresolved"
            detail = "must be satisfied by a separately reviewed real-transport implementation before any network call"
        checklist.append({"gate": gate, "status": status, "detail": detail})
    core = {
        "schema_version": 1,
        "mode": REVIEW_MODE,
        "review_state": state,
        "reviewed_at_utc": reviewed_at_utc,
        "expires_at_utc": proposal.get("expires_at_utc"),
        "real_transport_proposal_sha256": proposal_hash,
        "exact_scope_sha256": proposal.get("exact_scope_sha256"),
        "exact_scope": dict(scope),
        "source_compliance_evidence": normalized_evidence,
        "source_compliance_blockers": blockers,
        "gate_checklist": checklist,
        "human_decision_requested": compliance_ok,
        "authorization_granted": False,
        "real_user_authorization_present": False,
        "transport_enabled": False,
        "network_capable": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "action_enabled": False,
        "money_or_value_movement_enabled": False,
        "review_packet_is_authorization": False,
        "review_packet_is_execution_token": False,
    }
    return {**core, "human_review_packet_sha256": _hash(core)}
