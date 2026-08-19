"""Fail-closed PayanAgent raw-public-payload sanitizers.

Pure/offline transformations only. These helpers do not fetch, authenticate, bid,
accept, fulfill, approve, publish, or settle. Platform payloads cannot self-authorize
policy: trusted policy evidence must be supplied separately by the caller.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Mapping

_ALLOWED_CURRENCIES = {"USD", "USDC"}
_POLICY_FIELDS = ("rights_status", "tos_status", "automation_allowed", "source_data_permission")
_ESTIMATE_FIELDS = (
    "estimated_input_tokens", "estimated_output_tokens", "estimated_duration_seconds",
    "estimate_confidence", "external_cost_cap_usd",
)
_RAW_BUYER_KEYS = (
    "buyer", "buyerId", "buyer_id", "buyerAddress", "buyer_address",
    "wallet", "walletAddress", "wallet_address", "customer", "customerId",
    "customer_id", "payer", "payerAddress", "payer_address",
)


def _present(raw: Mapping[str, Any], keys: tuple[str, ...]) -> list[Any]:
    return [raw[key] for key in keys if key in raw and raw[key] is not None]


def _one_alias(raw: Mapping[str, Any], keys: tuple[str, ...], *, required: bool, error: str) -> Any:
    values = _present(raw, keys)
    if not values:
        if required:
            raise ValueError(error)
        return None
    canonical = {str(v) for v in values}
    if len(canonical) != 1:
        raise ValueError(f"conflicting_{error}")
    return values[0]


def _clean_text(value: Any, *, required: bool = False, limit: int = 20000, error: str = "text_required") -> str | None:
    if value is None:
        if required:
            raise ValueError(error)
        return None
    if not isinstance(value, str):
        raise ValueError(error)
    value = value.strip()
    if required and not value:
        raise ValueError(error)
    if len(value) > limit:
        raise ValueError("text_too_long")
    return value or None


def _positive_number(value: Any, *, error: str) -> float:
    if isinstance(value, bool):
        raise ValueError(error)
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(error) from exc
    if number <= 0:
        raise ValueError(error)
    return number


def _utc_iso(value: Any, *, required: bool = False, error: str = "timestamp_required") -> str | None:
    if value is None:
        if required:
            raise ValueError(error)
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(error)
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(error) from exc
    if dt.tzinfo is None:
        raise ValueError("timestamp_must_be_timezone_aware")
    return dt.astimezone(timezone.utc).isoformat()


def _skills(raw: Mapping[str, Any]) -> list[str]:
    value = _one_alias(raw, ("skills", "tags", "requiredCapabilities", "required_capabilities"), required=False, error="skills")
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > 64:
        raise ValueError("skills_must_be_bounded_list")
    out: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip() or len(item) > 100:
            raise ValueError("invalid_skill")
        cleaned = item.strip().lower()
        if cleaned not in out:
            out.append(cleaned)
    return out


def _trusted_metadata(trusted_policy: Mapping[str, Any] | None,
                      trusted_estimates: Mapping[str, Any] | None) -> dict[str, Any]:
    metadata = {field: "unknown" for field in _POLICY_FIELDS}
    if trusted_policy is not None:
        unknown = set(trusted_policy) - set(_POLICY_FIELDS)
        if unknown:
            raise ValueError("unsupported_trusted_policy_field")
        for field in _POLICY_FIELDS:
            if field in trusted_policy:
                value = trusted_policy[field]
                if not isinstance(value, str) or value.lower() not in {"confirmed", "allowed", "yes", "unknown", "denied", "no"}:
                    raise ValueError("invalid_trusted_policy_state")
                metadata[field] = value.lower()
    if trusted_estimates is not None:
        unknown = set(trusted_estimates) - set(_ESTIMATE_FIELDS)
        if unknown:
            raise ValueError("unsupported_trusted_estimate_field")
        estimates = dict(trusted_estimates)
        for field in ("estimated_input_tokens", "estimated_output_tokens", "estimated_duration_seconds"):
            if field in estimates:
                value = estimates[field]
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    raise ValueError("invalid_trusted_estimate")
        if "estimate_confidence" in estimates:
            value = estimates["estimate_confidence"]
            if isinstance(value, bool):
                raise ValueError("invalid_trusted_estimate")
            try:
                confidence = float(value)
            except (TypeError, ValueError) as exc:
                raise ValueError("invalid_trusted_estimate") from exc
            if not 0.0 <= confidence <= 1.0:
                raise ValueError("invalid_trusted_estimate")
            estimates["estimate_confidence"] = confidence
        if "external_cost_cap_usd" in estimates:
            value = estimates["external_cost_cap_usd"]
            if value is not None:
                if isinstance(value, bool):
                    raise ValueError("invalid_trusted_estimate")
                try:
                    cap = float(value)
                except (TypeError, ValueError) as exc:
                    raise ValueError("invalid_trusted_estimate") from exc
                if cap < 0:
                    raise ValueError("invalid_trusted_estimate")
                estimates["external_cost_cap_usd"] = cap
        metadata.update(estimates)
    return metadata


def sanitize_payan_request(raw: Mapping[str, Any], *,
                           trusted_policy: Mapping[str, Any] | None = None,
                           trusted_estimates: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Normalize a permitted raw public request into PayanAgentAdapter input.

    Platform-provided metadata is deliberately ignored for policy authorization.
    """
    if not isinstance(raw, Mapping):
        raise ValueError("payan_request_must_be_object")
    external_id = _clean_text(
        _one_alias(raw, ("id", "requestId", "request_id"), required=True, error="request_id_required"),
        required=True, limit=256, error="request_id_required",
    )
    status = _one_alias(raw, ("status", "state"), required=False, error="request_status")
    if status is not None and str(status).strip().lower() not in {"open", "active", "posted"}:
        raise ValueError("request_not_open")

    payout = _one_alias(
        raw, ("bountyUsd", "bounty_usd", "budgetUsd", "budget_usd", "payoutUsd", "payout_usd"),
        required=True, error="request_payout_required",
    )
    payout_usd = _positive_number(payout, error="invalid_request_payout")
    currency = str(_one_alias(raw, ("currency", "paymentCurrency", "payment_currency"),
                              required=False, error="request_currency") or "USD").upper()
    if currency not in _ALLOWED_CURRENCIES:
        raise ValueError("unsupported_request_currency")

    title = _clean_text(_one_alias(raw, ("title", "name"), required=False, error="request_title"), limit=500)
    description = _clean_text(
        _one_alias(raw, ("description", "prompt", "brief"), required=False, error="request_description"),
        limit=20000,
    )
    if not title and not description:
        raise ValueError("request_content_required")

    deadline = _utc_iso(
        _one_alias(raw, ("deadlineAt", "deadline_at", "deadline"), required=False, error="request_deadline")
    )
    metadata = _trusted_metadata(trusted_policy, trusted_estimates)
    metadata["required_capabilities"] = _skills(raw)

    return {
        "id": external_id,
        "title": title,
        "description": description,
        "bounty_usd": payout_usd,
        "currency": currency,
        "deadline_at": deadline,
        "skills": metadata["required_capabilities"],
        "metadata": metadata,
    }


