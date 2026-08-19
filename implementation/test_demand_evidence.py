import pytest
from demand_evidence import classify_demand_evidence


def test_strength_order_and_semantics():
    settled = classify_demand_evidence("settled_receipt")
    request = classify_demand_evidence("open_paid_request")
    listing = classify_demand_evidence("listing_only")
    marketing = classify_demand_evidence("marketing_claim")
    assert settled.strength > request.strength > listing.strength > marketing.strength
    assert settled.proves_paid_utilization and not settled.proves_open_paid_demand
    assert request.proves_open_paid_demand and not request.proves_paid_utilization
    assert not listing.proves_paid_utilization and not marketing.proves_open_paid_demand


def test_unknown_and_invalid_are_fail_closed():
    assert classify_demand_evidence(None).evidence_class == "unknown"
    with pytest.raises(ValueError, match="unsupported_demand_evidence_class"):
        classify_demand_evidence("seller_count")
