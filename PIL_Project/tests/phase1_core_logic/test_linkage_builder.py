# tests/test_linkage_builder.py
"""
Unit tests for pil_meta.builders.linkage_builder.

Covers:
- inject_call_links: verifies linkage population and safe file access
- extract_called_functions: verifies correct AST call extraction
All test graphs include required fields, and temporary files are used for any file IO.
@tags: ["test", "linkage_builder", "unit"]
@status: "stable"
"""

import pytest
from pil_meta.builders.linkage_builder import inject_call_links, extract_called_functions

def test_injects_call_link_between_functions(tmp_path):
    """
    Test that inject_call_links correctly identifies and links called functions within a file.
    """
    test_py = tmp_path / "test.py"
    test_py.write_text("def func_a():\n    func_b()\ndef func_b():\n    pass\n")
    graph = {
        "module.func_a": {
            "fqname": "module.func_a",
            "type": "function",
            "module": "module",
            "source_file": str(test_py.relative_to(tmp_path)),
            "metadata": {}
        },
        "module.func_b": {
            "fqname": "module.func_b",
            "type": "function",
            "module": "module",
            "source_file": str(test_py.relative_to(tmp_path)),
            "metadata": {}
        }
    }
    result = inject_call_links(graph, str(tmp_path))
    assert "links" in result["module.func_a"]
    assert any(link["target"] == "module.func_b" and link["type"] == "calls"
               for link in result["module.func_a"]["links"])

def test_missing_calls_field_results_in_no_links(tmp_path):
    """
    Test that inject_call_links handles nodes with no callable references without error.
    """
    test_py = tmp_path / "test.py"
    test_py.write_text("def func_a():\n    pass\n")
    graph = {
        "module.func_a": {
            "fqname": "module.func_a",
            "type": "function",
            "module": "module",
            "source_file": str(test_py.relative_to(tmp_path)),
            "metadata": {}
        }
    }
    result = inject_call_links(graph, str(tmp_path))
    assert result["module.func_a"].get("links", []) == []

def test_nonexistent_target_is_ignored(tmp_path):
    """
    Test that calls to functions not present in the graph do not cause errors in inject_call_links.
    """
    test_py = tmp_path / "test.py"
    test_py.write_text("def func_a():\n    missing_func()\n")
    graph = {
        "module.func_a": {
            "fqname": "module.func_a",
            "type": "function",
            "module": "module",
            "source_file": str(test_py.relative_to(tmp_path)),
            "metadata": {}
        }
    }
    result = inject_call_links(graph, str(tmp_path))
    assert "links" in result["module.func_a"]

def test_empty_graph_returns_empty():
    """
    Test that inject_call_links on an empty graph returns an empty dict.
    """
    result = inject_call_links({}, "any")
    assert result == {}

def test_extract_simple_function_calls():
    """
    Test extract_called_functions detects simple function calls by name.
    """
    code = "foo()\nbar()"
    result = extract_called_functions(code)
    assert sorted(result) == ["bar", "foo"]

def test_extract_attribute_calls():
    """
    Test extract_called_functions detects attribute and qualified calls.
    """
    code = "obj.func1()\nmodule.func2()"
    result = extract_called_functions(code)
    assert "func1" in result
    assert "func2" in result

def test_extract_nested_calls():
    """
    Test extract_called_functions detects nested function calls.
    """
    code = "outer(inner())"
    result = extract_called_functions(code)
    assert "outer" in result
    assert "inner" in result

def test_extract_handles_empty_and_bad_code():
    """
    Test extract_called_functions handles empty strings and bad syntax gracefully.
    """
    assert extract_called_functions("") == []
    assert extract_called_functions("def incomplete(:") == []
