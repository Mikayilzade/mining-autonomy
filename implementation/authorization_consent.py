"""Offline verifier for explicit, exact-scope authorization consent (I041)."""
from __future__ import annotations
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

REQUEST_WRAPPER_MODE="deterministic_exact_read_only_authorization_request"
REQUEST_MODE="exact_read_only_network_authorization_request"
DECISION_MODE="explicit_human_read_only_authorization_decision"
OUTPUT_MODE="deterministic_offline_authorization_consent_verification"

def _hash(v: Any)->str:
    return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def _utc(v: Any, code: str)->datetime:
    if not isinstance(v,str) or not v: raise ValueError(code)
    raw=v[:-1]+"+00:00" if v.endswith("Z") else v
    try: dt=datetime.fromisoformat(raw)
    except ValueError as exc: raise ValueError(code) from exc
    if dt.tzinfo is None or dt.utcoffset()!=timezone.utc.utcoffset(dt): raise ValueError(code+"_not_utc")
    return dt.astimezone(timezone.utc)

def _iso(dt: datetime)->str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00","Z")

def _validate_request(wrapper: Mapping[str,Any])->tuple[dict[str,Any],str]:
    if not isinstance(wrapper,Mapping) or wrapper.get("schema_version")!=1 or wrapper.get("mode")!=REQUEST_WRAPPER_MODE:
        raise ValueError("consent_request_wrapper_invalid")
    supplied=wrapper.get("exact_authorization_request_packet_sha256")
    core=dict(wrapper); core.pop("exact_authorization_request_packet_sha256",None)
    if not isinstance(supplied,str) or len(supplied)!=64 or _hash(core)!=supplied:
        raise ValueError("consent_request_wrapper_hash_mismatch")
    for k,w in {"authorization_granted":False,"credentials_allowed":False,"network_calls_performed":False,
                "transport_enabled":False,"dry_run_only":True,"action_enabled":False,
                "authorization_scope_widened":False}.items():
        if wrapper.get(k) is not w: raise ValueError("consent_request_wrapper_"+k+"_invalid")
    req=wrapper.get("exact_authorization_request")
    if wrapper.get("state")!="exact_single_get_ready_for_explicit_user_authorization" or not isinstance(req,Mapping):
        raise ValueError("consent_exact_request_not_available")
    if req.get("schema_version")!=1 or req.get("mode")!=REQUEST_MODE:
        raise ValueError("consent_exact_request_invalid")
    rs=req.get("authorization_request_sha256")
    rc=dict(req); rc.pop("authorization_request_sha256",None)
    if not isinstance(rs,str) or len(rs)!=64 or _hash(rc)!=rs: raise ValueError("consent_exact_request_hash_mismatch")
    scope=req.get("scope")
    if not isinstance(scope,Mapping) or req.get("scope_sha256")!=_hash(scope): raise ValueError("consent_scope_hash_mismatch")
    if scope.get("method")!="GET" or scope.get("required_environment")!="production" or scope.get("max_requests")!=1:
        raise ValueError("consent_scope_not_exact_single_production_get")
    if scope.get("credentials_allowed") is not False or scope.get("action_enabled") is not False:
        raise ValueError("consent_scope_unsafe")
    if req.get("authorization_granted") is not False or req.get("transport_enabled") is not False:
        raise ValueError("consent_request_not_inert")
    return dict(req), supplied

def verify_explicit_authorization_consent(
    exact_authorization_request_wrapper: Mapping[str,Any],
    decision: Mapping[str,Any],
    *,
    verification_time_utc: str,
)->dict[str,Any]:
    """Verify a future explicit decision. Offline only; never enables transport."""
    req, wrapper_hash=_validate_request(exact_authorization_request_wrapper)
    now=_utc(verification_time_utc,"consent_verification_time_invalid")
    not_before=_utc(req.get("not_before_utc"),"consent_request_not_before_invalid")
    expires=_utc(req.get("expires_at_utc"),"consent_request_expiry_invalid")
    if not (not_before <= now < expires): raise ValueError("consent_request_outside_validity_window")
    if not isinstance(decision,Mapping) or decision.get("schema_version")!=1 or decision.get("mode")!=DECISION_MODE:
        raise ValueError("consent_decision_schema_or_mode_invalid")
    supplied=decision.get("decision_sha256"); dc=dict(decision); dc.pop("decision_sha256",None)
    if not isinstance(supplied,str) or len(supplied)!=64 or _hash(dc)!=supplied:
        raise ValueError("consent_decision_hash_mismatch")
    if decision.get("decision") not in ("authorize","deny"): raise ValueError("consent_decision_value_invalid")
    decided=_utc(decision.get("decided_at_utc"),"consent_decided_at_invalid")
    if decided > now or decided < not_before or decided >= expires: raise ValueError("consent_decision_time_invalid")
    if decision.get("exact_authorization_request_packet_sha256")!=wrapper_hash:
        raise ValueError("consent_wrapper_binding_mismatch")
    if decision.get("authorization_request_sha256")!=req.get("authorization_request_sha256"):
        raise ValueError("consent_request_binding_mismatch")
    if decision.get("scope_sha256")!=req.get("scope_sha256"):
        raise ValueError("consent_scope_binding_mismatch")
    if decision.get("human_scope_acknowledged") is not True:
        raise ValueError("consent_human_scope_acknowledgement_required")
    if decision.get("max_requests")!=1 or decision.get("method")!="GET" or decision.get("credentials_allowed") is not False or decision.get("action_enabled") is not False:
        raise ValueError("consent_decision_scope_widened")
    authorized=decision["decision"]=="authorize"
    auth=None
    if authorized:
        acore={
            "schema_version":1,"mode":"verified_exact_read_only_execution_authorization",
            "exact_authorization_request_packet_sha256":wrapper_hash,
            "authorization_request_sha256":req["authorization_request_sha256"],
            "scope_sha256":req["scope_sha256"],"decision_sha256":supplied,
            "verified_at_utc":_iso(now),"expires_at_utc":_iso(expires),
            "max_requests":1,"method":"GET","required_environment":"production",
            "credentials_allowed":False,"action_enabled":False,
            "authorization_granted":True,
            "transport_enabled":False,"network_calls_performed":False,
            "offline_verification_only":True,
            "synthetic_fixture_not_real_consent":bool(decision.get("synthetic_fixture",False)),
        }
        auth={**acore,"execution_authorization_sha256":_hash(acore)}
    core={
        "schema_version":1,"mode":OUTPUT_MODE,"verified_at_utc":_iso(now),
        "decision":"authorize" if authorized else "deny","decision_sha256":supplied,
        "authorization_valid":authorized,"execution_authorization":auth,
        "transport_enabled":False,"network_calls_performed":False,"credentials_allowed":False,
        "action_enabled":False,"offline_only":True,
        "real_user_consent_inferred":False,
        "scope_widened":False,
    }
    return {**core,"consent_verification_sha256":_hash(core)}
