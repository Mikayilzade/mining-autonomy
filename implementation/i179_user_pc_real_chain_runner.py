#!/usr/bin/env python3
"""I179 one-command inert runner for the real owned-PC evidence chain through I177.

I179 reduces the user-PC handoff to one local command while preserving every existing
fail-closed gate. It first runs I178 exact-source/input checks, then composes:
I166 -> I167 -> I168 -> I174 -> I175/I171 -> I177/I169.

It does not execute I050, I066 or I123, does not apply the I176 hybrid proposal and
does not contact a market. The supplied measurement/accounting JSON remains caller
owned evidence; I179 never fills, estimates or repairs missing facts.

No network, credentials, CI dispatch, account creation, paid infrastructure, market
observation, task acceptance/submission, spend, settlement, payment or value movement
is implemented.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path
from typing import Any, Mapping

import i166_user_pc_real_evidence_gate as i166
import i167_owned_pc_router_bridge as i167
import i168_owned_pc_i050_evidence_adapter as i168
import i174_exact_executor_interface_probe as i174
import i175_i171_production_scope_binding as i175
import i177_owned_pc_evidence_assembly as i177
import i178_user_pc_handoff_manifest as i178
import resource_router

SCHEMA = "mining-autonomy/i179-user-pc-real-chain-runner/v1"


@dataclass(frozen=True)
class ChainResult:
    state: str
    blockers: tuple[str, ...]
    handoff_report: dict[str, Any]
    i166_result: dict[str, Any] | None
    i167_result: dict[str, Any] | None
    i168_result: dict[str, Any] | None
    i174_result: dict[str, Any] | None
    i175_result: dict[str, Any] | None
    i177_result: dict[str, Any] | None
    exact_i050_ready: bool
    declared_accounting_boundary_reached: bool
    i050_executed: bool = False
    i066_executed: bool = False
    i123_executed: bool = False
    hybrid_patch_applied: bool = False
    network_enabled: bool = False
    credentials_used: bool = False
    ci_dispatched: bool = False
    spend_or_value_movement: bool = False
    production_execution_enabled: bool = False


def _load_object(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("json_object_required")
    return value


def _owned_pc_reference() -> Mapping[str, Any]:
    for backend in resource_router.default_backend_families():
        if backend.backend_id == "owned_pc":
            # This is an identity/reference model only. I168 is forbidden to turn
            # its synthetic cost/capacity defaults into evidence.
            return asdict(backend)
    raise RuntimeError("owned_pc_reference_backend_missing")


def _accounting_inputs(raw: Mapping[str, Any]) -> tuple[i177.AccountingEvidenceInput, ...]:
    rows = raw.get("records")
    if not isinstance(rows, list):
        raise ValueError("accounting_records_list_required")
    result: list[i177.AccountingEvidenceInput] = []
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("accounting_record_must_be_object")
        result.append(i177.AccountingEvidenceInput(
            parameter=str(row.get("parameter") or ""),
            value=row.get("value"),
            source_kind=str(row.get("source_kind") or ""),
            source_ref=str(row.get("source_ref") or ""),
            observed_at=str(row.get("observed_at") or ""),
            max_age_seconds=int(row.get("max_age_seconds") or 0),
            source_content_digest=row.get("source_content_digest"),
            notes=str(row.get("notes") or ""),
        ))
    return tuple(result)


def _blocked(report, *blockers: str) -> ChainResult:
    return ChainResult(
        state="PASS_BLOCKED",
        blockers=tuple(sorted(set(report.blockers) | set(blockers))),
        handoff_report=asdict(report),
        i166_result=None,
        i167_result=None,
        i168_result=None,
        i174_result=None,
        i175_result=None,
        i177_result=None,
        exact_i050_ready=False,
        declared_accounting_boundary_reached=False,
    )


def run_real_local_chain(
    root: Path,
    *,
    measurement_json: Path,
    accounting_json: Path,
    observed_at: str,
    confirm_user_owned_pc: bool,
    repetitions: int = 20,
    inner_iterations: int = 500,
    parallelism_cap: int = 8,
) -> ChainResult:
    handoff = i178.inspect_handoff(
        root,
        measurement_json=measurement_json,
        accounting_json=accounting_json,
        confirm_user_owned_pc=confirm_user_owned_pc,
    )
    if handoff.state != "READY_TO_RUN_REAL_LOCAL_CHAIN":
        return _blocked(handoff, "i178_handoff_not_ready")

    try:
        measurement_raw = _load_object(measurement_json)
        accounting_raw = _load_object(accounting_json)
    except Exception as exc:
        return _blocked(handoff, f"input_load_error:{type(exc).__name__}")

    i166_body = i166.gate_and_materialize(
        measurement_raw,
        confirm_user_owned_pc=True,
        repetitions=repetitions,
        inner_iterations=inner_iterations,
        parallelism_cap=parallelism_cap,
    )
    gate = i166_body.get("gate")
    materialized = i166_body.get("i165_result")
    if not isinstance(gate, Mapping) or gate.get("state") != "REAL_EXTERNAL_EVIDENCE_ACCEPTED":
        return ChainResult(
            state="PASS_BLOCKED", blockers=("i166_real_external_evidence_not_accepted",),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=None,
            i168_result=None, i174_result=None, i175_result=None, i177_result=None,
            exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )
    if not isinstance(materialized, Mapping) or materialized.get("state") != "USER_PC_MATERIALIZED":
        return ChainResult(
            state="PASS_BLOCKED", blockers=("i165_user_pc_materialization_not_complete",),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=None,
            i168_result=None, i174_result=None, i175_result=None, i177_result=None,
            exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )

    bridge = i167.build_bridge(i166_body)
    bridge_dict = asdict(bridge)
    if bridge.state != "ROUTER_RESOURCE_FACTS_READY":
        return ChainResult(
            state="PASS_BLOCKED", blockers=("i167_router_resource_facts_not_ready", *bridge.errors),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=bridge_dict,
            i168_result=None, i174_result=None, i175_result=None, i177_result=None,
            exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )

    adapter = i168.build_adapter(
        i166_body,
        bridge_dict,
        _owned_pc_reference(),
        observed_at=observed_at,
    )
    adapter_dict = asdict(adapter)
    if adapter.state != "PARTIAL_I050_EVIDENCE_READY":
        return ChainResult(
            state="PASS_BLOCKED", blockers=("i168_partial_i050_evidence_not_ready", *adapter.errors),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=bridge_dict,
            i168_result=adapter_dict, i174_result=None, i175_result=None, i177_result=None,
            exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )

    executor_path = root / i174.TARGET_PATH
    try:
        executor_source = executor_path.read_text(encoding="utf-8")
    except Exception as exc:
        return ChainResult(
            state="PASS_BLOCKED", blockers=(f"i173_source_read_error:{type(exc).__name__}",),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=bridge_dict,
            i168_result=adapter_dict, i174_result=None, i175_result=None, i177_result=None,
            exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )
    proof = i174.inspect_source(executor_source)
    proof_dict = asdict(proof)
    if proof.state != "EXACT_EXECUTOR_INTERFACE_PROVED":
        return ChainResult(
            state="PASS_BLOCKED", blockers=("i174_exact_executor_interface_not_proved", *proof.errors),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=bridge_dict,
            i168_result=adapter_dict, i174_result=proof_dict, i175_result=None, i177_result=None,
            exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )

    binding = i175.bind_interface_proof(proof_dict)
    binding_dict = asdict(binding)
    if binding.state != "PRODUCTION_INTERFACE_CONTROLS_READY":
        return ChainResult(
            state="PASS_BLOCKED", blockers=("i175_production_interface_controls_not_ready", *binding.errors),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=bridge_dict,
            i168_result=adapter_dict, i174_result=proof_dict, i175_result=binding_dict,
            i177_result=None, exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )

    try:
        accounting = _accounting_inputs(accounting_raw)
    except Exception as exc:
        return ChainResult(
            state="PASS_BLOCKED", blockers=(f"accounting_parse_error:{type(exc).__name__}",),
            handoff_report=asdict(handoff), i166_result=i166_body, i167_result=bridge_dict,
            i168_result=adapter_dict, i174_result=proof_dict, i175_result=binding_dict,
            i177_result=None, exact_i050_ready=False, declared_accounting_boundary_reached=False,
        )

    assembly = i177.assemble_for_i169(
        adapter_dict,
        binding_dict,
        accounting,
        observed_at=observed_at,
    )
    assembly_dict = asdict(assembly)
    exact_ready = assembly.state == "ASSEMBLED_READY_FOR_EXACT_I050" and assembly.strict_i050_execution_ready
    declared_boundary = assembly.state == "ASSEMBLED_DECLARED_ACCOUNTING_BOUNDARY" and assembly.declared_accounting_boundary_reached

    if exact_ready:
        state = "REAL_CHAIN_READY_FOR_SEPARATE_EXACT_I050"
        blockers: tuple[str, ...] = ()
    elif declared_boundary:
        state = "REAL_CHAIN_DECLARED_ACCOUNTING_BOUNDARY"
        blockers = ("current_strict_i050_i123_source_class_blocks_user_declared_accounting",)
    else:
        state = "PASS_BLOCKED"
        blockers = tuple(assembly.errors) or ("i177_assembly_not_ready",)

    return ChainResult(
        state=state,
        blockers=blockers,
        handoff_report=asdict(handoff),
        i166_result=i166_body,
        i167_result=bridge_dict,
        i168_result=adapter_dict,
        i174_result=proof_dict,
        i175_result=binding_dict,
        i177_result=assembly_dict,
        exact_i050_ready=exact_ready,
        declared_accounting_boundary_reached=declared_boundary,
    )


def payload(result: ChainResult) -> dict[str, Any]:
    body = asdict(result)
    body.update({
        "schema": SCHEMA,
        "run": "I179",
        "next_gate": (
            "REAL_CHAIN_READY_FOR_SEPARATE_EXACT_I050 authorizes only a separate exact I050 evidence-attestation "
            "attempt. REAL_CHAIN_DECLARED_ACCOUNTING_BOUNDARY remains blocked under current strict semantics; "
            "I176 is review-only and is not applied here. Any other state remains fail-closed."
        ),
    })
    return body


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--measurement-json", required=True)
    parser.add_argument("--accounting-json", required=True)
    parser.add_argument("--observed-at", required=True, help="Explicit UTC timestamp, e.g. 2026-08-24T09:00:00Z")
    parser.add_argument("--confirm-user-owned-pc", action="store_true")
    parser.add_argument("--repetitions", type=int, default=20)
    parser.add_argument("--inner-iterations", type=int, default=500)
    parser.add_argument("--parallelism-cap", type=int, default=8)
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    result = run_real_local_chain(
        Path(args.root),
        measurement_json=Path(args.measurement_json),
        accounting_json=Path(args.accounting_json),
        observed_at=args.observed_at,
        confirm_user_owned_pc=args.confirm_user_owned_pc,
        repetitions=args.repetitions,
        inner_iterations=args.inner_iterations,
        parallelism_cap=args.parallelism_cap,
    )
    text = json.dumps(payload(result), indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result.state in {
        "REAL_CHAIN_READY_FOR_SEPARATE_EXACT_I050",
        "REAL_CHAIN_DECLARED_ACCOUNTING_BOUNDARY",
    } else 2


if __name__ == "__main__":
    raise SystemExit(main())
