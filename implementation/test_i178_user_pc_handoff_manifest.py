import json
from pathlib import Path

import i178_user_pc_handoff_manifest as i178


def _measurement():
    return {
        "measured_available_hours_per_day": 8.0,
        "availability_source_ref": "local-log:availability-2026-08-24",
        "energy_before_joules": 1000.0,
        "energy_after_joules": 4600.0,
        "energy_task_count": 10,
        "energy_source_ref": "local-meter:session-2026-08-24",
        "tariff_usd_per_kwh": 0.1,
        "tariff_source_ref": "utility-bill:tariff-2026-08",
        "opportunity_cost_usd_per_hour": 0.01,
        "opportunity_cost_source_ref": "owner-accounting:pc-occupation-2026-08-24",
    }


def _accounting(kind="user_declared"):
    digest = None if kind == "user_declared" else "d" * 64
    return {
        "records": [
            {
                "parameter": "fixed_monthly_cost_usd",
                "value": 0.0,
                "source_kind": kind,
                "source_ref": "owner-accounting:fixed-cost-2026-08-24",
                "observed_at": "2026-08-24T08:30:00Z",
                "max_age_seconds": 2592000,
                "source_content_digest": digest,
            },
            {
                "parameter": "sunk_or_already_committed",
                "value": True,
                "source_kind": kind,
                "source_ref": "owner-accounting:sunk-classification-2026-08-24",
                "observed_at": "2026-08-24T08:30:00Z",
                "max_age_seconds": 2592000,
                "source_content_digest": digest,
            },
        ]
    }


def _write_json(path: Path, value):
    path.write_text(json.dumps(value), encoding="utf-8")


def _single_exact_source(tmp_path, monkeypatch):
    target = tmp_path / "implementation" / "demo.py"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"print('offline')\n")
    expected = i178.git_blob_sha(target.read_bytes())
    monkeypatch.setattr(
        i178,
        "SOURCE_SPECS",
        (i178.SourceSpec("implementation/demo.py", expected, "test_source"),),
    )
    return target


def test_exact_sources_and_complete_inputs_reach_only_real_chain_handoff(tmp_path, monkeypatch):
    _single_exact_source(tmp_path, monkeypatch)
    measurement = tmp_path / "measurement.json"
    accounting = tmp_path / "accounting.json"
    _write_json(measurement, _measurement())
    _write_json(accounting, _accounting())

    result = i178.inspect_handoff(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        confirm_user_owned_pc=True,
    )
    assert result.state == "READY_TO_RUN_REAL_LOCAL_CHAIN"
    assert result.blockers == ()
    assert result.exact_source_tree_ready is True
    assert result.ready_to_run_real_chain is True
    assert result.i050_execution_allowed is False
    assert result.i066_execution_allowed is False
    assert result.i123_promotion_allowed is False


def test_source_byte_drift_blocks_even_with_complete_inputs(tmp_path, monkeypatch):
    target = _single_exact_source(tmp_path, monkeypatch)
    target.write_text("print('changed')\n", encoding="utf-8")
    measurement = tmp_path / "measurement.json"
    accounting = tmp_path / "accounting.json"
    _write_json(measurement, _measurement())
    _write_json(accounting, _accounting())

    result = i178.inspect_handoff(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        confirm_user_owned_pc=True,
    )
    assert result.state == "SOURCE_TREE_BLOCKED"
    assert any(item.startswith("source_blob_mismatch:") for item in result.blockers)
    assert result.ready_to_run_real_chain is False


def test_missing_confirmation_and_files_are_reported_not_inferred(tmp_path, monkeypatch):
    _single_exact_source(tmp_path, monkeypatch)
    result = i178.inspect_handoff(tmp_path)
    assert result.state == "HANDOFF_INPUTS_BLOCKED"
    assert "explicit_user_owned_pc_confirmation_required" in result.blockers
    assert "measurement_json_not_supplied" in result.blockers
    assert "accounting_json_not_supplied" in result.blockers


def test_placeholder_measurement_and_accounting_provenance_is_rejected(tmp_path, monkeypatch):
    _single_exact_source(tmp_path, monkeypatch)
    measurement_raw = _measurement()
    measurement_raw["energy_source_ref"] = "test-fixture:energy"
    accounting_raw = _accounting()
    accounting_raw["records"][0]["source_ref"] = "placeholder:fixed-cost"
    measurement = tmp_path / "measurement.json"
    accounting = tmp_path / "accounting.json"
    _write_json(measurement, measurement_raw)
    _write_json(accounting, accounting_raw)

    result = i178.inspect_handoff(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        confirm_user_owned_pc=True,
    )
    assert result.state == "HANDOFF_INPUTS_BLOCKED"
    assert "measurement_nonproduction_provenance:energy_source_ref" in result.blockers
    assert "accounting_nonproduction_provenance:fixed_monthly_cost_usd" in result.blockers


def test_reproducible_accounting_requires_digest(tmp_path, monkeypatch):
    _single_exact_source(tmp_path, monkeypatch)
    measurement = tmp_path / "measurement.json"
    accounting = tmp_path / "accounting.json"
    _write_json(measurement, _measurement())
    raw = _accounting("provider_first_party")
    raw["records"][1]["source_content_digest"] = "short"
    _write_json(accounting, raw)

    result = i178.inspect_handoff(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        confirm_user_owned_pc=True,
    )
    assert result.state == "HANDOFF_INPUTS_BLOCKED"
    assert "accounting_reproducible_digest_required:sunk_or_already_committed" in result.blockers


def test_git_blob_hash_depends_on_exact_bytes():
    assert i178.git_blob_sha(b"abc") != i178.git_blob_sha(b"abc\n")
