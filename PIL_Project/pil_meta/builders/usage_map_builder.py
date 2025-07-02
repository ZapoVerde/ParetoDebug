# usage_map_builder.py
"""
Usage Map Builder (builders)

Constructs a forward/reverse reference graph showing usage across the entity set.
Useful for auditing call relationships beyond simple call trees.
"""

from collections import defaultdict

def build_usage_map(graph: dict) -> dict:
    """
    Create bidirectional usage summaries for each FQ name.

    Parameters:
        graph (dict): Full graph with calls_fqns available on each node

    Returns:
        dict: { fqname: { used_by: [...], uses: [...] } }
    """
    usage_summary = defaultdict(lambda: {"used_by": [], "uses": []})

    for fqn, node in graph.items():
        for callee in node.get("calls_fqns", []):
            usage_summary[fqn]["uses"].append(callee)
            usage_summary[callee]["used_by"].append(fqn)

    return usage_summary
