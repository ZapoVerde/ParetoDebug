# tests/test_debugger.py
# [AI]
# Tests for core Debugger logging behavior with enforced ai_tags
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

# Skip entire module if debugging is disabled
if not DEBUG_MODE:
    pytest.skip("DEBUG_MODE is disabled — skipping debugger tests", allow_module_level=True)

# A complete, valid tag set for happy-path tests
VALID_TAGS = ["combat", "actor_data", "mvp", "runtime_behavior"]


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
    """Logs a valid entry and verifies file + structure."""
    dbg = get_debugger("test/context")

    entry = dbg(
        action="simulate_hit",
        data={"roll": 6},
        state={"hp": 8},
        ai_tags=VALID_TAGS,
        print_console=False,
    )

    assert entry is not None
    assert entry["action"] == "simulate_hit"
    assert os.path.exists(LOG_FILE)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logged = json.loads(f.readline())
        assert logged["context"] == "test_context"
        assert set(VALID_TAGS).issubset(logged["ai_tags"])


def test_missing_ai_tags_raises(clean_log_file):
    """Rejects log entry when ai_tags is missing."""
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError):
        dbg(
            action="fail_no_tags",
            data={"err": 1},
            state={"hp": 0},
            ai_tags=None,
            print_console=False,
        )


def test_invalid_ai_tags_format(clean_log_file):
    """Rejects ai_tags that are not a list of strings."""
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError):
        dbg(
            action="fail_bad_tag_format",
            data={"err": 2},
            state={"hp": 0},
            ai_tags="not_a_list",
            print_console=False,
        )


def test_missing_state_and_data_raises(clean_log_file):
    """Rejects when both state and data are absent."""
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError):
        dbg(
            action="fail_both",
            ai_tags=VALID_TAGS,
            print_console=False,
        )


def test_invalid_action_format_raises(clean_log_file):
    """Rejects action not in verb_noun format."""
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError):
        dbg(
            action="badformat",
            data={"x": 1},
            ai_tags=VALID_TAGS,
            print_console=False,
        )


def test_non_dict_state_rejected(clean_log_file):
    """Rejects state that is not a dict."""
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError):
        dbg(
            action="invalid_state_type",
            state="not_a_dict",
            data={"ok": True},
            ai_tags=VALID_TAGS,
            print_console=False,
        )


def test_non_dict_data_rejected(clean_log_file):
    """Rejects data that is not a dict."""
    dbg = get_debugger("test/context")

    with pytest.raises(ValueError):
        dbg(
            action="invalid_data_type",
            state={"valid": True},
            data="BAD",
            ai_tags=VALID_TAGS,
            print_console=False,
        )
