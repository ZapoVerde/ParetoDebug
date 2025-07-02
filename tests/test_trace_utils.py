# tests/test_trace_utils.py
# [AI]
# Tests for trace ID generation and propagation utilities
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: trigger_logic

import re
import uuid
from debug_core.trace_utils import generate_trace_id, attach_trace_id

UUID_PATTERN = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$")


def test_generate_trace_id_format():
    """Verifies that generated trace_id is a valid UUID v4.
    @status: "stable"
    """
    tid = generate_trace_id()
    assert isinstance(tid, str)
    assert UUID_PATTERN.match(tid)
    assert uuid.UUID(tid).version == 4


def test_attach_trace_id_injection():
    """Ensures the decorator injects a new trace_id if missing.
    @status: "stable"
    """
    @attach_trace_id
    def simulated_handler(trace_id=None):
        return trace_id

    tid = simulated_handler()
    assert isinstance(tid, str)
    assert UUID_PATTERN.match(tid)


def test_attach_trace_id_passthrough():
    """Ensures the decorator preserves existing trace_id.
    @status: "stable"
    """
    known = "00000000-1111-2222-3333-444444444444"

    @attach_trace_id
    def simulated_handler(trace_id=None):
        return trace_id

    result = simulated_handler(trace_id=known)
    assert result == known
