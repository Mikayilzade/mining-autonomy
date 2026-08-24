from pathlib import Path

import i181_local_energy_interface_inventory as i181


def _write(path: Path, text: str = "1\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_linux_powercap_energy_counter_is_candidate_without_reading_energy_value(tmp_path):
    base = tmp_path / "sys" / "class" / "powercap" / "intel-rapl:0"
    _write(base / "energy_uj", "123456\n")
    _write(base / "name", "package-0\n")
    _write(base / "max_energy_range_uj", "262143328850\n")

    result = i181.inventory_local_energy_interfaces(root=tmp_path, system="Linux")

    assert result.state == "CUMULATIVE_COUNTER_CANDIDATES_FOUND"
    assert result.direct_i166_candidate_count == 1
    row = result.candidates[0]
    assert row.interface_kind == "linux_powercap_energy_uj"
    assert row.cumulative_counter is True
    assert row.i166_before_after_candidate is True
    assert row.metadata["name"] == "package-0"
    assert row.metadata["max_energy_range_uj"] == "262143328850"
    assert result.energy_value_read is False
    assert result.evidence_created is False


def test_hwmon_energy_input_is_candidate_but_power_input_is_not(tmp_path):
    device = tmp_path / "sys" / "class" / "hwmon" / "hwmon0"
    _write(device / "name", "fakechip\n")
    _write(device / "energy1_input", "1000\n")
    _write(device / "power1_input", "50000\n")

    result = i181.inventory_local_energy_interfaces(root=tmp_path, system="Linux")

    assert result.state == "CUMULATIVE_COUNTER_CANDIDATES_FOUND"
    by_kind = {row.interface_kind: row for row in result.candidates}
    assert by_kind["linux_hwmon_energy_input"].i166_before_after_candidate is True
    assert by_kind["linux_hwmon_power_input"].i166_before_after_candidate is False
    assert by_kind["linux_hwmon_power_input"].cumulative_counter is False


def test_battery_energy_now_is_not_promoted_to_workload_counter(tmp_path):
    supply = tmp_path / "sys" / "class" / "power_supply" / "BAT0"
    _write(supply / "energy_now", "42000000\n")
    _write(supply / "type", "Battery\n")

    result = i181.inventory_local_energy_interfaces(root=tmp_path, system="Linux")

    assert result.state == "ONLY_NON_DIRECT_OR_UNREADABLE_INTERFACES_FOUND"
    assert result.direct_i166_candidate_count == 0
    assert len(result.candidates) == 1
    assert result.candidates[0].interface_kind == "linux_power_supply_energy_now"
    assert result.candidates[0].i166_before_after_candidate is False


def test_linux_without_known_interfaces_stays_explicitly_blocked(tmp_path):
    result = i181.inventory_local_energy_interfaces(root=tmp_path, system="Linux")

    assert result.state == "NO_SUPPORTED_LOCAL_ENERGY_INTERFACE_FOUND"
    assert result.candidates == ()
    assert "no_known_powercap_hwmon_or_power_supply_energy_interface_found" in result.blockers
    assert result.evidence_created is False


def test_windows_does_not_invent_a_stdlib_energy_counter(tmp_path):
    result = i181.inventory_local_energy_interfaces(root=tmp_path, system="Windows")

    assert result.state == "NO_SUPPORTED_LOCAL_ENERGY_INTERFACE_FOUND"
    assert result.candidates == ()
    assert "no_supported_stdlib_cumulative_energy_counter_detector_for_windows" in result.blockers
    assert result.subprocess_used is False
    assert result.software_installed is False
    assert result.elevated_privileges_requested is False


def test_macos_stays_blocked_without_subprocess_or_privilege_escalation(tmp_path):
    result = i181.inventory_local_energy_interfaces(root=tmp_path, system="Darwin")

    assert result.state == "NO_SUPPORTED_LOCAL_ENERGY_INTERFACE_FOUND"
    assert "no_supported_inert_cumulative_energy_counter_detector_for_macos" in result.blockers
    assert result.network_enabled is False
    assert result.credentials_used is False
    assert result.subprocess_used is False
    assert result.spend_or_value_movement is False
