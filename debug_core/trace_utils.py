# debug_core/trace_utils.py
# [AI]
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: trigger_logic

import uuid
import functools

def generate_trace_id() -> str:
    """Generates a unique trace ID using UUID v4.
    @status: "stable"
    """
    return str(uuid.uuid4())


def attach_trace_id(func):
    """Decorator that injects or propagates a trace_id in keyword arguments.
    
    If `trace_id` is already present in kwargs, it is preserved.
    If missing, one is generated and added automatically.
    @status: "stable"
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "trace_id" not in kwargs or kwargs["trace_id"] is None:
            kwargs["trace_id"] = generate_trace_id()
        return func(*args, **kwargs)
    return wrapper
