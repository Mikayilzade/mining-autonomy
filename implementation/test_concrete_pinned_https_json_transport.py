import gzip
from io import BytesIO
import ssl
import pytest

from concrete_pinned_https_json_transport import execute_concrete_pinned_https_json_transport as execute

def request(path="/api/opportunities", max_bytes=1024):
    return {"hostname":"example.com","pinned_addresses":["93.184.216.34"],"path":path,"scheme":"https","tls_required":True,"method":"GET","max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":max_bytes,"credentials_allowed":False,"action_enabled":False}

class FakeRaw:
    def __init__(self, peer="93.184.216.34"): self.peer=peer; self.closed=False
    def getpeername(self): return (self.peer,443)
    def close(self): self.closed=True

class FakeTLS(FakeRaw):
    def __init__(self, response, peer="93.184.216.34"): super().__init__(peer); self.response=response; self.sent=[]
    def sendall(self,b): self.sent.append(b)
    def makefile(self,_mode): return BytesIO(self.response)

class FakeConnector:
    def __init__(self, raw=None): self.raw=raw or FakeRaw(); self.calls=[]
    def connect(self, ip, port): self.calls.append((ip,port)); return self.raw
    def resolve(self,*_): raise AssertionError("DNS resolver must never be called")

class FakeTLSContext:
    check_hostname=True
    verify_mode=ssl.CERT_REQUIRED
    def __init__(self, response, peer="93.184.216.34"): self.response=response; self.peer=peer; self.server_names=[]; self.tls=None
    def wrap_socket(self, raw, server_hostname): self.server_names.append(server_hostname); self.tls=FakeTLS(self.response,self.peer); return self.tls

def response(body=b'{"opportunities":[]}', status=200, ctype="application/json", extra_headers=b""):
    return f"HTTP/1.1 {status} OK\r\nContent-Type: {ctype}\r\nContent-Length: {len(body)}\r\n".encode()+extra_headers+b"\r\n"+body

def test_success_uses_only_pinned_ip_and_sni_and_derives_metadata():
    c=FakeConnector(); t=FakeTLSContext(response()); out=execute(request(),connector=c,tls_context=t)
    assert c.calls==[("93.184.216.34",443)]; assert t.server_names==["example.com"]
    assert out["peer_ip"]=="93.184.216.34" and out["tls_server_name"]=="example.com"
    assert out["dns_reresolved_after_connect"] is False and out["adapter_metadata_derived_from_connection_state"] is True
    sent=t.tls.sent[0]; assert sent.startswith(b"GET /api/opportunities HTTP/1.1\r\n") and b"Host: example.com\r\n" in sent and b"Authorization:" not in sent

def test_exact_path_is_required_and_never_supplied_out_of_band():
    c=FakeConnector(); t=FakeTLSContext(response()); bad=request(); bad.pop("path")
    with pytest.raises(ValueError,match="exact_path_missing_or_invalid"): execute(bad,connector=c,tls_context=t)
    assert c.calls==[]

def test_connected_peer_must_equal_selected_pin_before_tls():
    c=FakeConnector(FakeRaw("8.8.8.8")); t=FakeTLSContext(response())
    with pytest.raises(ValueError,match="connected_peer_not_selected"): execute(request(),connector=c,tls_context=t)
    assert t.server_names==[]

def test_tls_peer_cannot_change_after_wrap():
    c=FakeConnector(); t=FakeTLSContext(response(),peer="8.8.8.8")
    with pytest.raises(ValueError,match="tls_peer_changed"): execute(request(),connector=c,tls_context=t)

def test_tls_context_must_verify_hostname_and_certificate():
    c=FakeConnector(); t=FakeTLSContext(response()); t.check_hostname=False
    with pytest.raises(ValueError,match="hostname_verification_not_enabled"): execute(request(),connector=c,tls_context=t)
    assert c.calls==[]

def test_redirect_response_is_rejected_without_following_second_request():
    c=FakeConnector(); t=FakeTLSContext(response(body=b"{}",status=302,extra_headers=b"Location: https://other.example/\r\n"))
    with pytest.raises(ValueError,match="redirect_response_forbidden"): execute(request(),connector=c,tls_context=t)
    assert c.calls==[("93.184.216.34",443)] and len(t.tls.sent)==1

def test_compressed_body_limit_is_enforced_while_reading():
    body=b'{"x":"'+b"a"*2000+b'"}'; c=FakeConnector(); t=FakeTLSContext(response(body=body))
    with pytest.raises(ValueError,match="compressed_response_over_limit"): execute(request(max_bytes=100),connector=c,tls_context=t)

def test_gzip_decompressed_limit_blocks_zip_bomb_shape():
    plain=b'{"x":"'+b"a"*2000+b'"}'; compressed=gzip.compress(plain)
    raw=f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Encoding: gzip\r\nContent-Length: {len(compressed)}\r\n\r\n".encode()+compressed
    c=FakeConnector(); t=FakeTLSContext(raw)
    with pytest.raises(ValueError,match="decompressed_response_over_limit"): execute(request(max_bytes=300),connector=c,tls_context=t)

def test_chunked_json_is_supported_with_bounded_wire_bytes():
    body=b'{"ok":true}'; raw=b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nTransfer-Encoding: chunked\r\n\r\n"+f"{len(body):X}\r\n".encode()+body+b"\r\n0\r\n\r\n"
    c=FakeConnector(); t=FakeTLSContext(raw); out=execute(request(),connector=c,tls_context=t)
    assert out["body_utf8"]=='{"ok":true}' and out["compressed_response_bytes"]==len(body)
