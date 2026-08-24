import json

import i180_user_pc_handoff_package as i180


def test_measurement_template_is_exactly_blank_non_evidence():
    template = i180.measurement_template()
    assert set(template) == set(i180.MEASUREMENT_FIELDS)
    assert all(value is None for value in template.values())
    assert i180._measurement_contract_complete(template) is False


def test_accounting_template_is_exactly_two_blank_rows():
    template = i180.accounting_template()
    rows = template["records"]
    assert len(rows) == 2
    assert {row["parameter"] for row in rows} == set(i180.ACCOUNTING_PARAMETERS)
    assert all(row["value"] is None for row in rows)
    assert all(row["source_kind"] is None for row in rows)
    assert all(row["source_ref"] is None for row in rows)
    assert all(row["observed_at"] is None for row in rows)
    assert all(row["max_age_seconds"] is None for row in rows)
    assert all(row["source_content_digest"] is None for row in rows)
    assert i180._accounting_contract_complete(template) is False


def test_write_package_round_trips_exact_generators(tmp_path):
    paths = i180.write_package(tmp_path)
    assert len(paths) == 3
    measurement = json.loads((tmp_path / i180.MEASUREMENT_TEMPLATE_NAME).read_text(encoding="utf-8"))
    accounting = json.loads((tmp_path / i180.ACCOUNTING_TEMPLATE_NAME).read_text(encoding="utf-8"))
    readme = (tmp_path / i180.INSTRUCTIONS_NAME).read_text(encoding="utf-8")
    assert measurement == i180.measurement_template()
    assert accounting == i180.accounting_template()
    assert "do not estimate energy" in readme.lower()
    assert "i178" in readme
    assert "i179" in readme


def test_binding_helper_accepts_exact_bytes_and_rejects_drift():
    data = b"exact-local-source\n"
    expected = i180.git_blob_sha(data)
    exact = i180._binding_from_data("implementation/example.py", expected, data)
    changed = i180._binding_from_data("implementation/example.py", expected, data + b"changed")
    missing = i180._binding_from_data("implementation/example.py", expected, None)
    assert exact.present is True and exact.exact is True
    assert changed.present is True and changed.exact is False
    assert missing.present is False and missing.exact is False


def test_runtime_source_drift_fails_closed(tmp_path):
    implementation = tmp_path / "implementation"
    implementation.mkdir()
    (tmp_path / i180.I178_PATH).write_text("changed", encoding="utf-8")
    (tmp_path / i180.I179_PATH).write_text("changed", encoding="utf-8")
    package_dir = implementation / "user_pc_handoff"
    i180.write_package(package_dir)
    report = i180.inspect_package(tmp_path, package_dir=package_dir)
    assert report.state == "PASS_BLOCKED"
    assert any(blocker.startswith("runtime_source_blob_mismatch:") for blocker in report.blockers)
    assert report.measurement_template_rejected_by_bound_i178_contract is True
    assert report.accounting_template_rejected_by_bound_i178_contract is True
    assert report.real_chain_ready is False
    assert report.i050_execution_allowed is False
    assert report.i123_promotion_allowed is False


def test_filled_structure_can_be_complete_but_is_not_created_by_i180():
    measurement = {field: 1 for field in i180.MEASUREMENT_FIELDS}
    accounting = {
        "records": [
            {
                "parameter": parameter,
                "value": 0,
                "source_kind": "user_declared",
                "source_ref": "owner-entry",
                "observed_at": "2026-08-24T09:00:00Z",
                "max_age_seconds": 86400,
                "source_content_digest": None,
            }
            for parameter in i180.ACCOUNTING_PARAMETERS
        ]
    }
    assert i180._measurement_contract_complete(measurement) is True
    assert i180._accounting_contract_complete(accounting) is True
    assert all(value is None for value in i180.measurement_template().values())
    assert all(row["value"] is None for row in i180.accounting_template()["records"])
