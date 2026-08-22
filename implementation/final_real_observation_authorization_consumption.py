from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import ipaddress, json
from typing import Any, Collection, Mapping
from urllib.parse import urlparse

MODE="deterministic_final_real_observation_authorization_consumption_preflight"
PACKET_MODE="final_one_shot_real_observation_human_review_packet"
AUTH_MODE="single_use_final_one_shot_real_observation_authorization"
POL_MODE="first_party_anonymous_read_only_policy_evidence"
DNS_MODE="offline_dns_resolution_evidence"
TX_MODE="offline_https_json_transport_contract"
ENV_MODE="single_attempt_final_real_observation_execution_envelope"
REC_MODE="single_use_final_real_observation_consumption_receipt"
MAX_BYTES=1048576

def _h(v:Any)->str:
    return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def _hok(o:Mapping[str,Any],k:str)->bool:
    x=dict(o); g=x.pop(k,None)
    return isinstance(g,str) and g==_h(x)

def _utc(v:str)->datetime:
    d=datetime.fromisoformat(v.replace("Z","+00:00"))
    if d.tzinfo is None or d.utcoffset()!=timedelta(0): raise ValueError("utc")
    return d.astimezone(timezone.utc)

def _sha(v:Any)->bool:
    try: return isinstance(v,str) and len(v)==64 and int(v,16)>=0
    except ValueError: return False

def _host(v:Any)->str:
    h=str(v).strip().lower().rstrip(".")
    if not h or len(h)>253 or any(x in h for x in "/:@") or any(c.isspace() for c in h):
        raise ValueError("host")
    return h

def _public_ip(v:Any)->bool:
    try:
        a=ipaddress.ip_address(str(v))
        return a.is_global and not any((a.is_private,a.is_loopback,a.is_link_local,a.is_multicast,a.is_reserved,a.is_unspecified))
    except ValueError:
        return False

def _false(o:Mapping[str,Any],keys:tuple[str,...],prefix:str,b:list[str])->None:
    for k in keys:
        if o.get(k) is not False:
            b.append(f"{prefix}_{k}_must_be_false")

def _fresh(e:Mapping[str,Any],now:datetime|None,max_cap:int,prefix:str,b:list[str])->None:
    try:
        obs=_utc(str(e.get("observed_at")))
    except Exception:
        b.append(prefix+"_observed_at_invalid"); return
    age=e.get("max_age_seconds")
    if isinstance(age,bool) or not isinstance(age,int) or not 1<=age<=max_cap:
        b.append(prefix+"_max_age_invalid"); return
    if now:
        if obs>now: b.append(prefix+"_from_future")
        elif (now-obs).total_seconds()>age: b.append(prefix+"_stale")

