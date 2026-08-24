from dataclasses import replace
from datetime import datetime, timezone
import math

import pytest

import i129_energy_measurement_receipt as m

OBS = "2026-08-23T21:00:00Z"
NOW = datetime(2026, 8, 23, 21, 1, tzinfo=timezone.utc)


def good(**overrides):
    base = dict(
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
    base.update(overrides)
    return m.build_energy_receipt(**base)


def test_receipt_computes_energy_per_task_and_converts_to_i054():
    r = good()
    assert r.energy_delta_joules == 720.0
    assert abs(r.energy_kwh_per_task - 0.00001) < 1e-15
    e = m.to_energy_measurement(r, now=NOW)
    assert e.energy_kwh_per_task == r.energy_kwh_per_task
    assert e.tariff_usd_per_kwh == 0.10
    assert e.source_ref.endswith(r.receipt_hash)


def test_counter_reset_wrap_fails_closed():
    with pytest.raises(ValueError, match="wrap"):
        good(energy_before_joules=10, energy_after_joules=9)


def test_zero_delta_cannot_become_zero_electricity_cost():
    with pytest.raises(ValueError, match="positive_finite_energy_delta_required"):
        good(energy_before_joules=1000, energy_after_joules=1000)


def test_nonfinite_energy_readings_fail_closed():
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError):
            good(energy_before_joules=value)
        with pytest.raises(ValueError):
            good(energy_after_joules=value)


def test_nonfinite_tariff_fails_closed():
    for value in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValueError, match="tariff_must_be_finite_nonnegative"):
            good(tariff_usd_per_kwh=value)


def test_extreme_task_count_cannot_underflow_per_task_energy_to_zero():
    with pytest.raises(ValueError):
        good(task_count=10 ** 400)


def test_bool_or_noninteger_task_count_is_not_accepted_as_capacity():
    for value in (True, False, 1.5, "20"):
        with pytest.raises(ValueError, match="positive_task_count_required"):
            good(task_count=value)


def test_tamper_and_stale_receipts_fail_closed():
    r = good()
    with pytest.raises(ValueError, match="hash"):
        m.verify_energy_receipt(replace(r, task_count=21), now=NOW)
    late = datetime(2026, 9, 10, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="current"):
        m.verify_energy_receipt(r, now=late)


def test_tariff_and_meter_provenance_are_mandatory():
    for kwargs in (
        {"counter_source_digest": "short"},
        {"tariff_source_ref": ""},
        {"tariff_source_digest": "short"},
        {"counter_source_ref": None},
    ):
        with pytest.raises(ValueError):
            good(**kwargs)


def test_observation_and_max_age_types_fail_closed_instead_of_crashing_open():
    with pytest.raises(ValueError, match="observed_at_must_be_utc"):
        good(observed_at="not-a-time")
    for value in (True, 0, -1, 1.5):
        with pytest.raises(ValueError, match="positive_max_age_required"):
            good(max_age_seconds=value)


def test_valid_positive_values_remain_finite():
    r = good()
    assert math.isfinite(r.energy_delta_joules)
    assert r.energy_delta_joules > 0
    assert math.isfinite(r.energy_kwh_per_task)
    assert r.energy_kwh_per_task > 0
    assert math.isfinite(r.tariff_usd_per_kwh)
