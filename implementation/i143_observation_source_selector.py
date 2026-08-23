"""I143 deterministic selector for already-shortlisted observation sources."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Optional
from i142_market_source_evidence_gate import SourceEvidenceDecision

@dataclass(frozen=True)
class ObservationSourceCandidate:
    platform: str
    priority_rank: int
    server_native_machine_tasks: bool
    public_read_possible: bool
    expected_external_request_cost_usd: float

@dataclass(frozen=True)
class SourceSelection:
    state: str
    selected_platform: Optional[str]
    rejected: tuple[tuple[str,str], ...]
    discovery_reopened: bool=False
    network_enabled: bool=False
    spend_enabled: bool=False


def select(candidates: Iterable[ObservationSourceCandidate], evidence: Iterable[SourceEvidenceDecision])->SourceSelection:
    cs=tuple(candidates); em={e.platform:e for e in evidence}
    rejected=[]; eligible=[]
    for c in cs:
        e=em.get(c.platform)
        if not c.server_native_machine_tasks:
            rejected.append((c.platform,"not_priority_machine_task_market")); continue
        if not c.public_read_possible:
            rejected.append((c.platform,"public_read_not_available")); continue
        if c.expected_external_request_cost_usd != 0:
            rejected.append((c.platform,"paid_observation_not_allowed")); continue
        if e is None or e.state != "SOURCE_READY_FOR_OBSERVATION_DESIGN":
            rejected.append((c.platform,"source_evidence_not_ready")); continue
        eligible.append(c)
    eligible.sort(key=lambda c:(c.priority_rank,c.expected_external_request_cost_usd,c.platform))
    return SourceSelection(
        state="SOURCE_SELECTED" if eligible else "HOLD_SOURCE_EVIDENCE",
        selected_platform=eligible[0].platform if eligible else None,
        rejected=tuple(rejected),
    )

def payload(result:SourceSelection)->dict:
    body=asdict(result); body.update({"schema":"mining-autonomy/i143-observation-source-selector/v1","run":"I143","production_observation_performed":False}); return body
