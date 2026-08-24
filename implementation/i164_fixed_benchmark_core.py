"""I164 lightweight deterministic benchmark core for I163.

This module contains only the fixed local JSON-transform benchmark primitives used
by the user-PC session wrapper. It deliberately has no Resource Router, calibration,
network, credential, CI, spend, task-action, payment, or value-moving dependencies.
"""
from __future__ import annotations

from hashlib import sha256
import json
from typing import Any, Mapping

BENCHMARK_ID = "python-local-fixed-json-transform-v1"
FIXTURE_INPUT = {
    "records": [
        {"id": "gamma", "value": 5},
        {"id": "alpha", "value": 2},
        {"id": "beta", "value": 3},
    ],
    "schema_version": 1,
}


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _hash(value: Any) -> str:
    payload = value if isinstance(value, str) else _canonical_json(value)
    return sha256(payload.encode("utf-8")).hexdigest()


def benchmark_transform(payload: Mapping[str, Any] = FIXTURE_INPUT) -> dict[str, Any]:
    if payload.get("schema_version") != 1:
        raise ValueError("unsupported_fixture_schema")
    rows = payload.get("records")
    if not isinstance(rows, list) or not rows:
        raise ValueError("fixture_records_required")
    normalized = []
    seen = set()
    for row in rows:
        if not isinstance(row, Mapping):
            raise ValueError("fixture_row_must_be_mapping")
        key = row.get("id")
        value = row.get("value")
        if not isinstance(key, str) or not key or key in seen:
            raise ValueError("invalid_or_duplicate_fixture_id")
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("fixture_value_must_be_nonnegative_int")
        seen.add(key)
        normalized.append({"id": key, "value": value})
    normalized.sort(key=lambda x: x["id"])
    checksum_input = "|".join(f'{row["id"]}:{row["value"]}' for row in normalized)
    return {
        "count": len(normalized),
        "sum": sum(row["value"] for row in normalized),
        "records": normalized,
        "records_checksum": _hash(checksum_input),
        "schema_version": 1,
    }


EXPECTED_OUTPUT = benchmark_transform()
EXPECTED_OUTPUT_DIGEST = _hash(EXPECTED_OUTPUT)
