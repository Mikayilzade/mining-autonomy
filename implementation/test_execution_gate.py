from copy import deepcopy
import pytest

from execution_gate import execute_synthetic_read_only
from test_transport_preflight import preflight, auth


class FakeResolver:
    def __init__(self, addresses=("93.184.216.34",)):
        self.addresses = list(addresses)
        self.calls = []

    def resolve(self, *, host, port):
        self.calls.append((host, port))
        return list(self.addresses)


class FakeTransport:
    def __init__(self, response=None):
        self.response = response or {
            "status_code": 200,
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": b'{"ok":true}',
        }
        self.calls = []

    def get(self, *, url, headers, timeout_seconds):
        self.calls.append((url, dict(headers), timeout_seconds))
        return deepcopy(self.response)


def run(response=None, addresses=("93.184.216.34",), now="2026-08-20T01:05:00Z"):
    p = preflight()
    a = auth(p)
    r = FakeResolver(addresses)
    t = FakeTransport(response)
    result = execute_synthetic_read_only(
        p, a, resolver=r, transport=t, now_utc=now, max_response_bytes=1024
    )
    return p, a, r, t, result


def test_valid_synthetic_execution_emits_hash_bound_receipt():
    p, a, r, t, result = run()
    assert len(r.calls) == 1 and len(t.calls) == 1
    assert result["executed_request_count"] == 1
    assert result["synthetic_transport_only"] is True
    assert result["real_network_calls_performed"] is False
    receipt = result["response_receipts"][0]
    assert receipt["request_binding_sha256"] == p["transport_envelopes"][0]["request_binding_sha256"]
    assert receipt["content_type"] == "application/json"
    assert receipt["response_bytes"] == len(b'{"ok":true}')
    assert len(receipt["body_sha256"]) == 64
    assert len(receipt["response_receipt_sha256"]) == 64
    assert len(result["execution_receipt_sha256"]) == 64


def test_missing_authorization_cannot_invoke_dependencies():
    p = preflight()
    r = FakeResolver()
    t = FakeTransport()
    with pytest.raises(ValueError, match="execution_authorization_missing"):
        execute_synthetic_read_only(p, None, resolver=r, transport=t, now_utc="2026-08-20T01:05:00Z")
    assert r.calls == [] and t.calls == []


def test_mismatched_authorization_cannot_invoke_dependencies():
    p = preflight()
    a = auth(p)
    a["session_plan_sha256"] = "0" * 64
    r = FakeResolver()
    t = FakeTransport()
    with pytest.raises(ValueError, match="plan_hash_mismatch"):
        execute_synthetic_read_only(p, a, resolver=r, transport=t, now_utc="2026-08-20T01:05:00Z")
    assert r.calls == [] and t.calls == []


def test_expired_authorization_cannot_invoke_dependencies():
    p = preflight()
    a = auth(p)
    r = FakeResolver()
    t = FakeTransport()
    with pytest.raises(ValueError, match="execution_authorization_expired"):
        execute_synthetic_read_only(p, a, resolver=r, transport=t, now_utc="2026-08-20T01:10:01Z")
    assert r.calls == [] and t.calls == []


def test_non_global_dns_blocks_before_transport_get():
    p = preflight()
    a = auth(p)
    r = FakeResolver(("10.0.0.5",))
    t = FakeTransport()
    with pytest.raises(ValueError, match="dns_non_global_forbidden"):
        execute_synthetic_read_only(p, a, resolver=r, transport=t, now_utc="2026-08-20T01:05:00Z")
    assert len(r.calls) == 1 and t.calls == []


@pytest.mark.parametrize("status,headers", [
    (302, {"Content-Type": "application/json", "Location": "https://example.org/next"}),
    (200, {"Content-Type": "application/json", "Location": "https://example.org/next"}),
])
def test_redirects_are_rejected(status, headers):
    p = preflight()
    a = auth(p)
    r = FakeResolver()
    t = FakeTransport({"status_code": status, "headers": headers, "body": b"{}"})
    with pytest.raises(ValueError, match="execution_redirect_forbidden"):
        execute_synthetic_read_only(p, a, resolver=r, transport=t, now_utc="2026-08-20T01:05:00Z")
    assert len(t.calls) == 1


def test_response_size_limit_rejects_declared_and_actual_oversize():
    p = preflight()
    a = auth(p)
    r = FakeResolver()
    t = FakeTransport({
        "status_code": 200,
        "headers": {"Content-Type": "application/json", "Content-Length": "5000"},
        "body": b"{}",
    })
    with pytest.raises(ValueError, match="execution_response_too_large"):
        execute_synthetic_read_only(p, a, resolver=r, transport=t, now_utc="2026-08-20T01:05:00Z", max_response_bytes=1024)

    t = FakeTransport({
        "status_code": 200,
        "headers": {"Content-Type": "application/json"},
        "body": b"x" * 1025,
    })
    with pytest.raises(ValueError, match="execution_response_too_large"):
        execute_synthetic_read_only(p, a, resolver=FakeResolver(), transport=t, now_utc="2026-08-20T01:05:00Z", max_response_bytes=1024)


def test_content_type_allowlist_is_enforced():
    p = preflight()
    a = auth(p)
    t = FakeTransport({
        "status_code": 200,
        "headers": {"Content-Type": "text/html"},
        "body": b"<html></html>",
    })
    with pytest.raises(ValueError, match="execution_content_type_forbidden"):
        execute_synthetic_read_only(p, a, resolver=FakeResolver(), transport=t, now_utc="2026-08-20T01:05:00Z")


def test_request_binding_tamper_blocks_before_resolver_or_transport():
    p = preflight()
    p["transport_envelopes"][0]["source_url"] = "https://api.example.com/tampered"
    a = auth(p)
    r = FakeResolver()
    t = FakeTransport()
    with pytest.raises(ValueError, match="request_binding_hash_mismatch"):
        execute_synthetic_read_only(p, a, resolver=r, transport=t, now_utc="2026-08-20T01:05:00Z")
    assert r.calls == [] and t.calls == []
