from dataclasses import replace
import pytest
import i123_execution_backend_portfolio as i123
import resource_router as rr

DIGEST="a"*64

def task():
    return rr.TaskEconomics(task_id="i194",required_capabilities=frozenset({"extract","validate"}),gross_payout_usd=1.0,minimum_success_probability=0.9,minimum_expected_margin_usd=0.01,minimum_expected_margin_ratio=0.01)

def backend(): return rr.default_backend_families()[0]

def evidence(**kw):
    base=dict(backend_id="python_local",provenance_class=i123.MEASURED,current_reproducible=True,non_synthetic=True,capacity_verified=True,policy_evidence_current=True,source_class="system_probe",source_artifact_id="receipt.json",source_artifact_sha256=DIGEST,observed_at_utc="2026-08-25T04:00:00Z")
    base.update(kw); return i123.BackendEvidence(**base)

def test_source_bound_measured_evidence_can_reach_ready():
    assert i123.route_portfolio(task(),(backend(),),(evidence(),)).state == "production_route_ready"

@pytest.mark.parametrize("source_class",["planning_reference","declaration","synthetic_fixture"])
def test_nonpromotable_origin_blocks_measured_promotion(source_class):
    d=i123.route_portfolio(task(),(backend(),),(evidence(source_class=source_class),))
    assert d.state == "hold"
    assert "backend_evidence_origin_not_promotable" in d.quotes[0].production_blockers

@pytest.mark.parametrize("field,value,error",[("source_artifact_id","","source_artifact_id_required"),("source_artifact_sha256","abc","source_artifact_sha256_invalid"),("observed_at_utc","2026-08-25T04:00:00","observed_at_utc_invalid"),("source_class","unknown","source_class_invalid")])
def test_malformed_origin_fails_closed(field,value,error):
    with pytest.raises(ValueError,match=error): i123.route_portfolio(task(),(backend(),),(replace(evidence(),**{field:value}),))

def test_authorization_true_without_separate_origin_fails_closed():
    with pytest.raises(ValueError,match="credentials_authorization_origin_invalid"):
        i123.route_portfolio(task(),(replace(backend(),requires_credentials=True),),(evidence(credentials_authorized=True),))

def test_explicit_user_authorization_reference_satisfies_origin_contract():
    b=replace(backend(),requires_credentials=True)
    e=evidence(credentials_authorized=True,credentials_authorization_origin="explicit_user_authorization",credentials_authorization_ref="user-approval:i194-fixture")
    assert i123.route_portfolio(task(),(b,),(e,)).state == "production_route_ready"
