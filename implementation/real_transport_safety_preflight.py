from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import ipaddress, json
from typing import Any, Mapping
from urllib.parse import urlparse

MODE="deterministic_real_transport_safety_preflight"
I084_MODE="deterministic_exact_real_read_only_invocation_authorization_consumption_preflight"
ENV_MODE="single_attempt_exact_real_read_only_invocation_envelope"
REC_MODE="single_use_exact_real_read_only_invocation_consumption_receipt"
POL_MODE="first_party_anonymous_read_only_policy_evidence"
DNS_MODE="offline_dns_resolution_evidence"
TX_MODE="offline_https_json_transport_contract"
MAX_BYTES=1048576

def _h(v:Any)->str:
    return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def _utc(v:str)->datetime:
    d=datetime.fromisoformat(v.replace("Z","+00:00"))
    if d.tzinfo is None or d.utcoffset()!=timedelta(0): raise ValueError("utc")
    return d.astimezone(timezone.utc)

def _sha(v:Any)->bool:
    try: return isinstance(v,str) and len(v)==64 and int(v,16)>=0
    except ValueError: return False

def _scope(s:Mapping[str,Any])->bool:
    return s.get("method")=="GET" and s.get("request_count")==1 and s.get("required_environment")=="production" and bool(s.get("target_fingerprint")) and s.get("credentials_allowed") is False and s.get("action_enabled") is False

def _host(v:Any)->str:
    h=str(v).strip().lower().rstrip(".")
    if not h or len(h)>253 or any(x in h for x in "/:@") or any(c.isspace() for c in h): raise ValueError("host")
    return h

def _public_ip(v:Any)->bool:
    try:
        a=ipaddress.ip_address(str(v))
        return a.is_global and not any((a.is_private,a.is_loopback,a.is_link_local,a.is_multicast,a.is_reserved,a.is_unspecified))
    except ValueError: return False

def _hash_ok(obj:Mapping[str,Any],key:str)->bool:
    x=dict(obj); got=x.pop(key,None)
    return isinstance(got,str) and got==_h(x)

def _fresh(e:Mapping[str,Any],now:datetime|None,max_cap:int,prefix:str,b:list[str])->None:
    try: obs=_utc(str(e.get("observed_at")))
    except Exception: b.append(prefix+"_observed_at_invalid"); return
    age=e.get("max_age_seconds")
    if isinstance(age,bool) or not isinstance(age,int) or not 1<=age<=max_cap: b.append(prefix+"_max_age_invalid"); return
    if now:
        if obs>now: b.append(prefix+"_from_future")
        elif (now-obs).total_seconds()>age: b.append(prefix+"_stale")

