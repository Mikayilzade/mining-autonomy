"""Deterministic offline bridge from I046 replay into I045 human review (I047).

The bridge has no network capability and never grants authorization. It accepts
only a hash-valid I046 replay and permits I045 to become human-decision-ready
only when that replay is reproducibly verified and exposes the exact bound
I045 evidence object.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

from transport_review_packet import build_real_transport_human_review_packet

REPLAY_MODE = "deterministic_offline_source_compliance_evidence_replay"
BRIDGE_MODE = "deterministic_offline_compliance_review_bridge"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _validate_replay(replay: Mapping[str, Any]) -> str:
    if not isinstance(replay, Mapping) or replay.get("schema_version") != 1 or replay.get("mode") != REPLAY_MODE:
        raise ValueError("replay_schema_or_mode_invalid")
    supplied = replay.get("source_compliance_replay_sha256")
    core = dict(replay)
    core.pop("source_compliance_replay_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("replay_hash_mismatch")
    if any(replay.get(k) is not False for k in ("network_calls_performed", "transport_enabled", "authorization_granted")):
        raise ValueError("replay_not_inert")
    return supplied


def bridge_reproducible_compliance_to_human_review(
    proposal: Mapping[str, Any],
    replay: Mapping[str, Any],
    *,
    reviewed_at_utc: str,
    max_source_evidence_age_hours: int = 168,
) -> dict[str, Any]:
    """Build I045 review state from I046 replay without widening any scope."""
    replay_hash = _validate_replay(replay)
    verified = (
        replay.get("replay_state") == "reproducible_evidence_verified"
        and replay.get("reproducible") is True
        and isinstance(replay.get("i045_evidence"), Mapping)
        and not replay.get("blockers")
    )

    # Manual-only/blocked replay is deliberately passed as no evidence. I045
    # therefore remains blocked rather than trusting caller-supplied metadata.
    evidence = replay.get("i045_evidence") if verified else None
    review = build_real_transport_human_review_packet(
        proposal,
        evidence,
        reviewed_at_utc=reviewed_at_utc,
        max_source_evidence_age_hours=max_source_evidence_age_hours,
    )

    if verified and review.get("review_state") != "ready_for_human_decision":
        raise ValueError("verified_replay_did_not_reach_expected_review_state")
    if not verified and review.get("review_state") == "ready_for_human_decision":
        raise ValueError("unverified_replay_reached_human_decision_ready_state")

    core = {
        "schema_version": 1,
        "mode": BRIDGE_MODE,
        "source_compliance_replay_sha256": replay_hash,
        "replay_state": replay.get("replay_state"),
        "reproducible_evidence_verified": verified,
        "human_review_packet_sha256": review.get("human_review_packet_sha256"),
        "real_transport_proposal_sha256": review.get("real_transport_proposal_sha256"),
        "exact_scope_sha256": review.get("exact_scope_sha256"),
        "review_state": review.get("review_state"),
        "human_decision_requested": review.get("human_decision_requested") is True,
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
        "human_review_packet": review,
    }
    return {**core, "compliance_review_bridge_sha256": _hash(core)}