def consume_final_real_observation_authorization(
    packet:Mapping[str,Any],
    authorization:Mapping[str,Any],
    *,
    policy_evidence:Mapping[str,Any],
    dns_evidence:Mapping[str,Any],
    transport_contract:Mapping[str,Any],
    consumed_at:str,
    prior_consumption_receipt_sha256s:Collection[str]=(),
)->dict[str,Any]:
    """Fail-closed, zero-network final authorization consumer. Never performs DNS/TLS/HTTP."""
    b:list[str]=[]
    try: now=_utc(consumed_at)
    except Exception: now=None; b.append("consumed_at_invalid_or_not_utc")

    ph=packet.get("final_real_observation_review_packet_sha256")
    if not _hok(packet,"final_real_observation_review_packet_sha256"): b.append("packet_hash_invalid")
    if packet.get("mode")!=PACKET_MODE or packet.get("request_state")!="ready_for_fresh_explicit_final_real_observation_decision":
        b.append("packet_not_ready")
    _false(packet,("final_real_observation_authorized","network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","credentials_allowed","task_acceptance_enabled","submission_enabled","execution_enabled","value_movement_enabled","packet_is_execution_token"),"packet",b)
    try:
        req=_utc(str(packet.get("requested_at"))); pexp=_utc(str(packet.get("expires_at")))
        ttl=packet.get("ttl_seconds")
        if isinstance(ttl,bool) or not isinstance(ttl,int) or not 60<=ttl<=900 or pexp!=req+timedelta(seconds=ttl): b.append("packet_ttl_invalid")
        if now and not req<=now<=pexp: b.append("packet_stale_or_not_yet_valid")
    except Exception:
        req=pexp=None; b.append("packet_time_invalid")

    limits=packet.get("transport_limits") if isinstance(packet.get("transport_limits"),Mapping) else {}
    if not (limits.get("scheme")=="https" and limits.get("tls_required") is True and limits.get("method")=="GET" and limits.get("max_network_requests")==1 and limits.get("allow_redirects") is False and limits.get("max_redirects")==0 and limits.get("allowed_content_types")==["application/json"] and isinstance(limits.get("max_response_bytes"),int) and not isinstance(limits.get("max_response_bytes"),bool) and 1<=limits.get("max_response_bytes")<=MAX_BYTES and limits.get("credentials_allowed") is False and limits.get("action_enabled") is False):
        b.append("packet_transport_limits_invalid")
    prereq=packet.get("remaining_prerequisites") if isinstance(packet.get("remaining_prerequisites"),Mapping) else {}
    for k in ("revalidate_packet_and_safety_evidence_freshness_at_execution","revalidate_dns_pinning_and_anti_rebinding_at_execution","network_capable_adapter_still_unreachable"):
        if prereq.get(k) is not True: b.append(f"packet_prerequisite_{k}_missing")

    ah=authorization.get("final_real_observation_authorization_sha256")
    if not _hok(authorization,"final_real_observation_authorization_sha256"): b.append("authorization_hash_invalid")
    if authorization.get("mode")!=AUTH_MODE or authorization.get("authorization_state")!="authorized_single_use_not_consumed": b.append("authorization_state_invalid")
    if authorization.get("single_use") is not True or authorization.get("consumed") is not False: b.append("authorization_not_unconsumed_single_use")
    if authorization.get("final_real_observation_review_packet_sha256")!=ph: b.append("authorization_packet_binding_invalid")
    for k in ("adapter_id","target_fingerprint","exact_scope_sha256","exact_scope","implementation_source_sha256","hostname","pinned_addresses","policy_evidence_sha256","dns_evidence_sha256","transport_contract_sha256","transport_limits"):
        if authorization.get(k)!=packet.get(k): b.append(f"authorization_{k}_binding_invalid")
    _false(authorization,("credentials_allowed","task_acceptance_enabled","submission_enabled","value_movement_enabled","network_capable_adapter_reachable","transport_enabled","network_enabled","network_calls_performed","authorization_is_payment_or_task_permission","authorization_is_execution_result"),"authorization",b)
    if authorization.get("max_network_requests")!=1: b.append("authorization_request_ceiling_invalid")
    if authorization.get("execution_time_safety_revalidation_required") is not True: b.append("authorization_safety_revalidation_not_required")
    if authorization.get("execution_time_dns_pinning_anti_rebinding_revalidation_required") is not True: b.append("authorization_dns_revalidation_not_required")
    try:
        issued=_utc(str(authorization.get("issued_at"))); aexp=_utc(str(authorization.get("expires_at")))
        if aexp<=issued: b.append("authorization_ttl_invalid")
        if pexp and aexp>pexp: b.append("authorization_exceeds_packet_expiry")
        if now and not issued<=now<=aexp: b.append("authorization_stale_or_not_yet_valid")
    except Exception:
        issued=aexp=None; b.append("authorization_time_invalid")

    common={"target_fingerprint":packet.get("target_fingerprint"),"adapter_id":packet.get("adapter_id"),"exact_scope_sha256":packet.get("exact_scope_sha256"),"implementation_source_sha256":packet.get("implementation_source_sha256")}
    p=policy_evidence; pd=p.get("policy_evidence_sha256")
    if not _hok(p,"policy_evidence_sha256"): b.append("policy_evidence_hash_invalid")
    if p.get("mode")!=POL_MODE or p.get("source_kind")!="provider_first_party": b.append("policy_evidence_identity_invalid")
    u=urlparse(str(p.get("source_ref","")))
    if u.scheme!="https" or not u.hostname: b.append("policy_evidence_source_ref_not_https")
    if not _sha(p.get("source_content_sha256")): b.append("policy_source_content_digest_invalid")
    _fresh(p,now,86400,"policy_evidence",b)
    for k,v in common.items():
        if p.get(k)!=v: b.append("policy_evidence_"+k+"_binding_invalid")
    if p.get("anonymous_read_only_get_allowed") is not True: b.append("policy_anonymous_read_only_get_not_allowed")
    if p.get("credentials_required") is not False: b.append("policy_credentials_required")
    if p.get("automated_access_prohibited") is not False: b.append("policy_automated_access_prohibited")

    d=dns_evidence; dd=d.get("dns_evidence_sha256")
    if not _hok(d,"dns_evidence_sha256"): b.append("dns_evidence_hash_invalid")
    if d.get("mode")!=DNS_MODE or d.get("source_kind") not in {"measured_local","system_probe","provider_first_party"}: b.append("dns_evidence_identity_invalid")
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
    if sorted(pv)!=sorted(str(x) for x in packet.get("pinned_addresses",[])): b.append("dns_pinned_addresses_changed_since_packet")
    if not rv or any(not _public_ip(x) for x in rv): b.append("dns_resolution_contains_non_public_address")
    if d.get("all_addresses_public") is not True: b.append("dns_all_addresses_public_not_attested")
    if d.get("alias_chain_checked") is not True: b.append("dns_alias_chain_not_checked")
    if d.get("rebinding_check_passed") is not True: b.append("dns_rebinding_check_not_passed")
    if d.get("address_pinning_required") is not True: b.append("dns_address_pinning_not_required")
    if dh and dh!=str(packet.get("hostname","")).strip().lower().rstrip("."): b.append("dns_hostname_changed_since_packet")

    t=transport_contract; td=t.get("transport_contract_sha256")
    if not _hok(t,"transport_contract_sha256"): b.append("transport_contract_hash_invalid")
    if t.get("mode")!=TX_MODE: b.append("transport_contract_mode_invalid")
    for k,v in common.items():
        if t.get(k)!=v: b.append("transport_contract_"+k+"_binding_invalid")
    try: th=_host(t.get("hostname"))
    except Exception: th=""; b.append("transport_contract_hostname_invalid")
    if dh and th and dh!=th: b.append("dns_transport_hostname_binding_invalid")
    if th and th!=str(packet.get("hostname","")).strip().lower().rstrip("."): b.append("transport_hostname_changed_since_packet")
    actual_limits={"scheme":t.get("scheme"),"tls_required":t.get("tls_required"),"method":t.get("method"),"max_network_requests":t.get("max_network_requests"),"allow_redirects":t.get("allow_redirects"),"max_redirects":t.get("max_redirects"),"allowed_content_types":t.get("allowed_content_types"),"max_response_bytes":t.get("max_response_bytes"),"credentials_allowed":t.get("credentials_allowed"),"action_enabled":t.get("action_enabled")}
    if actual_limits!=dict(limits): b.append("transport_contract_drift_from_packet")
    if t.get("reject_content_encoding_expansion_over_limit") is not True: b.append("transport_decompressed_size_limit_not_required")
    if t.get("pin_resolved_addresses") is not True: b.append("transport_address_pinning_not_required")
    if t.get("reuse_dns_after_connect") is not False: b.append("transport_dns_reuse_not_disabled")

    b=list(dict.fromkeys(b)); envelope=receipt=None
    if not b and now:
        ec={"schema_version":1,"mode":ENV_MODE,"envelope_state":"one_attempt_final_real_observation_ready_no_network","created_at":now.isoformat().replace("+00:00","Z"),"final_real_observation_review_packet_sha256":ph,"final_real_observation_authorization_sha256":ah,"adapter_id":packet.get("adapter_id"),"target_fingerprint":packet.get("target_fingerprint"),"exact_scope_sha256":packet.get("exact_scope_sha256"),"exact_scope":dict(packet.get("exact_scope") or {}),"implementation_source_sha256":packet.get("implementation_source_sha256"),"hostname":packet.get("hostname"),"pinned_addresses":sorted(pv),"policy_evidence_sha256":pd,"dns_evidence_sha256":dd,"transport_contract_sha256":td,"transport_limits":dict(limits),"max_adapter_invocations":1,"max_network_requests":1,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"envelope_is_execution_result":False}
        envelope={**ec,"final_real_observation_execution_envelope_sha256":_h(ec)}
        rc={"schema_version":1,"mode":REC_MODE,"consumption_state":"authorization_consumed_once_no_network","consumed_at":now.isoformat().replace("+00:00","Z"),"authorization_consumed":True,"final_real_observation_review_packet_sha256":ph,"final_real_observation_authorization_sha256":ah,"final_real_observation_execution_envelope_sha256":envelope["final_real_observation_execution_envelope_sha256"],"policy_evidence_sha256":pd,"dns_evidence_sha256":dd,"transport_contract_sha256":td,"adapter_id":packet.get("adapter_id"),"target_fingerprint":packet.get("target_fingerprint"),"exact_scope_sha256":packet.get("exact_scope_sha256"),"network_capable_adapter_reachable":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"receipt_is_execution_token":False}
        candidate={**rc,"final_real_observation_consumption_receipt_sha256":_h(rc)}
        if candidate["final_real_observation_consumption_receipt_sha256"] in set(prior_consumption_receipt_sha256s):
            b.append("authorization_replay_detected"); envelope=None
        else: receipt=candidate

    ready=not b and envelope is not None and receipt is not None
    c={"schema_version":1,"mode":MODE,"consumption_state":"authorization_consumed_once_envelope_ready_no_network" if ready else "authorization_consumption_rejected","final_real_observation_review_packet_sha256":ph if isinstance(ph,str) else None,"final_real_observation_authorization_sha256":ah if isinstance(ah,str) else None,"fresh_policy_evidence_sha256":pd if isinstance(pd,str) else None,"fresh_dns_evidence_sha256":dd if isinstance(dd,str) else None,"fresh_transport_contract_sha256":td if isinstance(td,str) else None,"real_observation_execution_envelope":envelope if ready else None,"consumption_receipt":receipt if ready else None,"blockers":b,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"consumption_record_is_execution_token":False}
    return {**c,"final_real_observation_authorization_consumption_preflight_sha256":_h(c)}