def _hash_identity(key: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("invalid_buyer_identity")
    normalized = value.strip().lower() if "address" in key.lower() or key.lower() in {"wallet", "buyer"} and value.strip().startswith("0x") else value.strip()
    return sha256(normalized.encode("utf-8")).hexdigest()


def sanitize_payan_receipt(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize a permitted raw public receipt while dropping/hash-minimizing identity."""
    if not isinstance(raw, Mapping):
        raise ValueError("payan_receipt_must_be_object")
    receipt_id = _clean_text(
        _one_alias(raw, ("id", "receiptId", "receipt_id"), required=True, error="receipt_id_required"),
        required=True, limit=256, error="receipt_id_required",
    )
    currency = str(_one_alias(raw, ("currency", "asset"), required=False, error="receipt_currency") or "USDC").upper()
    if currency not in _ALLOWED_CURRENCIES:
        raise ValueError("unsupported_receipt_currency")

    amount_direct = _present(raw, ("amountUsd", "amount_usd", "valueUsd", "value_usd", "paymentUsd", "payment_usd"))
    amount_cents = _present(raw, ("amountCents", "amount_cents", "valueCents", "value_cents"))
    if bool(amount_direct) == bool(amount_cents):
        raise ValueError("exactly_one_receipt_amount_representation_required")
    if amount_direct:
        if len({str(v) for v in amount_direct}) != 1:
            raise ValueError("conflicting_receipt_amount")
        amount_usd = _positive_number(amount_direct[0], error="invalid_receipt_amount")
    else:
        if len({str(v) for v in amount_cents}) != 1:
            raise ValueError("conflicting_receipt_amount")
        amount_usd = _positive_number(amount_cents[0], error="invalid_receipt_amount") / 100.0

    occurred_at = _utc_iso(
        _one_alias(raw, ("settledAt", "settled_at", "occurredAt", "occurred_at", "timestamp", "createdAt", "created_at"),
                   required=True, error="receipt_timestamp_required"),
        required=True, error="receipt_timestamp_required",
    )

    identities = [(key, raw[key]) for key in _RAW_BUYER_KEYS if key in raw and raw[key] is not None]
    hashes = {_hash_identity(key, value) for key, value in identities}
    if len(hashes) > 1:
        raise ValueError("conflicting_buyer_identity")
    out = {"receipt_id": receipt_id, "amount_usd": round(amount_usd, 6), "occurred_at": occurred_at}
    if hashes:
        out["buyer_hash"] = next(iter(hashes))
    return out
