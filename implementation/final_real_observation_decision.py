from __future__ import annotations
from datetime import datetime,timedelta,timezone
from hashlib import sha256
import json
from typing import Any,Collection,Mapping

MODE="deterministic_final_real_observation_decision_verifier"
DECISION_MODE="explicit_final_one_shot_real_observation_human_decision"
PACKET_MODE="final_one_shot_real_observation_human_review_packet"
AUTH_MODE="single_use_final_one_shot_real_observation_authorization"

def _h(v:Any)->str:return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def _hok(o:Mapping[str,Any],k:str)->bool:
    x=dict(o);g=x.pop(k,None);return isinstance(g,str) and g==_h(x)
def _utc(v:str)->datetime:
    d=datetime.fromisoformat(v.replace("Z","+00:00"))
    if d.tzinfo is None or d.utcoffset()!=timedelta(0):raise ValueError
    return d.astimezone(timezone.utc)
def _false(o:Mapping[str,Any],keys:tuple[str,...],p:str,b:list[str])->None:
    for k in keys:
        if o.get(k) is not False:b.append(f"{p}_{k}_must_be_false")

def verify_final_real_observation_decision(packet:Mapping[str,Any],decision:Mapping[str,Any],*,verified_at:str,authorization_ttl_seconds:int=120,prior_decision_sha256s:Collection[str]=())->dict[str,Any]:
    """Verify final packet-bound human authorize/deny; never performs DNS/TLS/HTTP."""
    b:list[str]=[]
    try:now=_utc(verified_at)
    except Exception:now=None;b.append("verified_at_invalid_or_not_utc")
    ph=packet.get("final_real_observation_review_packet_sha256")
    if not _hok(packet,"final_real_observation_review_packet_sha256"):b.append("packet_hash_invalid")
    if packet.get("mode")!=PACKET_MODE or packet.get("request_state")!="ready_for_fresh_explicit_final_real_observation_decision":b.append("packet_not_ready")
    _false(packet,("final_real_observation_authorized","network_capable_adapter_reachable","adapter_invoked","transport_enabled","network_enabled","network_calls_performed","credentials_allowed","task_acceptance_enabled","submission_enabled","execution_enabled","value_movement_enabled","packet_is_execution_token"),"packet",b)
    if packet.get("explicit_final_human_decision_required") is not True:b.append("packet_final_human_decision_not_required")
    limits=packet.get("transport_limits") if isinstance(packet.get("transport_limits"),Mapping) else {}
    if not (limits.get("scheme")=="https" and limits.get("tls_required") is True and limits.get("method")=="GET" and limits.get("max_network_requests")==1 and limits.get("allow_redirects") is False and limits.get("max_redirects")==0 and limits.get("allowed_content_types")==["application/json"] and isinstance(limits.get("max_response_bytes"),int) and not isinstance(limits.get("max_response_bytes"),bool) and 1<=limits.get("max_response_bytes")<=1048576 and limits.get("credentials_allowed") is False and limits.get("action_enabled") is False):b.append("packet_transport_limits_invalid")
    prereq=packet.get("remaining_prerequisites") if isinstance(packet.get("remaining_prerequisites"),Mapping) else {}
    for k in ("fresh_explicit_final_human_decision_bound_to_packet_hash","revalidate_packet_and_safety_evidence_freshness_at_execution","revalidate_dns_pinning_and_anti_rebinding_at_execution","network_capable_adapter_still_unreachable"):
        if prereq.get(k) is not True:b.append(f"packet_prerequisite_{k}_missing")
    try:
        req=_utc(str(packet.get("requested_at")));exp=_utc(str(packet.get("expires_at")))
        ttl=packet.get("ttl_seconds")
        if isinstance(ttl,bool) or not isinstance(ttl,int) or not 60<=ttl<=900 or exp!=req+timedelta(seconds=ttl):b.append("packet_ttl_invalid")
        if now and not req<=now<=exp:b.append("packet_stale_or_not_yet_valid")
    except Exception:req=exp=None;b.append("packet_time_invalid")
    if isinstance(authorization_ttl_seconds,bool) or not isinstance(authorization_ttl_seconds,int) or not 30<=authorization_ttl_seconds<=300:b.append("authorization_ttl_out_of_range")

    if decision.get("mode")!=DECISION_MODE:b.append("decision_mode_invalid")
    choice=decision.get("decision")
    if choice not in {"authorize","deny"}:b.append("decision_value_invalid")
    if decision.get("final_real_observation_review_packet_sha256")!=ph:b.append("decision_packet_binding_invalid")
    for k in ("adapter_id","target_fingerprint","exact_scope_sha256","implementation_source_sha256","hostname","pinned_addresses","policy_evidence_sha256","dns_evidence_sha256","transport_contract_sha256","transport_limits"):
        if decision.get(k)!=packet.get(k):b.append(f"decision_{k}_binding_invalid")
    if decision.get("single_use") is not True:b.append("decision_not_single_use")
    did=decision.get("decision_id")
    if not isinstance(did,str) or not did.strip():b.append("decision_id_missing")
    _false(decision,("credentials_allowed","task_acceptance_enabled","submission_enabled","value_movement_enabled"),"decision",b)
    try:
        decided=_utc(str(decision.get("decided_at")))
        if now and decided>now:b.append("decision_from_future")
        if req and exp and not req<=decided<=exp:b.append("decision_outside_packet_window")
    except Exception:decided=None;b.append("decision_time_invalid")
    dh=decision.get("final_real_observation_decision_sha256")
    if not _hok(decision,"final_real_observation_decision_sha256"):b.append("decision_hash_invalid")
    elif dh in set(prior_decision_sha256s):b.append("decision_replay_detected")

    b=list(dict.fromkeys(b));auth=None;state="decision_rejected"
    if not b and choice=="deny":state="denied_no_final_real_observation_authorization"
    elif not b and choice=="authorize" and now and exp:
        ae=min(now+timedelta(seconds=authorization_ttl_seconds),exp)
        if ae<=now:b.append("authorization_would_be_expired")
        else:
            ac={"schema_version":1,"mode":AUTH_MODE,"authorization_state":"authorized_single_use_not_consumed","issued_at":now.isoformat().replace("+00:00","Z"),"expires_at":ae.isoformat().replace("+00:00","Z"),"single_use":True,"consumed":False,"decision_id":did,"final_real_observation_decision_sha256":dh,"final_real_observation_review_packet_sha256":ph,"adapter_id":packet.get("adapter_id"),"target_fingerprint":packet.get("target_fingerprint"),"exact_scope_sha256":packet.get("exact_scope_sha256"),"exact_scope":packet.get("exact_scope"),"implementation_source_sha256":packet.get("implementation_source_sha256"),"hostname":packet.get("hostname"),"pinned_addresses":packet.get("pinned_addresses"),"policy_evidence_sha256":packet.get("policy_evidence_sha256"),"dns_evidence_sha256":packet.get("dns_evidence_sha256"),"transport_contract_sha256":packet.get("transport_contract_sha256"),"transport_limits":dict(limits),"max_network_requests":1,"execution_time_safety_revalidation_required":True,"execution_time_dns_pinning_anti_rebinding_revalidation_required":True,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"network_capable_adapter_reachable":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"authorization_is_payment_or_task_permission":False,"authorization_is_execution_result":False}
            auth={**ac,"final_real_observation_authorization_sha256":_h(ac)};state="final_real_observation_authorization_issued_not_consumed"
    c={"schema_version":1,"mode":MODE,"verification_state":state if not b else "decision_rejected","final_real_observation_review_packet_sha256":ph if isinstance(ph,str) else None,"final_real_observation_decision_sha256":dh if isinstance(dh,str) else None,"final_real_observation_authorization":auth if not b else None,"blockers":b,"network_capable_adapter_reachable":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"verification_record_is_execution_token":False}
    return {**c,"final_real_observation_decision_verification_sha256":_h(c)}
