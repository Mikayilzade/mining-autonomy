"""I131 no-spend watcher budget model.

Models cheap polling -> deterministic dedupe/filter -> selective AI escalation.
It never polls a real endpoint and never assumes ChatGPT subscription is an API.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class WatcherBudget:
    polls_per_hour: float
    polling_cost_usd: float
    candidates_per_poll: float
    dedupe_survival_probability: float
    deterministic_survival_probability: float
    ai_escalation_probability: float
    ai_cost_per_call_usd: float
    local_energy_per_poll_usd: float = 0.0
    maintenance_minutes_per_day: float = 0.0
    human_time_value_per_hour_usd: float = 0.0

@dataclass(frozen=True)
class WatcherEconomics:
    daily_polls: float
    daily_candidates: float
    daily_ai_calls: float
    daily_incremental_cost_usd: float
    cost_per_escalated_candidate_usd: float


def estimate(b: WatcherBudget) -> WatcherEconomics:
    vals=(b.polls_per_hour,b.polling_cost_usd,b.candidates_per_poll,b.dedupe_survival_probability,b.deterministic_survival_probability,b.ai_escalation_probability,b.ai_cost_per_call_usd,b.local_energy_per_poll_usd,b.maintenance_minutes_per_day,b.human_time_value_per_hour_usd)
    if any(x < 0 for x in vals): raise ValueError("negative_watcher_input")
    for p in (b.dedupe_survival_probability,b.deterministic_survival_probability,b.ai_escalation_probability):
        if p > 1: raise ValueError("probability_above_one")
    polls=b.polls_per_hour*24.0
    candidates=polls*b.candidates_per_poll*b.dedupe_survival_probability*b.deterministic_survival_probability
    ai=candidates*b.ai_escalation_probability
    maintenance=(b.maintenance_minutes_per_day/60.0)*b.human_time_value_per_hour_usd
    cost=polls*(b.polling_cost_usd+b.local_energy_per_poll_usd)+ai*b.ai_cost_per_call_usd+maintenance
    return WatcherEconomics(polls,candidates,ai,round(cost,8),round(cost/ai,8) if ai else 0.0)
