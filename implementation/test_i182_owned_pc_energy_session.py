from pathlib import Path

import i182_owned_pc_energy_session as i182


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _counter(tmp_path: Path, initial: int = 1_000_000) -> Path:
    path = tmp_path / "sys" / "class" / "powercap" / "intel-rapl:0" / "energy_uj"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(initial) + "\n", encoding="utf-8")
    (path.parent / "name").write_text("package-0\n", encoding="utf-8")
    (path.parent / "max_energy_range_uj").write_text("999999999999\n", encoding="utf-8")
    return path


def _incrementing_execute(monkeypatch, counter: Path, increment_uj: int = 1000):
    original = i182.i173.execute

    def wrapped(payload):
        result = original(payload)
        current = int(counter.read_text(encoding="utf-8").strip())
        counter.write_text(str(current + increment_uj) + "\n", encoding="utf-8")
        return result

    monkeypatch.setattr(i182.i173, "execute", wrapped)


def test_fixture_root_can_measure_but_never_become_real_evidence(tmp_path, monkeypatch):
    counter = _counter(tmp_path)
    _incrementing_execute(monkeypatch, counter)

    result = i182.run_energy_session(
        repo_root=_repo_root(), fs_root=tmp_path,
        counter_path="/sys/class/powercap/intel-rapl:0/energy_uj",
        task_count=100, confirm_user_owned_pc=True,
    )

    assert result.state == "TEST_ONLY_COUNTER_SESSION_COMPLETE"
    assert result.successful_tasks == 100
    assert result.energy_delta_joules == 0.1
    assert result.energy_kwh_per_task is not None and result.energy_kwh_per_task > 0
    assert result.evidence_eligible is False
    body = i182.payload(result)
    assert body["measurement_fragment"]["energy_before_joules"] is None
    assert body["measurement_fragment"]["energy_source_ref"] is None
    assert result.network_enabled is False
    assert result.subprocess_used is False


def test_missing_ownership_confirmation_blocks_before_counter_read(tmp_path):
    _counter(tmp_path)
    result = i182.run_energy_session(
        repo_root=_repo_root(), fs_root=tmp_path,
        counter_path="/sys/class/powercap/intel-rapl:0/energy_uj",
        task_count=100, confirm_user_owned_pc=False,
    )
    assert result.state == "PASS_BLOCKED"
    assert "explicit_user_owned_pc_confirmation_required" in result.blockers
    assert result.energy_before_joules is None


def test_non_i181_counter_path_is_rejected(tmp_path):
    arbitrary = tmp_path / "tmp" / "energy_uj"
    arbitrary.parent.mkdir(parents=True, exist_ok=True)
    arbitrary.write_text("1000\n", encoding="utf-8")
    result = i182.run_energy_session(
        repo_root=_repo_root(), fs_root=tmp_path,
        counter_path="/tmp/energy_uj", task_count=100,
        confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "counter_not_approved_by_i181_inventory" in result.blockers


def test_zero_delta_fails_closed(tmp_path):
    _counter(tmp_path)
    result = i182.run_energy_session(
        repo_root=_repo_root(), fs_root=tmp_path,
        counter_path="/sys/class/powercap/intel-rapl:0/energy_uj",
        task_count=100, confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "zero_energy_delta_counter_resolution_insufficient" in result.blockers
    assert result.evidence_eligible is False


def test_counter_wrap_or_reset_is_not_normalized_into_evidence(tmp_path, monkeypatch):
    counter = _counter(tmp_path, initial=10_000_000)
    original = i182.i173.execute
    calls = {"n": 0}

    def wrapped(payload):
        result = original(payload)
        calls["n"] += 1
        if calls["n"] == 100:
            counter.write_text("100\n", encoding="utf-8")
        return result

    monkeypatch.setattr(i182.i173, "execute", wrapped)
    result = i182.run_energy_session(
        repo_root=_repo_root(), fs_root=tmp_path,
        counter_path="/sys/class/powercap/intel-rapl:0/energy_uj",
        task_count=100, confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "counter_wrap_or_reset_detected_rerun_shorter_session" in result.blockers
    assert result.energy_kwh_per_task is None


def test_i173_source_drift_blocks_session_before_execution(tmp_path):
    counter = _counter(tmp_path)
    fake_repo = tmp_path / "repo"
    target = fake_repo / i182.I173_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# drift\n", encoding="utf-8")
    result = i182.run_energy_session(
        repo_root=fake_repo, fs_root=tmp_path,
        counter_path="/sys/class/powercap/intel-rapl:0/energy_uj",
        task_count=100, confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "i173_source_blob_mismatch" in result.blockers
    assert result.successful_tasks == 0


def test_too_short_session_is_rejected_for_counter_resolution(tmp_path):
    _counter(tmp_path)
    result = i182.run_energy_session(
        repo_root=_repo_root(), fs_root=tmp_path,
        counter_path="/sys/class/powercap/intel-rapl:0/energy_uj",
        task_count=99, confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "task_count_must_be_at_least_100_for_counter_resolution" in result.blockers
