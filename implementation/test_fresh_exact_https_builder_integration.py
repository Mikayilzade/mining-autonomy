from hashlib import sha256
import json
from exact_https_target_binding import build_exact_https_target_binding
from fresh_exact_https_builder_integration import bind_adapter_manifest, bind_i086_review_builder, bind_i089_gate, validate_pre_i090

def h(v): return sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def seal(c,k): return {**c,k:h(c)}
def ok(o,k):
    c=dict(o); got=c.pop(k); return got==h(c)
def binding():
    scope={"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"t","credentials_allowed":False,"action_enabled":False}
    return build_exact_https_target_binding(hostname="api.example.com",path_query="/v1/tasks?state=open",target_fingerprint="t",adapter_id="a",exact_scope=scope)["target_binding"]
def packet_builder():
    p=seal({"mode":"final_one_shot_real_observation_human_review_packet","adapter_id":"a","target_fingerprint":"t","hostname":"api.example.com","exact_scope":{},"exact_scope_sha256":"x"},"final_real_observation_review_packet_sha256")
    return seal({"final_real_observation_review_packet":p},"final_real_observation_review_packet_builder_sha256")

def test_review_is_resealed_before_decision():
    b=binding(); out=bind_i086_review_builder(packet_builder(),b); p=out["final_real_observation_review_packet"]
    assert p["path_query"]=="/v1/tasks?state=open" and p["exact_scope_sha256"]==b["bound_exact_scope_sha256"]
    assert ok(p,"final_real_observation_review_packet_sha256") and ok(out,"final_real_observation_review_packet_builder_sha256")

def test_i089_and_i090_drift_gate():
    b=binding(); req={"hostname":"api.example.com","target_fingerprint":"t","adapter_id":"a","exact_scope_sha256":b["bound_exact_scope_sha256"]}
    g=seal({"request_spec":req},"final_network_adapter_invocation_gate_sha256")
    i=seal({"invocation_gate":g},"final_network_adapter_invocation_gate_builder_sha256")
    bound=bind_i089_gate(i,b)
    assert bound["invocation_gate"]["request_spec"]["path"]=="/v1/tasks?state=open"
    assert validate_pre_i090(bound,b)==[]
    bad=json.loads(json.dumps(bound)); bad["invocation_gate"]["request_spec"]["path"]="/v1/tasks?state=closed"
    assert "i090_path_query_drift" in validate_pre_i090(bad,b)

def test_adapter_manifest_path_is_hash_bound():
    b=binding(); m=seal({"adapter_id":"a","target_fingerprint":"t","hostname":"api.example.com","exact_scope_sha256":"old"},"network_adapter_manifest_sha256")
    out=bind_adapter_manifest(m,b)
    assert out["path_query"]=="/v1/tasks?state=open" and ok(out,"network_adapter_manifest_sha256")

def test_binding_rejects_out_of_band_target():
    b=binding(); req={"hostname":"evil.example","target_fingerprint":"t","adapter_id":"a","exact_scope_sha256":b["bound_exact_scope_sha256"]}
    g=seal({"request_spec":req},"final_network_adapter_invocation_gate_sha256"); i=seal({"invocation_gate":g},"final_network_adapter_invocation_gate_builder_sha256")
    try: bind_i089_gate(i,b)
    except ValueError as e: assert "hostname" in str(e)
    else: assert False
