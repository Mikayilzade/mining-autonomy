#!/usr/bin/env python3
"""I098 network-inert fresh execution-evidence contract for the I096 one-shot target."""
from __future__ import annotations

import hashlib
import ipaddress
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping

EXPECTED_PACKET_SHA256 = "0519c67da402e5c9fe04f0768cb203eedf7666bbe0879f1435856d4c99f86f56"
EXPECTED_SCOPE_SHA256 = "df0d8cd3f7f2b833d5fdd7d2f992c2bb52c722422bd1d23046c6ea3617788a9e"
EXPECTED_HOST = "payanagent.com"
EXPECTED_PATH_QUERY = "/api/v1/requests?status=open&limit=1"
EXPECTED_METHOD = "GET"
POLICY_MAX_AGE_SECONDS = 21600
DNS_MAX_AGE_SECONDS = 300
TLS_MAX_AGE_SECONDS = 300
REBIND_MAX_AGE_SECONDS = 60


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


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


def _sha(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _public_ip(value: str) -> bool:
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        return False
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_unspecified or ip.is_reserved)


def _base_errors(artifact: Mapping[str, Any], evidence_type: str) -> list[str]:
    errors: list[str] = []
    if artifact.get("schema_version") != 1:
        errors.append(f"{evidence_type}.schema_version must be 1")
    if artifact.get("evidence_type") != evidence_type:
        errors.append(f"{evidence_type}.evidence_type mismatch")
    if artifact.get("bound_packet_sha256") != EXPECTED_PACKET_SHA256:
        errors.append(f"{evidence_type} not bound to exact I096 packet")
    if artifact.get("bound_scope_sha256") != EXPECTED_SCOPE_SHA256:
        errors.append(f"{evidence_type} not bound to exact I096 scope")
    if artifact.get("hostname") != EXPECTED_HOST:
        errors.append(f"{evidence_type}.hostname drift")
    return errors


def _freshness_errors(artifact: Mapping[str, Any], *, now: datetime, max_age_seconds: int, label: str) -> list[str]:
    errors: list[str] = []
    observed = _parse_time(artifact.get("observed_at"))
    valid_until = _parse_time(artifact.get("valid_until"))
    if observed is None or observed > now:
        errors.append(f"{label}.observed_at missing/invalid/future")
        return errors
    if (now - observed).total_seconds() > max_age_seconds:
        errors.append(f"{label} stale by max-age policy")
    if valid_until is None or valid_until <= now:
        errors.append(f"{label}.valid_until missing/expired")
    if valid_until and (valid_until - observed).total_seconds() > max_age_seconds:
        errors.append(f"{label}.valid_until exceeds contract freshness window")
    return errors


def validate_policy(artifact: Mapping[str, Any], *, now: datetime) -> list[str]:
    errors = _base_errors(artifact, "policy_tos")
    errors += _freshness_errors(artifact, now=now, max_age_seconds=POLICY_MAX_AGE_SECONDS, label="policy_tos")
    if artifact.get("source_kind") != "official_public_primary_source":
        errors.append("policy_tos.source_kind must be official_public_primary_source")
    if not isinstance(artifact.get("source_url"), str) or not artifact.get("source_url", "").startswith("https://"):
        errors.append("policy_tos.source_url must be HTTPS")
    if not _sha(artifact.get("content_sha256")):
        errors.append("policy_tos.content_sha256 missing/invalid")
    if artifact.get("anonymous_read_only_get_permitted") is not True:
        errors.append("policy_tos does not affirm exact anonymous read-only observation")
    if artifact.get("automation_prohibited_for_exact_observation") is not False:
        errors.append("policy_tos automation prohibition unresolved")
    if artifact.get("credentials_required") is not False:
        errors.append("policy_tos says credentials required/unknown")
    if artifact.get("value_movement_required") is not False:
        errors.append("policy_tos says value movement required/unknown")
    return errors


