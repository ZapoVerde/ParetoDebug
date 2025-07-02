# tests/phase2_export_utilities/test_graph_utils.py
"""
Unit tests for pil_meta.utils.graph_utils.

Covers:
- walk_graph: full visit, cycles, starting from a subset, no duplicates

@tags: ["test", "graph_utils", "unit"]
@status: "stable"
"""

import pytest
from pil_meta.utils.graph_utils import walk_graph

def test_walk_graph_visits_all_nodes():
    """
    Visits every node in a simple graph.
    """
    graph = {
        "a": {"links": [{"target": "b"}]},
        "b": {"links": [{"target": "c"}]},
        "c": {"links": []}
    }
    visited = []
    walk_graph(graph, lambda fqname, node: visited.append(fqname))
    assert set(visited) == {"a", "b", "c"}

def test_walk_graph_handles_cycles():
    """
    Walk graph does not revisit nodes in cycles.
    """
    graph = {
        "x": {"links": [{"target": "y"}]},
        "y": {"links": [{"target": "x"}]}
    }
    visited = []
    walk_graph(graph, lambda fqname, node: visited.append(fqname))
    # Should visit each node only once
    assert sorted(visited) == ["x", "y"]

def test_walk_graph_with_start_nodes():
    """
    Only start from specified nodes.
    """
    graph = {
        "m": {"links": [{"target": "n"}]},
        "n": {"links": [{"target": "o"}]},
        "o": {"links": []},
        "p": {"links": []}
    }
    visited = []
    walk_graph(graph, lambda fqname, node: visited.append(fqname), start_nodes={"p"})
    assert visited == ["p"]
