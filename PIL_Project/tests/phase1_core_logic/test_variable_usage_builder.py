# tests/builders/test_variable_usage_builder.py
"""
Unit tests for pil_meta.builders.variable_usage_builder.

Covers:
- build_variable_usage_map: finds variable usage across files,
  ignores unused variables, handles read errors, and empty cases.
All IO is handled via pytest tmp_path. Results are checked for key presence and correctness.

@tags: ["test", "variable_usage_builder", "unit"]
@status: "stable"
"""

from pathlib import Path
import pytest
from pil_meta.builders.variable_usage_builder import build_variable_usage_map

def write_temp_file(dirpath, filename, content):
    """
    Utility: write content to a temporary file in dirpath.
    """
    file = Path(dirpath) / filename
    file.write_text(content, encoding="utf-8")
    return file

def test_variable_used_in_multiple_files(tmp_path):
    """
    Variable is used in another file; usage is correctly recorded, but not in its own defining file.
    """
    var = {"function": "SHARED_VAR", "source_file": "a.py", "fqname": "a.SHARED_VAR"}
    file_a = write_temp_file(tmp_path, "a.py", "SHARED_VAR = 123\n")
    file_b = write_temp_file(tmp_path, "b.py", "print(SHARED_VAR)\n")
    files = [file_a, file_b]
    usage = build_variable_usage_map([var], files, tmp_path)
    assert "a.SHARED_VAR" in usage
    assert "b.py" in usage["a.SHARED_VAR"]
    assert "a.py" not in usage["a.SHARED_VAR"]

def test_variable_not_used(tmp_path):
    """
    Variable is not referenced in any file except its own; usage map returns empty.
    """
    var = {"function": "UNUSED_VAR", "source_file": "a.py", "fqname": "a.UNUSED_VAR"}
    file_a = write_temp_file(tmp_path, "a.py", "UNUSED_VAR = 1\n")
    file_b = write_temp_file(tmp_path, "b.py", "print('nothing')\n")
    files = [file_a, file_b]
    usage = build_variable_usage_map([var], files, tmp_path)
    assert usage == {}

def test_file_read_error(tmp_path, monkeypatch):
    """
    IO errors when reading a file are handled gracefully (file is skipped, no crash).
    """
    var = {"function": "FOO", "source_file": "a.py", "fqname": "a.FOO"}
    file_a = write_temp_file(tmp_path, "a.py", "FOO = 1\n")
    file_b = write_temp_file(tmp_path, "b.py", "FOO\n")
    orig_read_text = Path.read_text
    def read_text_fail(self, *args, **kwargs):
        if self.name == "b.py":
            raise IOError("fail")
        return orig_read_text(self, *args, **kwargs)
    monkeypatch.setattr(Path, "read_text", read_text_fail)
    files = [file_a, file_b]
    usage = build_variable_usage_map([var], files, tmp_path)
    assert usage == {}

def test_no_variables_returns_empty(tmp_path):
    """
    Empty input variable list yields an empty usage map.
    """
    files = []
    usage = build_variable_usage_map([], files, tmp_path)
    assert usage == {}
