"""Cross-market dry-run opportunity evaluator v0.1.

Credentials-free and value-movement-free by design. Settlement is hard disabled.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from hashlib import sha256
import json
from typing import Any, Dict, List, Optional, Set

REJECT = {
    "MALFORMED": "malformed_task",
    "PROHIBITED": "prohibited_task",
    "RIGHTS_UNKNOWN": "unknown_rights_or_tos",
    "UNSUPPORTED": "unsupported_capability",
    "PAYOUT_UNKNOWN": "unknown_payout",
    "NEGATIVE_MARGIN": "insufficient_expected_margin",
    "UNBOUNDED_COST": "unbounded_external_cost",
    "VALUE_ACTION": "requires_value_moving_action",
}

PROHIBITED_MARKERS = {
    "captcha bypass", "fake clicks", "fake views", "spam", "credential theft",
    "ad fraud", "stolen account", "malware", "cryptojacking"
}

@dataclass
class Opportunity:
    platform: str
    external_id: str
    observed_at: str
    kind: str
    status: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    fixed_payout_usd: Optional[float] = None
    currency: Optional[str] = None
    requires_auth_to_accept: bool = True
    requires_value_moving_action: bool = False
    source_url: Optional[str] = None
    rights_confirmed: bool = False
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    external_cost_cap_usd: Optional[float] = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Decision:
    opportunity_id: str
    platform: str
    decision: str
    reject_reasons: List[str]
    payout_usd: Optional[float]
    estimated_cost_usd: Optional[float]
    reserved_cost_usd: Optional[float]
    expected_margin_usd: Optional[float]
    dry_run_only: bool = True
    settlement_enabled: bool = False

class SettlementAdapter:
    enabled = False
    def settle(self, *_: Any, **__: Any) -> None:
        raise RuntimeError("Settlement is hard-disabled in dry-run evaluator v0.1")

def _text(o: Opportunity) -> str:
    return " ".join([o.title or "", o.description or "", *o.tags]).lower()

def validate(o: Opportunity) -> List[str]:
    missing = [k for k in ("platform", "external_id", "observed_at", "kind", "status") if not getattr(o, k)]
    return [REJECT["MALFORMED"]] if missing else []

def capability_match(o: Opportunity, capabilities: Set[str]) -> bool:
    required = set(o.metadata.get("required_capabilities", []))
    return required.issubset(capabilities)

def estimate_cost(o: Opportunity, input_per_million: float, output_per_million: float, reserve_pct: float) -> tuple[Optional[float], Optional[float]]:
    if o.external_cost_cap_usd is None:
        return None, None
    base = (o.estimated_input_tokens / 1_000_000) * input_per_million
    base += (o.estimated_output_tokens / 1_000_000) * output_per_million
    base += max(0.0, o.external_cost_cap_usd)
    reserved = base * (1 + reserve_pct)
    return round(base, 6), round(reserved, 6)

def evaluate(o: Opportunity, capabilities: Set[str], *, input_per_million: float = 1.0,
             output_per_million: float = 4.0, reserve_pct: float = 0.50,
             min_margin_usd: float = 0.25, min_margin_ratio: float = 0.30) -> Decision:
    reasons = validate(o)
    text = _text(o)
    if any(marker in text for marker in PROHIBITED_MARKERS): reasons.append(REJECT["PROHIBITED"])
    if not o.rights_confirmed: reasons.append(REJECT["RIGHTS_UNKNOWN"])
    if not capability_match(o, capabilities): reasons.append(REJECT["UNSUPPORTED"])
    if o.fixed_payout_usd is None or o.currency not in {"USD", "USDC"}: reasons.append(REJECT["PAYOUT_UNKNOWN"])
    if o.requires_value_moving_action: reasons.append(REJECT["VALUE_ACTION"])
    cost, reserved = estimate_cost(o, input_per_million, output_per_million, reserve_pct)
    if cost is None: reasons.append(REJECT["UNBOUNDED_COST"])
    margin = None
    if o.fixed_payout_usd is not None and reserved is not None:
        margin = round(o.fixed_payout_usd - reserved, 6)
        ratio = margin / o.fixed_payout_usd if o.fixed_payout_usd > 0 else -1
        if margin < min_margin_usd or ratio < min_margin_ratio:
            reasons.append(REJECT["NEGATIVE_MARGIN"])
    reasons = list(dict.fromkeys(reasons))
    return Decision(o.external_id, o.platform, "accept_dry_run" if not reasons else "reject",
                    reasons, o.fixed_payout_usd, cost, reserved, margin)

def ledger_record(o: Opportunity, d: Decision) -> Dict[str, Any]:
    raw = json.dumps(asdict(o), sort_keys=True, separators=(",", ":"))
    return {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "opportunity_hash": sha256(raw.encode()).hexdigest(),
        "opportunity": asdict(o),
        "decision": asdict(d),
    }

def dry_run_execute(o: Opportunity) -> Dict[str, Any]:
    return {"external_id": o.external_id, "executed": False, "mode": "dry_run", "artifact": None}

def validate_result(result: Dict[str, Any]) -> bool:
    return result.get("mode") == "dry_run" and result.get("executed") is False
