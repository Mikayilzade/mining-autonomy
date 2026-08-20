"""Deterministic read-only transport preflight over I029 session plans."""
from __future__ import annotations
from datetime import datetime, timezone, timedelta
from hashlib import sha256
import ipaddress, json, math
from typing import Any, Mapping, Protocol
from urllib.parse import urlsplit

SESSION_MODE="deterministic_no_network_capture_session_plan"
READINESS_MODE="deterministic_no_network_capture_readiness_packet"
PREFLIGHT_MODE="deterministic_read_only_transport_preflight"
AUTH_MODE="explicit_read_only_network_authorization"
READY_STATE="ready_for_future_explicit_read_only_capture"

class ReadOnlyGetTransport(Protocol):
    def get(self, *, url: str, headers: Mapping[str,str], timeout_seconds: float) -> Mapping[str,Any]: ...

def _hash(v: Any)->str:
    b=json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return sha256(b).hexdigest()

def _time(v: Any, err: str)->datetime:
    if not isinstance(v,str) or not v: raise ValueError(err)
    n=v[:-1]+"+00:00" if v.endswith("Z") else v
    try: d=datetime.fromisoformat(n)
    except ValueError as e: raise ValueError(err) from e
    if d.tzinfo is None or d.utcoffset() is None: raise ValueError(err)
    return d.astimezone(timezone.utc)

def _url(v: Any)->tuple[str,int|None]:
    if not isinstance(v,str) or not v: raise ValueError("transport_preflight_source_url_invalid")
    q=urlsplit(v)
    if q.scheme.lower()!="https" or not q.hostname or q.username or q.password or q.fragment:
        raise ValueError("transport_preflight_source_url_invalid")
    h=q.hostname.lower().rstrip(".")
    if h=="localhost" or h.endswith((".localhost",".local",".internal")):
        raise ValueError("transport_preflight_private_endpoint_forbidden")
    try: a=ipaddress.ip_address(h)
    except ValueError: a=None
    if a is not None and not a.is_global:
        raise ValueError("transport_preflight_private_endpoint_forbidden")
    try: port=q.port
    except ValueError as e: raise ValueError("transport_preflight_source_url_invalid") from e
    return h,port

def _flags(x: Mapping[str,Any], prefix: str)->None:
    for k,w in {"authorization_granted":False,"network_calls_performed":False,"credentials_allowed":False,
                "dry_run_only":True,"action_enabled":False,"missing_evidence_is_negative_demand":False}.items():
        if x.get(k) is not w: raise ValueError(f"{prefix}_{k}_invalid")

def _rate(r: Mapping[str,Any])->dict[str,Any]:
    x=r.get("rate_limit")
    if not isinstance(x,Mapping): raise ValueError("transport_preflight_rate_limit_missing")
    if x.get("budget_basis")!="project_conservative_self_limit": raise ValueError("transport_preflight_rate_limit_basis_invalid")
    try: mi=float(x["min_interval_seconds"]); mr=int(x["max_requests_per_window"]); ws=float(x["window_seconds"])
    except (KeyError,TypeError,ValueError) as e: raise ValueError("transport_preflight_rate_limit_invalid") from e
    if not math.isfinite(mi) or not math.isfinite(ws) or mi<0 or mr<=0 or ws<=0:
        raise ValueError("transport_preflight_rate_limit_invalid")
    return {"min_interval_seconds":mi,"max_requests_per_window":mr,"window_seconds":ws,"budget_basis":"project_conservative_self_limit"}

def _seq(v: Any, err: str)->tuple[str,...]:
    if not isinstance(v,(list,tuple)) or not v: raise ValueError(err)
    out=tuple(str(i) for i in v)
    if any(not i for i in out): raise ValueError(err)
    return out

