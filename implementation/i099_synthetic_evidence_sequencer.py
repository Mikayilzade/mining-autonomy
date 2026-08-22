#!/usr/bin/env python3
"""I099 network-inert synthetic evidence acquisition/sequencing harness.

Proves the I098 acquisition order using synthetic fixtures only:
policy -> DNS/pins -> TLS-to-pin -> anti-rebinding -> final bundle
-> I097 compatibility projection.

No DNS, sockets, HTTP, credentials, authorization creation, or value movement.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping

import i097_offline_packet_verifier as i097
import i098_fresh_execution_evidence_contract as i098

ORDER = ("policy_tos", "dns_resolution", "tls_transport", "anti_rebinding")


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _base(evidence_type: str, *, observed_at: datetime, valid_until: datetime) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "evidence_type": evidence_type,
        "bound_packet_sha256": i098.EXPECTED_PACKET_SHA256,
        "bound_scope_sha256": i098.EXPECTED_SCOPE_SHA256,
        "hostname": i098.EXPECTED_HOST,
        "observed_at": _iso(observed_at),
        "valid_until": _iso(valid_until),
    }


def synthetic_policy(now: datetime) -> dict[str, Any]:
    return {
        **_base("policy_tos", observed_at=now - timedelta(seconds=10), valid_until=now + timedelta(hours=1)),
        "source_kind": "official_public_primary_source",
        "source_url": "https://synthetic.invalid/official-policy-fixture",
        "content_sha256": "1" * 64,
        "anonymous_read_only_get_permitted": True,
        "automation_prohibited_for_exact_observation": False,
        "credentials_required": False,
        "value_movement_required": False,
        "synthetic_fixture": True,
    }


def synthetic_dns(now: datetime) -> dict[str, Any]:
    return {
        **_base("dns_resolution", observed_at=now - timedelta(seconds=8), valid_until=now + timedelta(seconds=120)),
        "resolver_mode": "fresh_system_or_authorized_resolver",
        "raw_answer_sha256": "2" * 64,
        "effective_ttl_seconds": 120,
        "public_addresses": ["93.184.216.34"],
        "synthetic_fixture": True,
    }


def synthetic_tls(now: datetime) -> dict[str, Any]:
    return {
        **_base("tls_transport", observed_at=now - timedelta(seconds=5), valid_until=now + timedelta(seconds=120)),
        "peer_certificate_sha256": "3" * 64,
        "certificate_chain_sha256": "4" * 64,
        "handshake_transcript_sha256": "5" * 64,
        "certificate_hostname_valid": True,
        "certificate_time_valid": True,
        "tls_version": "TLSv1.3",
        "connected_ip": "93.184.216.34",
        "synthetic_fixture": True,
    }


def synthetic_rebinding(now: datetime) -> dict[str, Any]:
    return {
        **_base("anti_rebinding", observed_at=now - timedelta(seconds=1), valid_until=now + timedelta(seconds=30)),
        "performed_immediately_before_request": True,
        "revalidated_public_addresses": ["93.184.216.34"],
        "revalidation_sha256": "6" * 64,
        "synthetic_fixture": True,
    }


@dataclass
class SyntheticSequencer:
    now: datetime
    components: dict[str, dict[str, Any]] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)

    @property
    def expected_next(self) -> str | None:
        index = len(self.components)
        return ORDER[index] if index < len(ORDER) else None

    def ingest(self, artifact: Mapping[str, Any]) -> bool:
        kind = artifact.get("evidence_type")
        expected = self.expected_next
        if kind != expected:
            self.blocked_reasons.append(f"sequence violation: expected {expected}, got {kind}")
            self.events.append({"event": "reject", "expected": expected, "received": kind})
            return False

        candidate = dict(artifact)
        if kind == "policy_tos":
            errors = i098.validate_policy(candidate, now=self.now)
        elif kind == "dns_resolution":
            errors = i098.validate_dns(candidate, now=self.now)
        elif kind == "tls_transport":
            dns_addresses = list(self.components["dns_resolution"]["public_addresses"])
            errors = i098.validate_tls(candidate, now=self.now, dns_addresses=dns_addresses)
        elif kind == "anti_rebinding":
            dns_addresses = list(self.components["dns_resolution"]["public_addresses"])
            errors = i098.validate_rebinding(candidate, now=self.now, dns_addresses=dns_addresses)
        else:
            errors = [f"unknown evidence type: {kind}"]

        if errors:
            self.blocked_reasons.extend(errors)
            self.events.append({"event": "reject", "expected": expected, "received": kind, "errors": errors})
            return False

        self.components[kind] = candidate
        self.events.append({"event": "accept", "sequence_index": len(self.components), "evidence_type": kind})
        return True

    def finalize_bundle(self) -> tuple[dict[str, Any] | None, dict[str, Any]]:
        missing = [kind for kind in ORDER if kind not in self.components]
        if missing:
            return None, {
                "result": "BLOCKED",
                "network_capable": False,
                "execution_token": False,
                "missing_components": missing,
                "errors": [f"cannot finalize before complete ordered sequence: {', '.join(missing)}"],
            }

        policy = self.components["policy_tos"]
        dns = self.components["dns_resolution"]
        tls = self.components["tls_transport"]
        rebinding = self.components["anti_rebinding"]
        expiry_values = [i098._parse_time(x["valid_until"]) for x in (policy, dns, tls, rebinding)]
        if any(x is None for x in expiry_values):
            return None, {"result": "BLOCKED", "errors": ["component expiry invalid"]}
        valid_until = min(x for x in expiry_values if x is not None)
        bundle = {
            "schema_version": 1,
            "artifact_type": "i098_fresh_execution_evidence_bundle",
            "bound_packet_sha256": i098.EXPECTED_PACKET_SHA256,
            "bound_scope_sha256": i098.EXPECTED_SCOPE_SHA256,
            "method": i098.EXPECTED_METHOD,
            "hostname": i098.EXPECTED_HOST,
            "path_query": i098.EXPECTED_PATH_QUERY,
            "request_count": 1,
            "credentials_allowed": False,
            "value_movement_allowed": False,
            "policy_tos": policy,
            "dns_resolution": dns,
            "tls_transport": tls,
            "anti_rebinding": rebinding,
            "component_sha256": {
                "policy_tos": i098.canonical_sha256(policy),
                "dns_resolution": i098.canonical_sha256(dns),
                "tls_transport": i098.canonical_sha256(tls),
                "anti_rebinding": i098.canonical_sha256(rebinding),
            },
            "valid_until": _iso(valid_until),
            "pinned_public_addresses": list(dns["public_addresses"]),
            "anti_rebinding_revalidation_required": True,
            "network_capable": False,
            "execution_token": False,
            "synthetic_fixture": True,
        }
        return bundle, i098.validate_bundle(bundle, now=self.now)


def project_i097_compatibility(bundle: Mapping[str, Any]) -> dict[str, Any]:
    observed_values = [i098._parse_time(bundle[name]["observed_at"]) for name in ORDER]
    if any(x is None for x in observed_values):
        raise ValueError("bundle observed_at missing")
    observed = max(x for x in observed_values if x is not None)
    hashes = bundle["component_sha256"]
    return {
        "schema_version": 1,
        "artifact_type": "i099_i097_execution_evidence_projection",
        "bound_packet_sha256": bundle["bound_packet_sha256"],
        "bound_scope_sha256": bundle["bound_scope_sha256"],
        "policy_tos_evidence_sha256": hashes["policy_tos"],
        "dns_resolution_evidence_sha256": hashes["dns_resolution"],
        "tls_transport_evidence_sha256": hashes["tls_transport"],
        "pinned_public_addresses": list(bundle["pinned_public_addresses"]),
        "observed_at": _iso(observed),
        "valid_until": bundle["valid_until"],
        "anti_rebinding_revalidation_required": True,
        "source_bundle_sha256": i098.canonical_sha256(bundle),
        "network_capable": False,
        "execution_token": False,
        "synthetic_fixture": True,
    }


def build_valid_synthetic_chain(now: datetime) -> tuple[SyntheticSequencer, dict[str, Any], dict[str, Any]]:
    seq = SyntheticSequencer(now=now)
    for artifact in (synthetic_policy(now), synthetic_dns(now), synthetic_tls(now), synthetic_rebinding(now)):
        assert seq.ingest(artifact), seq.blocked_reasons
    bundle, validation = seq.finalize_bundle()
    assert bundle is not None and validation["contract_valid"], validation
    return seq, bundle, project_i097_compatibility(bundle)


def run_self_test() -> dict[str, Any]:
    now = datetime(2026, 8, 22, 17, 0, tzinfo=timezone.utc)
    root = Path(__file__).resolve().parent
    packet = json.loads((root / "I096_FRESH_ONE_SHOT_REVIEW_PACKET.json").read_text(encoding="utf-8"))

    _, bundle, projection = build_valid_synthetic_chain(now)
    assert i097.verify_execution_evidence(projection, now=now) == []
    compatibility = i097.verify_bundle(packet, authorization=None, execution_evidence=projection, now=now)
    assert compatibility["packet_integrity_pass"] is True
    assert compatibility["execution_evidence_pass"] is True
    assert compatibility["authorization_pass"] is False
    assert compatibility["result"] == "BLOCKED"

    omitted = SyntheticSequencer(now=now)
    assert omitted.ingest(synthetic_policy(now))
    assert omitted.ingest(synthetic_dns(now))
    assert omitted.ingest(synthetic_tls(now))
    omitted_bundle, omitted_result = omitted.finalize_bundle()
    assert omitted_bundle is None and "anti_rebinding" in omitted_result["missing_components"]

    reordered = SyntheticSequencer(now=now)
    assert reordered.ingest(synthetic_policy(now))
    assert reordered.ingest(synthetic_tls(now)) is False
    assert reordered.expected_next == "dns_resolution"

    stale = synthetic_policy(now)
    stale["observed_at"] = _iso(now - timedelta(hours=7))
    stale["valid_until"] = _iso(now + timedelta(minutes=1))
    stale_seq = SyntheticSequencer(now=now)
    assert stale_seq.ingest(stale) is False

    tls_drift_seq = SyntheticSequencer(now=now)
    assert tls_drift_seq.ingest(synthetic_policy(now))
    assert tls_drift_seq.ingest(synthetic_dns(now))
    tls_drift = synthetic_tls(now)
    tls_drift["connected_ip"] = "1.1.1.1"
    assert tls_drift_seq.ingest(tls_drift) is False

    drifted_bundle = json.loads(json.dumps(bundle))
    drifted_bundle["path_query"] = "/api/v1/requests?status=open&limit=2"
    assert i098.validate_bundle(drifted_bundle, now=now)["contract_valid"] is False

    rebind_seq = SyntheticSequencer(now=now)
    assert rebind_seq.ingest(synthetic_policy(now))
    assert rebind_seq.ingest(synthetic_dns(now))
    assert rebind_seq.ingest(synthetic_tls(now))
    rebind_drift = synthetic_rebinding(now)
    rebind_drift["revalidated_public_addresses"] = ["1.1.1.1"]
    assert rebind_seq.ingest(rebind_drift) is False

    return {
        "schema_version": 1,
        "run": "I099",
        "result": "PASS_SYNTHETIC_SEQUENCING_ONLY",
        "network_capable": False,
        "execution_token": False,
        "authorization_manufactured": False,
        "valid_sequence": list(ORDER),
        "valid_bundle_sha256": i098.canonical_sha256(bundle),
        "i097_projection_sha256": i098.canonical_sha256(projection),
        "i097_packet_integrity_pass": compatibility["packet_integrity_pass"],
        "i097_execution_evidence_pass": compatibility["execution_evidence_pass"],
        "i097_authorization_pass": compatibility["authorization_pass"],
        "i097_final_result": compatibility["result"],
        "negative_cases_passed": [
            "omitted_component",
            "reordered_evidence",
            "stale_policy",
            "tls_connected_ip_outside_dns_pin_set",
            "exact_path_query_drift",
            "anti_rebinding_address_set_drift",
        ],
        "ready_for_network_invocation": False,
        "next_gate": "fresh real evidence acquisition and separate explicit user authorization remain required before the one-shot production GET",
    }


if __name__ == "__main__":
    result = run_self_test()
    print("I099 self-test PASS")
    print(json.dumps(result, indent=2, sort_keys=True))
