"""Deterministic offline bridge from I046 replay into I045 human-review state (I047).

The bridge never grants authorization and never enables transport. It accepts only a
hash-valid I045 review packet plus a hash-valid I046 replay result. A packet can remain
human-decision-ready only when the replay proves reproducible first-party evidence and
that evidence is exactly the evidence bound into I045.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

REVIEW_MODE = "deterministic_offline_real_transport_human_review_packet"
REPLAY_MODE = "deterministic_offline_source_compliance_evidence_replay"
BRIDGE_MODE = "deterministic_offline_reproducible_compliance_review_bridge"


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


def _validate_review_packet(packet: Mapping[str, Any]) -> tuple[str, Mapping[str, Any], Mapping[str, Any] | None]:
    if not isinstance(packet, Mapping) or packet.get("schema_version") != 1 or packet.get("mode") != REVIEW_MODE:
        raise ValueError("review_packet_schema_or_mode_invalid")
    supplied = packet.get("human_review_packet_sha256")
    core = dict(packet)
    core.pop("human_review_packet_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("review_packet_hash_mismatch")
    scope = packet.get("exact_scope")
    if not isinstance(scope, Mapping) or packet.get("exact_scope_sha256") != _hash(scope):
        raise ValueError("review_packet_scope_hash_mismatch")
    if (
        scope.get("method") != "GET"
        or scope.get("required_environment") != "production"
        or scope.get("request_count") != 1
        or scope.get("credentials_allowed") is not False
        or scope.get("action_enabled") is not False
    ):
        raise ValueError("review_packet_scope_invalid")
    inert_false = (
        "authorization_granted", "real_user_authorization_present", "transport_enabled", "network_capable",
        "network_calls_performed", "credentials_used", "action_enabled", "money_or_value_movement_enabled",
        "review_packet_is_authorization", "review_packet_is_execution_token",
    )
    if any(packet.get(k) is not False for k in inert_false):
        raise ValueError("review_packet_not_inert")
    _parse_utc(packet.get("reviewed_at_utc"))
    _parse_utc(packet.get("expires_at_utc"))
    return supplied, scope, packet.get("source_compliance_evidence")


def _validate_replay(replay: Mapping[str, Any]) -> tuple[str, Mapping[str, Any] | None]:
    if not isinstance(replay, Mapping) or replay.get("schema_version") != 1 or replay.get("mode") != REPLAY_MODE:
        raise ValueError("source_compliance_replay_schema_or_mode_invalid")
    supplied = replay.get("source_compliance_replay_sha256")
    core = dict(replay)
    core.pop("source_compliance_replay_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("source_compliance_replay_hash_mismatch")
    if any(replay.get(k) is not False for k in ("network_calls_performed", "transport_enabled", "authorization_granted")):
        raise ValueError("source_compliance_replay_not_inert")
    _parse_utc(replay.get("replayed_at_utc"))
    evidence = replay.get("i045_evidence")
    if replay.get("replay_state") == "reproducible_evidence_verified":
        if replay.get("reproducible") is not True or replay.get("blockers") != [] or not isinstance(evidence, Mapping):
            raise ValueError("verified_replay_contract_invalid")
    else:
        if replay.get("reproducible") is True or evidence is not None:
            raise ValueError("blocked_replay_contract_invalid")
    return supplied, evidence


def bridge_reproducible_compliance_to_human_review(
    review_packet: Mapping[str, Any],
    source_compliance_replay: Mapping[str, Any],
    *,
    bridged_at_utc: str,
) -> dict[str, Any]:
    """Require I046 reproducible replay before preserving I045 human-decision readiness."""
    packet_hash, scope, packet_evidence = _validate_review_packet(review_packet)
    replay_hash, replay_evidence = _validate_replay(source_compliance_replay)
    bridged_at = _parse_utc(bridged_at_utc)
    reviewed_at = _parse_utc(review_packet.get("reviewed_at_utc"))
    expires_at = _parse_utc(review_packet.get("expires_at_utc"))
    replayed_at = _parse_utc(source_compliance_replay.get("replayed_at_utc"))
    if bridged_at < reviewed_at or bridged_at < replayed_at:
        raise ValueError("bridge_time_precedes_inputs")

    blockers: list[str] = []
    if bridged_at >= expires_at:
        blockers.append("review_packet_expired")
    if review_packet.get("review_state") != "ready_for_human_decision" or review_packet.get("human_decision_requested") is not True:
        blockers.append("i045_review_not_ready")
    if source_compliance_replay.get("replay_state") != "reproducible_evidence_verified":
        blockers.append("reproducible_source_compliance_not_verified")
    if source_compliance_replay.get("provenance_class") != "reproducible_captured_content":
        blockers.append("source_compliance_provenance_not_captured")
    if replay_evidence is None:
        blockers.append("replay_i045_evidence_missing")
    elif packet_evidence != replay_evidence:
        blockers.append("replay_evidence_not_bound_to_i045_packet")
    if isinstance(replay_evidence, Mapping):
        if replay_evidence.get("source_url") != source_compliance_replay.get("source_url"):
            blockers.append("replay_source_url_binding_mismatch")

    ready = not blockers
    core = {
        "schema_version": 1,
        "mode": BRIDGE_MODE,
        "bridge_state": "ready_for_human_decision" if ready else "blocked_by_nonreproducible_or_unbound_evidence",
        "bridged_at_utc": bridged_at_utc,
        "expires_at_utc": review_packet.get("expires_at_utc"),
        "human_review_packet_sha256": packet_hash,
        "source_compliance_replay_sha256": replay_hash,
        "real_transport_proposal_sha256": review_packet.get("real_transport_proposal_sha256"),
        "exact_scope_sha256": review_packet.get("exact_scope_sha256"),
        "exact_scope": dict(scope),
        "source_content_sha256": source_compliance_replay.get("source_content_sha256"),
        "source_url": source_compliance_replay.get("source_url"),
        "source_compliance_evidence_sha256": replay_evidence.get("evidence_sha256") if isinstance(replay_evidence, Mapping) else None,
        "blockers": list(dict.fromkeys(blockers)),
        "human_decision_requested": ready,
        "reproducible_evidence_required": True,
        "manual_metadata_sufficient": False,
        "authorization_granted": False,
        "real_user_authorization_present": False,
        "transport_enabled": False,
        "network_capable": False,
        "network_calls_performed": False,
        "credentials_used": False,
        "action_enabled": False,
        "money_or_value_movement_enabled": False,
        "bridge_is_authorization": False,
        "bridge_is_execution_token": False,
    }
    return {**core, "compliance_review_bridge_sha256": _hash(core)}