def build_real_transport_safety_preflight(i084:Mapping[str,Any],*,policy_evidence:Mapping[str,Any],dns_evidence:Mapping[str,Any],transport_contract:Mapping[str,Any],checked_at:str)->dict[str,Any]:
    """Evidence-only fail-closed gate. Never performs DNS, sockets, TLS or HTTP."""
    b:list[str]=[]
    try: now=_utc(checked_at)
    except Exception: now=None; b.append("checked_at_invalid_or_not_utc")

    ph=i084.get("exact_real_read_only_invocation_consumption_preflight_sha256")
    if not _hash_ok(i084,"exact_real_read_only_invocation_consumption_preflight_sha256"): b.append("i084_preflight_hash_invalid")
    if i084.get("mode")!=I084_MODE or i084.get("consumption_state")!="authorization_consumed_once_envelope_ready_no_network": b.append("i084_preflight_not_ready")
    if i084.get("blockers"): b.append("i084_preflight_has_blockers")
    for k in ("network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","credentials_used","task_acceptance_enabled","submission_enabled","execution_enabled","value_movement_enabled","consumption_record_is_execution_token"):
        if i084.get(k) is not False: b.append("i084_"+k+"_must_be_false")

    e=i084.get("real_read_only_invocation_envelope")
    if not isinstance(e,Mapping): b.append("i084_envelope_missing"); e={}
    eh=e.get("exact_real_read_only_invocation_envelope_sha256")
    if not _hash_ok(e,"exact_real_read_only_invocation_envelope_sha256"): b.append("i084_envelope_hash_invalid")
    if e.get("mode")!=ENV_MODE or e.get("envelope_state")!="one_attempt_bound_no_network": b.append("i084_envelope_state_invalid")
    if e.get("max_adapter_invocations")!=1 or e.get("max_network_requests")!=1: b.append("i084_one_attempt_limits_invalid")
    s=e.get("exact_scope")
    if not isinstance(s,Mapping) or not _scope(s): b.append("exact_scope_not_one_anonymous_production_get"); s={}
    sh=e.get("exact_scope_sha256")
    if not isinstance(sh,str) or sh!=_h(dict(s)): b.append("exact_scope_hash_invalid")
    for k in ("credentials_allowed","task_acceptance_enabled","submission_enabled","value_movement_enabled","network_capable_adapter_reachable","transport_enabled","network_enabled","network_calls_performed","adapter_invoked","envelope_is_execution_result"):
        if e.get(k) is not False: b.append("i084_envelope_"+k+"_widened")
    adapter=e.get("adapter_id"); target=s.get("target_fingerprint")
    if not isinstance(adapter,str) or not adapter: b.append("adapter_id_missing")
    if not isinstance(target,str) or not target: b.append("target_fingerprint_missing")
    lineage=e.get("source_lineage")
    if not isinstance(lineage,Mapping): b.append("source_lineage_missing"); lineage={}
    for k in ("implementation_binding_audit_sha256","implementation_source_sha256","network_adapter_contract_validation_sha256","adapter_contract_readiness_sha256","real_network_activation_authorization_sha256","real_network_activation_request_sha256"):
        if not isinstance(lineage.get(k),str) or not lineage.get(k): b.append("source_lineage_"+k+"_missing")
    source=lineage.get("implementation_source_sha256")
    if not _sha(source): b.append("implementation_source_sha256_invalid")

    r=i084.get("consumption_receipt")
    if not isinstance(r,Mapping): b.append("i084_consumption_receipt_missing"); r={}
    rh=r.get("exact_real_read_only_invocation_consumption_receipt_sha256")
    if not _hash_ok(r,"exact_real_read_only_invocation_consumption_receipt_sha256"): b.append("i084_consumption_receipt_hash_invalid")
    if r.get("mode")!=REC_MODE or r.get("consumption_state")!="consumed_once_no_network" or r.get("authorization_consumed") is not True: b.append("i084_consumption_receipt_state_invalid")
    if r.get("exact_real_read_only_invocation_envelope_sha256")!=eh or r.get("adapter_id")!=adapter or r.get("exact_scope_sha256")!=sh: b.append("i084_receipt_envelope_scope_binding_invalid")
    for k in ("network_capable_adapter_reachable","network_enabled","network_calls_performed","credentials_used","task_acceptance_enabled","submission_enabled","value_movement_enabled","receipt_is_execution_token"):
        if r.get(k) is not False: b.append("i084_receipt_"+k+"_must_be_false")
    for k in ("exact_real_read_only_invocation_request_sha256","exact_real_read_only_invocation_decision_sha256","exact_real_read_only_invocation_authorization_sha256"):
        if r.get(k)!=e.get(k) or i084.get(k)!=e.get(k): b.append("i084_"+k+"_lineage_binding_invalid")

    common={"target_fingerprint":target,"adapter_id":adapter,"exact_scope_sha256":sh,"implementation_source_sha256":source}
    p=policy_evidence; p_hash=p.get("policy_evidence_sha256")
    if not _hash_ok(p,"policy_evidence_sha256"): b.append("policy_evidence_hash_invalid")
    if p.get("mode")!=POL_MODE: b.append("policy_evidence_mode_invalid")
    if p.get("source_kind")!="provider_first_party": b.append("policy_evidence_not_first_party")
    u=urlparse(str(p.get("source_ref","")))
    if u.scheme!="https" or not u.hostname: b.append("policy_evidence_source_ref_not_https")
    if not _sha(p.get("source_content_sha256")): b.append("policy_source_content_digest_invalid")
    _fresh(p,now,86400,"policy_evidence",b)
    for k,v in common.items():
        if p.get(k)!=v: b.append("policy_evidence_"+k+"_binding_invalid")
    if p.get("anonymous_read_only_get_allowed") is not True: b.append("policy_anonymous_read_only_get_not_allowed")
    if p.get("credentials_required") is not False: b.append("policy_credentials_required")
    if p.get("automated_access_prohibited") is not False: b.append("policy_automated_access_prohibited")

    d=dns_evidence; d_hash=d.get("dns_evidence_sha256")
    if not _hash_ok(d,"dns_evidence_sha256"): b.append("dns_evidence_hash_invalid")
    if d.get("mode")!=DNS_MODE: b.append("dns_evidence_mode_invalid")
    if d.get("source_kind") not in {"measured_local","system_probe","provider_first_party"}: b.append("dns_evidence_source_kind_invalid")
    if not _sha(d.get("source_content_sha256")): b.append("dns_source_content_digest_invalid")
    _fresh(d,now,900,"dns_evidence",b)
    for k,v in common.items():
        if d.get(k)!=v: b.append("dns_evidence_"+k+"_binding_invalid")
    try: dh=_host(d.get("hostname")); _host(d.get("canonical_name"))
    except Exception: dh=""; b.append("dns_hostname_invalid")
    aliases=d.get("aliases")
    if not isinstance(aliases,list) or len(aliases)>16: b.append("dns_aliases_invalid"); aliases=[]
    else:
        try:
            aa=[_host(x) for x in aliases]
            if len(aa)!=len(set(aa)): b.append("dns_aliases_duplicate")
        except Exception: b.append("dns_aliases_invalid")
    resolved=d.get("resolved_addresses"); pinned=d.get("pinned_addresses")
    if not isinstance(resolved,list) or not resolved: b.append("dns_resolved_addresses_missing"); resolved=[]
    if not isinstance(pinned,list) or not pinned: b.append("dns_pinned_addresses_missing"); pinned=[]
    rv=[str(x) for x in resolved]; pv=[str(x) for x in pinned]
    if len(rv)!=len(set(rv)) or len(pv)!=len(set(pv)): b.append("dns_addresses_duplicate")
    if sorted(rv)!=sorted(pv): b.append("dns_pinned_addresses_do_not_match_resolution")
    if not rv or any(not _public_ip(x) for x in rv): b.append("dns_resolution_contains_non_public_address")
    if d.get("all_addresses_public") is not True: b.append("dns_all_addresses_public_not_attested")
    if d.get("alias_chain_checked") is not True: b.append("dns_alias_chain_not_checked")
    if d.get("rebinding_check_passed") is not True: b.append("dns_rebinding_check_not_passed")
    if d.get("address_pinning_required") is not True: b.append("dns_address_pinning_not_required")

    t=transport_contract; t_hash=t.get("transport_contract_sha256")
    if not _hash_ok(t,"transport_contract_sha256"): b.append("transport_contract_hash_invalid")
    if t.get("mode")!=TX_MODE: b.append("transport_contract_mode_invalid")
    for k,v in common.items():
        if t.get(k)!=v: b.append("transport_contract_"+k+"_binding_invalid")
    try: th=_host(t.get("hostname"))
    except Exception: th=""; b.append("transport_contract_hostname_invalid")
    if dh and th and dh!=th: b.append("dns_transport_hostname_binding_invalid")
    if t.get("scheme")!="https": b.append("transport_scheme_not_https")
    if t.get("tls_required") is not True: b.append("transport_tls_not_required")
    if t.get("method")!="GET": b.append("transport_method_not_get")
    if t.get("max_network_requests")!=1: b.append("transport_request_ceiling_not_one")
    if t.get("allow_redirects") is not False or t.get("max_redirects")!=0: b.append("transport_redirects_not_zero")
    if t.get("credentials_allowed") is not False: b.append("transport_credentials_widened")
    if t.get("action_enabled") is not False: b.append("transport_action_widened")
    if t.get("allowed_content_types")!=["application/json"]: b.append("transport_content_type_not_json_only")
    mb=t.get("max_response_bytes")
    if isinstance(mb,bool) or not isinstance(mb,int) or not 1<=mb<=MAX_BYTES: b.append("transport_response_bound_invalid")
    if t.get("reject_content_encoding_expansion_over_limit") is not True: b.append("transport_decompressed_size_limit_not_required")
    if t.get("pin_resolved_addresses") is not True: b.append("transport_address_pinning_not_required")
    if t.get("reuse_dns_after_connect") is not False: b.append("transport_dns_reuse_not_disabled")

    b=list(dict.fromkeys(b)); ready=not b; safety=None
    if ready and now:
        c={"schema_version":1,"mode":"single_attempt_real_transport_safety_envelope","safety_state":"safety_prerequisites_attested_no_network","checked_at":now.isoformat().replace("+00:00","Z"),"i084_consumption_preflight_sha256":ph,"i084_invocation_envelope_sha256":eh,"i084_consumption_receipt_sha256":rh,"policy_evidence_sha256":p_hash,"dns_evidence_sha256":d_hash,"transport_contract_sha256":t_hash,"adapter_id":adapter,"target_fingerprint":target,"exact_scope_sha256":sh,"implementation_source_sha256":source,"hostname":th,"pinned_addresses":sorted(pv),"method":"GET","scheme":"https","tls_required":True,"max_network_requests":1,"allow_redirects":False,"max_redirects":0,"allowed_content_types":["application/json"],"max_response_bytes":mb,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"safety_envelope_is_execution_token":False}
        safety={**c,"real_transport_safety_envelope_sha256":_h(c)}
    c={"schema_version":1,"mode":MODE,"preflight_state":"real_transport_safety_evidence_ready_no_network" if ready else "real_transport_safety_evidence_rejected","i084_consumption_preflight_sha256":ph if isinstance(ph,str) else None,"i084_invocation_envelope_sha256":eh if isinstance(eh,str) else None,"policy_evidence_sha256":p_hash if isinstance(p_hash,str) else None,"dns_evidence_sha256":d_hash if isinstance(d_hash,str) else None,"transport_contract_sha256":t_hash if isinstance(t_hash,str) else None,"real_transport_safety_envelope":safety,"blockers":b,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"preflight_record_is_execution_token":False}
    return {**c,"real_transport_safety_preflight_sha256":_h(c)}
