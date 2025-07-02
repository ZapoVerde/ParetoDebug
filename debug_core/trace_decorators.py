# debug_core/trace_decorators.py
# [AI]
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: wrapper

import functools
import traceback
from adapters.debug_adapter import get_debugger
from debug_core.trace_utils import generate_trace_id


def debug_trace(context):
    """Decorator that logs entry, exit, and errors for any function using a Debugger.

    - Logs action="function_entry" on call with args
    - Logs action="function_exit" on return
    - Logs action="error_occurred" on exception with traceback

    Required:
    - context: used to bind the Debugger

    Automatically injects or propagates trace_id in kwargs.
    @status: "stable"
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            trace_id = kwargs.get("trace_id") or generate_trace_id()
            kwargs["trace_id"] = trace_id
            dbg = get_debugger(context)

            dbg(
                action="function_entry",
                state={"args": args, "kwargs": kwargs},
                ai_tags=["UI", "runtime_behavior"],
                trace_id=trace_id
            )

            try:
                result = func(*args, **kwargs)
                dbg(
                    action="function_exit",
                    state={"return": result},
                    ai_tags=["UI", "runtime_behavior"],
                    trace_id=trace_id
                )
                return result
            except Exception as e:
                dbg(
                    action="error_occurred",
                    data={"exception": str(e)},
                    state={"traceback": traceback.format_exc()},
                    ai_tags=["UI", "diagnostic"],
                    trace_id=trace_id
                )
                raise

        return wrapper
    return decorator
