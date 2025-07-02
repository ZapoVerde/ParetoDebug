# linkage_builder.py
"""
Adds call relationships between entities in the graph.

Uses AST parsing to detect structural function calls, updates each node with:
- calls_fqns
- called_by_fqns
- links: [ { target, type: "calls" } ]
- is_orphaned (recomputed after linkage)
"""

import ast
from pathlib import Path


def extract_called_functions(source: str) -> list[str]:
    """
    Parses source code and extracts all function names that are called.

    Parameters:
        source (str): The raw source code of a .py file

    Returns:
        list[str]: All direct call targets (unqualified names)
    """
    calls = []

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.append(node.func.attr)

    return calls


def inject_call_links(entity_graph: dict, project_root: str) -> dict:
    """
    Injects structural call links into the entity graph.

    Parameters:
        entity_graph (dict): Entity metadata keyed by fqname
        project_root (str): Project root to re-open source files

    Returns:
        dict: The enriched graph with linkage info
    """
    for fqn, node in entity_graph.items():
        rel_path = node["source_file"].replace("/", "\\")
        full_path = Path(project_root) / rel_path

        if not full_path.exists():
            continue

        try:
            with full_path.open("r", encoding="utf-8") as f:
                source = f.read()
        except Exception:
            continue

        called_names = extract_called_functions(source)

        matches = []
        for name in called_names:
            # Match to fqname by name suffix (non-qualified)
            for target_fqn, target_node in entity_graph.items():
                if target_node.get("ignore"):
                    continue
                if target_fqn.split(".")[-1] == name:
                    matches.append(target_fqn)

        node["calls_fqns"] = sorted(set(matches))
        node["links"] = node.get("links", []) + [
            {"target": target, "type": "calls"} for target in matches
        ]

        for target in matches:
            if target in entity_graph:
                entity_graph[target].setdefault("called_by_fqns", []).append(fqn)

    # Recompute orphans after linkage
    for fqn, node in entity_graph.items():
        inbound = node.get("called_by_fqns", [])
        outbound = node.get("calls_fqns", [])
        node["is_orphaned"] = not (inbound or outbound)

    return entity_graph
