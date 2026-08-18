import json
from pathlib import Path
from evaluator import Opportunity, evaluate, SettlementAdapter, dry_run_execute, validate_result

CAPS = {"extract", "summarize", "research"}

def load():
    return [Opportunity(**x) for x in json.loads(Path(__file__).with_name("fixtures_i004.json").read_text())]

def test_fixture_decisions():
    got = {o.external_id: evaluate(o, CAPS) for o in load()}
    assert "malformed_task" in got["malformed"].reject_reasons
    assert "prohibited_task" in got["prohibited"].reject_reasons
    assert "unknown_rights_or_tos" in got["rights_unknown"].reject_reasons
    assert "unsupported_capability" in got["unsupported"].reject_reasons
    assert "unknown_payout" in got["unknown_payout"].reject_reasons
    assert "insufficient_expected_margin" in got["negative_margin"].reject_reasons
    assert got["positive_margin"].decision == "accept_dry_run"
    assert "unbounded_external_cost" in got["unbounded_cost"].reject_reasons
    assert "requires_value_moving_action" in got["value_action"].reject_reasons

def test_executor_never_executes():
    o = next(x for x in load() if x.external_id == "positive_margin")
    assert validate_result(dry_run_execute(o))

def test_settlement_hard_disabled():
    try:
        SettlementAdapter().settle()
    except RuntimeError:
        return
    assert False, "settlement must never be enabled in v0.1"
