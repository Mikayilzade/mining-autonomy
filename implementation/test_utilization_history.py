from datetime import datetime, timezone

from observation_importer import import_saved_observation
from snapshot import ingest_snapshot, snapshot_record
from utilization_history import compare_utilization_snapshots


NOW = datetime(2026, 8, 19, 12, 0, tzinfo=timezone.utc)


def _import(records, source_timestamp):
    snap = ingest_snapshot(
        platform="payanagent",
        source_url="https://payanagent.com/api/v1/receipts",
        source_timestamp=source_timestamp,
        captured_at=source_timestamp,
        evidence_class="official_api",
        payload={"items": records},
        max_age_hours=100,
    )
    return import_saved_observation({
        "snapshot": snapshot_record(snap),
        "demand_evidence_class": "settled_receipt",
        "records_key": "items",
    }, now=NOW, max_age_hours=100)


def test_equal_coverage_windows_get_raw_deltas_only():
    a = _import([
        {"amount_usd": 1, "occurred_at": "2026-08-19T08:00:00Z"},
        {"amount_usd": 2, "occurred_at": "2026-08-19T09:00:00Z"},
    ], "2026-08-19T09:00:00Z")
    b = _import([
        {"amount_usd": 2, "occurred_at": "2026-08-19T10:00:00Z"},
        {"amount_usd": 2, "occurred_at": "2026-08-19T10:30:00Z"},
        {"amount_usd": 2, "occurred_at": "2026-08-19T11:00:00Z"},
    ], "2026-08-19T11:00:00Z")
    history = compare_utilization_snapshots([b, a], now=NOW, max_age_hours=100)
    c = history.comparisons[0]
    assert c.comparable_window is True
    assert c.transaction_delta == 1
    assert c.value_delta_usd == 3.0


def test_mismatched_coverage_never_extrapolates():
    a = _import([
        {"amount_usd": 1, "occurred_at": "2026-08-19T08:00:00Z"},
        {"amount_usd": 2, "occurred_at": "2026-08-19T09:00:00Z"},
    ], "2026-08-19T09:00:00Z")
    b = _import([
        {"amount_usd": 4, "occurred_at": "2026-08-19T10:00:00Z"},
        {"amount_usd": 4, "occurred_at": "2026-08-19T12:00:00Z"},
    ], "2026-08-19T12:00:00Z")
    c = compare_utilization_snapshots([a, b], now=NOW, max_age_hours=100).comparisons[0]
    assert c.comparable_window is False
    assert c.transaction_delta is None
    assert c.value_delta_usd is None
    assert c.reason == "mismatched_coverage_no_extrapolation"
