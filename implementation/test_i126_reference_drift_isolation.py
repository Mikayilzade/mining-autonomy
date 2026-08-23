from dataclasses import asdict
from datetime import datetime, timezone

from resource_profile_evidence import (
    BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
    attest_resource_profile,
    backend_config_invariant_digest,
    backend_config_invariant_source_ref,
    make_evidence,
    reference_backend_hash,
)
from resource_router import default_backend_families


def test_generic_i050_rejects_python_local_invariant_against_drifted_reference():
    reference = asdict(next(x for x in default_backend_families() if x.backend_id == "python_local"))
    drifted = dict(reference)
    drifted["fixed_monthly_cost_usd"] = 1.0
    record = make_evidence(
        evidence_id="forged-against-drifted-reference",
        backend_id="python_local",
        parameter="fixed_monthly_cost_usd",
        value=0.0,
        source_kind=BACKEND_CONFIG_INVARIANT_SOURCE_KIND,
        source_ref=backend_config_invariant_source_ref("python_local", "fixed_monthly_cost_usd"),
        observed_at="2026-08-23T19:55:00Z",
        max_age_seconds=3600,
        reference_hash=reference_backend_hash(drifted),
        source_content_digest=backend_config_invariant_digest("python_local", "fixed_monthly_cost_usd", 0.0),
    )
    att = attest_resource_profile(
        drifted, (record,), now=datetime(2026, 8, 23, 20, 0, tzinfo=timezone.utc)
    )
    row = next(x for x in att.parameter_calibrations if x.parameter == "fixed_monthly_cost_usd")
    assert row.state == "invalid_or_stale"
    assert "reference_value_mismatch" in row.reason
