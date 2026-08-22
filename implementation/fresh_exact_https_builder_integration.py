from __future__ import annotations
from hashlib import sha256
import json
from typing import Any, Mapping
from exact_https_target_binding import BOUND_MODE, canonical_path_query

MODE = "deterministic_fresh_exact_https_builder_integration"

def _h(v: Any) -> str:
    return sha256(json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()

def _hash_ok(o: Mapping[str, Any], key: str) -> bool:
    c = dict(o); got = c.pop(key, None)
    return isinstance(got, str) and got == _h(c)

def _reseal(o: Mapping[str, Any], key: str) -> dict[str, Any]:
    c = dict(o); c.pop(key, None)
    return {**c, key: _h(c)}

def _binding_fields(binding: Mapping[str, Any]) -> tuple[str,str,str,str,str,dict[str,Any]]:
    if not _hash_ok(binding, "exact_https_target_binding_sha256") or binding.get("mode") != BOUND_MODE:
        raise ValueError("binding_invalid")
    pq = canonical_path_query(binding.get("path_query"))
    scope = binding.get("bound_exact_scope")
    if not isinstance(scope, Mapping) or _h(dict(scope)) != binding.get("bound_exact_scope_sha256"):
        raise ValueError("binding_scope_invalid")
    return (str(binding.get("hostname")), pq, str(binding.get("target_fingerprint")),
            str(binding.get("adapter_id")), str(binding.get("bound_exact_scope_sha256")), dict(scope))

def bind_i086_review_builder(builder: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    host,pq,target,adapter,scope_hash,scope = _binding_fields(binding)
    packet = builder.get("final_real_observation_review_packet")
    if not isinstance(packet, Mapping): raise ValueError("i086_packet_missing")
    if packet.get("target_fingerprint") != target or packet.get("adapter_id") != adapter or packet.get("hostname") != host:
        raise ValueError("i086_target_binding_mismatch")
    p = dict(packet)
    p["path_query"] = pq; p["exact_scope"] = scope; p["exact_scope_sha256"] = scope_hash
    p["userinfo_allowed"] = False; p["fragment_allowed"] = False
    p = _reseal(p, "final_real_observation_review_packet_sha256")
    out = dict(builder); out["final_real_observation_review_packet"] = p
    return _reseal(out, "final_real_observation_review_packet_builder_sha256")

def bind_i087_decision_verification(verification: Mapping[str, Any], bound_packet: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    _,pq,target,adapter,scope_hash,scope = _binding_fields(binding)
    auth = verification.get("final_real_observation_authorization")
    if not isinstance(auth, Mapping): raise ValueError("i087_authorization_missing")
    if auth.get("final_real_observation_review_packet_sha256") != bound_packet.get("final_real_observation_review_packet_sha256"):
        raise ValueError("i087_packet_hash_binding_mismatch")
    if auth.get("target_fingerprint") != target or auth.get("adapter_id") != adapter:
        raise ValueError("i087_target_binding_mismatch")
    a=dict(auth); a["path_query"]=pq; a["exact_scope"]=scope; a["exact_scope_sha256"]=scope_hash
    a["userinfo_allowed"]=False; a["fragment_allowed"]=False
    a=_reseal(a,"final_real_observation_authorization_sha256")
    out=dict(verification); out["final_real_observation_authorization"]=a
    return _reseal(out,"final_real_observation_decision_verification_sha256")

def bind_i088_consumption(i088: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    host,pq,target,adapter,scope_hash,scope = _binding_fields(binding)
    env=i088.get("real_observation_execution_envelope"); rec=i088.get("consumption_receipt")
    if not isinstance(env,Mapping) or not isinstance(rec,Mapping): raise ValueError("i088_artifacts_missing")
    for obj,name in ((env,"envelope"),(rec,"receipt")):
        if obj.get("target_fingerprint") != target or obj.get("adapter_id") != adapter or obj.get("exact_scope_sha256") not in {scope_hash, None}:
            raise ValueError(f"i088_{name}_binding_mismatch")
    e=dict(env); e["path_query"]=pq; e["hostname"]=host; e["exact_scope"]=scope; e["exact_scope_sha256"]=scope_hash
    e=_reseal(e,"final_real_observation_execution_envelope_sha256")
    r=dict(rec); r["path_query"]=pq; r["exact_scope_sha256"]=scope_hash
    r["final_real_observation_execution_envelope_sha256"]=e["final_real_observation_execution_envelope_sha256"]
    r=_reseal(r,"final_real_observation_consumption_receipt_sha256")
    out=dict(i088); out["real_observation_execution_envelope"]=e; out["consumption_receipt"]=r
    return _reseal(out,"final_real_observation_authorization_consumption_preflight_sha256")

def bind_adapter_manifest(manifest: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    host,pq,target,adapter,scope_hash,_ = _binding_fields(binding)
    if manifest.get("target_fingerprint") != target or manifest.get("adapter_id") != adapter or manifest.get("hostname") != host:
        raise ValueError("adapter_manifest_target_binding_mismatch")
    m=dict(manifest); m["path_query"]=pq; m["exact_scope_sha256"]=scope_hash
    m["userinfo_allowed"]=False; m["fragment_allowed"]=False
    return _reseal(m,"network_adapter_manifest_sha256")

def bind_i089_gate(i089: Mapping[str, Any], binding: Mapping[str, Any]) -> dict[str, Any]:
    host,pq,target,adapter,scope_hash,_ = _binding_fields(binding)
    gate=i089.get("invocation_gate")
    if not isinstance(gate,Mapping): raise ValueError("i089_gate_missing")
    req=gate.get("request_spec")
    if not isinstance(req,Mapping): raise ValueError("i089_request_spec_missing")
    for key,expected in (("hostname",host),("target_fingerprint",target),("adapter_id",adapter),("exact_scope_sha256",scope_hash)):
        if req.get(key) != expected: raise ValueError(f"i089_{key}_binding_mismatch")
    q=dict(req); q["path"]=pq
    g=dict(gate); g["request_spec"]=q
    g=_reseal(g,"final_network_adapter_invocation_gate_sha256")
    out=dict(i089); out["invocation_gate"]=g
    return _reseal(out,"final_network_adapter_invocation_gate_builder_sha256")

def validate_pre_i090(i089: Mapping[str, Any], binding: Mapping[str, Any]) -> list[str]:
    host,pq,target,adapter,scope_hash,_ = _binding_fields(binding)
    gate=i089.get("invocation_gate") if isinstance(i089,Mapping) else None
    req=gate.get("request_spec") if isinstance(gate,Mapping) else None
    if not isinstance(req,Mapping): return ["i089_request_spec_missing"]
    blockers=[]
    try:
        if canonical_path_query(req.get("path")) != pq: blockers.append("i090_path_query_drift")
    except ValueError: blockers.append("i090_path_query_not_canonical")
    for key,expected in (("hostname",host),("target_fingerprint",target),("adapter_id",adapter),("exact_scope_sha256",scope_hash)):
        if req.get(key) != expected: blockers.append(f"i090_{key}_drift")
    return list(dict.fromkeys(blockers))
