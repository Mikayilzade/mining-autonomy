from copy import deepcopy
from exact_https_target_binding import build_exact_https_target_binding, canonical_path_query, propagate_binding, validate_i090_request_unchanged

def scope(): return {"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"target:1","credentials_allowed":False,"action_enabled":False}

def fixtures(path="/api/tasks?status=open&limit=10"):
    r=build_exact_https_target_binding(hostname="tasks.example.com",path_query=path,target_fingerprint="target:1",adapter_id="payan-readonly",exact_scope=scope()); b=r["target_binding"]; sh=b["bound_exact_scope_sha256"]; s=b["bound_exact_scope"]
    common={"hostname":b["hostname"],"path_query":b["path_query"],"target_fingerprint":"target:1","adapter_id":"payan-readonly","exact_scope_sha256":sh,"exact_scope":s,"userinfo_allowed":False,"fragment_allowed":False}
    packet=dict(common); auth=dict(common); env=dict(common); manifest={k:v for k,v in common.items() if k!="exact_scope"}; gate={"request_spec":{"hostname":b["hostname"],"path":b["path_query"],"target_fingerprint":"target:1","adapter_id":"payan-readonly","exact_scope_sha256":sh}}
    return b,packet,auth,env,manifest,gate

def test_canonical_origin_form_preserves_query_order(): assert canonical_path_query("/a?b=2&a=1")=="/a?b=2&a=1" and canonical_path_query("")=="/"
def test_rejects_absolute_authority_fragment_userinfo_shapes():
    for bad in ("https://evil.example/x","//evil.example/x","/x#frag","user@example.com/x","/x\\y","/x y"):
        try: canonical_path_query(bad)
        except ValueError: pass
        else: raise AssertionError(bad)
def test_build_binds_path_into_exact_scope_hash():
    r=build_exact_https_target_binding(hostname="Tasks.Example.com.",path_query="/v1/tasks?x=1",target_fingerprint="target:1",adapter_id="payan-readonly",exact_scope=scope()); b=r["target_binding"]
    assert r["binding_state"]=="canonical_exact_target_bound" and b["hostname"]=="tasks.example.com" and b["bound_exact_scope"]["https_path_query"]=="/v1/tasks?x=1" and b["out_of_band_target_components_allowed"] is False
def test_full_lineage_accepts_exact_unchanged_target():
    b,p,a,e,m,g=fixtures(); v=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g)
    assert v["validation_state"]=="exact_target_unchanged_ready_for_i090" and not v["blockers"] and validate_i090_request_unchanged(v,g["request_spec"])==[]
def test_packet_path_tamper_rejected_even_if_other_fields_match():
    b,p,a,e,m,g=fixtures(); p=deepcopy(p); p["path_query"]="/api/tasks?limit=999"; v=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g); assert "review_packet_path_query_binding_invalid" in v["blockers"]
def test_authorization_scope_tamper_rejected():
    b,p,a,e,m,g=fixtures(); a=deepcopy(a); a["exact_scope"]["https_path_query"]="/other"; v=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g); assert "authorization_exact_scope_binding_invalid" in v["blockers"]
def test_manifest_and_i089_path_drift_rejected():
    b,p,a,e,m,g=fixtures(); m=deepcopy(m); g=deepcopy(g); m["path_query"]="/other"; g["request_spec"]["path"]="/other"; v=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g); assert "adapter_manifest_path_query_binding_invalid" in v["blockers"] and "i089_request_spec_path_binding_invalid" in v["blockers"]
def test_i090_preflight_rejects_out_of_band_path_change():
    b,p,a,e,m,g=fixtures(); v=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g); req=deepcopy(g["request_spec"]); req["path"]="/api/tasks?status=closed&limit=10"; assert "i090_path_query_drift" in validate_i090_request_unchanged(v,req)
def test_replay_same_binding_is_idempotent_not_permission_widening():
    b,p,a,e,m,g=fixtures(); v1=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g); v2=propagate_binding(b,review_packet=p,authorization=a,execution_envelope=e,adapter_manifest=m,i089_gate=g); assert v1==v2 and v1["network_enabled"] is False and v1["value_movement_enabled"] is False
