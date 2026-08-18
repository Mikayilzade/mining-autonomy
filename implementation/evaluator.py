"""Cross-market dry-run opportunity evaluator v0.2 (I005).

Offline/credentials-free by design. No external execution or settlement is implemented.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

REJECT = {
    "MALFORMED": "malformed_task", "PROHIBITED": "prohibited_task",
    "POLICY": "policy_evidence_insufficient", "UNSUPPORTED": "unsupported_capability",
    "PAYOUT_UNKNOWN": "unknown_payout", "NEGATIVE_MARGIN": "insufficient_expected_margin",
    "UNBOUNDED_COST": "unbounded_external_cost", "VALUE_ACTION": "requires_value_moving_action",
    "STALE": "stale_observation", "DEADLINE": "deadline_too_close", "DUPLICATE": "duplicate_opportunity",
}
PROHIBITED_MARKERS = {"captcha bypass", "fake clicks", "fake views", "spam", "credential theft", "ad fraud", "stolen account", "malware", "cryptojacking"}
TRUE_STATES = {"confirmed", "allowed", "yes"}

@dataclass
class Opportunity:
    platform: str; external_id: str; observed_at: str; kind: str; status: str
    title: Optional[str] = None; description: Optional[str] = None; tags: List[str] = field(default_factory=list)
    fixed_payout_usd: Optional[float] = None; currency: Optional[str] = None
    requires_auth_to_accept: bool = True; requires_value_moving_action: bool = False
    source_url: Optional[str] = None
    rights_status: str = "unknown"; tos_status: str = "unknown"; automation_allowed: str = "unknown"; source_data_permission: str = "unknown"
    estimated_input_tokens: int = 0; estimated_output_tokens: int = 0
    external_cost_cap_usd: Optional[float] = 0.0; deadline_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CostProfile:
    input_per_million: float = 1.0; output_per_million: float = 4.0; reserve_pct: float = 0.50
    min_margin_usd: float = 0.25; min_margin_ratio: float = 0.30

@dataclass
class CapabilityProfile:
    capabilities: Set[str] = field(default_factory=lambda: {"extract", "summarize", "research"})

@dataclass
class Decision:
    decision_id: str; opportunity_id: str; platform: str; decision: str; reject_reasons: List[str]
    payout_usd: Optional[float]; estimated_cost_usd: Optional[float]; reserved_cost_usd: Optional[float]
    expected_margin_usd: Optional[float]; dry_run_only: bool = True; settlement_enabled: bool = False

class SettlementAdapter:
    enabled = False
    def enable(self) -> None: raise RuntimeError("Settlement cannot be enabled in dry-run evaluator v0.2")
    def settle(self, *_: Any, **__: Any) -> None: raise RuntimeError("Settlement is hard-disabled in dry-run evaluator v0.2")

class MarketAdapter:
    platform = "generic"
    def adapt(self, payload: Dict[str, Any], observed_at: Optional[str] = None) -> Opportunity: raise NotImplementedError

def _now() -> datetime: return datetime.now(timezone.utc)
def _iso(v: str) -> datetime: return datetime.fromisoformat(v.replace("Z", "+00:00"))
def _text(o: Opportunity) -> str: return " ".join([o.title or "", o.description or "", *o.tags]).lower()
def _stable_hash(x: Any) -> str: return sha256(json.dumps(x, sort_keys=True, separators=(",", ":"), default=list).encode()).hexdigest()
def decision_id(o: Opportunity) -> str: return sha256(f"{o.platform}:{o.external_id}:{o.observed_at}".encode()).hexdigest()[:24]

def _common(platform: str, external_id: Any, observed_at: Optional[str], title: Any, description: Any, payout: Any, currency: Any, deadline: Any, metadata: Dict[str, Any]) -> Opportunity:
    return Opportunity(platform=platform, external_id=str(external_id or ""), observed_at=observed_at or _now().isoformat(), kind="paid_task", status="open",
        title=title, description=description, fixed_payout_usd=float(payout) if payout is not None else None, currency=str(currency).upper() if currency else None,
        deadline_at=deadline, rights_status=str(metadata.pop("rights_status", "unknown")), tos_status=str(metadata.pop("tos_status", "unknown")),
        automation_allowed=str(metadata.pop("automation_allowed", "unknown")), source_data_permission=str(metadata.pop("source_data_permission", "unknown")), metadata=metadata)

class PayanAgentAdapter(MarketAdapter):
    platform = "payanagent"
    def adapt(self, p: Dict[str, Any], observed_at: Optional[str] = None) -> Opportunity:
        m = dict(p.get("metadata", {})); m["required_capabilities"] = p.get("skills", p.get("required_capabilities", []))
        return _common(self.platform, p.get("id", p.get("request_id")), observed_at or p.get("observed_at"), p.get("title"), p.get("description", p.get("prompt")), p.get("bounty_usd", p.get("payout_usd")), p.get("currency", "USD"), p.get("deadline_at"), m)

class OKXA2AAdapter(MarketAdapter):
    platform = "okx_a2a"
    def adapt(self, p: Dict[str, Any], observed_at: Optional[str] = None) -> Opportunity:
        m = dict(p.get("metadata", {})); m["required_capabilities"] = p.get("skills", [])
        return _common(self.platform, p.get("task_id", p.get("id")), observed_at or p.get("observed_at"), p.get("title"), p.get("description"), p.get("budget_usd", p.get("bounty_usd")), p.get("currency", "USDC"), p.get("deadline_at"), m)

class Agent2AgentAdapter(MarketAdapter):
    platform = "agent2agent_market"
    def adapt(self, p: Dict[str, Any], observed_at: Optional[str] = None) -> Opportunity:
        m = dict(p.get("metadata", {})); m["required_capabilities"] = p.get("skills", p.get("tags", []))
        return _common(self.platform, p.get("task_id", p.get("id")), observed_at or p.get("observed_at"), p.get("title"), p.get("acceptance_criteria", p.get("description")), p.get("bounty", p.get("bounty_usd")), p.get("currency", "USDC"), p.get("deadline", p.get("deadline_at")), m)

ADAPTERS = {x.platform: x for x in (PayanAgentAdapter(), OKXA2AAdapter(), Agent2AgentAdapter())}

def estimate_cost(o: Opportunity, c: CostProfile) -> tuple[Optional[float], Optional[float]]:
    if o.external_cost_cap_usd is None: return None, None
    base = (o.estimated_input_tokens / 1_000_000) * c.input_per_million + (o.estimated_output_tokens / 1_000_000) * c.output_per_million + max(0.0, o.external_cost_cap_usd)
    return round(base, 6), round(base * (1 + c.reserve_pct), 6)

def evaluate(o: Opportunity, capabilities: CapabilityProfile | Set[str], cost: Optional[CostProfile] = None, *, now: Optional[datetime] = None, seen: Optional[Set[str]] = None, max_age_seconds: int = 86400, deadline_reserve_seconds: int = 900) -> Decision:
    c = cost or CostProfile(); caps = capabilities.capabilities if isinstance(capabilities, CapabilityProfile) else capabilities; reasons: List[str] = []
    if not all([o.platform, o.external_id, o.observed_at, o.kind, o.status]): reasons.append(REJECT["MALFORMED"])
    if any(x in _text(o) for x in PROHIBITED_MARKERS): reasons.append(REJECT["PROHIBITED"])
    if not (o.rights_status.lower() in TRUE_STATES and o.tos_status.lower() in TRUE_STATES and o.automation_allowed.lower() in TRUE_STATES and o.source_data_permission.lower() in TRUE_STATES): reasons.append(REJECT["POLICY"])
    if not set(o.metadata.get("required_capabilities", [])).issubset(caps): reasons.append(REJECT["UNSUPPORTED"])
    if o.fixed_payout_usd is None or o.fixed_payout_usd <= 0 or o.currency not in {"USD", "USDC"}: reasons.append(REJECT["PAYOUT_UNKNOWN"])
    if o.requires_value_moving_action: reasons.append(REJECT["VALUE_ACTION"])
    n = now or _now()
    try:
        if (n - _iso(o.observed_at)).total_seconds() > max_age_seconds: reasons.append(REJECT["STALE"])
        if o.deadline_at and (_iso(o.deadline_at) - n).total_seconds() < deadline_reserve_seconds: reasons.append(REJECT["DEADLINE"])
    except Exception: reasons.append(REJECT["MALFORMED"])
    key = f"{o.platform}:{o.external_id}"
    if seen is not None and key in seen: reasons.append(REJECT["DUPLICATE"])
    base, reserved = estimate_cost(o, c)
    if base is None: reasons.append(REJECT["UNBOUNDED_COST"])
    margin = None
    if o.fixed_payout_usd is not None and reserved is not None:
        margin = round(o.fixed_payout_usd - reserved, 6); ratio = margin / o.fixed_payout_usd if o.fixed_payout_usd > 0 else -1
        if margin < c.min_margin_usd or ratio < c.min_margin_ratio: reasons.append(REJECT["NEGATIVE_MARGIN"])
    reasons = list(dict.fromkeys(reasons)); did = decision_id(o)
    return Decision(did, o.external_id, o.platform, "accept_dry_run" if not reasons else "reject", reasons, o.fixed_payout_usd, base, reserved, margin)

class HashChainLedger:
    def __init__(self, path: str | Path): self.path = Path(path)
    def _last_hash(self) -> str:
        if not self.path.exists() or not self.path.read_text().strip(): return "GENESIS"
        return json.loads(self.path.read_text().splitlines()[-1])["record_hash"]
    def append(self, o: Opportunity, d: Decision) -> Dict[str, Any]:
        previous = self._last_hash(); body = {"recorded_at": _now().isoformat(), "decision_id": d.decision_id, "opportunity_hash": _stable_hash(asdict(o)), "opportunity": asdict(o), "decision": asdict(d), "previous_hash": previous}
        body["record_hash"] = _stable_hash(body)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f: f.write(json.dumps(body, sort_keys=True, default=list) + "\n")
        return body
    def verify(self) -> bool:
        previous = "GENESIS"
        if not self.path.exists(): return True
        for line in self.path.read_text().splitlines():
            r = json.loads(line); h = r.pop("record_hash", None)
            if r.get("previous_hash") != previous or _stable_hash(r) != h: return False
            previous = h
        return True

def dry_run_execute(o: Opportunity) -> Dict[str, Any]: return {"external_id": o.external_id, "executed": False, "mode": "dry_run", "artifact": None}
def validate_result(r: Dict[str, Any]) -> bool: return r.get("mode") == "dry_run" and r.get("executed") is False

def evaluate_payloads(platform: str, payloads: Iterable[Dict[str, Any]], capabilities: Optional[CapabilityProfile] = None, cost: Optional[CostProfile] = None) -> List[Decision]:
    adapter = ADAPTERS[platform]; seen: Set[str] = set(); out = []
    for p in payloads:
        o = adapter.adapt(p); d = evaluate(o, capabilities or CapabilityProfile(), cost, seen=seen); seen.add(f"{o.platform}:{o.external_id}"); out.append(d)
    return out
