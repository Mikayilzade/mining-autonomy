from __future__ import annotations
from datetime import datetime,timedelta,timezone
from hashlib import sha256
import ipaddress,json
from typing import Any,Mapping

MODE="deterministic_final_real_observation_review_packet_builder"
PACKET_MODE="final_one_shot_real_observation_human_review_packet"
I084_MODE="deterministic_exact_real_read_only_invocation_authorization_consumption_preflight"
I085_MODE="deterministic_real_transport_safety_preflight"
I085_ENV="single_attempt_real_transport_safety_envelope"
MAX_BYTES=1048576

def _h(v:Any)->str:return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def _hok(o:Mapping[str,Any],k:str)->bool:
    x=dict(o);g=x.pop(k,None);return isinstance(g,str) and g==_h(x)
def _utc(v:str)->datetime:
    d=datetime.fromisoformat(v.replace("Z","+00:00"))
    if d.tzinfo is None or d.utcoffset()!=timedelta(0):raise ValueError
    return d.astimezone(timezone.utc)
def _sha(v:Any)->bool:
    try:return isinstance(v,str) and len(v)==64 and int(v,16)>=0
    except ValueError:return False
def _public(v:Any)->bool:
    try:a=ipaddress.ip_address(str(v));return a.is_global and not any((a.is_private,a.is_loopback,a.is_link_local,a.is_multicast,a.is_reserved,a.is_unspecified))
    except ValueError:return False
def _false(o:Mapping[str,Any],keys:tuple[str,...],p:str,b:list[str])->None:
    for k in keys:
        if o.get(k) is not False:b.append(f"{p}_{k}_must_be_false")

