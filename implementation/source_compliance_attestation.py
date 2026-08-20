"""Deterministic offline attestation/replay for I045 source-compliance evidence (I046).

No network access is implemented. Captured source bytes must be supplied by the caller.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping
from urllib.parse import urlparse

ATTESTATION_MODE = "deterministic_offline_source_compliance_evidence_attestation"
REPLAY_MODE = "deterministic_offline_source_compliance_evidence_replay"
ALLOWED_EVIDENCE_CLASSES = {"first_party_terms", "first_party_docs", "first_party_public_access_policy"}


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _content_hash(content: str | bytes) -> str:
    data = content.encode("utf-8") if isinstance(content, str) else content
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("source_content_must_be_text_or_bytes")
    return sha256(bytes(data)).hexdigest()


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


def _validate_i045_evidence(evidence: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    if not isinstance(evidence, Mapping):
        raise ValueError("source_compliance_evidence_missing")
    required = (
        "platform", "source_url", "evidence_class", "checked_at_utc",
        "anonymous_read_only_observation_permitted", "credentials_required",
        "human_only_access_required", "evidence_sha256",
    )
    if any(k not in evidence for k in required):
        raise ValueError("source_compliance_evidence_fields_missing")
    supplied = evidence.get("evidence_sha256")
    core = dict(evidence); core.pop("evidence_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("source_compliance_evidence_hash_mismatch")
    parsed = urlparse(str(evidence.get("source_url")))
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("source_compliance_source_url_not_https")
    if evidence.get("evidence_class") not in ALLOWED_EVIDENCE_CLASSES:
        raise ValueError("source_compliance_evidence_class_not_first_party")
    _parse_utc(evidence.get("checked_at_utc"))
    normalized = {
        "platform": evidence.get("platform"),
        "source_url": evidence.get("source_url"),
        "evidence_class": evidence.get("evidence_class"),
        "checked_at_utc": evidence.get("checked_at_utc"),
        "anonymous_read_only_observation_permitted": evidence.get("anonymous_read_only_observation_permitted"),
        "credentials_required": evidence.get("credentials_required"),
        "human_only_access_required": evidence.get("human_only_access_required"),
        "evidence_sha256": supplied,
    }
    return supplied, normalized


def attest_source_compliance_evidence(
    evidence: Mapping[str, Any],
    *,
    attested_at_utc: str,
    retrieved_at_utc: str | None = None,
    source_content: str | bytes | None = None,
) -> dict[str, Any]:
    """Attest caller-supplied I045 metadata and optional captured first-party bytes."""
    evidence_hash, normalized = _validate_i045_evidence(evidence)
    attested_at = _parse_utc(attested_at_utc)
    checked_at = _parse_utc(normalized["checked_at_utc"])
    if checked_at > attested_at:
        raise ValueError("checked_after_attestation")

    if source_content is None:
        if retrieved_at_utc is not None:
            raise ValueError("retrieved_time_without_source_content")
        provenance = "manual_metadata_only"
        content_sha256 = None
    else:
        if retrieved_at_utc is None:
            raise ValueError("captured_content_requires_retrieved_time")
        retrieved_at = _parse_utc(retrieved_at_utc)
        if retrieved_at > attested_at:
            raise ValueError("retrieved_after_attestation")
        provenance = "reproducible_captured_content"
        content_sha256 = _content_hash(source_content)

    policy_conclusion = {
        "anonymous_read_only_observation_permitted": normalized["anonymous_read_only_observation_permitted"],
        "credentials_required": normalized["credentials_required"],
        "human_only_access_required": normalized["human_only_access_required"],
    }
    core = {
        "schema_version": 1,
        "mode": ATTESTATION_MODE,
        "platform": normalized["platform"],
        "source_url": normalized["source_url"],
        "evidence_class": normalized["evidence_class"],
        "checked_at_utc": normalized["checked_at_utc"],
        "retrieved_at_utc": retrieved_at_utc,
        "attested_at_utc": attested_at_utc,
        "evidence_sha256": evidence_hash,
        "source_content_sha256": content_sha256,
        "provenance_class": provenance,
        "policy_conclusion": policy_conclusion,
        "normalized_i045_evidence": normalized,
        "network_calls_performed": False,
        "transport_enabled": False,
        "authorization_granted": False,
        "source_content_embedded": False,
    }
    return {**core, "source_compliance_attestation_sha256": _hash(core)}


def replay_source_compliance_attestation(
    attestation: Mapping[str, Any],
    *,
    replayed_at_utc: str,
    source_content: str | bytes | None = None,
    max_age_hours: int = 168,
) -> dict[str, Any]:
    """Replay an attestation offline and expose I045 evidence only when reproducible."""
    if not isinstance(max_age_hours, int) or not 1 <= max_age_hours <= 720:
        raise ValueError("source_evidence_max_age_invalid")
    if not isinstance(attestation, Mapping) or attestation.get("schema_version") != 1 or attestation.get("mode") != ATTESTATION_MODE:
        raise ValueError("attestation_schema_or_mode_invalid")
    supplied = attestation.get("source_compliance_attestation_sha256")
    core = dict(attestation); core.pop("source_compliance_attestation_sha256", None)
    if not isinstance(supplied, str) or len(supplied) != 64 or _hash(core) != supplied:
        raise ValueError("attestation_hash_mismatch")
    if any(attestation.get(k) is not False for k in ("network_calls_performed", "transport_enabled", "authorization_granted", "source_content_embedded")):
        raise ValueError("attestation_not_inert")

    normalized = attestation.get("normalized_i045_evidence")
    evidence_hash, revalidated = _validate_i045_evidence(normalized)
    if evidence_hash != attestation.get("evidence_sha256"):
        raise ValueError("attestation_evidence_binding_mismatch")
    if revalidated["source_url"] != attestation.get("source_url") or revalidated["platform"] != attestation.get("platform"):
        raise ValueError("attestation_source_binding_mismatch")
    if attestation.get("policy_conclusion") != {
        "anonymous_read_only_observation_permitted": revalidated["anonymous_read_only_observation_permitted"],
        "credentials_required": revalidated["credentials_required"],
        "human_only_access_required": revalidated["human_only_access_required"],
    }:
        raise ValueError("attestation_policy_binding_mismatch")

    replayed_at = _parse_utc(replayed_at_utc)
    checked_at = _parse_utc(revalidated["checked_at_utc"])
    age = (replayed_at - checked_at).total_seconds()
    blockers: list[str] = []
    if age < 0:
        blockers.append("source_compliance_checked_at_in_future")
    elif age > max_age_hours * 3600:
        blockers.append("source_compliance_evidence_stale")
    if revalidated["anonymous_read_only_observation_permitted"] is not True:
        blockers.append("anonymous_read_only_observation_not_confirmed")
    if revalidated["credentials_required"] is not False:
        blockers.append("credentials_free_access_not_confirmed")
    if revalidated["human_only_access_required"] is not False:
        blockers.append("machine_read_only_access_not_confirmed")

    provenance = attestation.get("provenance_class")
    reproducible = False
    if provenance == "manual_metadata_only":
        blockers.append("source_compliance_evidence_not_reproducibly_captured")
    elif provenance == "reproducible_captured_content":
        retrieved = attestation.get("retrieved_at_utc")
        if retrieved is None:
            raise ValueError("captured_attestation_missing_retrieved_time")
        retrieved_at = _parse_utc(retrieved)
        if retrieved_at > _parse_utc(attestation.get("attested_at_utc")):
            raise ValueError("retrieved_after_attestation")
        if source_content is None:
            blockers.append("captured_source_content_required_for_replay")
        elif _content_hash(source_content) != attestation.get("source_content_sha256"):
            blockers.append("captured_source_content_digest_mismatch")
        else:
            reproducible = True
    else:
        raise ValueError("attestation_provenance_class_invalid")

    verified = reproducible and not blockers
    result_core = {
        "schema_version": 1,
        "mode": REPLAY_MODE,
        "replayed_at_utc": replayed_at_utc,
        "source_compliance_attestation_sha256": supplied,
        "source_url": revalidated["source_url"],
        "source_content_sha256": attestation.get("source_content_sha256"),
        "provenance_class": provenance,
        "replay_state": "reproducible_evidence_verified" if verified else "blocked_or_manual_only",
        "reproducible": verified,
        "blockers": list(dict.fromkeys(blockers)),
        "i045_evidence": revalidated if verified else None,
        "network_calls_performed": False,
        "transport_enabled": False,
        "authorization_granted": False,
    }
    return {**result_core, "source_compliance_replay_sha256": _hash(result_core)}
