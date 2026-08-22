from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from typing import Any, Mapping

MODE = "deterministic_real_network_activation_decision_verifier"
_DECISION_MODE = "explicit_real_network_activation_human_decision"
_AUTH_MODE = "single_use_real_network_activation_authorization"
_EXPECTED_REQUEST_MODE = "real_network_activation_human_review_request"


def _hash(value: Any) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _parse_utc(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise ValueError("timestamp_must_be_utc")
    return dt.astimezone(timezone.utc)


def _exact_scope(scope: Mapping[str, Any]) -> bool:
    return (scope.get("method") == "GET" and scope.get("request_count") == 1
            and scope.get("required_environment") == "production"
            and isinstance(scope.get("target_fingerprint"), str) and bool(scope.get("target_fingerprint"))
            and scope.get("credentials_allowed") is False and scope.get("action_enabled") is False)


def verify_real_network_activation_decision(activation_request: Mapping[str, Any], human_decision: Mapping[str, Any], *, verified_at: str, authorization_ttl_seconds: int = 180) -> dict[str, Any]:
    """Verify an exact human decision; emit at most an inert single-use authorization record."""
    blockers: list[str] = []
    try:
        verified_dt = _parse_utc(verified_at)
    except Exception:
        verified_dt = None
        blockers.append("verified_at_invalid_or_not_utc")

    request_hash = activation_request.get("real_network_activation_request_sha256")
    request_core = dict(activation_request); request_core.pop("real_network_activation_request_sha256", None)
    if not isinstance(request_hash, str) or request_hash != _hash(request_core): blockers.append("activation_request_hash_invalid")
    if activation_request.get("mode") != _EXPECTED_REQUEST_MODE: blockers.append("activation_request_mode_invalid")
    if activation_request.get("request_state") != "ready_for_explicit_human_real_network_activation_decision": blockers.append("activation_request_not_ready")
    for key, required in {"explicit_human_decision_required":True,"activation_authorized":False,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"request_is_execution_token":False}.items():
        if activation_request.get(key) is not required: blockers.append(f"unsafe_or_missing_request_{key}")

    scope = activation_request.get("exact_scope")
    if not isinstance(scope, Mapping) or not _exact_scope(scope): blockers.append("scope_not_exact_single_anonymous_production_get"); scope = {}
    if not isinstance(activation_request.get("exact_scope_sha256"), str) or not activation_request.get("exact_scope_sha256"): blockers.append("exact_scope_hash_missing")
    try:
        requested_dt = _parse_utc(str(activation_request.get("requested_at"))); expires_dt = _parse_utc(str(activation_request.get("expires_at")))
        if expires_dt <= requested_dt: blockers.append("activation_request_expiry_invalid")
        if verified_dt is not None and not (requested_dt <= verified_dt <= expires_dt): blockers.append("activation_request_stale_or_not_yet_valid")
    except Exception: blockers.append("activation_request_time_invalid")
    if isinstance(authorization_ttl_seconds, bool) or not isinstance(authorization_ttl_seconds, int) or not 30 <= authorization_ttl_seconds <= 300: blockers.append("authorization_ttl_out_of_range")

    if human_decision.get("mode") != _DECISION_MODE: blockers.append("human_decision_mode_invalid")
    decision = human_decision.get("decision")
    if decision not in {"authorize", "deny"}: blockers.append("human_decision_value_invalid")
    if human_decision.get("real_network_activation_request_sha256") != request_hash: blockers.append("human_decision_request_binding_invalid")
    binding_fields = ("implementation_binding_audit_sha256","implementation_source_sha256","network_adapter_contract_validation_sha256","adapter_contract_readiness_sha256","adapter_id","exact_scope_sha256")
    for key in binding_fields:
        if human_decision.get(key) != activation_request.get(key): blockers.append(f"human_decision_{key}_binding_invalid")
    if human_decision.get("exact_scope") != dict(scope): blockers.append("human_decision_scope_not_exact")
    lineage = activation_request.get("authorization_lineage")
    if not isinstance(lineage, Mapping) or not lineage: blockers.append("activation_request_lineage_missing"); lineage = {}
    if human_decision.get("authorization_lineage") != dict(lineage): blockers.append("human_decision_lineage_binding_invalid")
    try:
        decided_dt = _parse_utc(str(human_decision.get("decided_at")))
        if verified_dt is not None and decided_dt > verified_dt: blockers.append("human_decision_from_future")
        if "requested_dt" in locals() and "expires_dt" in locals() and not (requested_dt <= decided_dt <= expires_dt): blockers.append("human_decision_outside_request_window")
    except Exception: decided_dt = None; blockers.append("human_decision_time_invalid")
    decision_id = human_decision.get("decision_id")
    if not isinstance(decision_id, str) or not decision_id.strip(): blockers.append("human_decision_id_missing")
    for key in ("credentials_allowed","task_acceptance_enabled","submission_enabled","value_movement_enabled"):
        if human_decision.get(key) is not False: blockers.append(f"human_decision_{key}_widened")
    if human_decision.get("single_use") is not True: blockers.append("human_decision_not_single_use")
    decision_hash = human_decision.get("real_network_activation_decision_sha256")
    decision_core = dict(human_decision); decision_core.pop("real_network_activation_decision_sha256", None)
    if not isinstance(decision_hash, str) or decision_hash != _hash(decision_core): blockers.append("human_decision_hash_invalid")

    blockers = list(dict.fromkeys(blockers)); authorization = None; state = "decision_rejected"
    if not blockers and decision == "deny": state = "denied_no_activation_authorization"
    elif not blockers and decision == "authorize" and verified_dt is not None and decided_dt is not None:
        auth_expires = min(verified_dt + timedelta(seconds=authorization_ttl_seconds), _parse_utc(str(activation_request["expires_at"])))
        if auth_expires <= verified_dt: blockers.append("authorization_would_be_expired")
        else:
            auth_core = {"schema_version":1,"mode":_AUTH_MODE,"authorization_state":"authorized_single_use_not_consumed","issued_at":verified_dt.isoformat().replace("+00:00","Z"),"expires_at":auth_expires.isoformat().replace("+00:00","Z"),"single_use":True,"consumed":False,"decision_id":decision_id,"real_network_activation_decision_sha256":decision_hash,"real_network_activation_request_sha256":request_hash,**{key:activation_request.get(key) for key in binding_fields},"exact_scope":dict(scope),"authorization_lineage":dict(lineage),"adapter_invocation_authorized":True,"max_network_requests":1,"credentials_allowed":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False,"authorization_is_payment_or_task_permission":False}
            authorization = {**auth_core,"real_network_activation_authorization_sha256":_hash(auth_core)}; state = "activation_authorization_issued_not_consumed"
    core = {"schema_version":1,"mode":MODE,"verification_state":state if not blockers else "decision_rejected","real_network_activation_request_sha256":request_hash if isinstance(request_hash,str) else None,"real_network_activation_decision_sha256":decision_hash if isinstance(decision_hash,str) else None,"activation_authorization":authorization if not blockers else None,"blockers":blockers,"adapter_invoked":False,"transport_enabled":False,"network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"verification_record_is_execution_token":False}
    return {**core,"real_network_activation_decision_verification_sha256":_hash(core)}