def validate_dns(artifact: Mapping[str, Any], *, now: datetime) -> list[str]:
    errors = _base_errors(artifact, "dns_resolution")
    errors += _freshness_errors(artifact, now=now, max_age_seconds=DNS_MAX_AGE_SECONDS, label="dns_resolution")
    if artifact.get("resolver_mode") != "fresh_system_or_authorized_resolver":
        errors.append("dns_resolution.resolver_mode invalid")
    if not _sha(artifact.get("raw_answer_sha256")):
        errors.append("dns_resolution.raw_answer_sha256 missing/invalid")
    ttl = artifact.get("effective_ttl_seconds")
    if not isinstance(ttl, int) or ttl <= 0 or ttl > DNS_MAX_AGE_SECONDS:
        errors.append("dns_resolution.effective_ttl_seconds out of contract range")
    addresses = artifact.get("public_addresses")
    if not isinstance(addresses, list) or not addresses:
        errors.append("dns_resolution public address set missing")
    elif any(not isinstance(x, str) or not _public_ip(x) for x in addresses):
        errors.append("dns_resolution contains non-public/invalid address")
    elif len(set(addresses)) != len(addresses):
        errors.append("dns_resolution contains duplicate addresses")
    return errors


def validate_tls(artifact: Mapping[str, Any], *, now: datetime, dns_addresses: list[str]) -> list[str]:
    errors = _base_errors(artifact, "tls_transport")
    errors += _freshness_errors(artifact, now=now, max_age_seconds=TLS_MAX_AGE_SECONDS, label="tls_transport")
    for field in ("peer_certificate_sha256", "certificate_chain_sha256", "handshake_transcript_sha256"):
        if not _sha(artifact.get(field)):
            errors.append(f"tls_transport.{field} missing/invalid")
    if artifact.get("certificate_hostname_valid") is not True:
        errors.append("tls_transport hostname validation did not pass")
    if artifact.get("certificate_time_valid") is not True:
        errors.append("tls_transport certificate time validation did not pass")
    if artifact.get("tls_version") not in ("TLSv1.2", "TLSv1.3"):
        errors.append("tls_transport TLS version below contract floor")
    connected = artifact.get("connected_ip")
    if connected not in dns_addresses:
        errors.append("tls_transport connected_ip not in fresh DNS pin set")
    return errors


def validate_rebinding(artifact: Mapping[str, Any], *, now: datetime, dns_addresses: list[str]) -> list[str]:
    errors = _base_errors(artifact, "anti_rebinding")
    errors += _freshness_errors(artifact, now=now, max_age_seconds=REBIND_MAX_AGE_SECONDS, label="anti_rebinding")
    if artifact.get("performed_immediately_before_request") is not True:
        errors.append("anti_rebinding must be performed immediately before request")
    addresses = artifact.get("revalidated_public_addresses")
    if not isinstance(addresses, list) or sorted(addresses) != sorted(dns_addresses):
        errors.append("anti_rebinding address set differs from pinned DNS set")
    if not _sha(artifact.get("revalidation_sha256")):
        errors.append("anti_rebinding.revalidation_sha256 missing/invalid")
    return errors


