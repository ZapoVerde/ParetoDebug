# pil_meta/validators/governance_validator.py
"""
Validation Rules (validators)

Applies all governance rules to the entity graph.
Includes docstring checks, test coverage, orphan detection, etc.

@tags: ["validation", "governance"]
@status: "stable"
@visibility: "public"
"""

from collections import Counter

def validate_governance_rules(graph: dict) -> tuple[dict, Counter]:
    """
    Run all rule checks over the graph.

    Parameters:
        graph (dict): Entity graph keyed by fqname

    Returns:
        tuple: (violations dict, issue counter)
    """
    exceptions = {}
    issue_counts = Counter()

    for fqn, node in graph.items():
        issues = []
        node_type = node.get("type", "function")

        if node_type in ("function", "method", "class", "module"):
            if not node.get("docstring_present"):
                issues.append("missing_docstring")

        if node_type in ("function", "method"):
            if not node.get("test_coverage"):
                issues.append("missing_test")

        if node_type in ("function", "method", "class", "module"):
            if not node.get("tags"):
                issues.append("missing_tags")
            if node.get("is_orphaned"):
                issues.append("orphaned")

        if node.get("deprecated") and node.get("called_by_fqns"):
            issues.append("deprecated_but_used")
        if node.get("ignore") and node.get("called_by_fqns"):
            issues.append("invalid_ignore_usage")

        if issues:
            for issue in issues:
                issue_counts[issue] += 1

            exceptions[fqn] = {
                "module": node.get("module"),
                "function": node.get("function"),
                "issues": issues,
                "calls": node.get("calls_fqns", []),
                "called_by": node.get("called_by_fqns", [])
            }

    return exceptions, issue_counts
