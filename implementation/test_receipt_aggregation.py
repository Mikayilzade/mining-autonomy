from datetime import datetime, timezone
import pytest
from observation_importer import import_saved_observation
from receipt_aggregation import aggregate_imported_utilization
from snapshot import canonical_payload_hash

NOW=datetime(2026,8,19,8,0,tzinfo=timezone.utc); A="a"*64; B="b"*64

def imported(evidence="settled_receipt",records=None):
    records=records or [{"amount_usd":5,"settled_at":"2026-08-19T07:00:00+00:00","buyer_hash":A},{"amount_usd":3,"settled_at":"2026-08-19T07:10:00+00:00","buyer_hash":A},{"amount_usd":2,"settled_at":"2026-08-19T07:20:00+00:00","buyer_hash":B}]
    payload={"items":records}
    env={"snapshot":{"platform":"payanagent","source_url":"https://example.com/receipts","source_timestamp":"2026-08-19T07:30:00+00:00","captured_at":"2026-08-19T07:31:00+00:00","evidence_class":"official_api","payload":payload,"payload_sha256":canonical_payload_hash(payload)},"demand_evidence_class":evidence,"records_key":"items"}
    return import_saved_observation(env,now=NOW)

def test_aggregation_metrics():
    s=aggregate_imported_utilization(imported(),now=NOW)
    assert (s.transaction_count,s.total_value_usd,s.unique_hashed_buyers,s.repeat_hashed_buyers)==(3,10,2,1)
    assert s.top_hashed_buyer_value_share==.8

def test_open_request_not_utilization():
    with pytest.raises(ValueError,match="paid_utilization_evidence_required"):
        aggregate_imported_utilization(imported("open_paid_request"),now=NOW)

def test_raw_identity_rejected():
    with pytest.raises(ValueError,match="raw_buyer_identity_not_allowed"):
        aggregate_imported_utilization(imported(records=[{"amount_usd":1,"settled_at":"2026-08-19T07:00:00+00:00","buyer_id":"x"}]),now=NOW)

def test_invalid_buyer_hash_rejected():
    with pytest.raises(ValueError,match="buyer_hash_must_be_sha256"):
        aggregate_imported_utilization(imported(records=[{"amount_usd":1,"settled_at":"2026-08-19T07:00:00+00:00","buyer_hash":"x"}]),now=NOW)
