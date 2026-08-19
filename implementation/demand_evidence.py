"""Demand-evidence classification for autonomous earning observations.

This module distinguishes proof of actual paid utilization/open buyer demand from
mere supply/listing/marketing signals. It contains no network or value-moving code.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DemandEvidence:
    evidence_class: str
    strength: int
    proves_paid_utilization: bool
    proves_open_paid_demand: bool
    description: str


_EVIDENCE = {
    "settled_receipt": DemandEvidence(
        "settled_receipt", 4, True, False,
        "Attributable completed paid transaction/settlement for provider work.",
    ),
    "paid_invocation": DemandEvidence(
        "paid_invocation", 4, True, False,
        "Attributable paid API/tool/service invocation.",
    ),
    "open_paid_request": DemandEvidence(
        "open_paid_request", 3, False, True,
        "Current machine-readable buyer request with explicit positive payout/budget.",
    ),
    "listing_only": DemandEvidence(
        "listing_only", 1, False, False,
        "Provider/service/catalog listing; proves supply or availability, not demand.",
    ),
    "marketing_claim": DemandEvidence(
        "marketing_claim", 0, False, False,
        "Non-attributable headline, calculator, testimonial, aggregate or marketing claim.",
    ),
    "unknown": DemandEvidence(
        "unknown", 0, False, False,
        "Evidence has not been classified strongly enough to support a demand claim.",
    ),
}

DEMAND_EVIDENCE_CLASSES = frozenset(_EVIDENCE)


def classify_demand_evidence(value: str | None) -> DemandEvidence:
    key = (value or "unknown").strip().lower()
    if key not in _EVIDENCE:
        raise ValueError("unsupported_demand_evidence_class")
    return _EVIDENCE[key]


def evidence_record(value: str | None) -> dict[str, object]:
    evidence = classify_demand_evidence(value)
    return {
        "evidence_class": evidence.evidence_class,
        "strength": evidence.strength,
        "proves_paid_utilization": evidence.proves_paid_utilization,
        "proves_open_paid_demand": evidence.proves_open_paid_demand,
        "description": evidence.description,
    }
