from pathlib import Path
import json

import i180_user_pc_handoff_package as i180


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_measurement_template_is_exactly_blank_non_evidence():
    template = i180.measurement_template()
    assert set(template) == set(i180.i178.MEASUREMENT_FIELDS)
    assert all(value is None for value in template.values())


def test_accounting_template_is_exactly_two_blank_rows():
    template = i180.accounting_template()
    rows = template["records"]
    assert len(rows) == 2
    assert {row["parameter"] for row in rows} == set(i180.i178.ACCOUNTING_PARAMETERS)
    assert all(row["value"] is None for row in rows)
    assert all(row["source_kind"] is None for row in rows)
    assert all(row["source_ref"] is None for row in rows)
    assert all(row["observed_at"] is None for row in rows)
    assert all(row["max_age_seconds"] is None for row in rows)
    assert all(row["source_content_digest"] is None for row in rows)


def test_written_blank_templates_are_rejected_by_i178(tmp_path):
    paths = i180.write_package(tmp_path)
    assert len(paths) == 3
    measurement = tmp_path / i180.MEASUREMENT_TEMPLATE_NAME
    accounting = tmp_path / i180.ACCOUNTING_TEMPLATE_NAME
    measurement_check = i180.i178.check_measurement_input(measurement)
    accounting_check = i180.i178.check_accounting_input(accounting)
    assert measurement_check.structurally_complete is False
    assert accounting_check.structurally_complete is False
    assert any(error.startswith("measurement_missing:") for error in measurement_check.errors)
    assert any(error.startswith("accounting_missing_value:") for error in accounting_check.errors)


def test_write_package_round_trips_exact_generators(tmp_path):
    i180.write_package(tmp_path)
    measurement = json.loads((tmp_path / i180.MEASUREMENT_TEMPLATE_NAME).read_text(encoding="utf-8"))
    accounting = json.loads((tmp_path / i180.ACCOUNTING_TEMPLATE_NAME).read_text(encoding="utf-8"))
    readme = (tmp_path / i180.INSTRUCTIONS_NAME).read_text(encoding="utf-8")
    assert measurement == i180.measurement_template()
    assert accounting == i180.accounting_template()
    assert "do not estimate energy" in readme.lower()
    assert "i179" in readme


def test_runtime_source_drift_fails_closed(tmp_path):
    (tmp_path / "implementation").mkdir()
    (tmp_path / i180.I178_PATH).write_text("changed", encoding="utf-8")
    (tmp_path / i180.I179_PATH).write_text("changed", encoding="utf-8")
    package_dir = tmp_path / "implementation" / "user_pc_handoff"
    i180.write_package(package_dir)
    report = i180.inspect_package(tmp_path, package_dir=package_dir)
    assert report.state == "PASS_BLOCKED"
    assert any(blocker.startswith("runtime_source_blob_mismatch:") for blocker in report.blockers)
    assert report.real_chain_ready is False
    assert report.i050_execution_allowed is False
    assert report.i123_promotion_allowed is False


def test_checked_in_package_is_ready_only_as_non_evidence():
    root = _repo_root()
    report = i180.inspect_package(root)
    assert report.state == "PACKAGE_READY_NON_EVIDENCE"
    assert report.blockers == ()
    assert all(binding.exact for binding in report.runtime_bindings)
    assert report.measurement_template_blank is True
    assert report.accounting_template_blank is True
    assert report.measurement_template_rejected_by_i178 is True
    assert report.accounting_template_rejected_by_i178 is True
    assert report.real_evidence_created is False
    assert report.real_chain_ready is False
    assert report.i050_execution_allowed is False
    assert report.i066_execution_allowed is False
    assert report.i123_promotion_allowed is False
