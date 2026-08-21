"""I057 deterministic local calibration session bundle and offline replay/report.

Wraps the I056 python_local portable probe transcript in a collector-bound session.
No market/network calls, credentials, spend, or value movement occur here.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
import argparse, json
from pathlib import Path
from typing import Any, Mapping, Optional

from python_local_calibration_fixture import (
    BENCHMARK_ID, EXPECTED_OUTPUT_DIGEST, replay_python_local_transcript,
    run_python_local_fixture, transcript_to_json,
)
from resource_evidence_adapter import (
    EnergyMeasurement, ExplicitDeclaration, build_resource_evidence,
    normalize_probe_summary_for_evidence,
)
from resource_router import ExecutionBackend, default_backend_families

FORMAT_VERSION=1
DECLARATION_PARAMETERS=("requires_credentials","requires_paid_account","requires_new_spend","fixed_monthly_cost_usd","sunk_or_already_committed","quota_units_remaining","rate_limit_per_minute")

def _json(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def _hash(v:str): return sha256(v.encode("utf-8")).hexdigest()
def _utc(v:str):
    if not isinstance(v,str) or not v.endswith("Z"): raise ValueError("utc_timestamp_z_required")
    try: d=datetime.fromisoformat(v[:-1]+"+00:00")
    except Exception as e: raise ValueError("invalid_utc_timestamp") from e
    if d.tzinfo is None or d.utcoffset()!=timezone.utc.utcoffset(d): raise ValueError("utc_timestamp_required")
    return d

@dataclass(frozen=True)
class DeclarationSlot:
    parameter:str; value:Any=None; observed_at:Optional[str]=None; max_age_seconds:int=86400; source_ref:Optional[str]=None; notes:str=""
@dataclass(frozen=True)
class EnergySlot:
    energy_kwh_per_task:Optional[float]=None; tariff_usd_per_kwh:Optional[float]=None; observed_at:Optional[str]=None; max_age_seconds:int=604800; source_ref:Optional[str]=None; source_content_digest:Optional[str]=None; notes:str=""
@dataclass(frozen=True)
class LocalCalibrationSession:
    format_version:int; backend_id:str; reference_backend_hash:str; benchmark_id:str; expected_output_digest:str
    collector_observed_at_utc:str; transcript_filename:str; transcript_file_digest:str; transcript_json:str
    declaration_slots:tuple[DeclarationSlot,...]; energy_slot:EnergySlot; immutable_session_digest:str
    collection_opt_in_required:bool=True; network_enabled:bool=False; credentials_used:bool=False; spend_performed:bool=False; value_movement_enabled:bool=False
@dataclass(frozen=True)
class SessionReplayReport:
    backend_id:str; state:str; transcript_verified:bool; transcript_file_digest:str; immutable_session_digest:str; collector_observed_at_utc:str
    probe_observation_count:int; probe_successful_runs:int; probe_latency_p95_seconds:float
    emitted_parameters:tuple[str,...]; missing_parameters:tuple[str,...]; source_kinds:tuple[str,...]; complete_for_attestation:bool; notes:tuple[str,...]
    execution_enabled:bool=False; network_enabled:bool=False; value_movement_enabled:bool=False

def _identity(s):
    return {"format_version":FORMAT_VERSION,"backend_id":s[0],"reference_backend_hash":s[1],"benchmark_id":BENCHMARK_ID,"expected_output_digest":EXPECTED_OUTPUT_DIGEST,"collector_observed_at_utc":s[2],"transcript_filename":s[3],"transcript_file_digest":s[4]}
def _slots():
    ages={"fixed_monthly_cost_usd":2592000,"sunk_or_already_committed":2592000,"requires_credentials":604800,"requires_paid_account":604800,"requires_new_spend":604800}
    return tuple(DeclarationSlot(p,max_age_seconds=ages.get(p,86400)) for p in DECLARATION_PARAMETERS)

def build_session_bundle(reference_backend:ExecutionBackend,raw_transcript_json:str,*,collector_observed_at_utc:str,transcript_filename:str="python_local_probe_transcript.json"):
    _utc(collector_observed_at_utc)
    if not transcript_filename or Path(transcript_filename).name!=transcript_filename: raise ValueError("plain_transcript_filename_required")
    replay=replay_python_local_transcript(reference_backend,raw_transcript_json)
    fd=_hash(raw_transcript_json)
    ident=_identity((replay.plan.backend_id,replay.plan.reference_backend_hash,collector_observed_at_utc,transcript_filename,fd))
    return LocalCalibrationSession(FORMAT_VERSION,replay.plan.backend_id,replay.plan.reference_backend_hash,BENCHMARK_ID,EXPECTED_OUTPUT_DIGEST,collector_observed_at_utc,transcript_filename,fd,raw_transcript_json,_slots(),EnergySlot(),_hash(_json(ident)))

def session_to_json(s): return json.dumps(asdict(s),sort_keys=True,indent=2,ensure_ascii=False)+"\n"
def session_from_json(raw):
    try: d=json.loads(raw)
    except Exception as e: raise ValueError("invalid_session_json") from e
    if not isinstance(d,Mapping) or d.get("format_version")!=FORMAT_VERSION: raise ValueError("unsupported_session_format")
    rows=d.get("declaration_slots")
    if not isinstance(rows,list): raise ValueError("declaration_slots_required")
    slots=tuple(DeclarationSlot(**r) for r in rows)
    if tuple(x.parameter for x in slots)!=DECLARATION_PARAMETERS: raise ValueError("declaration_template_shape_mismatch")
    return LocalCalibrationSession(FORMAT_VERSION,str(d.get("backend_id") or ""),str(d.get("reference_backend_hash") or ""),str(d.get("benchmark_id") or ""),str(d.get("expected_output_digest") or ""),str(d.get("collector_observed_at_utc") or ""),str(d.get("transcript_filename") or ""),str(d.get("transcript_file_digest") or ""),str(d.get("transcript_json") or ""),slots,EnergySlot(**dict(d.get("energy_slot") or {})),str(d.get("immutable_session_digest") or ""),bool(d.get("collection_opt_in_required",True)),bool(d.get("network_enabled")),bool(d.get("credentials_used")),bool(d.get("spend_performed")),bool(d.get("value_movement_enabled")))

def _declarations(s):
    out=[]
    for x in s.declaration_slots:
        if x.value is None and x.observed_at is None and x.source_ref is None: continue
        if x.observed_at is None or x.source_ref is None: raise ValueError(f"incomplete_declaration_slot:{x.parameter}")
        _utc(x.observed_at)
        out.append(ExplicitDeclaration(x.parameter,x.value,x.observed_at,x.max_age_seconds,x.source_ref,x.notes))
    return tuple(out)
def _energy(s):
    x=s.energy_slot; fields=(x.energy_kwh_per_task,x.tariff_usd_per_kwh,x.observed_at,x.source_ref,x.source_content_digest)
    if not any(v is not None for v in fields): return None
    if any(v is None for v in fields): raise ValueError("incomplete_energy_slot")
    _utc(str(x.observed_at))
    return EnergyMeasurement(float(x.energy_kwh_per_task),float(x.tariff_usd_per_kwh),str(x.observed_at),x.max_age_seconds,str(x.source_ref),str(x.source_content_digest),x.notes)

def replay_session_bundle(reference_backend:ExecutionBackend,raw_session_json:str):
    s=session_from_json(raw_session_json); _utc(s.collector_observed_at_utc)
    if s.network_enabled or s.credentials_used or s.spend_performed or s.value_movement_enabled: raise ValueError("session_not_inert")
    replay=replay_python_local_transcript(reference_backend,s.transcript_json)
    if s.backend_id!=replay.plan.backend_id: raise ValueError("session_backend_mismatch")
    if s.reference_backend_hash!=replay.plan.reference_backend_hash: raise ValueError("session_reference_hash_mismatch")
    if s.benchmark_id!=BENCHMARK_ID or s.expected_output_digest!=EXPECTED_OUTPUT_DIGEST: raise ValueError("session_benchmark_binding_mismatch")
    if _hash(s.transcript_json)!=s.transcript_file_digest: raise ValueError("transcript_file_digest_mismatch")
    ident=_identity((s.backend_id,s.reference_backend_hash,s.collector_observed_at_utc,s.transcript_filename,s.transcript_file_digest))
    if _hash(_json(ident))!=s.immutable_session_digest: raise ValueError("immutable_session_digest_mismatch")
    summary=normalize_probe_summary_for_evidence(replay.probe_summary,observed_at_utc=s.collector_observed_at_utc)
    ev=build_resource_evidence(replay.plan,probe_summary=summary,declarations=_declarations(s),energy_measurement=_energy(s))
    notes=[]
    if not ev.complete_for_attestation: notes.append("missing resource facts remain explicit; no synthetic reference values were copied")
    if "electricity_per_task_usd" in ev.missing_parameters: notes.append("energy cost remains unknown until measured or explicitly declared")
    return SessionReplayReport(s.backend_id,"evidence_ready_for_attestation" if ev.complete_for_attestation else "planning_only",True,s.transcript_file_digest,s.immutable_session_digest,s.collector_observed_at_utc,replay.probe_summary.observation_count,replay.probe_summary.successful_runs,replay.probe_summary.latency_p95_seconds,ev.emitted_parameters,ev.missing_parameters,ev.source_kinds,ev.complete_for_attestation,tuple(notes))

def _reference(): return next(x for x in default_backend_families() if x.backend_id=="python_local")
def main(argv=None):
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    c=sub.add_parser("create"); c.add_argument("--enable-probe",action="store_true"); c.add_argument("--observed-at-utc",required=True); c.add_argument("--output",required=True); c.add_argument("--repetitions",type=int,default=10)
    r=sub.add_parser("replay"); r.add_argument("bundle"); a=p.parse_args(argv); ref=_reference()
    if a.cmd=="create":
        t=run_python_local_fixture(ref,enabled=a.enable_probe,repetitions=a.repetitions); Path(a.output).write_text(session_to_json(build_session_bundle(ref,transcript_to_json(t),collector_observed_at_utc=a.observed_at_utc)),encoding="utf-8"); return 0
    print(json.dumps(asdict(replay_session_bundle(ref,Path(a.bundle).read_text(encoding="utf-8"))),sort_keys=True,indent=2,ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())