def validate_bundle(bundle: Mapping[str, Any], *, now: datetime | None = None) -> dict[str, Any]:
    current = now or datetime.now(timezone.utc)
    errors: list[str] = []
    if bundle.get("schema_version") != 1 or bundle.get("artifact_type") != "i098_fresh_execution_evidence_bundle":
        errors.append("bundle identity/schema invalid")
    if bundle.get("bound_packet_sha256") != EXPECTED_PACKET_SHA256:
        errors.append("bundle not bound to exact I096 packet")
    if bundle.get("bound_scope_sha256") != EXPECTED_SCOPE_SHA256:
        errors.append("bundle not bound to exact I096 scope")
    if bundle.get("method") != EXPECTED_METHOD or bundle.get("hostname") != EXPECTED_HOST or bundle.get("path_query") != EXPECTED_PATH_QUERY:
        errors.append("bundle exact request target drift")
    if bundle.get("request_count") != 1:
        errors.append("bundle request_count must be exactly one")
    if bundle.get("credentials_allowed") is not False or bundle.get("value_movement_allowed") is not False:
        errors.append("bundle safety widening")

    policy = bundle.get("policy_tos") if isinstance(bundle.get("policy_tos"), Mapping) else {}
    dns = bundle.get("dns_resolution") if isinstance(bundle.get("dns_resolution"), Mapping) else {}
    tls = bundle.get("tls_transport") if isinstance(bundle.get("tls_transport"), Mapping) else {}
    rebinding = bundle.get("anti_rebinding") if isinstance(bundle.get("anti_rebinding"), Mapping) else {}
    errors += validate_policy(policy, now=current)
    errors += validate_dns(dns, now=current)
    dns_addresses = list(dns.get("public_addresses", [])) if isinstance(dns.get("public_addresses"), list) else []
    errors += validate_tls(tls, now=current, dns_addresses=dns_addresses)
    errors += validate_rebinding(rebinding, now=current, dns_addresses=dns_addresses)

    declared_hashes = bundle.get("component_sha256")
    if not isinstance(declared_hashes, Mapping):
        errors.append("bundle.component_sha256 missing")
    else:
        for name, artifact in (("policy_tos", policy), ("dns_resolution", dns), ("tls_transport", tls), ("anti_rebinding", rebinding)):
            if declared_hashes.get(name) != canonical_sha256(artifact):
                errors.append(f"bundle component hash mismatch: {name}")

    valid_until_values = [_parse_time(x.get("valid_until")) for x in (policy, dns, tls, rebinding)]
    effective_valid_until = None if any(x is None for x in valid_until_values) else min(x for x in valid_until_values if x is not None)
    if effective_valid_until is None or _parse_time(bundle.get("valid_until")) != effective_valid_until:
        errors.append("bundle.valid_until must equal earliest component expiry")

    pins = bundle.get("pinned_public_addresses")
    if not isinstance(pins, list) or sorted(pins) != sorted(dns_addresses):
        errors.append("bundle pin set must equal fresh DNS public address set")
    if bundle.get("anti_rebinding_revalidation_required") is not True:
        errors.append("bundle must require anti-rebinding revalidation")
    if bundle.get("network_capable") is not False or bundle.get("execution_token") is not False:
        errors.append("I098 bundle must remain network-inert/non-token")

    return {
        "schema_version": 1,
        "mode": "i098_fresh_execution_evidence_contract",
        "network_capable": False,
        "execution_token": False,
        "contract_valid": not errors,
        "ready_for_network_invocation": False,
        "errors": errors,
        "note": "A valid evidence bundle still requires separate explicit user authorization bound to the I096 packet/scope and a later single-use executor gate.",
    }


def contract_spec() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "artifact_type": "i098_fresh_execution_evidence_contract",
        "network_capable": False,
        "execution_token": False,
        "bound_packet_sha256": EXPECTED_PACKET_SHA256,
        "bound_scope_sha256": EXPECTED_SCOPE_SHA256,
        "exact_request": {"method": EXPECTED_METHOD, "hostname": EXPECTED_HOST, "path_query": EXPECTED_PATH_QUERY, "request_count": 1},
        "freshness_windows_seconds": {"policy_tos": POLICY_MAX_AGE_SECONDS, "dns_resolution": DNS_MAX_AGE_SECONDS, "tls_transport": TLS_MAX_AGE_SECONDS, "anti_rebinding": REBIND_MAX_AGE_SECONDS},
        "required_components": ["policy_tos", "dns_resolution", "tls_transport", "anti_rebinding"],
        "consumption_rules": [
            "all components bind exact I096 packet and scope hashes",
            "all component hashes are recomputed canonically before use",
            "effective expiry is earliest component valid_until",
            "DNS pins contain public addresses only",
            "TLS connected IP must be inside fresh DNS pin set",
            "anti-rebinding revalidation must reproduce the same pin set immediately before the one GET",
            "credentials and value movement remain forbidden",
            "bundle never authorizes execution by itself"
        ]
    }