def build_transport_preflight(plan: Mapping[str,Any], packet: Mapping[str,Any], *, default_timeout_seconds: float=20.0)->dict[str,Any]:
    if not isinstance(plan,Mapping) or plan.get("schema_version")!=1 or plan.get("mode")!=SESSION_MODE:
        raise ValueError("transport_preflight_session_plan_invalid")
    _flags(plan,"transport_preflight_session")
    if plan.get("authorization_state")!="explicit_read_only_network_authorization_required":
        raise ValueError("transport_preflight_session_authorization_state_invalid")
    steps=plan.get("chronological_session_plan")
    if not isinstance(steps,list) or plan.get("planned_request_count")!=len(steps):
        raise ValueError("transport_preflight_request_count_mismatch")
    if not isinstance(packet,Mapping) or packet.get("schema_version")!=1 or packet.get("mode")!=READINESS_MODE:
        raise ValueError("transport_preflight_readiness_packet_invalid")
    _flags(packet,"transport_preflight_readiness")
    if plan.get("manifest_sha256")!=packet.get("manifest_sha256"):
        raise ValueError("transport_preflight_manifest_hash_mismatch")
    manifest=plan.get("manifest_sha256")
    if not isinstance(manifest,str) or len(manifest)!=64: raise ValueError("transport_preflight_manifest_hash_invalid")
    try: timeout=float(default_timeout_seconds)
    except (TypeError,ValueError) as e: raise ValueError("transport_preflight_timeout_invalid") from e
    if not math.isfinite(timeout) or timeout<=0 or timeout>60: raise ValueError("transport_preflight_timeout_invalid")
    try: budget=float(plan["total_time_budget_seconds"])
    except (KeyError,TypeError,ValueError) as e: raise ValueError("transport_preflight_time_budget_invalid") from e
    if not math.isfinite(budget) or budget<0: raise ValueError("transport_preflight_time_budget_invalid")
    start=_time(plan.get("start_time_utc"),"transport_preflight_start_time_invalid")
    ready=packet.get("ready_for_future_explicit_read_only_capture")
    if not isinstance(ready,list): raise ValueError("transport_preflight_readiness_rows_invalid")
    idx={}
    for r in ready:
        if not isinstance(r,Mapping) or r.get("readiness_state")!=READY_STATE: raise ValueError("transport_preflight_readiness_row_invalid")
        ih=r.get("manifest_item_sha256")
        if not isinstance(ih,str) or not ih: raise ValueError("transport_preflight_manifest_item_hash_invalid")
        if ih in idx: raise ValueError("transport_preflight_manifest_item_hash_duplicate")
        idx[ih]=r
    envs=[]; seen=set()
    for expected, s in enumerate(steps,1):
        if not isinstance(s,Mapping) or s.get("sequence")!=expected: raise ValueError("transport_preflight_sequence_invalid")
        if s.get("authorization_state")!="explicit_read_only_network_authorization_required": raise ValueError("transport_preflight_step_authorization_state_invalid")
        for k,w in {"credentials_allowed":False,"network_calls_performed":False,"dry_run_only":True,"action_enabled":False}.items():
            if s.get(k) is not w: raise ValueError(f"transport_preflight_step_{k}_invalid")
        if s.get("method")!="GET": raise ValueError("transport_preflight_non_get_forbidden")
        if s.get("required_environment")!="production": raise ValueError("transport_preflight_nonproduction_forbidden")
        ih=s.get("manifest_item_sha256")
        if ih in seen: raise ValueError("transport_preflight_duplicate_planned_item")
        seen.add(ih)
        r=idx.get(ih)
        if r is None: raise ValueError("transport_preflight_readiness_binding_missing")
        host,port=_url(s.get("source_url"))
        if s.get("host")!=host: raise ValueError("transport_preflight_host_binding_mismatch")
        for k in ("platform","item_index","source_url","method","required_environment"):
            if s.get(k)!=r.get(k): raise ValueError(f"transport_preflight_{k}_binding_mismatch")
        ev=_seq(s.get("expected_evidence_classes"),"transport_preflight_evidence_classes_invalid")
        if ev!=_seq(r.get("expected_evidence_classes"),"transport_preflight_evidence_classes_invalid"):
            raise ValueError("transport_preflight_evidence_binding_mismatch")
        prov=_seq(s.get("provenance_checklist"),"transport_preflight_provenance_invalid")
        if prov!=_seq(r.get("provenance_checklist"),"transport_preflight_provenance_invalid"):
            raise ValueError("transport_preflight_provenance_binding_mismatch")
        rate=_rate(r)
        sch=_time(s.get("scheduled_at_utc"),"transport_preflight_schedule_invalid")
        try: off=float(s.get("offset_seconds"))
        except (TypeError,ValueError) as e: raise ValueError("transport_preflight_offset_invalid") from e
        if not math.isfinite(off) or off<0 or off>budget: raise ValueError("transport_preflight_offset_invalid")
        if abs((sch-(start+timedelta(seconds=off))).total_seconds())>0.001:
            raise ValueError("transport_preflight_schedule_offset_mismatch")
        b={"sequence":expected,"priority_index":int(s["priority_index"]),"platform":str(s["platform"]),
           "item_index":int(s["item_index"]),"source_url":str(s["source_url"]),"host":host,"port":port,"method":"GET",
           "scheduled_at_utc":str(s["scheduled_at_utc"]),"offset_seconds":off,"manifest_item_sha256":str(ih),
           "manifest_sha256":manifest,"expected_evidence_classes":list(ev),"required_environment":"production",
           "provenance_checklist":list(prov),"rate_limit":rate,"timeout_seconds":timeout,
           "allowed_request_headers":["Accept","User-Agent"],"forbidden_request_headers":["Authorization","Cookie","Proxy-Authorization"],
           "redirect_policy":"disabled_until_explicit_authorized_transport",
           "dns_policy":"resolve_at_execution_and_reject_non_global_addresses",
           "credentials_allowed":False,"action_enabled":False}
        envs.append({**b,"request_binding_sha256":_hash(b),"transport_interface":"ReadOnlyGetTransportV1",
                     "transport_enabled":False,"authorization_granted":False,"network_calls_performed":False,"dry_run_only":True})
    psha=_hash(plan)
    return {"schema_version":1,"mode":PREFLIGHT_MODE,"manifest_sha256":manifest,"session_plan_sha256":psha,
            "readiness_packet_sha256":_hash(packet),"transport_envelope_set_sha256":_hash(envs),
            "planned_request_count":len(envs),"transport_envelopes":envs,
            "authorization_contract":{"required_mode":AUTH_MODE,"required_scope":"exact_preflight_plan",
             "required_session_plan_sha256":psha,"allowed_methods":["GET"],"required_max_requests":len(envs),
             "credentials_allowed":False,"action_enabled":False},
            "transport_enabled":False,"authorization_granted":False,"network_calls_performed":False,
            "credentials_allowed":False,"dry_run_only":True,"action_enabled":False,"missing_evidence_is_negative_demand":False}

