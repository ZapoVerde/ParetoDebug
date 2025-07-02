# debug_core/tag_rules.py
# [AI]
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: system_definition

"""
Utilities to validate ai_tags against the shared MECE tag vocabulary.
Raises ValueError on any violation so Debugger can enforce contract.
"""

import json
import os
from typing import List

_VOCAB_PATH = os.path.join(os.path.dirname(__file__), "tags_vocab.json")


def _load_vocab() -> dict:
    """Loads the tag vocabulary from disk once and caches it.
    @status: "stable"
    """
    if not hasattr(_load_vocab, "_cache"):
        with open(_VOCAB_PATH, "r", encoding="utf-8") as fp:
            _load_vocab._cache = json.load(fp)
    return _load_vocab._cache


def validate_ai_tags(tags: List[str]) -> None:
    """Validates a list of ai_tags against the MECE vocabulary.

    Rules:
    1. Every tag must exist in the official vocabulary.
    2. At least one tag from **each** semantic group must be present.
       (domain, data_affinity, scope_horizon, semantic_role)

    Raises
    ------
    ValueError
        If any tag is unknown or a group is missing.
    """
    vocab = _load_vocab()

    # Unknown tag check
    unknown = [t for t in tags if not any(t in vals for vals in vocab.values())]
    if unknown:
        raise ValueError(f"[DEBUG] Unknown ai_tag(s): {unknown}")

    # Group coverage check
    missing_groups = [group for group, vals in vocab.items() if not set(vals).intersection(tags)]
    if missing_groups:
        raise ValueError(f"[DEBUG] ai_tags missing required group(s): {missing_groups}")
