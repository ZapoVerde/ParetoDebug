# docstring_utils.py
"""
Docstring Utilities (utils)

Houses reusable docstring validation logic shared across pipeline components.
Also supports docstring extraction and structured annotation parsing.

@tags: ["docstring", "metadata", "parsing"]
@status: "stable"
@visibility: "internal"
"""

import ast
import textwrap
import re

def check_docstring_signature_match(node: dict) -> bool:
    """
    Checks if the function docstring references the function name and its parameters.

    @tags: ["validation", "docstring"]
    @status: "stable"
    @visibility: "internal"

    Parameters:
        node (dict): Metadata dictionary for a function or method.

    Returns:
        bool: True if name and all params appear in the first line of the docstring
    """
    doc = node.get("description", "").lower()
    name = node.get("function", "").lower()
    params = node.get("metadata", {}).get("args", [])

    if not doc or not name:
        return False

    return name in doc and all(p.lower() in doc for p in params)

def extract_docstring_metadata(docstring: str) -> dict:
    """
    Extracts structured metadata from a docstring.

    @tags: ["parser", "metadata"]
    @status: "stable"
    @visibility: "internal"

    Parameters:
        docstring (str): Full function/class/module docstring

    Returns:
        dict: Contains 'description', 'docstring_full', 'tags', 'journal', 'deprecated', plus optional future fields.

    Supports:
        - @tags: ["tag1", "tag2"]
        - @journal: "linked entry"
        - @deprecated
        - @status: "draft"
        - @visibility: "internal"
    """
    result = {
        "description": "",
        "docstring_full": docstring.strip() if docstring else "",
        "tags": [],
        "linked_journal_entry": None,
        "deprecated": False,
        "status": None,
        "visibility": None
    }

    if not docstring:
        return result

    lines = textwrap.dedent(docstring).strip().splitlines()
    if lines:
        result["description"] = lines[0].strip()

    tag_pattern = re.compile(r"@tags:\s*(\[.*?\])")
    journal_pattern = re.compile(r"@journal:\s*['\"](.*?)['\"]")
    deprecated_pattern = re.compile(r"@deprecated\b")
    status_pattern = re.compile(r"@status:\s*['\"](.*?)['\"]")
    visibility_pattern = re.compile(r"@visibility:\s*['\"](.*?)['\"]")

    for line in lines:
        tag_match = tag_pattern.search(line)
        journal_match = journal_pattern.search(line)
        status_match = status_pattern.search(line)
        visibility_match = visibility_pattern.search(line)
        if tag_match:
            try:
                result["tags"] = ast.literal_eval(tag_match.group(1))
            except Exception:
                pass  # fail silently on malformed list
        if journal_match:
            result["linked_journal_entry"] = journal_match.group(1).strip()
        if deprecated_pattern.search(line):
            result["deprecated"] = True
        if status_match:
            result["status"] = status_match.group(1).strip()
        if visibility_match:
            result["visibility"] = visibility_match.group(1).strip()

    return result
