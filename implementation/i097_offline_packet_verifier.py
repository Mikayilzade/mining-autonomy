#!/usr/bin/env python3
"""I097 fail-closed verifier for the exact I096 one-shot review packet.

Network-inert by construction: stdlib-only JSON/hash/time validation. This module
never resolves DNS, opens sockets, performs HTTP, reads credentials, or executes
market actions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

EXPECTED_PACKET_SHA256 = "0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56"
EXPECTED_SCOPE_SHA256 = "df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e"
EXPECTED_HOST = "payanagent.com"
EXPECTED_PATH_QUERY = "/api/v1/requests?status=open&limit=1"
EXPECTED_TARGET = f"https://{EXPECTED_HOST}{EXPECTED_PATH_QUERY}"
EXPECTED_ADAPTER = "payanagent_readonly_requests_v1"
EXPECTED_FINGERPRINT = "payanagent_public_open_requests_v1"


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _is_sha256(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def verify_packet(packet: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    scope = packet.get("exact_scope")
    if not isinstance(scope, Mapping):
        return ["packet.exact_scope missing or invalid"]

    actual_scope_hash = canonical_sha256(scope)
    if actual_scope_hash != packet.get("exact_scope_sha256"):
        errors.append("exact_scope hash mismatch")
    if actual_scope_hash != EXPECTED_SCOPE_SHA256:
        errors.append("exact_scope differs from I096 bound scope")

    unhashed = dict(packet)
    declared_packet_hash = unhashed.pop("i096_review_packet_sha256", None)
    actual_packet_hash = canonical_sha256(unhashed)
    if actual_packet_hash != declared_packet_hash:
        errors.append("review packet hash mismatch")
    if actual_packet_hash != EXPECTED_PACKET_SHA256:
        errors.append("review packet differs from I096 bound packet")

    exact_fields = {
        "scheme": "https",
        "hostname": EXPECTED_HOST,
        "path_query": EXPECTED_PATH_QUERY,
        "request_target": EXPECTED_TARGET,
        "adapter_id": EXPECTED_ADAPTER,
        "target_fingerprint": EXPECTED_FINGERPRINT,
    }
    for field, expected in exact_fields.items():
        if packet.get(field) != expected:
            errors.append(f"packet.{field} drift")

    scope_fields = {
        "method": "GET",
        "request_count": 1,
        "required_environment": "production",
        "credentials_allowed": False,
        "action_enabled": False,
        "target_fingerprint": EXPECTED_FINGERPRINT,
        "https_path_query": EXPECTED_PATH_QUERY,
    }
    for field, expected in scope_fields.items():
        if scope.get(field) != expected:
            errors.append(f"exact_scope.{field} drift")

    safety = packet.get("safety")
    if not isinstance(safety, Mapping):
        errors.append("packet.safety missing or invalid")
    else:
        must_be_false = (
            "network_enabled",
            "network_calls_performed",
            "credentials_allowed",
            "task_acceptance_enabled",
            "submission_enabled",
            "execution_enabled",
            "value_movement_enabled",
            "packet_is_execution_token",
        )
        for field in must_be_false:
            if safety.get(field) is not False:
                errors.append(f"safety.{field} must remain false")

    return errors


def verify_authorization(authorization: Mapping[str, Any] | None, *, now: datetime) -> list[str]:
    if authorization is None:
        return ["fresh explicit user authorization is absent"]
    errors: list[str] = []
    if authorization.get("explicit_user_authorization") is not True:
        errors.append("authorization is not explicitly affirmative")
    if authorization.get("authorized_packet_sha256") != EXPECTED_PACKET_SHA256:
        errors.append("authorization is not bound to exact I096 packet hash")
    if authorization.get("authorized_scope_sha256") != EXPECTED_SCOPE_SHA256:
        errors.append("authorization is not bound to exact I096 scope hash")
    if authorization.get("allowed_operation") != "ONE_ANONYMOUS_READ_ONLY_GET":
        errors.append("authorization operation is not exact one-shot read-only GET")
    if authorization.get("max_request_count") != 1:
        errors.append("authorization request count is not exactly one")
    if authorization.get("credentials_allowed") is not False:
        errors.append("authorization must forbid credentials")
    if authorization.get("value_movement_allowed") is not False:
        errors.append("authorization must forbid value movement")
    expires_at = _parse_time(authorization.get("expires_at"))
    if expires_at is None or expires_at <= now:
        errors.append("authorization is absent, malformed, or stale")
    if not authorization.get("authorization_id"):
        errors.append("authorization_id missing")
    return errors


def verify_execution_evidence(evidence: Mapping[str, Any] | None, *, now: datetime) -> list[str]:
    if evidence is None:
        return ["fresh policy/DNS/pinning/TLS transport evidence is absent"]
    errors: list[str] = []
    if evidence.get("bound_packet_sha256") != EXPECTED_PACKET_SHA256:
        errors.append("execution evidence not bound to exact I096 packet")
    if evidence.get("bound_scope_sha256") != EXPECTED_SCOPE_SHA256:
        errors.append("execution evidence not bound to exact I096 scope")

    for field in (
        "policy_tos_evidence_sha256",
        "dns_resolution_evidence_sha256",
        "tls_transport_evidence_sha256",
    ):
        if not _is_sha256(evidence.get(field)):
            errors.append(f"{field} missing or invalid")

    pins = evidence.get("pinned_public_addresses")
    if not isinstance(pins, list) or not pins or any(not isinstance(x, str) or not x.strip() for x in pins):
        errors.append("fresh pinned public address set missing")

    valid_until = _parse_time(evidence.get("valid_until"))
    observed_at = _parse_time(evidence.get("observed_at"))
    if observed_at is None or observed_at > now:
        errors.append("execution evidence observed_at missing/invalid")
    if valid_until is None or valid_until <= now:
        errors.append("execution evidence is absent, malformed, or stale")
    if evidence.get("anti_rebinding_revalidation_required") is not True:
        errors.append("anti-rebinding revalidation requirement missing")
    return errors


def verify_bundle(
    packet: Mapping[str, Any],
    authorization: Mapping[str, Any] | None = None,
    execution_evidence: Mapping[str, Any] | None = None,
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    packet_errors = verify_packet(packet)
    authorization_errors = verify_authorization(authorization, now=current)
    evidence_errors = verify_execution_evidence(execution_evidence, now=current)
    errors = packet_errors + authorization_errors + evidence_errors
    return {
        "schema_version": 1,
        "mode": "i097_offline_packet_verifier",
        "network_capable": False,
        "expected_packet_sha256": EXPECTED_PACKET_SHA256,
        "expected_scope_sha256": EXPECTED_SCOPE_SHA256,
        "packet_integrity_pass": not packet_errors,
        "authorization_pass": not authorization_errors,
        "execution_evidence_pass": not evidence_errors,
        "ready_for_network_invocation": False,
        "result": "PASS_OFFLINE_BINDING_ONLY" if not errors else "BLOCKED",
        "errors": errors,
        "note": "Even PASS_OFFLINE_BINDING_ONLY is not an execution token; network invocation remains outside this module.",
    }


def _load(path: str | None) -> Mapping[str, Any] | None:
    if path is None:
        return None
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _self_test() -> None:
    root = Path(__file__).resolve().parent
    packet = _load(str(root / "I096_FRESH_ONE_SHOT_REVIEW_PACKET.json"))
    assert packet is not None
    assert verify_packet(packet) == []
    blocked = verify_bundle(packet, now=datetime(2026, 8, 22, 16, 0, tzinfo=timezone.utc))
    assert blocked["result"] == "BLOCKED"
    assert blocked["packet_integrity_pass"] is True
    assert blocked["authorization_pass"] is False
    assert blocked["execution_evidence_pass"] is False

    tampered = json.loads(json.dumps(packet))
    tampered["path_query"] = "/api/v1/requests?status=open&limit=2"
    assert any("drift" in error or "hash" in error for error in verify_packet(tampered))

    scope_tampered = json.loads(json.dumps(packet))
    scope_tampered["exact_scope"]["request_count"] = 2
    assert verify_packet(scope_tampered)
    print("I097 self-test PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", default=str(Path(__file__).resolve().parent / "I096_FRESH_ONE_SHOT_REVIEW_PACKET.json"))
    parser.add_argument("--authorization")
    parser.add_argument("--execution-evidence")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        _self_test()
        return 0
    result = verify_bundle(_load(args.packet) or {}, _load(args.authorization), _load(args.execution_evidence))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["result"] == "PASS_OFFLINE_BINDING_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
