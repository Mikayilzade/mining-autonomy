"""I077 inert future HTTPS/JSON adapter surface.

This module intentionally contains no networking library imports and performs no
DNS/HTTP. The only future activation interface is a fail-closed stub until a
separate, exact, single-use real-network activation layer exists.
"""
from __future__ import annotations
from typing import Any, Mapping


def execute_single_authorized_get(*, authorized_envelope: Mapping[str, Any]) -> None:
    """Defined interface only; unreachable for real transport in I077."""
    del authorized_envelope
    raise RuntimeError("real_network_activation_not_enabled")
