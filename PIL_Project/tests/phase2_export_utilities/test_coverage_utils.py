# tests/phase2_export_utilities/test_coverage_utils.py
"""
Unit tests for pil_meta.utils.test_coverage_utils.

Covers:
- estimate_test_coverage: marks 'test_coverage' True for covered symbols, False for uncovered

@tags: ["test", "test_coverage_utils", "unit"]
@status: "stable"
"""

import tempfile
import os
from pil_meta.utils.test_coverage_utils import estimate_test_coverage

def test_estimate_test_coverage_detects_covered(tmp_path):
    """
    Marks test_coverage True for symbols appearing in test files.
    """
    # Create a fake test file mentioning 'foo_fn'
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    test_file = test_dir / "test_demo.py"
    # The function must match the symbol name exactly:
    test_file.write_text("def foo_fn(): pass", encoding="utf-8")

    symbols = [
        {"function": "foo_fn"},
        {"function": "bar_fn"}
    ]
    results = estimate_test_coverage(symbols, test_dir=str(test_dir))
    foo = next(s for s in results if s["function"] == "foo_fn")
    bar = next(s for s in results if s["function"] == "bar_fn")
    assert foo["test_coverage"] is True
    assert bar["test_coverage"] is False

def test_estimate_test_coverage_no_tests(tmp_path):
    """
    If no test files, all symbols should be marked False.
    """
    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    symbols = [
        {"function": "alpha"},
        {"function": "beta"}
    ]
    results = estimate_test_coverage(symbols, test_dir=str(test_dir))
    for s in results:
        assert s["test_coverage"] is False
