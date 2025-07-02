# tests/test_tag_rules.py
# [AI]
# @tags:
#   domain: UI
#   data_affinity: actor_data
#   scope_horizon: mvp
#   semantic_role: system_definition

import pytest
from debug_core.tag_rules import validate_ai_tags

GOOD_TAGS = [
    "combat",
    "actor_data",
    "mvp",
    "runtime_behavior"
]

def test_validate_good_tags():
    """Accepts a complete, valid tag set."""
    validate_ai_tags(GOOD_TAGS)  # Should not raise


def test_unknown_tag_rejected():
    """Rejects tags not present in vocabulary."""
    with pytest.raises(ValueError):
        validate_ai_tags(GOOD_TAGS + ["not_real"])


def test_missing_group_rejected():
    """Rejects list lacking a required group."""
    incomplete = ["combat", "actor_data"]  # missing scope_horizon & semantic_role
    with pytest.raises(ValueError):
        validate_ai_tags(incomplete)
