import i182_windows_emi_preflight as i182


def test_non_windows_is_inert():
    result = i182.preflight_windows_emi(system="Linux", counter=lambda: 99)
    assert result.state == "NOT_WINDOWS"
    assert result.candidate_count == 0
    assert result.energy_value_read is False
    assert result.evidence_created is False


def test_windows_candidate_is_discovery_only():
    result = i182.preflight_windows_emi(system="Windows", counter=lambda: 2)
    assert result.state == "EMI_DEVICE_CANDIDATES_FOUND"
    assert result.candidate_count == 2
    assert result.energy_value_read is False
    assert result.evidence_created is False
    assert result.subprocess_used is False
    assert result.elevated_privileges_requested is False


def test_windows_without_candidate_stays_blocked():
    result = i182.preflight_windows_emi(system="Windows", counter=lambda: 0)
    assert result.state == "NO_EMI_DEVICE_INTERFACE_FOUND"
    assert "no_present_windows_emi_device_interface" in result.blockers


def test_discovery_failure_fails_closed():
    def fail():
        raise OSError("no setupapi")
    result = i182.preflight_windows_emi(system="Windows", counter=fail)
    assert result.state == "EMI_DISCOVERY_FAILED"
    assert result.candidate_count == 0
    assert result.energy_value_read is False


def test_negative_candidate_count_is_rejected():
    result = i182.preflight_windows_emi(system="Windows", counter=lambda: -1)
    assert result.state == "EMI_DISCOVERY_FAILED"


def test_payload_preserves_no_value_movement_boundary():
    body = i182.payload(i182.preflight_windows_emi(system="Windows", counter=lambda: 1))
    assert body["schema"] == i182.SCHEMA
    assert body["network_enabled"] is False
    assert body["credentials_used"] is False
    assert body["software_installed"] is False
    assert body["spend_or_value_movement"] is False
