from datetime import datetime, timezone
import pytest
from evaluator import CapabilityProfile
from observation_importer import import_saved_observation
from orchestrator import observe_imported_tasks
from snapshot import canonical_payload_hash

POLICY=dict(rights_status="confirmed",tos_status="confirmed",automation_allowed="allowed",source_data_permission="confirmed")
NOW=datetime(2026,8,19,7,30,tzinfo=timezone.utc)

def imported(evidence="open_paid_request"):
    payload={"items":[{"id":"saved-1","title":"extract data","bounty_usd":4,"currency":"USD","skills":["extract"],"observed_at":"1999-01-01T00:00:00+00:00","metadata":dict(POLICY,estimated_input_tokens=1000,estimated_output_tokens=1000,estimated_duration_seconds=120,estimate_confidence=.9,external_cost_cap_usd=0)}]}
    envelope={"snapshot":{"platform":"payanagent","source_url":"https://example.com/open-requests","source_timestamp":"2026-08-19T07:00:00+00:00","captured_at":"2026-08-19T07:01:00+00:00","evidence_class":"official_api","payload":payload,"payload_sha256":canonical_payload_hash(payload)},"demand_evidence_class":evidence,"records_key":"items"}
    return import_saved_observation(envelope,now=NOW)

def test_imported_open_request_bridges_to_dry_run_queue():
    q=observe_imported_tasks(imported(),now=NOW,capabilities=CapabilityProfile({"extract"}))
    assert len(q)==1 and q[0].external_id=="saved-1"
    assert q[0].state=="accept_dry_run"
    assert q[0].open_paid_demand_proven and not q[0].action_enabled

def test_non_open_evidence_fails_closed():
    with pytest.raises(ValueError,match="open_paid_request_evidence_required"):
        observe_imported_tasks(imported("listing_only"),now=NOW)
