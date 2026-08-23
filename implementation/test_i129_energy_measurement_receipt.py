from dataclasses import replace
from datetime import datetime, timezone

import i129_energy_measurement_receipt as m

OBS = "2026-08-23T21:00:00Z"
NOW = datetime(2026, 8, 23, 21, 1, tzinfo=timezone.utc)


def good():
    return m.build_energy_receipt(
        workload_id="python-local-fixed-json-transform-v1",
        task_count=20,
        counter_source_ref="local-meter:package-energy",
        counter_source_digest="c" * 64,
        energy_before_joules=1000.0,
        energy_after_joules=1720.0,
        tariff_usd_per_kwh=0.10,
        tariff_source_ref="explicit-tariff:test-fixture",
        tariff_source_digest="t" * 64,
        observed_at=OBS,
    )


def test_receipt_computes_energy_per_task_and_converts_to_i054():
    r = good()
    assert r.energy_delta_joules == 720.0
    assert abs(r.energy_kwh_per_task - 0.00001) < 1e-15
    e = m.to_energy_measurement(r, now=NOW)
    assert e.energy_kwh_per_task == r.energy_kwh_per_task
    assert e.tariff_usd_per_kwh == 0.10
    assert e.source_ref.endswith(r.receipt_hash)


def test_counter_reset_wrap_fails_closed():
    try:
        m.build_energy_receipt(
            workload_id="x", task_count=1, counter_source_ref="meter",
            counter_source_digest="c" * 64, energy_before_joules=10,
            energy_after_joules=9, tariff_usd_per_kwh=0.1,
            tariff_source_ref="tariff", tariff_source_digest="t" * 64,
            observed_at=OBS,
        )
    except ValueError as exc:
        assert "wrap" in str(exc)
    else:
        raise AssertionError("counter reset/wrap must fail closed")


def test_tamper_and_stale_receipts_fail_closed():
    r = good()
    try:
        m.verify_energy_receipt(replace(r, task_count=21), now=NOW)
    except ValueError as exc:
        assert "hash" in str(exc)
    else:
        raise AssertionError("tamper must fail")
    late = datetime(2026, 9, 10, tzinfo=timezone.utc)
    try:
        m.verify_energy_receipt(r, now=late)
    except ValueError as exc:
        assert "current" in str(exc)
    else:
        raise AssertionError("stale receipt must fail")


def test_tariff_and_meter_provenance_are_mandatory():
    for kwargs in (
        {"counter_source_digest": "short"},
        {"tariff_source_ref": ""},
        {"tariff_source_digest": "short"},
    ):
        base = dict(
            workload_id="x", task_count=1, counter_source_ref="meter",
            counter_source_digest="c" * 64, energy_before_joules=0,
            energy_after_joules=1, tariff_usd_per_kwh=0.1,
            tariff_source_ref="tariff", tariff_source_digest="t" * 64,
            observed_at=OBS,
        )
        base.update(kwargs)
        try:
            m.build_energy_receipt(**base)
        except ValueError:
            pass
        else:
            raise AssertionError("missing provenance must fail")
