# tests/phase2_export_utilities/test_path_utils.py
"""
Unit tests for pil_meta.utils.path_utils.

Covers:
- resolve_path: absolute, relative, and base-relative resolution
- Returns normalized string paths

@tags: ["test", "path_utils", "unit"]
@status: "stable"
"""

from pathlib import Path
import os
from pil_meta.utils.path_utils import resolve_path

def test_resolve_absolute_path(tmp_path):
    """
    Absolute paths remain unchanged and normalized.
    """
    abs_path = tmp_path / "foo" / "bar"
    abs_path.mkdir(parents=True)
    result = resolve_path(str(abs_path))
    assert Path(result).is_absolute()
    assert Path(result).parts[-2:] == ("foo", "bar")

def test_resolve_relative_path(tmp_path, monkeypatch):
    """
    Relative paths are resolved from current working directory.
    """
    cwd = os.getcwd()
    os.chdir(tmp_path)
    rel_path = "rel/sub"
    (tmp_path / "rel" / "sub").mkdir(parents=True)
    try:
        result = resolve_path(rel_path)
        assert Path(result).is_absolute()
        assert Path(result).parts[-2:] == ("rel", "sub")
    finally:
        os.chdir(cwd)

def test_resolve_with_base(tmp_path):
    """
    Relative paths are resolved using the provided base directory.
    """
    base = tmp_path / "base"
    base.mkdir()
    rel_path = "myfolder"
    (base / rel_path).mkdir()
    result = resolve_path(rel_path, str(base))
    assert Path(result).is_absolute()
    assert Path(result).parts[-2:] == ("base", "myfolder")
