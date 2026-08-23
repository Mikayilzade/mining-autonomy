"""I142 market-source evidence gate for bounded read-only observation.

Offline evaluator only. It consumes already-collected source facts and refuses to
promote a source when current policy/economics facts conflict or required observation
facts are missing. It performs no network access.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable

@dataclass(frozen=True)
class SourceFact:
    field: str
    value: str
    source_ref: str
    observed_date: str

@dataclass(frozen=True)
class SourceEvidenceDecision:
    platform: str
    state: str
    blockers: tuple[str, ...]
    conflicting_fields: tuple[str, ...]
    required_fields_present: tuple[str, ...]
    network_enabled: bool=False
    credentials_enabled: bool=False
    spend_enabled: bool=False
    task_acceptance_enabled: bool=False
    value_movement_enabled: bool=False

REQUIRED_FIELDS=(
    "task_list_read_auth_requirement",
    "task_detail_read_auth_requirement",
    "platform_fee_rate",
    "payout_to_worker_rate",
    "rate_limit_or_minimum_interval",
    "geography_access_rule",
    "automation_permission",
)

def assess_source(platform: str, facts: Iterable[SourceFact]) -> SourceEvidenceDecision:
    fs=tuple(facts)
    by_field={}
    for fact in fs:
        by_field.setdefault(fact.field, []).append(fact)
    conflicts=[]
    for field, rows in by_field.items():
        values={r.value.strip() for r in rows}
        if len(values)>1:
            conflicts.append(field)
    present=tuple(f for f in REQUIRED_FIELDS if f in by_field)
    blockers=[]
    for f in REQUIRED_FIELDS:
        if f not in by_field:
            blockers.append(f"missing_required_fact:{f}")
    blockers.extend(f"conflicting_fact:{f}" for f in sorted(conflicts))
    return SourceEvidenceDecision(
        platform=platform,
        state="SOURCE_READY_FOR_OBSERVATION_DESIGN" if not blockers else "HOLD",
        blockers=tuple(blockers),
        conflicting_fields=tuple(sorted(conflicts)),
        required_fields_present=present,
    )

def payload(result: SourceEvidenceDecision)->dict:
    body=asdict(result)
    body.update({"schema":"mining-autonomy/i142-market-source-evidence-gate/v1","run":"I142","production_observation_performed":False})
    return body