def _self_test() -> None:
    now = datetime(2026, 8, 22, 16, 30, tzinfo=timezone.utc)
    def ts(delta: int) -> str:
        return (now + timedelta(seconds=delta)).isoformat().replace("+00:00", "Z")
    base = {"schema_version": 1, "bound_packet_sha256": EXPECTED_PACKET_SHA256, "bound_scope_sha256": EXPECTED_SCOPE_SHA256, "hostname": EXPECTED_HOST}
    policy = {**base, "evidence_type": "policy_tos", "observed_at": ts(-10), "valid_until": ts(3600), "source_kind": "official_public_primary_source", "source_url": "https://example.invalid/terms", "content_sha256": "1"*64, "anonymous_read_only_get_permitted": True, "automation_prohibited_for_exact_observation": False, "credentials_required": False, "value_movement_required": False}
    dns = {**base, "evidence_type": "dns_resolution", "observed_at": ts(-10), "valid_until": ts(120), "resolver_mode": "fresh_system_or_authorized_resolver", "raw_answer_sha256": "2"*64, "effective_ttl_seconds": 120, "public_addresses": ["93.184.216.34"]}
    tls = {**base, "evidence_type": "tls_transport", "observed_at": ts(-5), "valid_until": ts(120), "peer_certificate_sha256": "3"*64, "certificate_chain_sha256": "4"*64, "handshake_transcript_sha256": "5"*64, "certificate_hostname_valid": True, "certificate_time_valid": True, "tls_version": "TLSv1.3", "connected_ip": "93.184.216.34"}
    rebinding = {**base, "evidence_type": "anti_rebinding", "observed_at": ts(-1), "valid_until": ts(30), "performed_immediately_before_request": True, "revalidated_public_addresses": ["93.184.216.34"], "revalidation_sha256": "6"*64}
    bundle = {"schema_version": 1, "artifact_type": "i098_fresh_execution_evidence_bundle", "bound_packet_sha256": EXPECTED_PACKET_SHA256, "bound_scope_sha256": EXPECTED_SCOPE_SHA256, "method": EXPECTED_METHOD, "hostname": EXPECTED_HOST, "path_query": EXPECTED_PATH_QUERY, "request_count": 1, "credentials_allowed": False, "value_movement_allowed": False, "policy_tos": policy, "dns_resolution": dns, "tls_transport": tls, "anti_rebinding": rebinding, "component_sha256": {"policy_tos": canonical_sha256(policy), "dns_resolution": canonical_sha256(dns), "tls_transport": canonical_sha256(tls), "anti_rebinding": canonical_sha256(rebinding)}, "valid_until": ts(30), "pinned_public_addresses": ["93.184.216.34"], "anti_rebinding_revalidation_required": True, "network_capable": False, "execution_token": False}
    result = validate_bundle(bundle, now=now)
    assert result["contract_valid"], result
    drifted = json.loads(json.dumps(bundle)); drifted["path_query"] = "/api/v1/requests?status=open&limit=2"
    assert not validate_bundle(drifted, now=now)["contract_valid"]
    private_pin = json.loads(json.dumps(bundle)); private_pin["dns_resolution"]["public_addresses"] = ["127.0.0.1"]
    private_pin["component_sha256"]["dns_resolution"] = canonical_sha256(private_pin["dns_resolution"])
    assert not validate_bundle(private_pin, now=now)["contract_valid"]
    print("I098 self-test PASS")


if __name__ == "__main__":
    _self_test()
    print(json.dumps(contract_spec(), indent=2, sort_keys=True))
