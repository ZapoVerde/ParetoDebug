# pil_meta/utils/graph_utils.py
"""
Graph Utilities

Common functions for working with the code entity graph: walking nodes, traversing edges, etc.
"""
from typing import Dict, Set, Callable, Optional

def walk_graph(
    graph: Dict[str, dict],
    visit: Callable[[str, dict], None],
    start_nodes: Optional[Set[str]] = None
):
    """
    Walk the entity graph, applying a visitor function to each node.
    Optionally start at a subset of nodes; otherwise walk all.

    Args:
        graph (dict): { fqname: node dict }
        visit (callable): function(fqname, node)
        start_nodes (set): Subset of fqn names to start from (optional)
    """
    seen = set()
    def _walk(fqname):
        if fqname in seen or fqname not in graph:
            return
        seen.add(fqname)
        visit(fqname, graph[fqname])
        for link in graph[fqname].get('links', []):
            target = link.get('target')
            if target and target in graph:
                _walk(target)
    nodes = start_nodes or set(graph.keys())
    for fqn in nodes:
        _walk(fqn)
