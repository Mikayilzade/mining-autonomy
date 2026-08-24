from dataclasses import dataclass
import json

import i179_user_pc_real_chain_runner as i179


def _handoff(ready=True):
    return i179.i178.HandoffReport(
        state="READY_TO_RUN_REAL_LOCAL_CHAIN" if ready else "HANDOFF_INPUTS_BLOCKED",
        blockers=() if ready else ("measurement_json_not_supplied",),
        source_checks=(),
        measurement_input=i179.i178.InputCheck("measurement_json", True, ready, ()),
        accounting_input=i179.i178.InputCheck("accounting_json", True, ready, ()),
        ownership_confirmation_supplied=True,
        exact_source_tree_ready=True,
        ready_to_run_real_chain=ready,
    )


def _write_inputs(tmp_path):
    measurement = tmp_path / "measurement.json"
    accounting = tmp_path / "accounting.json"
    measurement.write_text(json.dumps({"x": 1}), encoding="utf-8")
    accounting.write_text(json.dumps({
        "records": [
            {
                "parameter": "fixed_monthly_cost_usd",
                "value": 0.0,
                "source_kind": "user_declared",
                "source_ref": "owner-accounting:fixed",
                "observed_at": "2026-08-24T09:00:00Z",
                "max_age_seconds": 100,
            },
            {
                "parameter": "sunk_or_already_committed",
                "value": True,
                "source_kind": "user_declared",
                "source_ref": "owner-accounting:sunk",
                "observed_at": "2026-08-24T09:00:00Z",
                "max_age_seconds": 100,
            },
        ]
    }), encoding="utf-8")
    return measurement, accounting


@dataclass(frozen=True)
class _Bridge:
    state: str = "ROUTER_RESOURCE_FACTS_READY"
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Adapter:
    state: str = "PARTIAL_I050_EVIDENCE_READY"
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Proof:
    state: str = "EXACT_EXECUTOR_INTERFACE_PROVED"
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Binding:
    state: str = "PRODUCTION_INTERFACE_CONTROLS_READY"
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class _Assembly:
    state: str
    errors: tuple[str, ...] = ()
    strict_i050_execution_ready: bool = False
    declared_accounting_boundary_reached: bool = False


def _patch_to_assembly(monkeypatch, assembly):
    monkeypatch.setattr(i179.i178, "inspect_handoff", lambda *args, **kwargs: _handoff(True))
    monkeypatch.setattr(i179.i166, "gate_and_materialize", lambda *args, **kwargs: {
        "gate": {"state": "REAL_EXTERNAL_EVIDENCE_ACCEPTED"},
        "i165_result": {"state": "USER_PC_MATERIALIZED"},
    })
    monkeypatch.setattr(i179.i167, "build_bridge", lambda *args, **kwargs: _Bridge())
    monkeypatch.setattr(i179, "_owned_pc_reference", lambda: {"backend_id": "owned_pc"})
    monkeypatch.setattr(i179.i168, "build_adapter", lambda *args, **kwargs: _Adapter())
    monkeypatch.setattr(i179.i174, "TARGET_PATH", "executor.py")
    monkeypatch.setattr(i179.i174, "inspect_source", lambda *args, **kwargs: _Proof())
    monkeypatch.setattr(i179.i175, "bind_interface_proof", lambda *args, **kwargs: _Binding())
    monkeypatch.setattr(i179.i177, "assemble_for_i169", lambda *args, **kwargs: assembly)


def test_handoff_block_stops_before_i166(tmp_path, monkeypatch):
    measurement, accounting = _write_inputs(tmp_path)
    monkeypatch.setattr(i179.i178, "inspect_handoff", lambda *args, **kwargs: _handoff(False))
    called = {"i166": False}
    monkeypatch.setattr(i179.i166, "gate_and_materialize", lambda *args, **kwargs: called.__setitem__("i166", True))
    result = i179.run_real_local_chain(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        observed_at="2026-08-24T09:00:00Z",
        confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert "i178_handoff_not_ready" in result.blockers
    assert called["i166"] is False
    assert result.i050_executed is False
    assert result.i123_executed is False


def test_i166_failure_stops_downstream(tmp_path, monkeypatch):
    measurement, accounting = _write_inputs(tmp_path)
    monkeypatch.setattr(i179.i178, "inspect_handoff", lambda *args, **kwargs: _handoff(True))
    monkeypatch.setattr(i179.i166, "gate_and_materialize", lambda *args, **kwargs: {
        "gate": {"state": "PASS_BLOCKED"},
        "i165_result": None,
    })
    result = i179.run_real_local_chain(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        observed_at="2026-08-24T09:00:00Z",
        confirm_user_owned_pc=True,
    )
    assert result.state == "PASS_BLOCKED"
    assert result.blockers == ("i166_real_external_evidence_not_accepted",)
    assert result.i167_result is None


def test_declared_accounting_boundary_never_applies_hybrid_patch(tmp_path, monkeypatch):
    measurement, accounting = _write_inputs(tmp_path)
    (tmp_path / "executor.py").write_text("# exact source is mocked at this orchestration layer\n", encoding="utf-8")
    _patch_to_assembly(monkeypatch, _Assembly(
        state="ASSEMBLED_DECLARED_ACCOUNTING_BOUNDARY",
        declared_accounting_boundary_reached=True,
    ))
    result = i179.run_real_local_chain(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        observed_at="2026-08-24T09:00:00Z",
        confirm_user_owned_pc=True,
    )
    assert result.state == "REAL_CHAIN_DECLARED_ACCOUNTING_BOUNDARY"
    assert result.declared_accounting_boundary_reached is True
    assert result.exact_i050_ready is False
    assert result.hybrid_patch_applied is False
    assert result.i050_executed is False
    assert result.i066_executed is False
    assert result.i123_executed is False


def test_strict_assembly_reaches_only_separate_i050_gate(tmp_path, monkeypatch):
    measurement, accounting = _write_inputs(tmp_path)
    (tmp_path / "executor.py").write_text("# exact source is mocked at this orchestration layer\n", encoding="utf-8")
    _patch_to_assembly(monkeypatch, _Assembly(
        state="ASSEMBLED_READY_FOR_EXACT_I050",
        strict_i050_execution_ready=True,
    ))
    result = i179.run_real_local_chain(
        tmp_path,
        measurement_json=measurement,
        accounting_json=accounting,
        observed_at="2026-08-24T09:00:00Z",
        confirm_user_owned_pc=True,
    )
    assert result.state == "REAL_CHAIN_READY_FOR_SEPARATE_EXACT_I050"
    assert result.blockers == ()
    assert result.exact_i050_ready is True
    assert result.i050_executed is False
    assert result.i066_executed is False
    assert result.i123_executed is False
    assert result.production_execution_enabled is False