def build_final_real_observation_review_packet(i084:Mapping[str,Any],i085:Mapping[str,Any],*,requested_at:str,ttl_seconds:int=300)->dict[str,Any]:
    """Build an inert final human-review packet; never performs DNS/TLS/HTTP."""
    b:list[str]=[]
    try:now=_utc(requested_at)
    except Exception:now=None;b.append("requested_at_invalid_or_not_utc")
    if isinstance(ttl_seconds,bool) or not isinstance(ttl_seconds,int) or not 60<=ttl_seconds<=900:b.append("ttl_out_of_range")

    h84=i084.get("exact_real_read_only_invocation_consumption_preflight_sha256")
    if not _hok(i084,"exact_real_read_only_invocation_consumption_preflight_sha256"):b.append("i084_hash_invalid")
    if i084.get("mode")!=I084_MODE or i084.get("consumption_state")!="authorization_consumed_once_envelope_ready_no_network" or i084.get("blockers"):b.append("i084_not_ready")
    _false(i084,("network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","credentials_used","task_acceptance_enabled","submission_enabled","execution_enabled","value_movement_enabled","consumption_record_is_execution_token"),"i084",b)
    e=i084.get("real_read_only_invocation_envelope")
    r=i084.get("consumption_receipt")
    if not isinstance(e,Mapping):b.append("i084_envelope_missing");e={}
    if not isinstance(r,Mapping):b.append("i084_receipt_missing");r={}
    eh=e.get("exact_real_read_only_invocation_envelope_sha256");rh=r.get("exact_real_read_only_invocation_consumption_receipt_sha256")
    if not _hok(e,"exact_real_read_only_invocation_envelope_sha256"):b.append("i084_envelope_hash_invalid")
    if not _hok(r,"exact_real_read_only_invocation_consumption_receipt_sha256"):b.append("i084_receipt_hash_invalid")
    s=e.get("exact_scope") if isinstance(e.get("exact_scope"),Mapping) else {}
    sh=e.get("exact_scope_sha256");adapter=e.get("adapter_id");target=s.get("target_fingerprint")
    if not (s.get("method")=="GET" and s.get("request_count")==1 and s.get("required_environment")=="production" and s.get("credentials_allowed") is False and s.get("action_enabled") is False and isinstance(target,str) and target and sh==_h(dict(s))):b.append("i084_scope_invalid")
    source=(e.get("source_lineage") or {}).get("implementation_source_sha256") if isinstance(e.get("source_lineage"),Mapping) else None
    if not _sha(source):b.append("implementation_source_sha256_invalid")

    h85=i085.get("real_transport_safety_preflight_sha256")
    if not _hok(i085,"real_transport_safety_preflight_sha256"):b.append("i085_hash_invalid")
    if i085.get("mode")!=I085_MODE or i085.get("preflight_state")!="real_transport_safety_evidence_ready_no_network" or i085.get("blockers"):b.append("i085_not_ready")
    if i085.get("i084_consumption_preflight_sha256")!=h84 or i085.get("i084_invocation_envelope_sha256")!=eh:b.append("i085_i084_binding_invalid")
    _false(i085,("network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","credentials_used","task_acceptance_enabled","submission_enabled","execution_enabled","value_movement_enabled","preflight_record_is_execution_token"),"i085",b)

    se=i085.get("real_transport_safety_envelope")
    if not isinstance(se,Mapping):b.append("i085_safety_envelope_missing");se={}
    seh=se.get("real_transport_safety_envelope_sha256")
    if not _hok(se,"real_transport_safety_envelope_sha256"):b.append("i085_safety_envelope_hash_invalid")
    if se.get("mode")!=I085_ENV or se.get("safety_state")!="safety_prerequisites_attested_no_network":b.append("i085_safety_envelope_state_invalid")
    _false(se,("credentials_allowed","task_acceptance_enabled","submission_enabled","value_movement_enabled","network_capable_adapter_reachable","transport_enabled","network_enabled","network_calls_performed","safety_envelope_is_execution_token"),"i085_safety",b)
    expected={"i084_consumption_preflight_sha256":h84,"i084_invocation_envelope_sha256":eh,"i084_consumption_receipt_sha256":rh,"adapter_id":adapter,"target_fingerprint":target,"exact_scope_sha256":sh,"implementation_source_sha256":source}
    if any(se.get(k)!=v for k,v in expected.items()):b.append("i085_safety_binding_invalid")

    pd,dd,td=se.get("policy_evidence_sha256"),se.get("dns_evidence_sha256"),se.get("transport_contract_sha256")
    for k,v in (("policy_evidence_sha256",pd),("dns_evidence_sha256",dd),("transport_contract_sha256",td)):
        if not _sha(v) or i085.get(k)!=v:b.append(k+"_invalid_or_unbound")
    host=se.get("hostname");pins=se.get("pinned_addresses")
    if not isinstance(host,str) or not host or any(c.isspace() for c in host):b.append("hostname_invalid")
    if not isinstance(pins,list) or not pins:pins=[];b.append("pinned_addresses_missing")
    pins=[str(x) for x in pins]
    if len(pins)!=len(set(pins)):b.append("pinned_addresses_duplicate")
    if any(not _public(x) for x in pins):b.append("pinned_addresses_non_public")
    if se.get("scheme")!="https" or se.get("tls_required") is not True:b.append("https_tls_invalid")
    if se.get("method")!="GET" or se.get("max_network_requests")!=1:b.append("one_get_invalid")
    if se.get("allow_redirects") is not False or se.get("max_redirects")!=0:b.append("redirect_contract_invalid")
    if se.get("allowed_content_types")!=["application/json"]:b.append("json_only_invalid")
    mb=se.get("max_response_bytes")
    if isinstance(mb,bool) or not isinstance(mb,int) or not 1<=mb<=MAX_BYTES:b.append("response_bound_invalid")
    try:
        checked=_utc(str(se.get("checked_at")))
        if now and checked>now:b.append("safety_check_from_future")
    except Exception:b.append("safety_checked_at_invalid")

    b=list(dict.fromkeys(b));packet=None
    if not b and now:
        exp=now+timedelta(seconds=ttl_seconds)
        pc={"schema_version":1,"mode":PACKET_MODE,"request_state":"ready_for_fresh_explicit_final_real_observation_decision","requested_at":now.isoformat().replace("+00:00","Z"),"expires_at":exp.isoformat().replace("+00:00","Z"),"ttl_seconds":ttl_seconds,"i084_consumption_preflight_sha256":h84,"i084_invocation_envelope_sha256":eh,"i084_consumption_receipt_sha256":rh,"i085_safety_preflight_sha256":h85,"i085_safety_envelope_sha256":seh,"adapter_id":adapter,"target_fingerprint":target,"exact_scope_sha256":sh,"exact_scope":dict(s),"implementation_source_sha256":source,"hostname":host,"pinned_addresses":sorted(pins),"policy_evidence_sha256":pd,"dns_evidence_sha256":dd,"transport_contract_sha256":td,"transport_limits":{"scheme":"https","tls_required":True,"method":"GET","max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":mb,"credentials_allowed":False,"action_enabled":False},"remaining_prerequisites":{"fresh_explicit_final_human_decision_bound_to_packet_hash":True,"revalidate_packet_and_safety_evidence_freshness_at_execution":True,"revalidate_dns_pinning_and_anti_rebinding_at_execution":True,"network_capable_adapter_still_unreachable":True},"explicit_final_human_decision_required":True,"final_real_observation_authorized":False,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"packet_is_execution_token":False}
        packet={**pc,"final_real_observation_review_packet_sha256":_h(pc)}
    c={"schema_version":1,"mode":MODE,"builder_state":"final_real_observation_review_packet_ready_no_network" if packet else "final_real_observation_review_packet_rejected","i084_consumption_preflight_sha256":h84 if isinstance(h84,str) else None,"i085_safety_preflight_sha256":h85 if isinstance(h85,str) else None,"i085_safety_envelope_sha256":seh if isinstance(seh,str) else None,"final_real_observation_review_packet":packet,"blockers":b,"final_real_observation_authorized":False,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"builder_record_is_execution_token":False}
    return {**c,"final_real_observation_review_packet_builder_sha256":_h(c)}
