from copy import deepcopy
from pathlib import Path
from adapter_implementation_binding import _hash, audit_adapter_implementation_binding, build_inert_implementation_manifest

SOURCE = Path(__file__).with_name('future_https_json_adapter.py').read_text()

def validation_fixture():
    scope = {"method":"GET","request_count":1,"required_environment":"production","target_fingerprint":"payanagent:public-task-feed:v1","credentials_allowed":False,"action_enabled":False}
    readiness_core = {
        "schema_version":1,"mode":"network_capable_adapter_contract_readiness_artifact","readiness_state":"adapter_contract_ready_for_separate_review_no_execution",
        "adapter_id":"future-safe-https-json-v1","adapter_contract_sha256":"c"*64,"real_transport_authorization_consumption_sha256":"u"*64,
        "authorized_attempt_envelope_sha256":"e"*64,"real_transport_authorization_sha256":"a"*64,"pre_real_transport_review_sha256":"r"*64,
        "real_transport_decision_sha256":"d"*64,"exact_scope_sha256":"s"*64,"exact_scope":scope,
        "request_contract":{"method":"GET","max_network_requests":1,"required_environment":"production","target_fingerprint":scope["target_fingerprint"],"credentials_allowed":False,"action_enabled":False,"task_acceptance_enabled":False,"submission_enabled":False,"value_movement_enabled":False},
        "enforced_transport_gates":{"dns_policy":{"resolve_before_connect_required":True}},
        "network_capable_contract_declared":True,"execution_entrypoint_present":False,"execution_entrypoint_reachable":False,"transport_callable_attached":False,
        "ready_for_real_network_execution":False,"separate_human_review_required":True,"credentials_allowed":False,"task_acceptance_enabled":False,
        "submission_enabled":False,"execution_enabled":False,"value_movement_enabled":False,"transport_enabled":False,"network_enabled":False,
        "network_calls_performed":False,"readiness_artifact_is_execution_token":False,
    }
    readiness = {**readiness_core,"adapter_contract_readiness_sha256":_hash(readiness_core)}
    core = {
        "schema_version":1,"mode":"deterministic_network_capable_adapter_contract_validator","validation_state":"adapter_contract_ready_for_separate_review_no_execution",
        "real_transport_authorization_consumption_sha256":"u"*64,"authorized_attempt_envelope_sha256":"e"*64,"adapter_contract_sha256":"c"*64,
        "adapter_id":"future-safe-https-json-v1","adapter_readiness_artifact":readiness,"blockers":[],"adapter_contract_validated":True,
        "execution_entrypoint_present":False,"execution_entrypoint_reachable":False,"transport_callable_attached":False,"transport_enabled":False,
        "network_enabled":False,"network_calls_performed":False,"credentials_used":False,"task_acceptance_enabled":False,"submission_enabled":False,
        "execution_enabled":False,"value_movement_enabled":False,"validation_record_is_execution_token":False,
    }
    return {**core,"network_adapter_contract_validation_sha256":_hash(core)}

def rehash(obj, field):
    c=deepcopy(obj); c.pop(field,None); return {**c,field:_hash(c)}

def test_exact_source_and_manifest_bind_review_only():
    v=validation_fixture(); m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE)
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert out['audit_state']=='implementation_bound_review_ready_no_execution'
    assert out['blockers']==[] and out['implementation_binding_validated'] is True
    assert out['activation_reachable'] is False and out['network_enabled'] is False

def test_source_digest_tamper_fails_closed():
    v=validation_fixture(); m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE)
    out=audit_adapter_implementation_binding(v,m,SOURCE+'\n#tamper')
    assert 'implementation_source_digest_mismatch' in out['blockers']

def test_validation_hash_tamper_rejected():
    v=validation_fixture(); v['network_enabled']=True
    m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE)
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert 'i076_validation_hash_invalid' in out['blockers']

def test_readiness_hash_tamper_rejected_even_if_outer_rehashed():
    v=validation_fixture(); v['adapter_readiness_artifact']['adapter_id']='tampered'; v=rehash(v,'network_adapter_contract_validation_sha256')
    m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE)
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert 'i076_readiness_hash_invalid' in out['blockers']

def test_manifest_hash_tamper_rejected():
    v=validation_fixture(); m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE); m['module_path']='x.py'
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert 'implementation_manifest_hash_invalid' in out['blockers']

def test_scope_widening_rejected_after_rehashes():
    v=validation_fixture(); r=v['adapter_readiness_artifact']; r['exact_scope']['request_count']=2; r=rehash(r,'adapter_contract_readiness_sha256'); v['adapter_readiness_artifact']=r; v=rehash(v,'network_adapter_contract_validation_sha256')
    m=build_inert_implementation_manifest(r,SOURCE)
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert 'i076_scope_not_exact_anonymous_get' in out['blockers']

def test_activation_interface_widening_rejected():
    v=validation_fixture(); m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE); m['future_activation_interface']['max_network_requests']=2; m=rehash(m,'implementation_manifest_sha256')
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert 'future_activation_interface_not_exact' in out['blockers']

def test_reachable_entrypoint_manifest_rejected():
    v=validation_fixture(); m=build_inert_implementation_manifest(v['adapter_readiness_artifact'], SOURCE); m['execution_entrypoint_reachable']=True; m['activation_reachable']=True; m=rehash(m,'implementation_manifest_sha256')
    out=audit_adapter_implementation_binding(v,m,SOURCE)
    assert 'unsafe_or_missing_manifest_execution_entrypoint_reachable' in out['blockers']
    assert 'unsafe_or_missing_manifest_activation_reachable' in out['blockers']

def test_network_library_marker_in_source_rejected_even_with_matching_digest():
    v=validation_fixture(); bad=SOURCE+'\nimport requests\n'; m=build_inert_implementation_manifest(v['adapter_readiness_artifact'],bad)
    out=audit_adapter_implementation_binding(v,m,bad)
    assert 'network_or_process_transport_surface_present_in_source' in out['blockers']

def test_fail_closed_stub_required():
    v=validation_fixture(); bad=SOURCE.replace('raise RuntimeError("real_network_activation_not_enabled")','return None'); m=build_inert_implementation_manifest(v['adapter_readiness_artifact'],bad)
    out=audit_adapter_implementation_binding(v,m,bad)
    assert 'future_activation_interface_not_fail_closed' in out['blockers']
