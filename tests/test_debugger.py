# tests/test_debugger.py
# [AI]
# Tests for core Debugger logging behavior
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: runtime_behavior

import os
import json
import pytest
from config import DEBUG_MODE
from adapters.debug_adapter import get_debugger

LOG_FILE = "debug_logs/test_context.jsonl"

# Skip this test module entirely if debugging is disabled
if not DEBUG_MODE:
    pytest.skip("DEBUG_MODE is disabled — skipping debugger tests", allow_module_level=True)


@pytest.fixture
def clean_log_file():
    """Removes the test log file before and after each test.
    @status: "stable"
    """
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


def test_valid_log_entry(clean_log_file):
    """Logs a valid debug entry and verifies its file and structure.
    @status: "stable"
    """
    dbg = get_debugger("test/context")

    entry = dbg(
        action="simulate_hit",
        data={"roll": 6},
        state={"hp": 8},
        ai_tags=["combat", "performance"],
        print_console=False
    )

    assert entry is not None, "Debugger returned None — check DEBUG_MODE"
    assert entry["action"] == "simulate_hit"
    assert os.path.exists(LOG_FILE)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        line = f.readline()
        logged = json.loads(line)
        assert logged["context"] == "test_context"
        assert "timestamp" in logged
        assert "data" in logged
        assert "state" in logged


def test_missing_ai_tags_raises(clean_log_file):
    """Rejects debug entry if ai_tags are missing or invalid.
    @status: "stable"
    """
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError) as e:
        dbg(
            action="fail_check",
            data={"error": "no tags"},
            state={"hp": 0},
            ai_tags=None,
            print_console=False
        )

    assert "ai_tags" in str(e.value)


def test_missing_state_and_data_raises(clean_log_file):
    """Rejects debug entry if both state and data are missing.
    @status: "stable"
    """
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError) as e:
        dbg(
            action="fail_both",
            ai_tags=["combat"],
            print_console=False
        )

    assert "at least 'data' or 'state'" in str(e.value)


def test_invalid_action_format_raises(clean_log_file):
    """Rejects debug entry if action format is not verb_noun.
    @status: "stable"
    """
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError) as e:
        dbg(
            action="badformat",
            data={"x": 1},
            ai_tags=["combat"],
            print_console=False
        )

    assert "verb_noun" in str(e.value)
