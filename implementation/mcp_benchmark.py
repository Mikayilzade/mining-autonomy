"""Offline MCP paid-capability economics benchmark (I007).

No network calls, credentials, publication, wallet, billing or settlement.
Models bounded local capabilities and break-even utilization.
"""
from dataclasses import dataclass, asdict
import csv
import io
import json
import re
from typing import Callable, Any

@dataclass(frozen=True)
class CapabilityEconomics:
    name: str
    price_per_call_usd: float
    variable_cost_per_call_usd: float
    monthly_fixed_cost_usd: float = 0.0
    creator_share: float = 0.80

    @property
    def creator_revenue_per_call(self) -> float:
        return self.price_per_call_usd * self.creator_share

    @property
    def contribution_per_call(self) -> float:
        return self.creator_revenue_per_call - self.variable_cost_per_call_usd

    def break_even_calls(self) -> int | None:
        contribution = self.contribution_per_call
        if contribution <= 0:
            return None
        if self.monthly_fixed_cost_usd <= 0:
            return 0
        return int(-(-self.monthly_fixed_cost_usd // contribution))

    def monthly_net(self, calls: int) -> float:
        return round(calls * self.contribution_per_call - self.monthly_fixed_cost_usd, 6)


def normalize_text(payload: dict[str, Any]) -> dict[str, Any]:
    text = str(payload.get("text", ""))
    text = re.sub(r"\s+", " ", text).strip()
    return {"text": text, "characters": len(text), "words": len(text.split()) if text else 0}


def json_stats(payload: dict[str, Any]) -> dict[str, Any]:
    value = payload.get("value")
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    def count(v: Any) -> tuple[int, int]:
        if isinstance(v, dict):
            pairs = [count(x) for x in v.values()]
            return 1 + sum(x[0] for x in pairs), sum(x[1] for x in pairs)
        if isinstance(v, list):
            pairs = [count(x) for x in v]
            return 1 + sum(x[0] for x in pairs), sum(x[1] for x in pairs)
        return 1, 1
    nodes, leaves = count(value)
    return {"canonical_json": encoded, "nodes": nodes, "leaves": leaves, "bytes_utf8": len(encoded.encode())}


def csv_profile(payload: dict[str, Any]) -> dict[str, Any]:
    raw = str(payload.get("csv", ""))
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        return {"rows": 0, "columns": 0, "header": [], "ragged_rows": 0}
    width = len(rows[0])
    return {"rows": max(0, len(rows)-1), "columns": width, "header": rows[0], "ragged_rows": sum(len(r) != width for r in rows[1:])}

CAPABILITIES: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "normalize_text": normalize_text,
    "json_stats": json_stats,
    "csv_profile": csv_profile,
}

DEFAULT_MODELS = {
    # MCPize current standard share is 80%; free hosting tier makes fixed hosting $0
    # for a bounded initial benchmark. Prices are experiment assumptions, not demand evidence.
    "normalize_text": CapabilityEconomics("normalize_text", 0.01, 0.00001),
    "json_stats": CapabilityEconomics("json_stats", 0.01, 0.00002),
    "csv_profile": CapabilityEconomics("csv_profile", 0.01, 0.00003),
}


def benchmark(name: str, payload: dict[str, Any], iterations: int = 1000) -> dict[str, Any]:
    import time
    fn = CAPABILITIES[name]
    start = time.perf_counter()
    result = None
    for _ in range(iterations):
        result = fn(payload)
    elapsed = time.perf_counter() - start
    model = DEFAULT_MODELS[name]
    return {
        "capability": name,
        "iterations": iterations,
        "elapsed_seconds": round(elapsed, 6),
        "mean_ms": round(elapsed * 1000 / iterations, 6),
        "sample_result": result,
        "economics": asdict(model),
        "creator_revenue_per_call_usd": round(model.creator_revenue_per_call, 6),
        "contribution_per_call_usd": round(model.contribution_per_call, 6),
        "break_even_calls_month": model.break_even_calls(),
        "net_at_100_calls_month_usd": model.monthly_net(100),
        "net_at_1000_calls_month_usd": model.monthly_net(1000),
    }


def run_suite() -> list[dict[str, Any]]:
    fixtures = {
        "normalize_text": {"text": "  Autonomous   tools\nshould be bounded.  "},
        "json_stats": {"value": {"a": [1, 2, 3], "b": {"ok": True}}},
        "csv_profile": {"csv": "name,value\na,1\nb,2\nc,3\n"},
    }
    return [benchmark(name, fixtures[name]) for name in CAPABILITIES]

if __name__ == "__main__":
    print(json.dumps(run_suite(), indent=2))
