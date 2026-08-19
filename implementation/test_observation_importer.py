from datetime import datetime, timezone
import json
import pytest

from observation_importer import import_saved_observation, replay_imported_open_tasks
from snapshot import canonical_payload_hash

NOW = datetime(2026, 8, 19, 6, 30, tzinfo=timezone.utc)


def envelope(evidence="open_paid_request"):
    payload={"items":[{"id":"r1","title":"extract","bounty_usd":3,"currency":"USD","skills":["extract"],
        "metadata":{"rights_status":"confirmed","tos_status":"confirmed","automation_allowed":"allowed",
        "source_data_permission":"confirmed","estimated_input_tokens":100,"estimated_output_tokens":100,
        "estimated_duration_seconds":30,"estimate_confidence":.9,"external_cost_cap_usd":0}}]}
    return {"snapshot":{"platform":"payanagent","source_url":"https://example.com/api/tasks",
        "source_timestamp":"2026-08-19T06:00:00+00:00","captured_at":"2026-08-19T06:01:00+00:00",
        "evidence_class":"official_api","payload":payload,"payload_sha256":canonical_payload_hash(payload)},
        "demand_evidence_class":evidence,"records_key":"items"}


def test_import_json_has_no_network_and_revalidates_snapshot():
    imported=import_saved_observation(json.dumps(envelope()),now=NOW)
    assert imported.snapshot.platform=="payanagent"
    assert imported.demand_evidence.proves_open_paid_demand


def test_import_rejects_tampered_hash():
    value=envelope(); value["snapshot"]["payload"]["items"][0]["id"]="tampered"
    with pytest.raises(ValueError,match="snapshot_hash_mismatch"):
        import_saved_observation(value,now=NOW)


def test_only_open_paid_request_can_replay_as_tasks():
    imported=import_saved_observation(envelope("listing_only"),now=NOW)
    with pytest.raises(ValueError,match="open_paid_request_evidence_required"):
        replay_imported_open_tasks(imported,now=NOW)


def test_open_request_replay_uses_trusted_timestamp():
    imported=import_saved_observation(envelope(),now=NOW)
    opportunities=replay_imported_open_tasks(imported,now=NOW)
    assert opportunities[0].external_id=="r1"
    assert opportunities[0].observed_at=="2026-08-19T06:00:00+00:00"
