# tests/test_usage_map_builder.py
"""
Unit tests for pil_meta.builders.usage_map_builder.

Covers:
- build_usage_map: validates correct API output, used_by/uses relationships, cycles.
Note: Orphan nodes (no uses/no used_by) are not included in the result per builder implementation.

@tags: ["test", "usage_map_builder", "unit"]
@status: "stable"
"""

from pil_meta.builders.usage_map_builder import build_usage_map

def test_empty_graph_returns_empty_map():
    """
    Empty graph yields an empty usage map.
    """
    result = build_usage_map({})
    assert dict(result) == {}

def test_single_node_no_uses():
    """
    Node with no calls_fqns: usage map is empty dict (orphan nodes not included).
    """
    graph = {
        "foo.bar": {
            "fqname": "foo.bar",
            "calls_fqns": []
        }
    }
    result = build_usage_map(graph)
    assert dict(result) == {}

def test_call_links_are_registered_as_usage():
    """
    Node with calls_fqns creates correct uses/used_by mapping.
    """
    graph = {
        "foo.a": {
            "fqname": "foo.a",
            "calls_fqns": ["foo.b"]
        },
        "foo.b": {
            "fqname": "foo.b",
            "calls_fqns": []
        }
    }
    result = build_usage_map(graph)
    result = dict(result)
    assert result["foo.a"]["uses"] == ["foo.b"]
    assert result["foo.b"]["used_by"] == ["foo.a"]

def test_usage_map_cycle_and_orphan():
    """
    Cycle in calls_fqns is reflected; orphans are not included in result.
    """
    graph = {
        "cycle.one": {"fqname": "cycle.one", "calls_fqns": ["cycle.two"]},
        "cycle.two": {"fqname": "cycle.two", "calls_fqns": ["cycle.one"]},
        "orphan": {"fqname": "orphan", "calls_fqns": []}
    }
    result = build_usage_map(graph)
    result = dict(result)
    assert sorted(result["cycle.one"]["uses"]) == ["cycle.two"]
    assert sorted(result["cycle.two"]["used_by"]) == ["cycle.one"]
    assert "orphan" not in result

def test_missing_node_in_calls():
    """
    Calls to missing nodes should still populate the used_by field in the map.
    """
    graph = {
        "a": {"fqname": "a", "calls_fqns": ["b"]},
    }
    result = build_usage_map(graph)
    result = dict(result)
    assert "b" in result
    assert result["b"]["used_by"] == ["a"]
