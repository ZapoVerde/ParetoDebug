# adapters/debug_adapter.py
# [AI], [ADAPTER]
# Role: Mediates access to [DEAD-END] or cross-layer systems
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: render_contract

from debug_core.debugger import Debugger

# Global fallback debugger (used if no specific context is supplied)
_global_debugger = Debugger("global/default")


def get_debugger(context: str) -> Debugger:
    """Returns a context-bound Debugger instance."""
    return Debugger(context)


def debug(action, data=None, state=None, ai_tags=None, print_console=False):
    """Routes a debug call to the global fallback debugger.

    Useful for quick standalone debug calls where context isn't critical.
    """
    return _global_debugger(
        action=action,
        data=data,
        state=state,
        ai_tags=ai_tags,
        print_console=print_console
    )
