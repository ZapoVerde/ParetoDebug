# pil_meta/builders/entity_graph_builder.py
"""
Wraps pre-enriched code entities into graph nodes for the entity graph.

Assumes upstream loader (code_loader) has already attached all required metadata,
including tags, docstring status, and test coverage placeholders.

Output format conforms to the `entity_graph.json` specification.
"""

def build_entity_graph(entities: list[dict]) -> dict:
    """
    Wrap each enriched entity into a compliant graph node.

    Parameters:
        entities (list[dict]): Raw or enriched entity records.

    Returns:
        dict: fqname → wrapped graph node
    """
    graph = {}

    for entry in entities:
        fqname = entry["fqname"]

        # Defensive: prefer top-level keys, fallback to metadata if needed
        def get_field(key, default=None):
            return entry.get(key) or entry.get("metadata", {}).get(key, default)

        node_type = get_field("type", "unknown")
        description = entry.get("description", "")
        tags = entry.get("tags", [])
        source_file = entry.get("source_file", "")
        test_coverage = entry.get("test_coverage", False)
        docstring_present = entry.get("docstring_present", False)
        linked_journal_entry = entry.get("linked_journal_entry", None)
        is_orphaned = entry.get("is_orphaned", False)
        links = entry.get("links", [])
        called_by_fqns = entry.get("called_by_fqns", [])
        calls_fqns = entry.get("calls_fqns", [])

        graph[fqname] = {
            "fqname": fqname,
            "type": node_type,
            "description": description,
            "tags": tags,
            "source_file": source_file,
            "test_coverage": test_coverage,
            "docstring_present": docstring_present,
            "linked_journal_entry": linked_journal_entry,
            "is_orphaned": is_orphaned,
            "metadata": entry,  # Retain all original fields for future analysis
            "links": links,
            "called_by_fqns": called_by_fqns,
            "calls_fqns": calls_fqns,
        }

    return graph
