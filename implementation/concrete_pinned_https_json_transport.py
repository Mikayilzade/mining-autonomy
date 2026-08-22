from __future__ import annotations
import ipaddress, json, ssl, zlib
from typing import Any, Mapping, Protocol

MODE = "concrete_pinned_https_json_transport_boundary"
MAX_HEADER_BYTES = 32768
READ_CHUNK_BYTES = 16384

class Connector(Protocol):
    def connect(self, ip_address: str, port: int): ...

def _public_ip(value: Any) -> bool:
    try:
        a = ipaddress.ip_address(str(value))
        return a.is_global and not any((a.is_private,a.is_loopback,a.is_link_local,a.is_multicast,a.is_reserved,a.is_unspecified))
    except ValueError:
        return False

def _strict_request(request: Mapping[str, Any]):
    req = {"scheme":"https","tls_required":True,"method":"GET","max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"credentials_allowed":False,"action_enabled":False}
    for k,v in req.items():
        if request.get(k) != v: raise ValueError(f"request_spec_{k}_invalid")
    host=request.get("hostname")
    if not isinstance(host,str) or not host or any(c.isspace() for c in host): raise ValueError("request_spec_hostname_invalid")
    pins=request.get("pinned_addresses")
    if not isinstance(pins,list) or not pins or len({str(x) for x in pins})!=len(pins) or any(not _public_ip(x) for x in pins): raise ValueError("request_spec_pinned_addresses_invalid")
    path=request.get("path")
    if not isinstance(path,str) or not path.startswith("/") or "\r" in path or "\n" in path or "#" in path: raise ValueError("request_spec_exact_path_missing_or_invalid")
    maxb=request.get("max_response_bytes")
    if not isinstance(maxb,int) or isinstance(maxb,bool) or not 1<=maxb<=1048576: raise ValueError("request_spec_max_response_bytes_invalid")
    return host, sorted(str(x) for x in pins), path, maxb

def _peer_ip(sock):
    p=sock.getpeername()
    if not isinstance(p,tuple) or not p: raise ValueError("transport_peer_state_invalid")
    return str(p[0])

def _readline(stream,budget):
    line=stream.readline(MAX_HEADER_BYTES+1)
    if not isinstance(line,(bytes,bytearray)): raise ValueError("transport_http_header_read_invalid")
    budget[0]+=len(line)
    if len(line)>MAX_HEADER_BYTES or budget[0]>MAX_HEADER_BYTES: raise ValueError("transport_http_headers_over_limit")
    return bytes(line)

def _read_exact(stream,size,maxb):
    if size<0 or size>maxb: raise ValueError("transport_compressed_response_over_limit")
    out=bytearray()
    while len(out)<size:
        c=stream.read(min(READ_CHUNK_BYTES,size-len(out)))
        if not c: raise ValueError("transport_response_truncated")
        out.extend(c)
        if len(out)>maxb: raise ValueError("transport_compressed_response_over_limit")
    return bytes(out)

def _read_eof(stream,maxb):
    out=bytearray()
    while True:
        c=stream.read(READ_CHUNK_BYTES)
        if not c: return bytes(out)
        out.extend(c)
        if len(out)>maxb: raise ValueError("transport_compressed_response_over_limit")

def _read_chunked(stream,maxb):
    out=bytearray(); budget=[0]
    while True:
        line=_readline(stream,budget)
        if not line.endswith(b"\r\n"): raise ValueError("transport_chunk_header_invalid")
        try: n=int(line[:-2].split(b";",1)[0].strip(),16)
        except Exception as e: raise ValueError("transport_chunk_size_invalid") from e
        if n==0:
            while True:
                t=_readline(stream,budget)
                if t==b"\r\n": return bytes(out)
                if not t: raise ValueError("transport_chunk_trailer_invalid")
        if n<0 or len(out)+n>maxb: raise ValueError("transport_compressed_response_over_limit")
        out.extend(_read_exact(stream,n,maxb-len(out)))
        if stream.read(2)!=b"\r\n": raise ValueError("transport_chunk_terminator_invalid")

def _decompress(body,encoding,maxb):
    if encoding in ("","identity"):
        if len(body)>maxb: raise ValueError("transport_decompressed_response_over_limit")
        return body
    if encoding!="gzip": raise ValueError("transport_content_encoding_not_allowed")
    d=zlib.decompressobj(16+zlib.MAX_WBITS); out=bytearray()
    for i in range(0,len(body),READ_CHUNK_BYTES):
        out.extend(d.decompress(body[i:i+READ_CHUNK_BYTES], maxb+1-len(out)))
        if len(out)>maxb or d.unconsumed_tail: raise ValueError("transport_decompressed_response_over_limit")
    out.extend(d.flush(maxb+1-len(out)))
    if len(out)>maxb: raise ValueError("transport_decompressed_response_over_limit")
    return bytes(out)

def execute_concrete_pinned_https_json_transport(request: Mapping[str, Any], *, connector: Connector, tls_context: Any) -> dict[str,Any]:
    """One pinned HTTPS GET. This module bundles no live connector/resolver; tests inject offline doubles."""
    host,pins,path,maxb=_strict_request(request); chosen=pins[0]
    if getattr(tls_context,"check_hostname",None) is not True: raise ValueError("transport_tls_hostname_verification_not_enabled")
    if getattr(tls_context,"verify_mode",None) != ssl.CERT_REQUIRED: raise ValueError("transport_tls_certificate_verification_not_required")
    raw=connector.connect(chosen,443); tls=None; stream=None
    try:
        raw_peer=_peer_ip(raw)
        if raw_peer!=chosen or raw_peer not in pins or not _public_ip(raw_peer): raise ValueError("transport_connected_peer_not_selected_pinned_address")
        tls=tls_context.wrap_socket(raw,server_hostname=host)
        tls_peer=_peer_ip(tls)
        if tls_peer!=chosen or tls_peer!=raw_peer: raise ValueError("transport_tls_peer_changed_from_pinned_address")
        req=(f"GET {path} HTTP/1.1\r\nHost: {host}\r\nAccept: application/json\r\nAccept-Encoding: gzip\r\nConnection: close\r\nUser-Agent: mining-autonomy-readonly-observer/1\r\n\r\n").encode("ascii")
        tls.sendall(req)
        stream=tls.makefile("rb"); budget=[0]
        sl=_readline(stream,budget)
        if not sl.endswith(b"\r\n"): raise ValueError("transport_http_status_line_invalid")
        try: ver,st,_=sl[:-2].split(b" ",2); status=int(st)
        except Exception as e: raise ValueError("transport_http_status_line_invalid") from e
        if ver not in {b"HTTP/1.0",b"HTTP/1.1"} or not 100<=status<=599: raise ValueError("transport_http_status_invalid")
        if 300<=status<=399: raise ValueError("transport_redirect_response_forbidden")
        headers={}
        while True:
            line=_readline(stream,budget)
            if line==b"\r\n": break
            if not line or not line.endswith(b"\r\n") or b":" not in line: raise ValueError("transport_http_header_invalid")
            nb,vb=line[:-2].split(b":",1); name=nb.decode("ascii").strip().lower(); val=vb.decode("latin-1").strip()
            if not name or name in headers: raise ValueError("transport_duplicate_or_empty_header")
            headers[name]=val
        ctype=headers.get("content-type","").split(";",1)[0].strip().lower()
        if ctype!="application/json": raise ValueError("transport_content_type_not_json")
        te=headers.get("transfer-encoding","").strip().lower(); cl=headers.get("content-length")
        if te and te!="chunked": raise ValueError("transport_transfer_encoding_not_allowed")
        if te=="chunked":
            if cl is not None: raise ValueError("transport_ambiguous_length_headers")
            compressed=_read_chunked(stream,maxb)
        elif cl is not None:
            try: n=int(cl)
            except Exception as e: raise ValueError("transport_content_length_invalid") from e
            compressed=_read_exact(stream,n,maxb)
        else: compressed=_read_eof(stream,maxb)
        body=_decompress(compressed,headers.get("content-encoding","identity").strip().lower(),maxb)
        try: text=body.decode("utf-8"); json.loads(text)
        except UnicodeDecodeError as e: raise ValueError("transport_body_not_utf8") from e
        except json.JSONDecodeError as e: raise ValueError("transport_body_invalid_json") from e
        return {"mode":MODE,"network_requests_performed":1,"peer_ip":tls_peer,"tls_verified":True,"tls_server_name":host,"dns_reresolved_after_connect":False,"redirect_count":0,"status_code":status,"content_type":ctype,"compressed_response_bytes":len(compressed),"decompressed_response_bytes":len(body),"body_utf8":text,"selected_pinned_address":chosen,"request_path":path,"adapter_metadata_derived_from_connection_state":True,"live_connector_bundled":False,"credentials_used":False,"action_performed":False}
    finally:
        if stream is not None:
            try: stream.close()
            except Exception: pass
        target=tls if tls is not None else raw
        try: target.close()
        except Exception: pass
