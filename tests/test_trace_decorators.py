# tests/test_trace_decorators.py
# [AI]
# Tests for debug_trace decorator instrumentation
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: wrapper

import os
import json
import uuid
import pytest
from config import DEBUG_MODE
from debug_core.trace_decorators import debug_trace

LOG_FILE = "debug_logs/test_trace.jsonl"

if not DEBUG_MODE:
    pytest.skip("DEBUG_MODE is disabled — skipping decorator tests", allow_module_level=True)

@pytest.fixture(autouse=True)
def clean_trace_log():
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)
    yield
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)


@debug_trace("test_trace")
def simple_add(x, y, trace_id=None):
    return x + y


@debug_trace("test_trace")
def raise_error(trace_id=None):
    raise RuntimeError("Forced failure for test")


def test_trace_logs_entry_and_exit():
    """Verifies that decorated function logs both entry and exit.
    @status: "stable"
    """
    tid = str(uuid.uuid4())
    result = simple_add(3, 4, trace_id=tid)
    assert result == 7
    assert os.path.exists(LOG_FILE)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = [json.loads(line) for line in f.readlines()]
        actions = [log["action"] for log in logs]
        assert "function_entry" in actions
        assert "function_exit" in actions
        for log in logs:
            assert log.get("trace_id") == tid


def test_trace_logs_exception():
    """Verifies that exceptions are logged with traceback and trace_id.
    @status: "stable"
    """
    tid = str(uuid.uuid4())

    with pytest.raises(RuntimeError):
        raise_error(trace_id=tid)

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = [json.loads(line) for line in f.readlines()]
        assert any(log["action"] == "error_occurred" for log in logs)
        err_log = next(log for log in logs if log["action"] == "error_occurred")
        assert "traceback" in err_log.get("state", {})
        assert "exception" in err_log.get("data", {})
        assert err_log["trace_id"] == tid