def validate_explicit_read_only_authorization(preflight: Mapping[str,Any], authorization: Mapping[str,Any])->dict[str,Any]:
    if not isinstance(preflight,Mapping) or preflight.get("mode")!=PREFLIGHT_MODE: raise ValueError("transport_authorization_preflight_invalid")
    _flags(preflight,"transport_authorization_preflight")
    if preflight.get("transport_enabled") is not False: raise ValueError("transport_authorization_preflight_transport_flag_invalid")
    if not isinstance(authorization,Mapping): raise ValueError("transport_authorization_missing")
    if authorization.get("schema_version")!=1 or authorization.get("mode")!=AUTH_MODE: raise ValueError("transport_authorization_mode_invalid")
    if authorization.get("authorization_granted") is not True: raise ValueError("transport_authorization_not_granted")
    if authorization.get("scope")!="exact_preflight_plan": raise ValueError("transport_authorization_scope_invalid")
    if authorization.get("session_plan_sha256")!=preflight.get("session_plan_sha256"): raise ValueError("transport_authorization_plan_hash_mismatch")
    if authorization.get("allowed_methods")!=["GET"]: raise ValueError("transport_authorization_methods_invalid")
    if authorization.get("credentials_allowed") is not False: raise ValueError("transport_authorization_credentials_forbidden")
    if authorization.get("action_enabled") is not False: raise ValueError("transport_authorization_action_forbidden")
    if authorization.get("max_requests")!=preflight.get("planned_request_count"): raise ValueError("transport_authorization_request_cap_invalid")
    if not isinstance(authorization.get("authorization_nonce"),str) or not authorization["authorization_nonce"].strip():
        raise ValueError("transport_authorization_nonce_missing")
    expires=_time(authorization.get("expires_at_utc"),"transport_authorization_expiry_invalid")
    latest=max((_time(e.get("scheduled_at_utc"),"transport_authorization_preflight_schedule_invalid") for e in preflight.get("transport_envelopes",[])), default=None)
    if latest is not None and expires<latest: raise ValueError("transport_authorization_expired_before_session_end")
    return {"schema_version":1,"mode":"read_only_authorization_validation_receipt","authorization_valid":True,
            "session_plan_sha256":preflight["session_plan_sha256"],"transport_envelope_set_sha256":preflight["transport_envelope_set_sha256"],
            "max_requests":authorization["max_requests"],"allowed_methods":["GET"],"credentials_allowed":False,"action_enabled":False,
            "transport_enabled":False,"network_calls_performed":False,"validation_only":True}
